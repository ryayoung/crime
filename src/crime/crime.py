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
    print("""Get DataFrame with basic info on all datasets:
>>> crime.sources()

View FULL details on a source (description, column descriptions, etc.)
>>> crime.sources('dataset_name')

Load full dataset
>>> crime.load('dataset_name')
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
            print(f"  Type: {c['dataTypeName']}")
            print(f"  Null: {cached.get('null', None)}")
            print(f"  Non-Null: {cached.get('non_null', None)}")
            if c['dataTypeName'] == 'number':
                if cached.get('average', "").isdigit():
                    print(f"  Avg: {round(float(cached.get('average', 0)), 2)}")
                if cached.get('largest', "").isdigit():
                    print(f"  Max: {float(cached.get('largest', 0))}")
                if cached.get('smallest', "").isdigit():
                    print(f"  Min: {float(cached.get('smallest', 0))}")
                if cached.get('sum', "").isdigit():
                    print(f"  Sum: {float(cached.get('sum', 0))}")
            else:
                cached = c.get('cachedContents', {})
                if len(cached.get('top', [])) > 1:
                    if not str(cached.get('top')[1]['item'])[0:1].isdigit():
                        print("  ITEMS:")
                        for i in c.get('cachedContents', {}).get('top', []):
                            print(f"     {str(i['item'])[:60]}  ({i['count']})")
            print()

        return None


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
