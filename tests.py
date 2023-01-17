import requests
import pandas as pd
import bs4 as bs
from fugitiveData import Fugitive

response = requests.get('https://api.fbi.gov/wanted/v1/list', params={
            'page': 1,
            'pageSize': 1
        }).json()['items']

# Batch processing for 1
# to be >1
fugitive = Fugitive(pd.DataFrame(response))
attrs = vars(fugitive)
