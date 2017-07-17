import os
import requests
import json

def get_chain(source, alternatives):
    for a in alternatives:
        if a in source and source[a]:
            return source[a]
    return None

def pretty_dict(some_dictionary):
    return json.dumps(some_dictionary, sort_keys=True, indent=4)

def safe_merge(d1, d2):
    keys = set(d1.keys()).union(set(d2.keys()))
    result = {}
    for k in keys:
        if k in d2 and d2[k]:
            result.update({k: d2[k]})
        elif k in d1 and d1[k]:
            result.update({k: d1[k]})
        else:
            result.update({k: None})
    return result

def session_builder(selfvar, keyenv):
    def class_init(selfvar, api_key="ENV"):
        if api_key == "ENV":
            try:
                selfvar.api_key = os.environ[keyenv]
            except KeyError as e:
                raise Exception("API token is missing. Please set the {} environment variable or pass the token to the session constructor.".format(keyenv)) from e
        else:
            selfvar.api_key = api_key
        selfvar.auth_header = {'X-API-Key': selfvar.api_key}
        selfvar.total_requests_this_session = 0
    return class_init

def request_builder(selfvar, baseurl):
    def request(selfvar, endpoint="", headers={}, parameters=None):
        if endpoint.startswith("https://"):
            ep = endpoint
        else:
            ep = baseurl + endpoint
        h = {}
        h = safe_merge(h, headers)
        h = safe_merge(h, selfvar.auth_header)
        result = requests.get(ep, headers=h, params=parameters)
        selfvar.total_requests_this_session += 1
        result.raise_for_status()
        return result.json()
    return request
