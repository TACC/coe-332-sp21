Introduction to APIs
====================

An Application Programming Interface (API) establishes the protocols and methods
for one piece of a program to communicate with another. APIs are useful for (1)
allowing larger software systems to be built from smaller components, (2)
allowing the same component/code to be used by different systems, and (3)
insulating consumers from changes to the implementation.

Some examples of APIs:

* In OOP languages, abstract classes provide the interface for all concrete
  classes to implement
* Software libraries provide an external interface for consuming programs
* Web APIs (or “web services”) provide interfaces for computer programs to
  communicate over the internet

In this section, we will see some Web APIs, and in particular REST APIs, and we
will learn how to interact with them using Python scripts. After going through
this module, students should be able to:

* Identify and describe Web APIs (including REST APIs)
* Find API endpoints to various websites, e.g. Bitbucket and GitHub
* List and define the four most important HTTP verbs
* Install and import the Python requests library
* Interact with a web API using the Python requests library, and parse the
  return information


Web APIs
--------

In this course, we will focus on Web APIs (or HTTP APIs). These are interfaces
that are exposed over HTTP. There are a number of advantages to Web-based APIs
that we will use in this class:

* A Web API is accessible from any computer or application that has access to
  the public internet
* No software installation is required on the client's side to consume a web API
* Web APIs can change their implementation without clients knowing (or caring)
* Virtually every modern programming language provides one or more libraries for
  interacting with a web API - thus, "language agnostic"


HTTP - the Protocol of the Internet
-----------------------------------

HTTP (Hyper Text Transfer Protocol) is one way for two computers on the internet
to communicate with each other. It was designed to enable the exchange of data
(specifically, "hypertext"). In particular, our web browsers use HTTP when
communicating with web servers running web applications. HTTP uses a
message-based, **client-server model**: clients make requests to servers by
sending a message, and servers respond by sending a message back to the client.

HTTP is an "application layer" protocol in the language of the
Internet Protocols; it assumes a lower level transport layer protocol. While
this can swapped, in practice it is almost always TCP. The basics of the
protocol are:

* Web resources are identified with URLs (Uniform Resource Locators).
  Originally, **resources** were just files/directories on a server, but today
  resources refer to more general objects.
* HTTP "verbs" represent actions to take on the resource. The most common verbs
  are ``GET``, ``POST``, ``PUT``, and ``DELETE``.
* A **request** is made up of a URL, an HTTP verb, and a message
* A **response** consists of a status code (numerical between 100-599) and a
  message. The first digit of the status code specifies the kind of response:

    * 1xx - informational
    * 2xx - success
    * 3xx - redirection
    * 4xx - error in the request (client)
    * 5xx - error fulfilling a valid request (server)


REST APIs - Overview
--------------------

REST (Representational State Transfer) is a way of building APIs for computer
programs on the internet leveraging HTTP. In other words, a program on computer
1 interacts with a program on computer 2 by making an HTTP request to it.

In HTTP terms, “resources” are the nouns of the application domain and are
associated with URLs. The API has a **base URL** from which all other URLs in
that API are formed, e.g.:

.. code-block:: console

   https://api.github.com/

The other URLS in the API are either "collections", e.g.:

.. code-block:: console

   <base_url>/users
   <base_url>/files
   <base_url>/programs

or they are specific items in a collection, e.g.:

.. code-block:: console

   <base_url>/users/12345
   <base_url>/files/test.txt
   <base_url>/programs/myapplication

or subcollections / items in subcollections, e.g.:

.. code-block:: console

   <base_url>/companies/<company_id>/employees
   <base_url>/companies/<company_id>/employees/<employee_id>


Continuing along with HTTP terms, “operations” are the actions that can be taken
on the resources and are associated with HTTP verbs:

* ``GET`` - list items in a collection or retrieve a specific item in the
  collection
* ``POST`` - create a new item in the collection based on the description in the
  message
* ``PUT`` - replace an item in a collection with the description in the message
* ``DELETE`` - delete an item in a collection

