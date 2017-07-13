pythonic interface to version 3 of the courtlistener.com api (as of 7/13/17) --- for legal data crunching on cases, it's nice to have cases.

requires python 3.x.  Tested on OSX, should work on any unix-like, no clue whether it'll work on windows.

requires courtlistener.com api key, which can be gotten for free when you register on `courtlistener.com <https://www.courtlistener.com/register/>`_. 

**Usage** 

1. Initialize a connection object: ``conn = lawpy.session(api_key)``. By default, lawpy will look for an api key in an environment variable called COURTLISTENER, but you can also pass it explicitly to the session.
