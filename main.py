import requests
import json
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import re as re
from fugitiveData import Fugitive
import pprint
import networkx as nx

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
    fugitives = []
    for i in range(0, data.shape[0]):
        fugitives.append(Fugitive(data.iloc[i, :]))

    df = pd.DataFrame([x.to_dict() for x in fugitives])
    print(df)
