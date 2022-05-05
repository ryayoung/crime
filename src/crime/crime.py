# Maintainer:     Ryan Young
# Last Modified:  May 05, 2022
from sodapy import Socrata
import pandas as pd
import json

"""
THE PLAN
---
App key
- Function to let someone set it
- Secret function for bia students to use mine
- Allow the api to be used without app key
---
Displaying sources
- Sources function to view all source names, row count, type, location, and url
- Pass name of source to view its details. An api request will be sent.
- Head function to view just the first 10 rows of any source
"""
def something():
    pass




client = Socrata("data.colorado.gov", app_token="POb9E2hovuHBBgdVFLt18TtEG")

results = client.get_metadata("6vnq-az4b")
print(json.dumps(results, indent=2))
# results = client.get("6vnq-az4b", limit=2_000)
# df = pd.DataFrame.from_records(results)
# print(df)
