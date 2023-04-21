from itertools import combinations, chain
import sys

# Given a list of sets, output all unique combinations of size k
# This for generating all next-round candidates based on current frequent itemsets
def get_unique_sets(list_of_sets, k):
    unique_sets = set()
    set_combinations = combinations(list_of_sets, k)
    for sets in set_combinations:
        element_combinations = set(combinations(set(chain(*sets)), k))
        unique_sets |= element_combinations
    return [set(t) for t in list(unique_sets)]

# Given all candidate sets of size k, output all sets that meet the min support threshold
def calculate_support(transactions, candidates, min_support):
    frequent_itemsets = []
    for candidate in candidates:
        count = 0
        for transaction in transactions:
            if candidate.issubset(transaction):
                count += 1
        if count / len(transactions) >= min_support:
            print(str(candidate) + " has a support of " + "{:.2f}".format(count / len(transactions)) + " appending it to frequent itemset")
            frequent_itemsets.append(candidate)

    print("Candidates were: " + str(candidates))
    print("Min support is: " + str(min_support))
    print("Frequent itemsets from this round are: " + str(frequent_itemsets))
    return frequent_itemsets


def apriori(transactions, min_support, initial_candidates):
    frequent_itemsets = []
    k = 1
    while True:
        print("k is " + str(k))
        # Generate all candidate itemsets of size k
        candidates = get_unique_sets([s for s in frequent_itemsets if len(s) == k-1], k)
        if k == 1:
            candidates = initial_candidates

        # Kepp only all the candidates that meet the min support threshold
        frequent_itemsets_k = calculate_support(transactions, candidates, min_support)

        # If no frequent itemsets found, terminate the algorithm
        if not frequent_itemsets_k:
            print("No more frequent itemsets. Terminating...\n")
            break

        # Add frequent itemsets of size k to the result frequent itemsets
        for ele in frequent_itemsets_k:
            frequent_itemsets.append(ele)

        print("Frequent itemsets are now " + str(frequent_itemsets) + "\n")
        k += 1
    return frequent_itemsets

# From frequent itemsets, generate all association rules given a min confidence
def generate_association_rules(frequent_itemsets, transactions, min_confidence):
    association_rules = []
    for itemset in frequent_itemsets:
        if len(itemset) > 1:
            combinations = partitions(list(itemset))
            for combination in combinations:
                antecedent = frozenset(combination[0])
                consequent = frozenset(combination[1])
                if len(antecedent) > 0 and len(consequent) > 0:
                    confidence = calculate_confidence(antecedent, consequent, transactions)
                    if confidence >= min_confidence:
                        association_rules.append((antecedent, consequent, confidence))
    return association_rules


# Calculate the confidence score given an antecedent, a consequent and all transactions
def calculate_confidence(antecedent, consequent, transactions):
    antecedent_support = calculate_support_2(antecedent, transactions)
    rule_support = calculate_support_2(antecedent.union(consequent), transactions)
    confidence = rule_support / antecedent_support
    return confidence

# Calculate the support for a itemset given all transactions
def calculate_support_2(itemset, transactions):
    count = 0
    for transaction in transactions:
        if itemset.issubset(transaction):
            count += 1
    support = count / len(transactions)
    return support

# Given a frequent itemset, return all possible antecedent and consequent combinations
def partitions(set_elements):
    if len(set_elements) == 0:
        return [([], [])]
    partitions_list = []
    for p in partitions(set_elements[1:]):
        partitions_list.extend([([set_elements[0]] + p[0], p[1]), (p[0], [set_elements[0]] + p[1])])
    return partitions_list
