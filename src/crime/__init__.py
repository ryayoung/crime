import requests
from crime.soda_api import Soda
from crime.crime import (
    Library,
    help,
    set_token,
    sources,
    load,
    df,
    set_sources,
    reset_sources,
    get_current_token,
    set_top_secret_token,
)

try:
    tokens = requests.get("https://raw.githubusercontent.com/ryayoung/crime/main/cloud_variables.json").json()
    Soda.token = tokens['app_token']
    Soda.alt_token = tokens.get('app_token_alt', None)
except Exception as e:
    Soda.token = None
    Soda.alt_token = None
