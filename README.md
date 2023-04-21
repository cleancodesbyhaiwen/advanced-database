# Query Expansion
 
<p> This is a Python program that uses Rocchio's techique of query expansion. 
Usage: python3 main.py api_key engine_id precision query

<br>
<p>Sometimes, a query term can refer to different things. For example, "jaguar" may refer to
the animal or the car brand. Our program first accept such query and uses google's search api to
return the top 10 results. The user can select the result that appears to be relevant. And the program will
do query expansion to optimize the results until a specific percentage of the results are relevant. 

# Relation Extraction

<p> This program extract relation tuples from webpages
<br>
for example: with the initial query "bill gates microsoft", it will get the plain text of top ten google search result websites and use spacy to split sentences and tokenize entities. Then, it used spanBERT to extract relationship and give a confidence score on the relationship.

# Association Rule Mining

<p> This is a program that first perform boolean mapping of a dataset and then generate association rules from the mapped dataset
