import pandas as pd
import numpy as np
import requests
import os

base_url = 'https://python.zach.lol'
items_url = 'https://python.zach.lol/api/v1/items'
sales_url = 'https://python.zach.lol/api/v1/sales'
stores_url = 'https://python.zach.lol/api/v1/stores'

def get_zach_data(key, request_url, base_url=base_url):
    '''
    Utlizes rest API to gather data from Zach's python stash
    Keys = items, stores, sales for each their respective data sets
    request_url = items_url, sales_url, or stores_url for their respective data sets
    base_url = base_url and referes to 'https://python.zach.lol'
    '''
    
    response = requests.get(request_url)
    data = response.json()
    page = data['payload']['page']
    max_page = data['payload']['max_page']
        
    file = f'{key}.csv'

    if os.path.isfile(file):
        df = pd.read_csv(f'{key}.csv')
        return df
    
    else:
        df = pd.DataFrame(data['payload'][key])
        while page <= max_page:
            next_page = data['payload']['next_page']
            if next_page is None or next_page == "None":
                break
            response = requests.get(base_url + next_page)
            data = response.json()
            df = pd.concat([df, pd.DataFrame(data['payload'][key])])
            page = data['payload']['page']

        df.reset_index(inplace=True, drop=True)
        df.to_csv(str(key) + '.csv', index=False)
        return df
    
    return df

def all_zach_data():
    '''
    Once you've loaded all zach's into CSV using the get_zach_data function you can run this function to stitch the individual 
    data frames together
    '''
    sales = pd.read_csv('sales.csv')
    items = pd.read_csv('items.csv')
    stores = pd.read_csv('stores.csv')
    full = sales.merge(store, left_on='store', right_on='store_id')
    full = full.merge(items, left_on='item', right_on='item_id')
    return full
    
def get_de_electric():
    '''
    Load the Open Power Systems Data for Germany by reading the CSV url into the a DF and CSV (de_electric) if applicable
    '''
    file = 'de_electric.csv'

    if os.path.isfile(file):
        df = pd.read_csv('de_electric.csv')
        return df
    
    else:
        df = pd.read_csv('https://raw.githubusercontent.com/jenfly/opsd/master/opsd_germany_daily.csv')
        return df