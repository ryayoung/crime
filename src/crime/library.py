# Maintainer:     Ryan Young
# Last Modified:  May 05, 2022
import requests
import pandas as pd

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
    _data = None
    try:
        _data = dict(requests.get(_url).json())
    except Exception as e:
        _data = None


    @classmethod
    def tabular(cls):
        """
        Gives the end user the contents of the self.data dictionary
        as a pandas dataframe, including only the important fields,
        and excluding base_url and id.
        """
        return pd.DataFrame([
            {
                'Name': k,
                'Location': v['location'],
                'Rows': v['rows'],
                'Type': v['type'],
                'From': v['date_range'][0],
                'To': v['date_range'][1],
                'URL': v['web_url']
            } for k, v in cls.data.items()
        ]).set_index('Name')
