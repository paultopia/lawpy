# BADLY NEEDS ERROR HANDLING FOR CASES WHERE SOMETHING MIGHT NOT BE RETURNED.

import os
from requests import get as g
from requests import options
import json
from html2text import html2text

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

class Opinion(object):
    def __init__(self, api_data, name):
        self.case_name = name
        self.html = get_chain(api_data, ["html", "html_columbia", "html_lawbox", "html_with_citations"])
        self.text = api_data.get("plain_text")
        if self.html:
            self.markdown=html2text(self.html)
        else:
            self.markdown = ""

    def __repr__(self):
        return "<lawpy Opinion (poss. one of several), " + self.case_name + ">"

    def __str__(self):
        return json.dumps(self.__dict__, sort_keys=True, indent=4)


class Case(object):
    def __init__(self, api_data):
        self.name = get_chain(api_data, ["case_name", "case_name_full", "caseName"])
        self.citation_count = get_chain(api_data, ["citation_count", "citeCount"])
        self.citations = api_data["citation"]
        self.court = get_chain(api_data, ["court", "court_exact", "court_id", "court_citation_string"])
        self.opinions = [Opinion(op, self.name) for op in api_data["opinions"]]
        self.opinion_shape = {0: None, 1: "singleton"}.get(len(self.opinions), "list")
        self.date = get_chain(api_data, ["date_filed", "dateFiled"])
        self.people = {
            "panel": api_data["panel"],
            "non_participating_judges": api_data["non_participating_judges"],
            'judges': get_chain(api_data, ["judges", "judge"]),
            "attorneys": get_chain(api_data, ["attorneys", "attorney"])
        }
        self.courtlistener_cluster = api_data.get("cluster_id")
        self.courtlistener_docket = api_data.get("docket")

    def __repr__(self):
        return "<lawpy Case, " + self.name + ">"

    def __str__(self):
        basics = {key: val for key, val in self.__dict__.items() if key != "opinions"}
        basics.update({"opinions": [x.__dict__ for x in self.opinions]})
        return json.dumps(basics, sort_keys=True, indent=4)



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
            bigdict = {}
            bigdict = safe_merge(bigdict, res)
            cluster = self.request("clusters/" + str(res["cluster_id"]))
            bigdict = safe_merge(bigdict, cluster)
            docket = self.raw_url_request(cluster["docket"])
            bigdict = safe_merge(bigdict, docket)
            opinion_results = []
            for op in cluster["sub_opinions"]:
                opinion_results.append(self.raw_url_request(op))
            bigdict = safe_merge(bigdict, {"opinions": opinion_results})
            cases.append(bigdict)
        return [Case(x) for x in cases]


# need to add more data in case and opinion objects.  also for stuff that might return either a singleton or a list I should just have getter functions that either map over the list or just dispatch for a single, so that it's easy to get results and reports.

# need to provide a facility to dump all cases straight to JSON
