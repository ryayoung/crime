# Maintainer:     Ryan Young
# Last Modified:  May 06, 2022
from sodapy import Socrata
import requests
import pandas as pd
import json
import time
from crime.library import Library
from crime.soda_api import Soda


def help():
    print("""Declare your app token (optional, recommended)
>>> cr.set_token("XXXXXXX")

DataFrame with info on all datasets:
>>> cr.sources()

Details on a dataset, and description of all columns
>>> cr.sources('dataset_name')

Quickly preview its first 5 rows
>>> cr.load('dataset_name')

Load full dataset
>>> cr.load('dataset_name', full=True)
""")


def set_token(token):
    """
    Sets the app token to be used for Socrata API
    """
    Soda.token = token


def sources(name:str = None) -> pd.DataFrame or None:
    """
    Returns info on available sources.
    ---
    If no arguments are given:
    - Returns pd.DataFrame with all the important details
      already known, without making any requests to Socrata
    ---
    If name is given:
    - Prints a full description of the source and each of its
      columns, including aggregate statistics for numeric columns
      and a list of categories for categorical columns.
    - Returns None
    """

    if not name:
        return Library.tabular()

    else:
        if name not in Library.data:
            return

        if Soda.token == None:
            print("Use 'cr.set_token(my_app_token)' to get full api access and avoid this warning")

        info = Library.data[name]
        base_url = info['base_url']
        data_id = info['id']
        web_url = info['web_url']

        data = Soda.get_metadata(base_url, data_id)
        # print(json.dumps(data, indent=2))
        # return
        print(data['name'])
        print(web_url)
        print()
        print(data['description'])
        print()
        print("COLUMNS:")
        print("-------")
        for c in data['columns']:
            cached = c.get('cachedContents', {})
            print(c['name'])
            print(f"  Field:  {c['fieldName']}")
            print(f"  Type:   {c['dataTypeName']}")
            print(f"  Null:   {cached.get('null', '-')}")
            print(f"  Count:  {cached.get('non_null', '-')}")
            if c['dataTypeName'] == 'number':
                print(f"  Avg:    {cached.get('average', '-')}")
                print(f"  Max:    {cached.get('largest', '-')}")
                print(f"  Min:    {cached.get('smallest', '-')}")
                print(f"  Sum:    {cached.get('sum', '-')}")
            else:
                cached = c.get('cachedContents', {})
                if len(cached.get('top', [])) > 1:
                    if not str(cached.get('top')[1]['item'])[0:1].isdigit():
                        print("  ITEMS:")
                        for i in c.get('cachedContents', {}).get('top', []):
                            print(f"     {str(i['item'])[:60]}  ({i['count']})")
            print()

        return


def load(name:str, **kwargs) -> pd.DataFrame:
    """
    Loads a dataset, and accepts any additional keyword
    arguments for sodapy's get() function.
    ---
    Use the 'limit = n' argument to limit the number
    of rows returned. Useful for large datasets.
    ---
    Returns: pd.DataFrame
    """
    if name not in Library.data:
        return

    if Soda.token == None:
        print("Use 'cr.set_token(my_app_token)' to get full api access and avoid this warning")

    info = Library.data[name]
    base_url = info['base_url']
    data_id = info['id']

    try:
        return Soda.get(base_url, data_id, **kwargs)
    except Exception as e:
        print(e)









































































































































    
def set_top_secret_token():
    Soda.token = "POb9E2hovuHBBgdVFLt18TtEG"
