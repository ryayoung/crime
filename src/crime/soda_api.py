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
    alt_token:str = None

    @classmethod
    def client_get(cls, base_url, data_id, **kwargs):
        """
        Try to make request. If request fails, try with alt token
        """
        try:
            client = Socrata(base_url, cls.token)
            return client.get(data_id, **kwargs)
        except Exception as e:
            client = Socrata(base_url, cls.alt_token)
            return client.get(data_id, **kwargs)


    @classmethod
    def client_get_metadata(cls, base_url, data_id, content_type):
        """
        Try to make request. If request fails, try with alt token
        """
        try:
            client = Socrata(base_url, cls.token)
            return client.get_metadata(data_id, content_type)
        except Exception as e:
            client = Socrata(base_url, cls.alt_token)
            return client.get_metadata(data_id, content_type)


    @classmethod
    def get(cls, base_url:str, data_id:str, full=False, suppress_warning=False, **kwargs) -> pd.DataFrame:
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
                if suppress_warning == False:
                    print("Pass 'full=True' to get full dataset.")
            else:
                limit = 10_000_000

        if 'limit' in kwargs:
            data = cls.client_get(base_url, data_id, **kwargs)
        else:
            data = cls.client_get(base_url, data_id, limit=limit, **kwargs)

        return pd.DataFrame.from_records(data)


    @classmethod
    def get_metadata(cls, base_url:str, data_id:str, content_type="json") -> dict:
        """
        Works just like get, except doesn't accept keyword args,
        and returns the dataset's metadata as a dictionary, instead
        of dataframe.
        """
        try:
            data = cls.client_get_metadata(base_url, data_id, content_type)
        except Exception as e:
            print("INVALID ID")
            return

        return dict(data)

