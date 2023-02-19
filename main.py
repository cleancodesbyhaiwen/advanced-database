import sys
from functions import *

if len(sys.argv) != 5:
    sys.exit("Usage: /home/gkaraman/run <API Key> <Engine Key> <Precision> <Query>")

my_api_key = sys.argv[1]                # AIzaSyA8_Fp-XCfK4hNXyx7kD5SF6lDLhgIsflM
my_cse_id = sys.argv[2]                 # f188c466808db6e17
precision = float(sys.argv[3])
query = sys.argv[4]

# set the start word freq to 10
q_dic = {}
q_dic[query] = 10

curr_precision = 0 # Actual precision@10 for each round
while True:
    print("Parameter:")
    print("Client key  = " + my_api_key)
    print("Engine key  = " + my_cse_id)
    print("Query       = " + query)
    print("Precision   = " + str(precision))
    selected_list = []
    results = google_search(query ,my_api_key,my_cse_id,num=10)
    print("Google Search Results:")
    print("======================")
    for idx, result in enumerate(results):
        print("Result " + str(idx+1))
        print("[")
        print(" URL: " + result["link"])
        print(" TITLE: " + result["title"])
        print(" Summary: " + result["snippet"])
        print("]")
        if input("Relevant (Y/N)? ") == "Y":
            selected_list.append(idx+1)

    curr_precision = len(selected_list) / len(results)

    print("====================")
    print("FEEDBACK SUMMARY")
    print("Query       = " + query)
    print("Precision   = " + str(curr_precision))
    if curr_precision == 0:
        print(f"\n{bcolors.FAIL}Current precision@10 is 0. End of program.{bcolors.ENDC}\n")
        break
    elif curr_precision >= precision:
        print(f"\n{bcolors.OKGREEN}Current precision@10 is greater or equal to the expected precision@10. End of program.{bcolors.ENDC}\n")
        break
    else:
        print(f"\n{bcolors.WARNING}Current precision@10 is lower than expectation.{bcolors.ENDC}\n")

    print("Indexing results .... ")
    # Geeting top 5 frequent words in relevant snippets
    selected_words = extract_keywords(results, selected_list, query, True)
    # Getting top 5 frequent words in irrelevant snippets
    no_words = extract_keywords(results, selected_list, query, False)
    # Add one to two words to q_dic
    select_keywords(selected_words, no_words, q_dic)

    # build the query based on q-dic
    query = ''
    for key in q_dic :
        query += key + ' '