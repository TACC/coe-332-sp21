Flask, Continued
================

We first continue our discussion of the Flask framework so that we are
ready to expose our data retrieval functions from homework 1 as a
RESTful API.

Defining the URLs of Our API
----------------------------

The first basic goal of our API is to provide an interface to our
dataset, which is a set of data points in a time series. Since the URLs
in a REST API are defined by the "nouns" or collections of the
application domain, we can use a noun that represents.

For example, suppose we have the following dataset that represents the
number of students earning an undergraduate degree for a given year.

::

    def get_data():
        return [{'id': 0, 'year': 1990, 'degrees': 5818},
        {'id': 1, 'year': 1991, 'degrees': 5725},
        {'id': 2, 'year': 1992, 'degrees': 6005},
        {'id': 3, 'year': 1993, 'degrees': 6123},
        {'id': 4, 'year': 1994, 'degrees': 6096},
        ]

In this case, the collection described by the data is "degrees". So,
let's define a route, ``/degrees``, that by default returns all of the
data points.

Exercise. Create a new file, ``degrees_api.py`` to hold a Flask
application then do the following:

-  import the Flask class and instantiate a Flask application object.
-  add code so that the Flask server is started when ths module is
   executed directly by the Python interpreter.
-  copy the ``get_data`` function above in the module.
-  Add a route, ``/degrees``, which responds to the HTTP GET verb and
   returns the complete list of data returned by ``get_data``.

You can look back at the previous Intro to Flask lecture from last week
if you need help remembering the boiler-plate code.

Exercise 2. In a separate terminal on your VM, use curl to test out your
new route. Does it work as expected?

Responses in Flask
------------------

If you tried to return the list object directly in your route function
definition, you got an error when you tried to request it with curl
(something like ``"TypeError”: 'list' object is not callable flask``).
Flask allows you three options for creating responses:

-  

   1) Return a string (``str``) object

-  

   2) Return a raw bytes (``bytes``) object.

-  

   3) Return a ``flask.Response`` object.

Some notes:

-  Option 1) is good for text or html such as when returning a web page
   or text file.
-  Option 2) is useful when returning binary data such as an image or an
   audio file.
-  Option 3) gives you the most flexibility, as it allows you to
   customize the headers and other aspects of the response.

For our REST API, we will return JSON data, which is a string that has
been formatted in a special way. But instead of returning a string
directly, we will use a flask helper function, ``flask.jsonify``. See
below.

Working with JSON
-----------------

JSON (JavaScript Object Notation) is a data serialization format that is
quickly becoming one of the most popular data formats on the web. Here
we review the basics of JSON:

-  JSON allows one to convert from structured data objects (e.g. Python
   lists or dictionaries) to strings that can be transmitted over a
   network as "messages".
-  JSON also allows one to convert these strings back to structured data
   objects.
-  The process of converting from strctured data to a string is called
   ``encoding``.
-  The reverse process of converting a JSON-formatted string to a
   structured data object is called "decoding".

Modern programming languages provide libraries for ``encoding`` and
``decoding`` JSON data. For Python:

-  The ``json`` library is part of the standard library and can be
   imported with ``import json``.
-  The ``json.dumps()`` function will encode a Python object and return
   a string.
-  The ``json.loads()`` function will decode a JSON string and create a
   Python object.
-  Only relatively "simple" Python objects can be encoded; just built-in
   types: ``str``, ``int``, ``bool``, ``float``, ``list`` and ``dict``.
-  Only properly formatted JSON strings can be decoded, otherwise a
   ``JSONDecodeError`` exception will be thrown.

Exercise 3.

-  

   a) Serialize the list returned by the ``get_data`` function above
      into a JSON-formatted string using the ``json`` library. Verify
      that the type returned is a string.

-  

   b) Deserialize the string returned in part a) by using the ``json``
      library to decode it. Verify that the result equals the original
      list.

Content Type Headers and Returning JSON (and Other Kinds of Data)
-----------------------------------------------------------------

You probably are thinking at this point we can fix our solution to
Exercise 2 by using the ``json`` library (which function?). Let's try
that and see what happens.

Exercise 4. Update your code for exercise 2 to use the ``json`` library
to return a properly formatted JSON string.

