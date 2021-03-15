Advanced Flask
================

Following our brief introduction to the Flask framework, we continue here with a
look at more complex endpoints and data retrieval functions for our REST API.
After going through this module, students should be able to:

* Identify valid and invalid Flask route return types
* Convert unsupported types (e.g. ``list``) to valid Flask route return types
* Extract Content-Type and other headers from Flask route responses
* Add query parameters to GET requests, and extract their values inside Flask routes


Defining the URLs of Our API
----------------------------

The first basic goal of our API is to provide an interface to a dataset. Since
the URLs in a REST API are defined by the "nouns" or collections of the
application domain, we can use a noun that represents our data.

For example, suppose we have the following dataset that represents the number of
students earning an undergraduate degree for a given year:

.. code-block:: python3

   def get_data():
       return [ {'id': 0, 'year': 1990, 'degrees': 5818},
       {'id': 1, 'year': 1991, 'degrees': 5725},
       {'id': 2, 'year': 1992, 'degrees': 6005},
       {'id': 3, 'year': 1993, 'degrees': 6123},
       {'id': 4, 'year': 1994, 'degrees': 6096} ]


In this case, one collection described by the data is "degrees". So, let's
define a route, ``/degrees``, that by default returns all of the data points.

EXERCISE 1
~~~~~~~~~~

Create a new file, ``degrees_api.py`` to hold a Flask application then do the
following:

* Import the Flask class and instantiate a Flask application object
* Add code so that the Flask server is started with this file is executed
  directly by the Python interpreter
* Copy the ``get_data()`` method above into the application script
* Add a route (``/degrees``) which responds to the HTTP ``GET`` request and
  returns the complete list of data returned by ``get_data()``

In a separate Terminal use ``curl`` to test out your new route. Does it work as
expected?

.. tip::

   Refer back to the `Intro to Flask material <../week06/intro_flask.html>`_ if
   you need help remembering the boiler-plate code.



Responses in Flask
------------------

If you tried to return the list object directly in your route function
definition, you got an error when you tried to request it with curl. Something
like:

.. code-block:: console

   TypeError: The function did not return a valid response

Flask allows you three options for creating responses:

1) Return a string (``str``) object
2) Return a dictionary (``dict``) object
3) Return a tuple (``tuple``) object
4) Return a ``flask.Response`` object

Some notes:

* Option 1 is good for text or html such as when returning a web page or text
  file
* Option 2 is good for returning rich information in JSON-esque format
* Option 3 is good for returning a list of data using a special type of Python
  list - a ``tuple`` - which is ordered and unchangeable
* Option 4 gives you the most flexibility, as it allows you to customize the
  headers and other aspects of the response.

For our REST API, we will want to return JSON-formatted data. We will use a
special Flask method to convert our list to JSON - ``flask.jsonify``. (More on
this later.)

.. tip::

   Refer back to the `Working with JSON material <../week02/json.html>`_ for a
   primer on the JSON format and relevant JSON-handling methods.


EXERCISE 2
~~~~~~~~~~

Serialize the list returned by the ``get_data()`` method above into a
JSON-formatted string using the Python ``json`` library. Verify that the type
returned is a string.

Next, Deserialize the string returned in part a) by using the ``json`` library
to decode it. Verify that the result equals the original list.



Returning JSON (and Other Kinds of Data)
----------------------------------------

You probably are thinking at this point we can fix our solution to **Exercise 1**
by using the ``json`` library (which function?). Let's try that and see what
happens:

EXERCISE 3
~~~~~~~~~~

Update your code for Exercise 1 to use the ``json`` library to return a properly
formatted JSON string.

Then, with your API server running in one window, open a Python3 interactive
session in another window and:

* Make a ``GET`` request to your ``/degrees`` URL and capture the response in a
  variable, say ``r``
* Verify that ``r.status_code`` is what you expect (what do you expect it to be?)
* Verify that ``r.content`` is what you expect
* Try to use ``r.json()`` to decode the response - does it work?
* Compare that with the response from the Bitbucket API to the URL
  ``https://api.bitbucket.org/2.0/repositories``

