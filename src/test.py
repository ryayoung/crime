from sodapy import Socrata
import pandas as pd
import json

token = ""

def set_token(app_token):
    token = app_token

def get_info(base_url, source_id):
    pass


# client = Socrata("data.colorado.gov", app_token="POb9E2hovuHBBgdVFLt18TtEG")
client = Socrata("policedata.coloradosprings.gov", app_token="POb9E2hovuHBBgdVFLt18TtEG")

results = client.get_metadata("jw9n-x43p")
print(json.dumps(results, indent=2))
# results = client.get("6vnq-az4b", limit=2_000)
# df = pd.DataFrame.from_records(results)
# print(df)

