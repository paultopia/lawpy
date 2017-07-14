import os
from requests import get as g
from requests import options
import json

def pretty_dict(some_dictionary):
    return json.dumps(some_dictionary, sort_keys=True, indent=4)

class session(object):
    def __init__(self, api_key="ENV"):
        if api_key == "ENV":
            try:
                self.api_key = os.environ['COURTLISTENER']
            except KeyError as e:
                raise Exception("API key is missing. Please set the COURTLISTENER environment variable or pass the key to the session constructor. You can get an API key directly from courtlistner.com by registering on their website.") from e
        else:
            self.api_key = api_key
        self.auth_header = {'Authorization': 'Token ' + self.api_key}

    def get_key(self):
        return self.api_key

    def request(self, endpoint="", headers={}, parameters=None):
        url = "https://www.courtlistener.com/api/rest/v3/" + endpoint
        h = headers.update(self.auth_header)
        return g(url, headers=h, params=parameters).json()

    def raw_url_request(self, endpoint, headers={}, parameters=None):
        h = headers.update(self.auth_header)
        return g(endpoint, headers=h, params=parameters).json()

    def options(self, endpoint="", headers={}):
        url = "https://www.courtlistener.com/api/rest/v3/" + endpoint
        h = headers.update(self.auth_header)
        return options(url, headers=h).json()

    def find_cite(self, cite):
        return self.request("search/", parameters={'citation': cite})

    def fetch_cases_by_cite(self, cite):
        searchres = self.request("search/", parameters={'citation': cite})
        cases = []
        for res in searchres["results"]:
            print(res)
            bigdict = {}
            print(bigdict)
            bigdict.update(res)
            cluster = self.request("clusters/" + str(res["cluster_id"]))
            bigdict.update(cluster)
            opinion_results = []
            for op in cluster["sub_opinions"]:
                opinion_results.append(self.raw_url_request(op))
            bigdict.update({"opinions": opinion_results})
            cases.append(bigdict)
        return cases


# result.json just parses a json and gives a dict, it's amazing. 

# search -> cluster -> opinion

# search endpoint gives me a list of results under the results key. Each result hopefully will have a cluster_id. Then I can loop over the clusterIDs and clusters will have a list of sub_opinions.

#class Case(object):
#    def __init__(self, )
