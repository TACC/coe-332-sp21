Introduction to Application Programming Interfaces (APIs)
=========================================================

In general an Application Programming Interface (API) establishes the
protocols and methods for one piece of a program to communicate with
another.

-  Allow larger software systems to be built from smaller components.
-  Allow the same component/code to be used by different systems.
-  Insulate consumers from changes to the implementation.

Some examples of APIs:

-  In OOP languages, abstract classes provide the interface for all
   concrete classes to implement.
-  Software libraries provide an external interface for consuming
   programs.
-  Web APIs (or “web services”) provide interfaces for computer programs
   to communicate over the internet.

Web APIs
~~~~~~~~

In this course, we will focus on web APIs (or HTTP APIs). These are
interfaces that are exposed over HTTP.

Advantages of Web APIs
^^^^^^^^^^^^^^^^^^^^^^

There are a number of advantages to Web-bases APIs that we will take
advantage of in this class:

-  A web API is accessible from any computer or application that has
   access to the public internet.
-  No software installation is required on the client's side to consume
   a web API.
-  Web APIs can change their implementation without clients knowing (or
   caring).
-  Virtually every modern programming language provides one or more
   libraries for interacting with a web API - thus, "language agnostic".

HTTP - the Protocol of the Internet
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

-  HTTP (Hyper Text Transfer Protocol) is one way for two computers on
   the internet communicate with each other.
-  It was designed to enable the exchange of data (specifically,
   "hypertext"); In particular, our web browsers use HTTP when
   communicating with web servers running web applications.
-  HTTP uses a message-based, client-server model: clients make
   ``requests`` to servers by sending a message, and servers respond by
   sending a message back to the client.
-  HTTP is an "application layer" protocol in the language of the
   Internet Protocols; it assumes a lower level transport layer
   protocol. While this can swapped, in practice it is almost always
   TCP.

The basics of the protocol are:

-  Web resources are identified with URLs (Uniform Resource Locators).
   Originally, ``resources`` were just files/directories on a server,
   but today resources refer to more general objects.
-  HTTP "verbs" represent actions to take on the resource. The most
   common verbs are GET, POST, PUT and DELETE.
-  A request is made up of a URL, an HTTP verb, and a message. The
   message
-  A response consists of a status code (numerical between 100-599) and
   a message. The first digit of the status code specifies the kind of
   response:

   -  1xx - informational
   -  2xx - success
   -  3xx - redirection
   -  4xx - error in the request (client)
   -  5xx - error fulfilling a valid request (server).

REST APIs - Overview
^^^^^^^^^^^^^^^^^^^^

REST (Representational state transfer) is a way of building APIs for
computer programs on the internet leveraging HTTP in following sense:

-  A program on computer 1 interacts with a program on computer 2 by
   making an HTTP request to it.
-  “Resources” are the nouns of the application domain and are
   associated with URLs.

   -  The API has a base URL from which all other URLs in the API are
      formed. For example, ``https://api.github.com``
   -  The other URLs in the API are either:
   -  entire collections, such as ``<base_url>/users``,
      ``<base_url>/files``, ``<base_url>/programs``, etc.
   -  specific items in a collection, such as ``<base_url>/users/3`` or
      ``<base_url>/files/test.txt``

-  “Operations” are the actions that can be taken on the resources and
   are associated with HTTP verbs:

   -  GET - list items in a collection or retrieve a specific item in
      the collection.
   -  POST - create a new item in the collection based on the
      description in the message.
   -  PUT - replace an item in a collection with the description in the
      message.
   -  DELETE - delete an item in a collection.

-  Collection names can be "chained" to reference subcollections; e.g.
   ``<base_url>/companies/<company_id>/employees`` - all employees of
   the company ``<company_id>``.
-  Response messages often make use of some data serialization format
   standard such as JSON or XML.

REST APIs - some toy examples
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Virtually every application domain can be mapped into a REST API
architecture. Some examples include:

-  Articles in a collection (e.g., on a blog or wiki) with author
   attributes: ``<base_url>/articles``,
   ``<base_url>/articles/<id>,``\ /articles//authors\`
-  Properties in a real estate database with associated purchase
   history: ``<base_url>/properties``,
   ``<base_url>/properties/<id>,``\ /properties//purchases\`
-  A catalog of countries, cities and neighborhoods:
   ``<base_url>/countries``,
   ``<base_url>/countries/<country_id>/cities``,
   ``<base_url>/countries/<country_id>/cities/<city_id>/neighborhoods``

Real REST APIs - the Bitbucket APIs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Open a web browser and navigate to:
``https://api.bitbucket.org/2.0/repositories``

-  Your browser made a GET request to the bitbucket API. What you see is
   a JSON object describing public repositories.
-  You notice the response message is formatted in JSON.
-  You will see three top level objects in the response: ``pagelen``
   (int), ``values`` (list) and ``next`` (string). What do you think
   each is?

::

    Exercise 1. Were all bitbucket repositories returned? How many were returned? What URL would you use to get the next set of repositories?

    Exercise 2. What URL would we use to get a list of public repositories owned by a specific user?

    Exercise 3. What URL would we use to get a list of commits for a specific public repository?

Using the Python requests library
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We'll use the python requests library to interact with the github API
programmatically.

we need to pip3 install the request library

::

    pip3 install --user request

In order to do anything, we need to:

::

    import requests

The basic usage of the requests library is as follows:

::

    # make a request
    response = requests.<method>(url=some_url, data=some_message, <other options>)

    # work with the response:

    response.status_code -- the status code

    response.content -- the raw content

    response.json() -- for services returning JSON, create a Python list or dictionary from the response message.

Let's explore the Bitbucket API using the requests library in a Python
program. Write functions to return the following:

::

    1. Retrieve a list of public bitbucket repositories.
    2. Retrieve a list of public bitbucket repositories for a particular user.
    3. Retrieve a list of pull requests for a particular public bitbucket repository.

