import os
import requests
import json
from .utils import *

class propublica(object):
    def __init__(self, api_key="ENV"):
        if api_key == "ENV":
            try:
                self.api_key = os.environ['PROPUBLICA']
            except KeyError as e:
                raise Exception("API key is missing. Please set the COURTLISTENER environment variable or pass the key to the session constructor. You can get an API key directly from courtlistner.com by registering on their website.") from e
        else:
            self.api_key = api_key
        self.auth_header = {'X-API-Key': self.api_key}
        self.total_requests_this_session = 0

    def request(self, endpoint="", headers={}, parameters=None):
        if endpoint.startswith("https://"):
            ep = endpoint
        else:
            ep = "https://api.propublica.org/congress/v1/" + endpoint
        h = {}
        h = safe_merge(h, headers)
        h = safe_merge(h, self.auth_header)
        result = requests.get(ep, headers=h, params=parameters)
        self.total_requests_this_session += 1
        result.raise_for_status()
        return result.json()

    def bill_info_by_stub(self, congress, bill):
        ep = str(congress) + "/bills/" + bill + ".json"
        return self.request(endpoint=ep)
