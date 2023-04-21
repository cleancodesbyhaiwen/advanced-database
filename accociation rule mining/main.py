from apriori import *
import csv

file_path = sys.argv[1]  
min_support = float(sys.argv[2])
min_confidence = float(sys.argv[3])  

# transform the csv into the form that can be processed by a-priori algorithm
transactions = []
with open(file_path, 'r') as csvfile:
    reader = csv.reader(csvfile)
    # These are all labels of the csv file
    labels = next(reader)
    for row in reader:
        transaction = []
        for index,ele in enumerate(row):
            if ele == "True":
                transaction.append(labels[index])
            else:
                pass
        transactions.append(transaction)

# Construct the list of candidates sets for the first iteration of the a-priori algorithm (itemsets of size 1)
initial_candidates = [{element} for element in labels]
# Run the a-priori algorithm and get the frequent itemsets
frequent_itemsets = apriori(transactions, min_support, initial_candidates)
# Just incase there are duplicates in frequent itemsets
unique_list_of_sets = []
for s in frequent_itemsets:
    if s not in unique_list_of_sets:
        unique_list_of_sets.append(s)
frequent_itemsets = unique_list_of_sets
frequent_itemsets_supp = [calculate_support_2(s,transactions) for s in frequent_itemsets]

with open('output.txt', 'w') as file:
    file.write("Frequent Itemsets are: " + '\n')
    print("\nFrequent Itemsets are: ")
    for index, itemset in enumerate(frequent_itemsets):
        file.write("Frequent Itemset " + str(index+1) + ": " + str(itemset) + " Support: " + "{:.2f}".format(frequent_itemsets_supp[index]) + '\n')
        print("Frequent Itemset " + str(index+1) + ": " + str(itemset) + " Support: " + "{:.2f}".format(frequent_itemsets_supp[index]) )

# For each frequent item set, determine whether meet min confidence threshold
frequent_itemsets = [list(s) for s in frequent_itemsets]
association_rules = generate_association_rules(frequent_itemsets, transactions, min_confidence)

with open('output.txt', 'a') as file:
    file.write("Accociation Rules are: " + '\n')
    print("\nAccociation Rules are: ")
    for index, association_rule in enumerate(association_rules):
        file.write("Accociation Rule " + str(index+1) + ": " + str(list(association_rule[0])) + " -> " + str(list(association_rule[1])) + " Confidence: " + "{:.2f}".format(association_rule[2]) + '\n')
        print("Accociation Rule " + str(index+1) + ": " + str(list(association_rule[0])) + " -> " + str(list(association_rule[1])) + " Confidence: " + "{:.2f}".format(association_rule[2]))



