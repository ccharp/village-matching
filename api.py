import requests
import json

def get_api_key():
    with open('apikey.txt', 'r') as file:
        return file.read()
    
url_base = 'https://api.airtable.com/v0/appWmmEdG1k8ceP7j/'
auth_key= 'Bearer ' + get_api_key()

def get_user_preferences():
    j = requests.get(url_base + 'People', headers={'Authorization': auth_key}).json()
    #print(json.dumps(j, indent=2))
    records = j['records']

    idToName = {}
    for record in records:
        idToName[record['id']] = record['fields']['Name']

    preferences = {}
    for record in records:
        id = record['id']
        fields = record['fields']
        if 'Matching Preferences' not in fields:
            print('No preferences found for user ' + idToName[id] + '. Skipping.')
            continue
        preferences[record['id']] = fields['Matching Preferences']

    return preferences

def chunk_list(l, num_chunks): 
    # looping till length l 
    for i in range(0, len(l), num_chunks):  
        yield l[i:i + num_chunks] 

def upload_matches(matches):
    chunked_matches = chunk_list(matches, len(matches)//10 + 1)
    for chunked_match in chunked_matches:
        # Wrap matches in the required fields for AirTable
        output = {
            'records': [{'fields': x} for x in chunked_match]
        }
        #print("poop my pants")
        #print(json.dumps(output, indent=2))
        resp = requests.post(url_base + 'Session%20Output', json=output, headers={
            'Authorization': auth_key,
            'Content-type': 'application/json'
            })

        print(resp.content)
    

""" Example output json
'{
  "records": [
    {
      "fields": {
        "Person 1": [
          "rec9khZKGdII64txx"
        ],
        "Person 2": [
          "recsMmyMjmlEXDM5l"
        ],
        "Session": "A",
        "Room Assignment": "Room 1"
      }
    },
"""

# print(get_user_preferences())