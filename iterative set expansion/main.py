import sys
from functions import *
import requests
from bs4 import BeautifulSoup
import spacy
from spanbert import SpanBERT 
from spacy_help_functions import extract_relations,get_entities, create_entity_pairs

argumentsCheck(sys.argv)

my_api_key = sys.argv[1]                # AIzaSyA8_Fp-XCfK4hNXyx7kD5SF6lDLhgIsflM
my_cse_id = sys.argv[2]                 # f188c466808db6e17
openai_secret_key = sys.argv[3]         # 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
method = sys.argv[4]                    # -spanBERT/GPT-3
r = sys.argv[5]                         #  1 is for Schools_Attended, 2 is for Work_For, 
                                        #  3 is for Live_In, and 4 is for Top_Member_Employees
t = sys.argv[6]                         # Minimum confidence level 0-1
q = sys.argv[7]                         # Initial query
k = sys.argv[8]                         # Number of output tuples


#############################
# SPANBERT
#############################
if sys.argv[4].lower() == "-spanbert":
    target_relation = ""
    _subject = []
    _object = []
    if r == str(1):
        target_relation = "per:schools_attended"
        _subject.append("PERSON")
        _object.append("ORGANIZATION")
    elif r == str(2):
        target_relation = "per:employee_of"
        _subject.append("PERSON")
        _object.append("ORGANIZATION")
    elif r == str(3):
        target_relation = "per:cities_of_residence"
        _subject.append("PERSON")
        _object =  ["LOCATION", "CITY", "STATE_OR_PROVINCE", "COUNTRY"]
    elif r == str(4):
        target_relation = "per:top_members/employees"
        _subject.append("ORGANIZATION")
        _object.append("PERSON")

    entities_of_interest = ["ORGANIZATION", "PERSON", "LOCATION", "CITY", "STATE_OR_PROVINCE", "COUNTRY"]

    print("Parameters:")
    print("Client Key      = " + my_api_key)
    print("Engine Key      = " + my_cse_id)
    print("OpenAI Key      = " + openai_secret_key)
    print("Method          = " + method)
    print("Relation        = " + target_relation)
    print("Threshold       = " + t)
    print("Query           = " + q)
    print("# of Tuples     = " + k)

    nlp = spacy.load("en_core_web_lg")
    spanbert = SpanBERT("./pretrained_spanbert")  

    X = set()                # set of output tuples (SUBJECT, OBJECT, CONFIDENCE)
    iter = 0                 # current number of query iteration (spanBERT)
    used_query = [q]         # list of queries that already used
    while True:
        iter += 1
        print("\t=========== Iteration: " + str(iter) + " - Query: " + q + "===========")
        results = google_search(q,my_api_key,my_cse_id,num=10) 
        for idx, result in enumerate(results):
            # getting webpage
            url = result["link"]
            print("URL ( " + str(idx+1) + " / 10): " + url)
            print("\tFetching text from url ...")
            response = requests.get(url)
            # Parse the HTML content of the webpage using Beautiful Soup
            soup = BeautifulSoup(response.content, 'html.parser')
            # Extract the text content of the webpage
            text_content = soup.get_text()
            # If greater than 10000 characters, truncate to 10000 characters
            if len(text_content) > 10000:
                print("\tTrimming webpage content from " + str(len(text_content)) + " to 10000 characters")
                text_content = text_content[:10000]
            print("\tWebpage length (num characters): " + str(len(text_content)))
            # Use spacy to split the text into sentences and extract named entities
            print("\tAnnotating the webpage using spacy...")
            doc = nlp(text_content)
            num_sentences = len(list(doc.sents))
            print("\tExtracted " + str(num_sentences) + " sentences. Processing each sentence one by \
            one to check for presence of right pair of named entity types; if so, will run the second pipeline ...")

            num_contributing_sents = 0           # number of sentences for this websites that yields tuples
            num_tuples = 0                    # total number of tuples this websites yields
            for idx, sentence in enumerate(doc.sents):
                num_tuples_this_sent = 0         # number of tuple this sentence yields
                if((idx+1)%5==0) or ((idx+1)==num_sentences):
                    print("\tProcessed " + str(idx+1) + " / " + str(num_sentences) + " sentences")
                # Extracting entities from sentence
                ents = get_entities(sentence, entities_of_interest)
                # create entity pairs
                candidate_pairs = []
                sentence_entity_pairs = create_entity_pairs(sentence, entities_of_interest)
                for ep in sentence_entity_pairs:
                    # keep subject-object pairs of the right type for the target relation (e.g., Person:Organization for the "Work_For" relation)
                    if ep[1][1] in _subject and ep[2][1] in _object:
                        candidate_pairs.append({"tokens": ep[0], "subj": ep[1], "obj": ep[2]})  # e1=Subject, e2=Object
                    if ep[2][1] in _subject and ep[1][1] in _object:
                        candidate_pairs.append({"tokens": ep[0], "subj": ep[2], "obj": ep[1]})  # e1=Object, e2=Subject

                # ignore subject entities with date/location type
                candidate_pairs = [p for p in candidate_pairs if not p["subj"][1] in ["DATE", "LOCATION"]]  
                # Classify Relations for all Candidate Entity Pairs using SpanBERT
                if len(candidate_pairs) == 0:
                    continue
                relation_preds = spanbert.predict(candidate_pairs)  # get predictions: list of (relation, confidence) pairs
                # Print Extracted Relations
                for ex, pred in list(zip(candidate_pairs, relation_preds)):
                    # if it is our target relation and has a confidence score greater than threshold t, add it to set X
                    if pred[0] == target_relation and pred[1] >= float(t):
                        X.add((ex["subj"][0], ex["obj"][0], pred[1]))
                        num_tuples += 1
                        num_tuples_this_sent += 1
                        print("\t\t=== Extracted Relation ===")
                        print("\t\tInput tokens: " + str(ex["tokens"]))
                        print("\t\tOutput Confidence: " + str(pred[1]) +  "; Subject: " + ex["subj"][0] + "; Object: " + ex["obj"][0] + ";")
                        print("\t\tAdding to set of extracted relations")
                        print("\t\t==========")

                if num_tuples_this_sent > 0:
                    num_contributing_sents += 1
            print("\n")
            print("\tExtracted annotations for  " + str(num_contributing_sents) + "  out of total " + str(len(list(doc.sents))) + " sentences")
            print("\tRelations extracted from this website: " + str(num_tuples) + " (Overall: " + str(len(X)) + " )")
            print("\n")
        # if already have enough output tuple, end the program
        if len(X) >= int(k):
            break
        # otherwise use the highest confidence tuple to issue another query
        else:
            X = sorted(X, key=lambda x: x[2], reverse=True)
            for ele in X:
                # make sure the query is not used before
                if ele[0] + " " + ele[1] not in used_query:
                    q = ele[0] + " " + ele[1]
                    used_query.append(q)
                    X = set(X)

    # Sorted the output based on confidence
    X = sorted(X, key=lambda x: x[2], reverse=True)
    print("================== ALL RELATIONS for " + target_relation + " ( " + str(len(X)) + " ) =================")
    for ele in X:
        print("Confidence: " + str(ele[2]) + "           | Subject: " + ele[0] + "           | Object: " + ele[1])
