# Maintainer:     Ryan Young
# Last Modified:  May 08, 2022
import requests
import pandas as pd
import numpy as np
import textwrap as tw
from crime.library import Library
from crime.soda_api import Soda

# Declare your app token (optional, recommended)
# >>> cr.set_token("XXXXXXX")

def help():
    print("""DataFrame with info on all datasets:
>>> cr.sources()

Details on a dataset, and description of all columns
>>> cr.sources('dataset_name')

Quickly preview its first 5 rows
>>> cr.load('dataset_name')

Load full dataset
>>> cr.load('dataset_name', full=True)

Declare your own collection of sources (pass a dictionary)
>>> cr.set_sources({
        'district_arrests': { # this is the nickname you'll refer to
            "id": "2e5i-5hfy",
            "base_url": "data.colorado.gov"
        },
        'district_crime': {
            "id": "ya69-n6ta",
            "base_url": "data.colorado.gov"
        },
        # etc...
    }
)

Revert to using the default sources
>>> cr.reset_sources()
""")


def set_token(token):
    """
    Sets the app token to be used for Socrata API
    """
    Soda.token = token


def isnum(val):
    """
    The only fool-proof way to test if val is a number
    and keep it an integer if int, or rounded float if decimal
    """
    val = str(val)
    try:
        return int(val)
    except Exception:
        try:
            return round(float(val), 2)
        except Exception:
            return None


def metadata(name:str) -> dict:
    """
    Returns re-formatted metadata on a source
    as a dictionary. The API metadata is modified to
    include the contents of Library.data, and NOT include
    all the unneccessary bullshit the API gives us.
    """

    cached = Library.meta_cache_get(name)
    if cached != None:
        return cached

    if name not in Library.data:
        return dict()
    
    if Soda.token == None:
        print("Use 'cr.set_token(my_app_token)' to get full api access and avoid this warning")

    # Basic info already stored in Library, but not in metadata
    info = Library.data[name]
    out = dict()

    # Not using dictionary comprehension here, since we're handling
    # different variables differently
    out['id'] = info['id']
    out['base_url'] = info['base_url']
    out['from_year'] = info.get('date_range', [None, None])[0]
    out['to_year'] = info.get('date_range', [None, None])[1]
    out['full_name'] = info.get('full_name', None)
    out['rows'] = info.get('rows', None)
    out['web_url'] = info.get('web_url', None)
    out['location'] = info.get('location', None)
    out['type'] = info.get('type', None)
    out['topic'] = info.get('topic', None)
    out['num_columns'] = None
    out['description'] = None
    out['columns'] = []

    # Socrata metadata
    meta = Soda.get_metadata(info['base_url'], info['id'])

    out['name'] = meta['name']
    out['num_columns'] = len(meta['columns'])
    out['description'] = meta['description']

    for c in meta['columns']:
        cached = c.get('cachedContents', {})
        outc = dict()

        # Occasionally the api hasn't processed display names for
        # for fields, so we have to do it ourself: Split name into
        # separate words by underscore and capitalize each word
        outc['name'] = c['name']
        if c['name'].islower():
            outc['name'] = " ".join([w.title() for w in c['name'].split('_')])

        outc['field'] = c['fieldName']
        outc['type'] = c['dataTypeName']
        outc['null'] = isnum(cached.get('null', None))
        outc['non_null'] = isnum(cached.get('non_null', None))

        outc['avg'] = isnum(cached.get('average', None))
        outc['max'] = isnum(cached.get('largest', None))
        outc['min'] = isnum(cached.get('smallest', None))
        outc['sum'] = isnum(cached.get('sum', None))

        outc['items'] = []

        # If it's a text column, print top items and their frequencies
        if c['dataTypeName'] == 'text':
            if len(cached.get('top', [])) > 1:
                # Check if the text variable is ACTUALLY categorical (IDs, for example, are NOT)
                # To validate, make sure the first couple characters aren't numbers
                if not str(cached.get('top')[1]['item'])[0:1].isdigit():
                    outc['items'] = [
                            {'item': i['item'], 'count': i.get('count', None)}
                        for i in c.get('cachedContents', {}).get('top', [])
                    ]

        out['columns'].append(outc)

    Library.meta_cache_add(name, out)
    return out


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
        meta = metadata(name)
        if meta == dict():
            return

        print(meta['name'])
        if meta['web_url']:
            print(meta['web_url'], "\n")
        # Wrap description text at 70 characters. (tw.wrap returns a list)
        print(*tw.wrap(meta['description'], width=70), sep="\n")
        print()
        # These likely won't be present if the user defined their own sources
        if meta['rows']:
            print(f"Rows:    {meta['rows']}")
        if meta['num_columns']:
            print(f"Cols:    {meta['num_columns']}")
        if meta['from_year'] and meta['to_year']:
            print(f"Period:  {meta['from_year']} to {meta['to_year']}")
        print()
        print("COLUMNS:")
        print("-------")
        for c in meta['columns']:
            cached = c.get('cachedContents', {})
            print(c['name'])
            print(f"  Field:  {c['field']}")
            print(f"  Type:   {c['type']}")
            null = f"{c['null']:,}" if c['null'] else '-'
            non_null = f"{c['non_null']:,}" if c['non_null'] else '-'
            print(f"  Null:   {null}")
            print(f"  Count:  {non_null}")

            # If it's numeric, print stats.
            if c['type'] == 'number':
                for num in ['min', 'max', 'avg', 'sum']:
                    val = f"{c[num]:,}" if c[num] else '-'
                    print(f"  {num.title()}:    {val}")

            # If it's a text column, print top items and their frequencies
            elif c['type'] == 'text':
                for i in c['items']:
                    count = f"{int(i['count']):,}" if i['count'] else '-'
                    print(f"     {i['item']}  ({count})")

            print()

        return


def columns(name:str) -> pd.DataFrame:
    """
    Returns dataframe with stats on each column.
    Includes all column data from metadata
    EXCEPT the 'items' array for categorical columns.
    """
    col_data = metadata(name)['columns']
    for c in col_data:
        if 'items' in c:
            c.pop('items')

    df = pd.DataFrame(col_data).set_index('field')
    df.index.name = None
    df.columns = df.columns.str.title()
    return df


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
    
    df = Library.cache_get(name)
    if not df.empty:
        return df

    if Soda.token == None:
        print("Use 'cr.set_token(my_app_token)' to get full api access and avoid this warning")

    info = Library.data[name]
    base_url = info['base_url']
    data_id = info['id']

    try:
        df = Soda.get(base_url, data_id, **kwargs)
        if kwargs.get('full', False) == True:
            Library.cache_add(name, df)
        return df
    except Exception as e:
        print(e)



def df(name:str) -> pd.DataFrame:
    return Library.cache_get(name)



def set_sources(data:dict):
    Library.set_data(data)

def reset_sources():
    Library.reset_data()

def get_current_token():
    return Soda.token








































































































































    
def set_top_secret_token():
    print("No need to set token anymore! A default one is already defined.")
    Soda.token = "POb9E2hovuHBBgdVFLt18TtEG"
