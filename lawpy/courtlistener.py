import requests
import json
from html2text import html2text
from .utils import session_builder, request_builder, get_chain, pretty_dict, safe_merge

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
        self.citations = api_data.get("citation")
        self.court = get_chain(api_data, ["court", "court_exact", "court_id", "court_citation_string"])
        if "opinions" in api_data and api_data["opinions"]:
            self.opinions = [Opinion(op, self.name) for op in api_data["opinions"]]
        else:
            self.opinions = []
        self.opinion_shape = {0: None, 1: "singleton"}.get(len(self.opinions), "list")
        self.date = get_chain(api_data, ["date_filed", "dateFiled"])
        self.people = {
            "panel": api_data.get("panel"),
            "non_participating_judges": api_data.get("non_participating_judges"),
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



class courtlistener(object):
    def __init__(self):
        session_builder(self, "COURTLISTENER")(self)

    def request(self, endpoint="", headers={}, parameters=None):
        return request_builder(self, "https://www.courtlistener.com/api/rest/v3/")(self, endpoint, headers, parameters)

    def options(self, endpoint="", headers={}):
        ep = "https://www.courtlistener.com/api/rest/v3/" + endpoint
        h = {}
        h = safe_merge(h, headers)
        h = safe_merge(h, self.auth_header)
        return requests.options(ep, headers=h).json()

    def find_cite(self, cite):
        return self.request("search/", parameters={'citation': cite})

    def extract_case_searches(self, searchres):
        cases = []
        for res in searchres:
            bigdict = {}
            bigdict = safe_merge(bigdict, res)
            cluster = self.request("clusters/" + str(res["cluster_id"]))
            bigdict = safe_merge(bigdict, cluster)
            docket = self.request(cluster["docket"])
            bigdict = safe_merge(bigdict, docket)
            opinion_results = []
            for op in cluster["sub_opinions"]:
                opinion_results.append(self.request(op))
            bigdict = safe_merge(bigdict, {"opinions": opinion_results})
            cases.append(bigdict)
        return [Case(x) for x in cases]

    def search(self, search_header, noisy=False):
        current = self.request("search/", parameters=search_header)
        reslist = []
        while True:
            reslist = reslist + current["results"]
            if current["next"]:
                if noisy:
                    print("requesting: " + current["next"])
                current = self.request(current["next"])
            else:
                break
        return self.extract_case_searches(reslist)

    def fetch_cases_by_cite(self, cite):
        return self.search({'citation': cite})

    def fetch_cases_by_judge(self, judge):
        return self.search({'judge': judge})

# need to add more data in case and opinion objects.  also for stuff that might return either a singleton or a list I should just have getter functions that either map over the list or just dispatch for a single, so that it's easy to get results and reports.

# need to provide a facility to dump all cases straight to JSON

# also should store search strings for future record-keeping use?
