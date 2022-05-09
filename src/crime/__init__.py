import requests
from crime.crime import (
    Library,
    help,
    set_token,
    metadata,
    sources,
    columns,
    load,
    df,
    set_sources,
    reset_sources,
    get_current_token,
    set_top_secret_token,
)
from crime.soda_api import Soda

"""
Since we're declaring app token for the user, we should have a backup token in case
the main one fails.
---
Additionally, both of these tokens should be declared in an external file, in case they
need to be changed quickly.
"""
try:
    tokens = requests.get("https://raw.githubusercontent.com/ryayoung/crime/main/cloud_variables.json").json()
    Soda.token = tokens['app_token']
    Soda.alt_token = tokens.get('app_token_alt', None)
except Exception as e:
    Soda.token = None
    Soda.alt_token = None
