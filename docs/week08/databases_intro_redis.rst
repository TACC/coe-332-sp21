Intro to Databases and Persistence
==================================

Application data that lives inside a container is ephemeral - it only persists
for the lifetime of the container. We can use databases to extend the life of
our application (or user) data, and even access it from outside the container.

After going through this module, students should be able to:

* Explain the differences between SQL and NoSQL databases
* Choose the appropriate type of database for a given application / data set
* Start and find the correct port for a Redis server
* Install and import the Redis Python library
* Add data to and retrieve data from a Redis database from a Python script

What's Our Motivation?
----------------------

This week we work to extend our Flask App - which we will now refer to as our
Flask API - to enable users to query and analyze our data sets.

Our basic approach to this will be:

1. Our dataset will be stored in our database
2. The user submits a request to a Flask endpoint which describes some sort of
   analysis they wish to perform
3. We will create functions to perform the analysis and retrieve the desired
   data from the database

.. tip::

   For future lectures, think about the following: The analysis may take "a while"
   to execute, so we need to figure out how to (1) run the job in the background,
   (2) let the user know when the job has finished, and possibly (3) receive and
   handle multiple jobs at the same time. More on this coming soon!




Quick Intro to Databases
------------------------

**What is a database?**

* A database is an organized collection of structured information, or data,
  typically stored electronically in a computer system


**So why use one?**

* Our data needs permanence and we want to be able to stop and start our Flask
  API without losing data
* We want multiple Python processes to be able to access the data at the same
  time

**Why not use a file?**

* It is not easy to make a file accessible to Python processes on different
  computers / VMs
* When multiple processes are reading from and writing to a file, race conditions
  can occur
* With files, our Flask API would have to implement all the structure in the data


**NoSQL databases**

* Yes, this implies a "Yes"SQL - or just SQL - database
* NoSQL databases do **NOT** use tables (data structured using rows and columns)
  connected through relations
* NoSQL databases store data in "collections" or "logical databases"
* Can allow for missing or different attributes on objects in the same collection
* Objects in one collection do not relate or link to objects in another
  collection
* The objects themselves could be JSON objects without a pre-defined schema

**SQL vs NoSQL**

* Both SQL and NoSQL databases have advantages and disadvantages
* The *primary* deciding factor should be the *shape* of the data
* Also consider how the data may change over time, and how important is the
  relationship between the data tables
* SQL "enforce" relationships between data types, including one-to-one, one-to-many,
  and many-to-many (important for some types of data; think hospitals or banks)
* In NoSQL, the relationship enforcement must be programmed into the application
  (think Twitter)
* SQL databases have challenges scaling to "large" quantities of data because of
  the ACID (Atomicity, Consistency, Isolation, Durability) guarantees they make
* NoSQL databases trade ACID guarantees for "eventual consistency" and greater
  scalability (i.e., a relational database would almost certainly not scale to
  "all tweets")

For the projects in this class, NoSQL is the way to go. We need a flexible data
model as our 'animals' data structure keeps changing, we need something that is
quick to get started, we need something that will allow our data to persist, and
we need something to manage communication between our services.



Enter Redis
-----------

Redis is a very popular NoSQL database and "data structure store" with lots of
advanced features including:

**Key-value store**

* The items stored in a Redis database are structured as ``key:value`` objects
* The primary requirement is that the ``key`` be unique across the database
* A single Redis server can support multiple databases, indexed by an integer
* The data itself can be stored as JSON

**Notes about keys**

* Keys are often strings, but they can be any "binary sequence"
* Long keys can lead to performance issues
* A format such as ``<object_type>:<object_id>`` is a good practice


**Notes on values**

* Values are typed; some of the primary types include:

  - Binary-safe strings
  - Lists (sorted collections of strings)
  - Sets (unsorted, unique collections of strings)
  - Hashes (maps of fields with associated values; both field and value are type ``string``)

* There is no native "JSON" type; to store JSON, one can use an encoding and store
  the data as a binary-safe string, or one can use a hash and convert the object
  into and out of JSON
* The basic string type is a "binary-safe" string, meaning it must include an
  encoding

  - In Python terms, the string is stored and returned as type ``bytes``
  - By default, the string will be encoded with UTF-8, but we can specify the
    encoding when storing the string
  - Since bytes are returned, it will be our responsibility to decode using the
    same encoding


**Hash maps**

* Hashes provide another way of storing dictionary-like data in Redis
* The values of the keys are type ``string``



Running Redis
-------------

To use Redis on the class VM (ISP), we must have an instance of the Redis server
running. For demonstration purposes, we will all share the same instance of
Redis server on the same port (6379).


.. code-block:: console

   # start the Redis server on the command line:
   [isp02]$ redis-server
   3823:C 31 Mar 10:20:51.194 # Warning: no config file specified, using the default config. In order to specify a config file use redis-server /path/to/redis.conf
   3823:M 31 Mar 10:20:51.198 # You requested maxclients of 10000 requiring at least 10032 max file descriptors.
   3823:M 31 Mar 10:20:51.198 # Server can't set maximum open files to 10032 because of OS error: Operation not permitted.
   3823:M 31 Mar 10:20:51.198 # Current maximum open files is 4096. maxclients has been reduced to 4064 to compensate for low ulimit. If you need higher maxclients increase 'ulimit -n'.
   3823:M 31 Mar 10:20:51.202 # Creating Server TCP listening socket *:6379: bind: Address already in use

   # already started! (remember, we are all logged in to the same VM)

   # Ping the server to make sure it is up
   [isp02]$ redis-cli ping
   PONG

The Redis server is up and available. Although we could use the Redis CLI to
interact with the server directly, in this class we will focus on the Redis
Python library so we can interact with the server from our Python scripts.

