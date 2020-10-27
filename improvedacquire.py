import pandas as pd
import numpy as np
import requests
import os

def get_zach_data(key):
    '''
    Utlizes rest API to gather data from Zach's python stash
    Key = 'items', 'stores', or 'sales' (with the ' ') acesses the data for each their respective data sets. 
    Using 'full' will return a single dataframe with that contains all the above dfs stitched together
    The function will return a df and CSV (if one does not exist) for each.
    '''
    if key == 'stores':
        request_url = 'https://python.zach.lol/api/v1/stores'
    elif key == 'items':
        request_url = 'https://python.zach.lol/api/v1/items'
    elif key == 'sales':
        request_url = 'https://python.zach.lol/api/v1/sales'

    while key != 'full':
        response = requests.get(request_url)
        data = response.json()
        page = data['payload']['page']
        max_page = data['payload']['max_page']
        break
        
    file = f'{key}.csv'

    if os.path.isfile(file):
        df = pd.read_csv(f'{key}.csv')
        return df
    
    elif key == 'full':
        sales = pd.read_csv('sales.csv')
        items = pd.read_csv('items.csv')
        stores = pd.read_csv('stores.csv')
        full = sales.merge(stores, left_on='store', right_on='store_id')
        full = full.merge(items, left_on='item', right_on='item_id')
        full.to_csv(str(key) + '.csv', index=False)
        return full

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