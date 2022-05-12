# Maintainer:     Ryan Young
# Last Modified:  May 10, 2022
import requests
import pandas as pd
import numpy as np
from copy import deepcopy

class MetaLibrary(type):
    """
    This is my solution to applying property decorator to class
    variables. This allows us to execute logic when the Library's
    variables are accessed. In this case, the 'data' variable
    won't be loaded with online api data until the variable
    is actually accessed for the first time. That way we aren't
    sending unnecessary api requests when the user doesn't need us to.
    """

    @property
    def data(cls):
        """
        Once user_data is set, cls.data will return user_data UNTIL
        user_data is set to None, using reset_sources. This 
        """
        if cls._data == None:
            try:
                cls._data = dict(requests.get(cls._url).json())
                cls._default_data = deepcopy(cls._data)
            except Exception as e:
                print("Can't find crime library sources.\nEither you don't have internet, or Github's API isn't working.")
                return dict()

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
    _default_data = None
    _data = None # default sources
    _cache = dict()
    _meta_cache = dict()

    # Try to load default sources online
    try:
        _data = dict(requests.get(_url).json())
        _default_data = deepcopy(_data)
    except Exception as e:
        _data = None
        _default_data = None


    @classmethod
    def add_data(cls, name, id, base_url, **kwargs):
        """
        Append new row to library data
        """
        date_range = [np.NaN, np.NaN]

        if "from_year" in kwargs:
            date_range[0] = kwargs.pop('from_year')
            kwargs['date_range'] = date_range

        if "to_year" in kwargs:
            date_range[1] = kwargs.pop('to_year')
            kwargs['date_range'] = date_range

        new = {name: {"id": id, "base_url": base_url, **kwargs}}
        cls.data.update(new)


    @classmethod
    def reset_data(cls):
        if cls._default_data != None:
            cls._data = deepcopy(cls._default_data)
        else:
            cls._data = dict(requests.get(cls._url).json())

    @classmethod
    def clear_data(cls):
        cls._data = dict()


    @classmethod
    def tabular(cls) -> pd.DataFrame:
        """
        Gives the end user the contents of the self.data dictionary
        as a pandas dataframe, including only the important fields,
        and excluding base_url and id.
        """
        if cls.data == dict():
            # we already know cls.data can't return None bcas of metaclass
            return pd.DataFrame()

        df = pd.DataFrame([
            {
                'Name': k,
                'Topic': v.get('topic', np.NaN),
                'Location': v.get('location', np.NaN),
                'Rows': v.get('rows', np.NaN),
                'Type': v.get('type', np.NaN),
                'From': v.get('date_range', [np.NaN, np.NaN])[0],
                'To': v.get('date_range', [np.NaN, np.NaN])[1],
                'Full Name': v.get('full_name', np.NaN),
                'Web URL': v.get('web_url', np.NaN),
            } for k, v in cls.data.items()
        ]).set_index('Name')
        df.index.name = None
        return df
    

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
        return cls._cache.get(name, pd.DataFrame()).copy(deep=True)


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
        return deepcopy(cls._meta_cache.get(name, None))
