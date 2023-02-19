from googleapiclient.discovery import build
import re

# read all stop words from "words.txt" into a list
my_file = open("words.txt", "r")
lines = my_file.readlines()
stop_words = []
for line in lines:
    stop_words.append(line.replace('\n', ''))


# google search api function call
def google_search(search_term, api_key, cse_id, **kwargs):
      service = build("customsearch", "v1", developerKey=api_key)
      res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
      return res['items']

# Count words frequency in a string
def count(elements, dictionary):
    if elements[-1] == '.':
        elements = elements[0:len(elements) - 1]
    if elements in dictionary:
        dictionary[elements] += 1
    else:
        dictionary.update({elements: 1})

class bcolors:
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

## issue1: how to deal with compounded words? Like name?

# if relevant is TRUE, then return the top 5 frequent wrods from revelant snippets
# if relevant is FALSE, then return top 5 frequent words from irrelevant snippets
def build_freq_dict(results, selected_list, current_query, relevant):
    curr_query_words = current_query.split()
    combined_snippets = ""
    dictionary = {}
    snippet_range = len(results)
    if relevant:
        for num in selected_list:
            combined_snippets += results[num-1]["snippet"]
    else:
        for num in range(snippet_range):
            if num + 1 not in selected_list:
                combined_snippets += results[num]["snippet"]
    combined_snippets = combined_snippets.lower()
    combined_snippets = re.sub("[^a-zA-Z0-9 ]", "", combined_snippets)
    lst = combined_snippets.split()
    for elements in lst:
        count(elements, dictionary)
    dictionary = {k: v for k, v in sorted(dictionary.items(), key=lambda item: item[1],reverse=True)}
    """
    for allKeys in dictionary:
        print ("Frequency of ", allKeys, end = " ")
        print (":", end = " ")
        print (dictionary[allKeys], end = " ")
        print()
    """
    top5words = {}
    temp_num = 0
    for key in dictionary:
        if (key not in curr_query_words) and (key not in stop_words):
            top5words[key] = dictionary[key]
            temp_num += 1
        if temp_num == 5:
            break

    return top5words


# setting up to use some concept from Rocchio's algorithm
## simple explanation: to make sure the words we add to the current search list are relevant,
## we will first calculate the term freq of each words in relevant docs
## then we will calculate the term freq of each words in irrelevant docs
## with the help of beta and gamma, we will count a overall term freq in the displayed 10 search results, and pick the most relevant new words
## for current word lists, we will modifiy the term freq to maintain a proper ordering
alpha = 1 # to be 1 so algorithm cannot delete words that are already in the word lists
beta = 0.75
gamma = 0.25
# take both the extracted words from relevent doc and irrelvant doc
# Add two new words to q_dic
def select_keywords(r_dic, ir_dic, q_dic):
    # first count, make sure to set the order for word dic
    # if round == 1:
    #     q_dic[query] = 10
    temp = {}
    ir_keys = ir_dic.keys()
    for key in r_dic:
        if key in ir_keys:
            temp[key] = r_dic[key] * beta - ir_dic[key] * gamma
        else:
            temp[key] = r_dic[key] * beta
    temp = {k: v for k, v in sorted(temp.items(), key=lambda item: item[1], reverse=True)}

    augmenting_by = ""
    top2 = 2
    for key in temp:
        q_dic[key] = temp[key]
        augmenting_by += key + " "
        top2 = top2-1
        if top2 < 1:
            break
    print("Augmenting by " + augmenting_by)
    q_dic = {k: v for k, v in sorted(q_dic.items(), key=lambda item: item[1],reverse=True)}
    """
    print("in the current search list")
    for key in q_dic:
        print(str(key) + ": " + str(q_dic[key]))
    """