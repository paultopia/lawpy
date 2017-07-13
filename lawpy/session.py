import os
from requests import get as g
from requests import options

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

    def request(self, endpoint="", headers={}):
        url = "https://www.courtlistener.com/api/rest/v3/" + endpoint
        h = headers.update(self.auth_header)
        return g(url, h)

    def options(self, endpoint):
        return "foo"

