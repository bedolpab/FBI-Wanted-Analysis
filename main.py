import requests
import json
import pandas as pd

# Fetches all fugitives
# Testing done on batch size: 1 to apply to all
if __name__ == '__main__':
    i = 1
    hasContent = True
    empty = []
    while hasContent:
        response = requests.get('https://api.fbi.gov/wanted/v1/list', params={
            'page': i
        }).json()['items']

        if pd.DataFrame(response).empty:
            hasContent = False
            continue
        else:
            for item in response:
                empty.append(item)
            i += 1

    data = pd.DataFrame(empty)
    data.to_csv("./wanted-list.csv")

