# Maintainer:     Ryan Young
# Last Modified:  May 08, 2022
import requests
import pandas as pd
import numpy as np

class MetaLibrary(type):
    """
    This is my solution to effectively applying the property
    decorator to class variables. This allows us to execute
    logic when the Library's variables are accessed. In this
    case, the 'data' variable won't be loaded with online api
    data until the variable is actually accessed for the first
    time. That way we aren't sending unnecessary api requests
    when the user doesn't need us to.
    """

    @property
    def data(cls):
        if cls._user_data != None:
            return cls._user_data

        if cls._data == None:
            try:
                cls._data = dict(requests.get(cls._url).json())
            except Exception as e:
                print("Can't find crime library sources.\nEither you don't have internet, or Github's API isn't working.")
                return
        return cls._data
    

    @property
    def url(cls):
        return cls._url



class Library(object, metaclass=MetaLibrary):
    """
    A simple class to interact with the datasources defined
    in a json file stored in the cloud.
    """

    _url = "https://raw.githubusercontent.com/ryayoung/crime/main/colorado-crime-datasets-doc.json"
    _data = None # default sources
    _user_data = None # user-defined sources
    _cache = dict()
    _meta_cache = dict()

    # Try to load default sources online
    try:
        _data = dict(requests.get(_url).json())
    except Exception as e:
        _data = None
    

    @classmethod
    def set_data(cls, data:dict):
        if type(data) != dict:
            raise ValueError("""
Must provide a dict of dicts. Example:
{
    "my_dataset_1": {
        "id": "ab3c-e4gh",
        "base_url": "data.colorado.gov"
    },
    "my_dataset_2": {
        "id": "..."
        "base_url": "..."
    },
    etc...
}""")

        for k, v in data.items():
            if type(v) != dict:
                raise ValueError(f"The value of '{k}' must be a dict with at least two items, 'id' and 'base_url'")
            if "id" not in v:
                raise ValueError(f"Item '{k}' must contain an 'id' element.")
            if "base_url" not in v:
                raise ValueError(f"Item '{k}' must contain a 'base_url' element.")
            
        cls._user_data = data
    

    @classmethod
    def reset_data(cls):
        cls._user_data = None


    @classmethod
    def tabular(cls) -> pd.DataFrame:
        """
        Gives the end user the contents of the self.data dictionary
        as a pandas dataframe, including only the important fields,
        and excluding base_url and id.
        """
        return pd.DataFrame([
            {
                'Name': k,
                'Topic': v.get('topic', np.NaN),
                'Location': v.get('location', np.NaN),
                'Rows': v.get('rows', np.NaN),
                'Type': v.get('type', np.NaN),
                'From': v.get('date_range', [np.NaN, np.NaN])[0],
                'To': v.get('date_range', [np.NaN, np.NaN])[1],
                'Full Name': v.get('full_name', np.NaN),
                'URL': v.get('web_url', np.NaN),
            } for k, v in cls.data.items()
        ]).set_index('Name')
    

    @classmethod
    def cache_add(cls, name, df) -> bool:
        """
        Adds a fully loaded dataframe to cache
        """

        if name not in cls._cache:
            cls._cache[name] = df
            return True

        return False
    

    @classmethod
    def cache_get(cls, name) -> pd.DataFrame:
        """
        Returns dataframe stored in cache
        """
        return cls._cache.get(name, pd.DataFrame()).copy()


    @classmethod
    def meta_cache_add(cls, name, meta) -> bool:
        """
        Adds metadata for particular dataset to cache
        """

        if name not in cls._meta_cache:
            cls._meta_cache[name] = meta
            return True

        return False
    

    @classmethod
    def meta_cache_get(cls, name) -> dict:
        """
        Returns metadata stored in cache
        """
        return cls._meta_cache.get(name, None)
