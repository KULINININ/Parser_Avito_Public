import json

def get_requests_list():
    with open('Avito//requests.json', 'r') as requests_list:
        requests_data = json.load(requests_list)
        for request in requests_data:
            request['viewed_ids'] = [] 
        return requests_data