.. note::

   According to the log above, Redis is listening on the default port, **6379**.


First install the Redis Python library in your user account:

.. code-block:: console

   [isp02]$ pip3 install --user redis


Then open up an interactive Python interpreter to connect to the server:

.. code-block:: console

   [isp02]$ python3
   Python 3.6.8 (default, Aug  7 2019, 17:28:10)
   [GCC 4.8.5 20150623 (Red Hat 4.8.5-39)] on linux
   Type "help", "copyright", "credits" or "license" for more information.

.. code-block:: python3

   >>> import redis
   >>>
   >>> rd=redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
   >>>
   >>> type(rd)
   <class 'redis.client.Redis'>

You've just created a client connection to the Redis server called ``rd``. This
class contains methods for adding, modifying, deleting, and analyzing data in
the database instance, among other things.

Some quick notes:

* We are using the IP of the gateway (``127.0.0.1``) on our localhost and the
  default Redis port (``6379``).
* Redis organizes collections into "databases" identified by an integer index.
  Here, we are specifying ``db=0``; if that database does not exist it will be
  created for us.


Working with Redis
------------------

We can create new entries in the dabase using the ``.set()`` method. Remember,
entries in a Redis database take the form of a key:value pair. For example:

.. code-block:: python3

   >>> rd.set('my_key', 'my_value')
   True

This operation saved a key in the Redis server (``db=0``) called ``my_key`` and
with value ``my_value``. Note the method returned True, indicating that the
request was successful.

We can retrieve it using the ``.get()`` method:

.. code-block:: python3

   >>> rd.get('my_key')
   b'my_value'

Note that ``b'my_value'`` was returned; in particular, Redis returned binary
data (i.e., type ``bytes``). The string was encoded for us (in this case, using
Unicode). We could have been explicit and set the encoding ourselves. The
``bytes`` class has a ``.decode()`` method that can convert this back to a
normal string, e.g.:


.. code-block:: python3

   >>> rd.get('my_key')
   b'my_value'
   >>> type(rd.get('my_key'))
   <class 'bytes'>
   >>>
   >>> rd.get('my_key').decode('utf-8')
   'my_value'
   >>> type( rd.get('my_key').decode('utf-8') )
   <class 'str'>


Exercise 1
~~~~~~~~~~

With this knowledge, write a Python program that:

* Uses a loop to create 10 random numbers and chooses a random heads
* Store the random number as a ``key`` and the random head as the ``value``



Redis and JSON
--------------

A lot of the information we exchange comes in JSON or Python dictionary format.
To store pure JSON as a binary-safe string ``value`` in a Redis database, we
need to be sure to dump it as a string (``json.dumps()``):

.. code-block:: python3

   >>> import json
   >>> d = {'a': 1, 'b': 2, 'c': 3}
   >>> rd.set('k1', json.dumps(d))
   True


Retrieve the data again and get it back into JSON / Python dictionary format
using the ``json.loads()`` method:

.. code-block:: python3

   >>> rd.get('k1')
   b'{"a": 1, "b": 2, "c": 3}'
   >>> type(rd.get('k1'))
   <class 'bytes'>
   >>>
   >>> json.loads(rd.get('k1'))
   {'a': 1, 'b': 2, 'c': 3}
   >>> type(json.loads(rd.get('k1')))
   <class 'dict'>

.. note::

   In some versions of Python, you may need to specify the encoding as we did
   earlier, e.g.:

   .. code-block:: python3

      >>> json.loads(rd.get('k1').decode('utf-8'))
      {'a': 1, 'b': 2, 'c': 3}




Hashes
~~~~~~

Hashes provide another way of storing dictionary-like data in Redis.

* Hashes are useful when different fields are encoded in different ways; for
  example, a mix of binary and unicode data.
* Each field in a hash can be treated with a separate decoding scheme, or not
  decoded at all.
* Use ``hset()`` to set a single field value in a hash; use ``hmset()`` to set
  multiple fields at once.
* Similarly, use ``hget()`` to get a single field within a hash, use ``hmget()``
  to get multiple fields, or use ``hgetall()`` to get all of the fields.

.. code-block:: python3

   >>> rd.hmset('k2', {'name': 'Charlie', 'email': 'charlie@tacc.utexas.edu'})
   >>> rd.hgetall('k2')
   {b'name': b'Charlie', b'email': b'charlie@tacc.utexas.edu'}

   >>> rd.hset('k2', 'name', 'Charlie Dey')
   >>> rd.hgetall('k2')
   {b'name': b'Charlie Dey', b'email': b'charlie@tacc.utexas.edu'}

   >>> rd.hget('k2', 'name')
   b'Charlie Dey'

   >>> rd.hmget('k2', 'name', 'email')
   [b'Charlie Dey', b'charlie@tacc.utexas.edu']


.. tip::

   You can use ``rd.keys()`` to return all keys from a database, and
   ``rd.hkeys(key)`` to return the list of keys within hash '``key``', e.g.:

   .. code-block:: python3

      >>> rd.hkeys('k2')
      [b'name', b'email']



Exercise 2
~~~~~~~~~~

Modify your animal producer - your app that creates your animals - to write out
five animals to the Redis database. Use a random number as the key and a hash as
your value.


Exercise 3
~~~~~~~~~~

Create another animal consumer - your app that reads in the animals - to read in
five random animals from the database using a random key.

Exercise 4
~~~~~~~~~~

Modify your animal consumer to read in all the animals with a specific type of
head.

.. warning::

   What happens when a key is not found? How can we adjust our code for this?

Additional Resources
--------------------

* `Redis Docs <https://redis.io/documentation>`_
* `Redis Python Library <https://redis-py.readthedocs.io/en/stable/>`_
