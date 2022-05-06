# Maintainer:     Ryan Young
# Last Modified:  May 06, 2022
from sodapy import Socrata
import requests

import pandas as pd

class Soda:
    """
    A basic wrapper for sodapy, which is a wrapper to communicate
    with Socrata API.
    ---
    Holds the user's app token as a class variable, and wraps
    important functions by declaring a new Socrata() object client
    with each method call.
    """

    token:str = None

    @classmethod
    def client(cls, base_url:str) -> Socrata:
        """
        Returns a Socrata api object and the token. Don't
        worry, it's okay if cls.token is None. The Socrata
        object expects both of these positional variables,
        even if a token isn't being declared.
        """
        return Socrata(base_url, cls.token)


    @classmethod
    def get(cls, base_url:str, data_id:str, full=False, **kwargs) -> pd.DataFrame:
        """
        Creates a Socrata client using base url, and then
        retrieves data with data_id, passing any additional kwargs
        to client.get()
        ---
        Returns: pd.DataFrame
        """
        if 'limit' not in kwargs:
            if full == False:
                limit = 5
                print("Pass 'full=True' to get full dataset.")
            else:
                limit = 10_000_000

        client = cls.client(base_url)

        if 'limit' in kwargs:
            data = client.get(data_id, **kwargs)
        else:
            data = client.get(data_id, limit=limit, **kwargs)

        return pd.DataFrame.from_records(data)


    @classmethod
    def get_metadata(cls, base_url:str, data_id:str, content_type="json") -> dict:
        """
        Works just like get, except doesn't accept keyword args,
        and returns the dataset's metadata as a dictionary, instead
        of dataframe.
        """
        client = cls.client(base_url)

        try:
            data = client.get_metadata(data_id, content_type)
        except Exception as e:
            print("INVALID ID")
            return

        return dict(data)
    

    @classmethod
    def datasets(cls, base_url:str, fmt="df", **kwargs) -> pd.DataFrame or list:
        """
        Retrieves metadata on all datasets within a given domain.
        """
        client = cls.client(base_url)

        try:
            data = client.datasets(**kwargs)
        except Exception as e:
            print("INVALID DOMAIN")
            return

        if fmt == "df":
            return pd.DataFrame.from_records(data)
        elif fmt == "dict":
            return [dict(d) for d in data]
        else:
            raise ValueError("Invalid 'fmt' attribute. Choose 'dict' or 'df'.")



