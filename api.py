import requests
import json

def getApiKey():
    with open('apikey.txt', 'r') as file:
        return file.read()
    
def getUserPreferences():
    url = 'https://api.airtable.com/v0/appWmmEdG1k8ceP7j/People'
    j = requests.get(url, headers={'Authorization': 'Bearer ' + getApiKey()}).json()

    print(json.dumps(j, indent=2))
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

print(getUserPreferences())