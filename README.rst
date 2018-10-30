**Lawpy: Get You Some Legal Data**

Pythonic interface to (U.S.) legal data APIs.  Includes: courtlistener.com (U.S. legal cases), propublica (U.S. Congress, votes, bills), openstates (U.S. state legislators, bills), and the regulations API of data.gov (U.S. federal administrative regulations). 

Requires python 3.x.  Tested on OSX, should work on any unix-like, no clue whether it'll work on windows.

(this is a random edit for a test.  Yay random edit.)


[add fec api! https://api.open.fec.gov/developers/ and other us gov: https://api.data.gov/docs/ ]

master list of APIs to wrap:

courtlistener (in progress) env=COURTLISTENER
e
propublica (in progress) env=PROPUBLICA

api.data.gov (have api key, not yet started) env=DATAGOV

openstates.org (have api key, not yet started) env=OPENSTATES


Does not include opensecrets, their api is sufficiently nonstandard that it would require a big refactor to get it working, but check our their python wrapper at: https://github.com/opensecrets/python-crpapi 

**GENERAL USAGE**

For each of the APIs covered, you'll need to get an API token from the provider.  Then you can either set that in an environment variable on your system (see below for the correct names), or pass to a constructor function.

Each API has its own constructor function, which is used to initialize a session at that provider.  Access to the APIs is then provided by a series of custom methods on that constructor function.  For example::

  import lawpy

  sess = lawpy.courtlistener()

  brown_v_board=sess.fetch_cases_by_cite("347 U.S. 483")

The specific methods and data structures returned are documented below.

There is also a ``to_pandas()`` global function that takes a list of objects (which must be of the same time) and returns a Pandas DataFrame containing all the contents of that list (TODO).

Generally, this library is designed for two workflows:

1.  Discrete data fetching: if you want a case, or a summary of a bill, or something, then you can stick around in lawpy data structures, which provide convenience methods for pretty-printing and reading, fetching associated information, etc. (TODO).

2.  Data analysis on large batches of documents: you can run searches producing a chunk of case, legislative, etc. data and then bail out directly to Pandas; from there, you're on your own wrt things like bringing together data from disparate sources, etc. 

**Contributing**

Adding more methods to get different, useful, kinds of data, or more entire legal APIs, is highly encouraged.  I'm also totally open to PRs refactoring some of my craziness, or to adding compatibility with Python 2.

There are (woefully incomplete) tests, but you need an api key to run them.  If you change something, please add a test for the old and new behavior.  I use nose2 for testing.  Please try and be conservative with hitting APIs for testing, no need to waste the resources of the nonprofits whose libraries are being wrapped. (For example, please have your tests pull down one or two items, not thousands.)

At time of 0.1 release, the courtlistener API is most developed, and can be considered basically feature-complete.  The other APIs are less well developed, primarily because I have less of an idea what would be most useful to people---those APIs could use contributors to help fill them out, although I will slowly do so over the coming months.

**INDIVIDUAL API DOCUMENTATION**

**Courtlistener**

Provides legal cases.  They also have other data, like data about individual judges, who appointed them, etc., but I consider that low-priority, and so have not implemented a robust set of methods to search that.  Pull requests welcome. 

To get an API token, register on `courtlistener.com <https://www.courtlistener.com/register/>`_.  You may pass it to the courtlistener constructor, or (if not passed) lawpy will look for an api key in an environment variable called COURTLISTENER.

Uses version 3 of the courtlistener.com api (as of 7/13/17).

In the below, we assume that conn is a connection initialized with the courtlistener constructor. 

1. Fetch a case(s) by citation: ``mycases = conn.fetch_cases_by_cite(citation)``.  Takes a single citation, e.g., "373 U.S. 668", and returns all cases matching that citation. ``mycases`` will be a *list* of ``Case`` objects (which may be empty, or may contain just one case... actually, it should usually just contain one case, but it's always alist in any event), see below for the properties and methods of that object.


*the Case object*

if ``somecase`` is an instance of ``Case``:

*Key Properties*

``somecase.name`` is the name of the case.

``somecase.court`` is the court that heard the case.

``somecase.citations`` is a list of citations for the case (i.e., potentially across several reporters).

``somecase.date`` is the filing date.

``somecase.opinion`` is a list of ``Opinion`` objects associated with the case (which may contain 0, 1, or several items).  See below for the ``Opinion`` object.

``somecase.people.judges`` is a list of judges on the case. If that doesn't return anything, try ``somecase.people.panel``. 

*Methods and functions*

``somecase.citations()`` (WIP NOT IMPLEMENTED YET) will fetch and return a list of all cases that cite this case (so long as courtlistener has identified them).

``str(somecase)`` returns a pretty-printed JSON string of all the data in a case (including underlying opinions). This is suitable to read on screen or save directly to a JSON file. If you want raw python data structures, you can also pass this directly to standard library ``json.loads`` and it should behave just fine.

Similarly, if you have a list of cases, the easiest and most strightforward way to get raw json data out of them is ``rawdata = [json.loads(str(case)) for case in mycases]``. 


*The Opinion Object*

``someopinion.case_name`` is the name of the case associated with the opinion (if there are multiple opinions associated with a case, this property will be non-unique).

``someopinion.html`` is a html representation of the opinion text.

``someopinion.text`` is a plaintext representation of the opinion text. (Often does not exist.)

``someopinion.markdown`` is a markdown representation of the opinion text.


Not all properties are guaranteed to be present or in the same format for every case or opinion.  There are some redundancies and inconsistencies in the courtlistener API, as well as data gaps, and I've done my best to smooth over those as much as possible. In general, where there is a more informative/useful version of some property and a less informative/useful version, this library looks for the most useful version, and, if that isn't present, takes the less useful version; if neither is present it just fills the slot with ``None``. 

**Propublica**

**Openstates**

Environment variable: OPENSTATES.  `Get an API key from their site <https://openstates.org/api/register/>`.

1. Get legislators by state. ``conn.legislators_by_state(state, options=None)``.