Response messages often make use of some data serialization format standard such
as ``JSON`` or ``XML``.

.. note::

   The base URL to the GitHub API is listed above, https://api.github.com/. You
   can discover the API to GitHub and other popular websites by searching in
   Google something like "GitHub API endpoint".


REST APIs - Toy Examples
------------------------

Virtually every application domain can be mapped into a REST API architecture.
Some examples may include:

Articles in a collection (e.g., on a blog or wiki) with author attributes:

.. code-block:: console

   <base_url>/articles
   <base_url>/articles/<id>
   <base_url>/articles/<id>/authors


Properties in a real estate database with associated purchase history:

.. code-block:: console

   <base_url>/properties
   <base_url>/properties/<id>
   <base_url>/properties/<id>/purchases


A catalog of countries, cities and neighborhoods:

.. code-block:: console

   <base_url>/countries
   <base_url>/countries/<country_id>/cities
   <base_url>/countries/<country_id>/cities/<city_id>/neighborhoods



REST APIs - A Real Example
--------------------------

Bitbucket is a website for managing git repositories. You may already be
familiar with the Bitbucket website, https://bitbucket.org/. Let's now take a
look at the Bitbucket Web API. Open a web browser and navigate to:

* https://api.bitbucket.org/2.0/repositories

When you opened that page, your browser made a ``GET`` request to the Bitbucket
API. What you see is a ``JSON`` object describing public repositories.

.. figure:: images/bitbucket_api.png
    :width: 600px
    :align: center

    The first entries returned from the Bitbucket API.

If you look closely, you will see three top level objects in the response:
``pagelen`` (int), ``values`` (list), and ``next`` (str). What do you think each
represents?

EXERCISE
~~~~~~~~

* Were all Bitbucket repositories returned? How many were returned? What URL
  would you use to get the next set of repositories?
* What URL would we use to get a list of public repositories owned by a specific
  user?
* What URL would we use to get a list of commits for a specific public
  repository?

.. tip::

   Web APIs for popular sites (like Bitbucket) often come with
   `online documentation <https://developer.atlassian.com/bitbucket/api/2/reference/>`_.


Using Python to Interact with Web APIs
--------------------------------------

Viewing API response messages in a web browsers is of limited use. We can
interact with Web APIs in a much more powerful and programmatic way using the
Python ``requests`` library.

First install the ``requests`` library in your userspace on the ISP server using
pip:

.. code-block:: console

   [isp02]$ pip3 install --user requests
   ...
   Successfully installed requests-2.25.1

You might test that the install was successful by trying to import the library
in the interactive Python interpreter:

.. code-block:: console

   [isp02]$ python3
   Python 3.6.8 (default, Aug  7 2019, 17:28:10)
   [GCC 4.8.5 20150623 (Red Hat 4.8.5-39)] on linux
   Type "help", "copyright", "credits" or "license" for more information.
   >>> import requests
   >>>

The basic usage of the ``requests`` library is as follows:

.. code-block:: python3

   >>> # make a request
   >>> response = requests.<method>(url=some_url, data=some_message, <other options>)
   >>>
   >>> # e.g. try:
   >>> response = requests.get(url='https://api.bitbucket.org/2.0/repositories')
   >>>
   >>> # return the status code:
   >>> response.status_code
   >>>
   >>> # return the raw content
   >>> response.content
   >>>
   >>> # return a Python list or dictionary from the response message
   >>> response.json()


EXERCISE
~~~~~~~~

Let's explore the Bitbucket API using the ``requests`` library in a Python
script. Write functions to return the following:

* Retrieve a list of public bitbucket repositories
* Retrieve a list of public bitbucket repositories for a particular user
* Retrieve a list of pull requests for a particular public bitbucket repository


Additional Resources
--------------------

* `Bitbucket API <https://api.bitbucket.org/2.0/repositories/>`_
* `Bitbucket API Documentation <https://developer.atlassian.com/bitbucket/api/2/reference/>`_
* `Python requests Documentatino <https://requests.readthedocs.io/en/master/>`_
