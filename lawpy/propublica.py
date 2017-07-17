from .utils import session_builder

class propublica(object):

    def __init__(self):
        session_builder(self, "PROPUBLICA", "https://api.propublica.org/congress/v1/", 'X-API-Key')(self)

    def bill_info_by_stub(self, congress, bill):
        ep = str(congress) + "/bills/" + bill + ".json"
        return self.request(endpoint=ep)
