**Lawpy: Legal and Political Data**

Pythonic interface to legal and political data APIs.  Includes: courtlistener.com (U.S. legal cases), propublica (U.S. Congress, votes, bills), opensecrets (U.S. campaign finance data) [OTHERS?]

Requires python 3.x.  Tested on OSX, should work on any unix-like, no clue whether it'll work on windows.


[CHANGING: need to rewrite. session is now courtlistener, because I've decided to include a bunch of other APIS as well, courtlistener, propublica, eu law, canadian law]

[add fec api! https://api.open.fec.gov/developers/ and other us gov: https://api.data.gov/docs/ ]

**APIs Included**

Courtlistener.com.  Requires courtlistener.com api key, which can be gotten for free when you register on `courtlistener.com <https://www.courtlistener.com/register/>`_.  You may pass it to the courtlistener constructor, or (if not passed) lawpy will look for an api key in an environment variable called COURTLISTENER.

Uses version 3 of the courtlistener.com api (as of 7/13/17).

Example: ``import lawpy; sess = lawpy.courtlistener(); brown = sess.fetch_cases_by_cite("347 U.S. 483") + sess.fetch_cases_by_cite("349 U.S. 294")``


**Usage** 

Initialize a connection object: ``conn = lawpy.courtlistener(api_key)``. By default, 

You must initialize a connection before you can do anything else.

**Affordances**

1. Fetch a case(s) by citation: ``mycases = conn.fetch_cases_by_cite(citation)``.  Takes a single citation, e.g., "373 U.S. 668", and returns all cases matching that citation. ``mycases`` will be a *list* of ``Case`` objects (which may be empty, or may contain just one case... actually, it should usually just contain one case, but it's always alist in any event), see below for the properties and methods of that object.



**the Case object**

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


**The Opinion Object**

*Key Properties*

``someopinion.case_name`` is the name of the case associated with the opinion (if there are multiple opinions associated with a case, this property will be non-unique).

``someopinion.html`` is a html representation of the opinion text.

``someopinion.text`` is a plaintext representation of the opinion text. (Often does not exist.)

``someopinion.markdown`` is a markdown representation of the opinion text.


Not all properties are guaranteed to be present or in the same format for every case or opinion.  There are some redundancies and inconsistencies in the courtlistener API, as well as data gaps, and I've done my best to smooth over those as much as possible. In general, where there is a more informative/useful version of some property and a less informative/useful version, this library looks for the most useful version, and, if that isn't present, takes the less useful version; if neither is present it just fills the slot with ``None``. 


(note to self: need to add an examples directory).
