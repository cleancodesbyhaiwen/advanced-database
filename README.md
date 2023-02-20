# Query Expansion
 
<p> This is a Python program that uses Rocchio's techique of query expansion. 
Usage: python3 main.py <api_key> <engine_id> <precision> <query>
<\p>
<br>
<p>Sometimes, a query term can refer to different things. For example, "jaguar" may refer to
the animal or the car brand. Our program first accept such query and uses google's search api to
return the top 10 results. The user can select the result that appears to be relevant. And the program will
do query expansion to optimize the results until a specific percentage of the results are relevant. <\p>
