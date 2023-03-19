from googleapiclient.discovery import build

# google search api function call
def google_search(search_term, api_key, cse_id, **kwargs):
      service = build("customsearch", "v1", developerKey=api_key)
      res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
      return res['items']

def argumentsCheck(argv):
      if argv[4].lower() not in ['-gpt3','-spanbert']:
            print("the 4th argument (model of choice) should be -gpt3 or -spanbert")
            exit(1)
      if argv[5] not in ['1','2','3','4']:
            print("the 5th argument (target relation) should be among 1,2,3,4")
            exit(1)     
      if float(argv[6]) < 0 or float(argv[6]) > 1:
            print("the 6th argument (confidence level threshold) should be among 1,2,3,4")
            exit(1)      
      if int(argv[8]) <= 0:
            print("the 8th argument (expected number of tuple) should be a positive integer")
            exit(1)                      


