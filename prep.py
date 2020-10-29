import pandas as pd
import numpy as np
import requests
import os
import acquire as ac

def prep_zach():
    df = ac.all_zach_data()
    df['sale_date'] = pd.to_datetime(df.sale_date, format='%a, %d %b %Y %H:%M:%S %Z')
    df.set_index('sale_date', inplace=True)
    df['day'] = df.index.day_name()
    df['month'] = df.index.month
    df['sales_total'] = df['sale_amount'] * df['item_price']
    return df

def prep_ops():
    df = ac.get_de_electric()
    df['Date'] = pd.to_datetime(df.Date)
    df.set_index('Date', inplace=True)
    df['month'] = df.index.month
    df['year'] = df.index.year
    df.fillna(0, inplace=True) 
    df['Wind+Solar'] = df['Solar'] + df['Wind']
    return df