Exercise 5. With your API server running in one window, open a python3
shell in another window and

-  

   a. Make a GET request to your ``/degrees`` URL and capture the
      response in a variable, say ``r``.

-  

   b. Verify that ``r.status_code`` is what you expect (what do you
      expect it to be?).

-  

   c. Verify that ``r.content`` is what you expect.

-  

   d. Now, try to use ``r.json()`` to decode the response. Does it work?

-  

   e. Compare that with the response from the bitbucket API to the URL
      ``https://api.bitbucket.org/2.0/repositories``.

The issue you are encountering has to do with the ``Content-Type``
header being returned by the degrees API.

HTTP Headers
~~~~~~~~~~~~

-  Requests and Responses have ``headers`` which describe additional
   metadata about them.
-  Headers are ``key: value`` pairs (much like dictionary entries). The
   key is called the header name and the value is the header value.
-  There are many pre-defined headers for common metadata such as
   specifying the size of the message (``Content-Length``), the domain
   the server is listening on (``Host``) and the type of content
   included in the message (``Content-Type``).

Media Type (or Mime Type)
~~~~~~~~~~~~~~~~~~~~~~~~~

The allowed values for the ``Content-Type`` header are the defined
``media types`` (formerly, ``mime types``). The main thing you want to
know about media types are that they

-  Consist of a type and subtype.
-  The most common types are ``application``, ``text``, ``audio``,
   ``image`` and ``multipart``.
-  The most common values (type and subtype) are ``application/json``,
   ``application/xml``, ``text/html``, ``audio/mpeg``, ``image/png``,
   and ``multipart/form-data``.

Content Types in Flask
~~~~~~~~~~~~~~~~~~~~~~

The Flask library has the following built-in conventions you want to
keep in mind:

-  When returning a string as part of a route function in Flask, a
   ``Content-Type`` of ``text/html`` is returned.
-  To convert a Python object to a JSON-formatted string **and** set the
   content type properly, use the ``flask.jsonify()`` function.

For example, ``return flask.jsonify(['a', 'b', 'c'])`` will convert the
list to a JSON string and return a content type of ``application/json``.

Exercise 6.

-  

   a. Use the ``flask.jsonify()`` method to update your code from
      Exercise 2.

-  

   b. Validate that your ``/degrees`` endpoint works as expected by
      using the ``requests`` library to make an API request and check
      that the ``.json()`` method works as expected on the response.

-  

   c. Use the ``.headers()`` method on the response to verify the
      ``Content-Type`` is what you expect.

Query Parameters
----------------

The HTTP spec allows for parameters to be added to the URL in form
``key=value`` pairs. Query parameters come after a ``?`` character and
are separated by ``&`` characters; for example, the following request:

::

      GET https://api.example.com/degrees?limit=3&offset=2

passes two query parameters: ``limit=3`` and ``offset=``.

In REST architectures, query parameters are often used to allow clients
to provide additional, optional arguments to the request.

Common uses of query parameters in RESTful APIs include:

-  Pagination: specifying a specific page of results from a collection.
-  Search terms: filtering the objects within a collection by additional
   search attributes.
-  Other parameters that might apply to most if not all collections such
   as an ordering attribute (``ascending`` vs ``descending``).

Extracting Query Parameters in Flask
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Flask makes the query parameters available on the ``request.args``
object, which is a "dictionary-like" object. To work with the query
parameters supplied on a request, add the following:

-  Import the ``request`` object at the top of your program:
   ``from flask import request``
-  In your route function, use the ``.get()`` method on the
   ``request.args`` object to get the value of a parameter.

For example, in the following code:

::

    from flask import Flask, request

    @app.route('/degrees', methods=['GET'])
    def degrees():
        start = request.args.get('start')

the ``start`` variable will be the value of the ``start`` parameter, if
one is passed, or it will be ``None`` otherwise.

Note: ``request.args.get()`` will always return a **string**, regardless
of the type of data being passed in.

Exercise 7. Add support for a ``limit`` parameter to the code you wrote
for exercise 6. The ``limit`` parameter should be optional. When passed
with an integer value, the API should return no more than ``limit``
degrees datapoints.