The issue you may be encountering has to do with the ``Content-Type`` header
being returned by the degrees API.


HTTP Content Type Headers
-------------------------

Requests and responses have ``headers`` which describe additional metadata about
them. Headers are ``key: value`` pairs (much like dictionary entries). The ``key``
is called the header name and the ``value`` is the header value.

There are many pre-defined headers for common metadata such as specifying the
size of the message (``Content-Length``), the domain the server is listening on
(``Host``), and the type of content included in the message (``Content-Type``).


Media Type (or Mime Type)
~~~~~~~~~~~~~~~~~~~~~~~~~

The allowed values for the ``Content-Type`` header are the defined
**media types** (formerly, **mime types**). The main thing you want to know
about media types are that they:

* Consist of a type and subtype
* The most common types are application, text, audio, image, and multipart
* The most common values (type and subtype) are application/json,
  application/xml, text/html, audio/mpeg, image/png, and multipart/form-data


Content Types in Flask
~~~~~~~~~~~~~~~~~~~~~~

The Flask library has the following built-in conventions you want to keep in
mind:

* When returning a string as part of a route function in Flask, a
  ``Content-Type`` of text/html is returned
* To convert a Python object to a JSON-formatted string **and** set the content
  type properly, use the ``flask.jsonify()`` function.

For example, the following code will convert the list to a JSON string and
return a content type of aplication/json:

.. code-block:: python3

   return flask.jsonify(['a', 'b', 'c'])


EXERCISE 4
~~~~~~~~~~

Use the ``flask.jsonify()`` method to update your code from Exercise 1. Then:


* Validate that your ``/degrees`` endpoint works as expected by using the
  ``requests`` library to make an API request and check that the ``.json()``
  method works as expected on the response.
* Use the ``.headers()`` method on the response to verify the ``Content-Type``
  is what you expect.


Query Parameters
----------------

The HTTP spec allows for parameters to be added to the URL in form of
``key=value`` pairs. Query parameters come after a ``?`` character and are
separated by ``&`` characters; for example, the following request:

.. code-block:: console

      GET https://api.example.com/degrees?limit=3&offset=2

Passes two query parameters: ``limit=3`` and ``offset=2``.

In REST architectures, query parameters are often used to allow clients to
provide additional, optional arguments to the request.

Common uses of query parameters in RESTful APIs include:

* Pagination: specifying a specific page of results from a collection
* Search terms: filtering the objects within a collection by additional search
  attributes
* Other parameters that might apply to most if not all collections such as an
  ordering attribute (``ascending`` vs ``descending``)


Extracting Query Parameters in Flask
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Flask makes the query parameters available on the ``request.args`` object, which
is a "dictionary-like" object. To work with the query parameters supplied on a
request, you must import the Flask request method (this is different from the
Python3 ``requests`` library), and use an imbedded method to extract the passed
query parameter into a variable:

.. code-block:: python3

   from flask import Flask, request

   @app.route('/degrees', methods=['GET'])
   def degrees():
       start = request.args.get('start')


The ``start`` variable will be the value of the ``start`` parameter, if one is
passed, or it will be ``None`` otherwise:

.. code-block:: console

   GET https://api.example.com/degrees?start=2


.. note::

   ``request.args.get()`` will always return a ``string``, regardless of the
   type of data being passed in.


EXERCISE 5
~~~~~~~~~~

Add support for a ``limit`` parameter to the code you wrote for Exercise 4. The
``limit`` parameter should be optional. When passed with an integer value, the
API should return no more than ``limit`` data points.



Additional Resources
--------------------

* `Flask JSON support <https://flask.palletsprojects.com/en/1.1.x/api/?highlight=jsonify#module-flask.json>`_
* `Flask query parameter support <https://flask.palletsprojects.com/en/1.1.x/api/?highlight=jsonify#flask.Request.args>`_
