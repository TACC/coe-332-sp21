Databases
=========

We need a better way to connect our data and a future platform to communicate
with our other services

Where are we? What's our motivation?
------------------------------------

This week we need to extend our Flask APP - which we will now refer to as our Flask API
to enable users to query and analyze our data sets

- Our basic approach to this will be:

   - our dataset will have to be saved in our database
   - the user submits a request to an endpoint which describes some sort of analysis they wish to perform
   - we'll create a function to perform the analysis and retrieve the desired data
   - Also, I want you to think about this: 
      - since the analysis may take "awhile" to execute, we need to figure out how to run the job in the background and let the user know when the job has finished
      - and we need to tackle multiple jobs at the same time




Why User a Database?
--------------------
- What is a Database?

   - A database is an organized collection of structured information, or data, typically stored electronically in a computer system

- So why use one?

   - our data needs permanence, we want to be able to start and stop our program without losing data.
   - we want multiple Python processes to be able to access the data at the same time.

- Why not use a file?

   - It is not easy to make a file accessible to Python processes on different computers/VMs.
   - When multiple processes are reading from and writing to a file, race conditions can occur.
   - With files, our *application* will have to implement all the structure in the data.

- NoSQL Databases - yes this implies a "Yes"SQL - or just SQL - Databases

   - NoSQL Databases do not use tables - that is data structured using rows and columns - connected through relations
   - Store data in "collections" or "logical databases".
   - Store objects in the collection instead of rows/records.
   - Can allow for missing or different attributes on objects in the same collection.
   - Objects in one collection do not relate or link to objects in another collection.
   - the objects themselves could be JSON objects without a pre-defined schema.

- SQL vs NoSQL

   - Both SQL and NoSQL databases have advantages and disadvantages
   - the *primary* deciding factor should be the *shape* of the data
   - also consider how the data may change over time
   - and how important is the relationship between the data tables
   - SQL "enforce" relationships between types data, including one-to-one, one-to-many, and many-to-many
      - this enforcement feature is important for some types of data, this hospitals or banks
   - NoSQL, the relationship enforcement must be programmed into the application
      - think Twitter
   - SQL databases have challenges scaling to "large" quantities of data because of the ACID (Atomicity, Consistency, Isolation, Durability) guarantees they make.
   - NoSQL databases trade ACID guarantees for "eventual consistency" and greater scalability. A relational database would almost certainly not scale to the "all tweets" example.

   - For us, NoSQL is the way to go
      - we need a flexible data module
      - NoSQL databases are quick to get started
         - we can get up and running with only the basics of a persisitent store without defining tables, schemas, relations, etc...
         - Multiple uses... not only are we going to store our dataset, we also need "something" to manage communication between our services



Enter Redis
===========

Redis is a very popular NoSQL database and "data structure store" with lots of advanced features.

- Key-Value Store

   - The items stored in Redis are structured as Key:Value objects
   - The primary requirement is that the *key* be unique across the database
   - a single Redis server can support multiple databases, indexed by an integer
   - the data itself can be stored as JSON

- notes about keys

   - keys are often strings, but they can be any "binary sequence"
   - long keys can lead to performance issues.
   - a format such as <object_type>:<object_id> is a good practice

- notes on values

   - Values are typed; some of the primary types include:
      - Binary-safe strings
      - Lists: sorted collections of strings
      - Sets: unsorted, unique collections of strings
      - Hashes: maps of fields with associated values; both field and value are type string.
   - There is no native "JSON" type; to store JSON, one can use an encoding and store the data as a binary-safe string, or one can use a hash and convert the object into and out of JSON.
   - the basic string type is a "binary-safe" string; this means it must include an encoding.
      - In Python terms, the string is stored and returned as type "bytes".
      - By default, the string will be encoded with UTF-8, but we can specify the encoding when storing the string.
      - Since bytes are returned, it will be our responsibility to decode using the same encoding.

- Hash maps
   - Hashes provide another way of storing dictionary-like data in Redis.
   - The values of the keys are string types.

Running Redis
=============

- ssh into our class VMs
- Redis is already installed, the following command starts the server up:

.. code-block:: console

   $ redis-server

- sanity check:

.. code-block:: console

   $ redis-cli ping

- working with redis in Python

.. code-block:: console

   $ pip3 --user install redis

-lets do interactive python

.. code-block:: console

   $ python3

first steps:

.. code-block:: console

   >>> import redis

create a client connection to the Redis server and specify a database using the StrictRedis class:

.. code-block:: console

   >>> rd = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)

- Some quick notes
   - We are using the IP of the gateway (127.0.0.1) on our localhost and the standard Redis port 6379).
   - Redis organizes collections into "databases" identified by an integer index. Here, we are specifying db=0; if that database does not exist it will be created for us.


Working with Redis
==================

The .set() and .get() Methods

   - We can create and/or update a key-value string pair using rd.set(key, value).
   - For example:

.. code-block:: console

   >>> rd.set('my_key', 'my_value')
   Out[1]: True

This saved a key in the Redis server (db=0) with key my_key and value my_value. Note the method returned True, indicating that the request was successful.

   - We can retrieve it with:

.. code-block:: console
   >>> rd.get('my_key')
   Out[2]: b'my_value'

Note: 
Note that b'my_value' was returned; in particular, Redis returned binary data (i.e., type bytes).
the string was encoded for us (in this case, using Unicode). We could have been explicit and set the encoding ourselves.

################
Quick Exercise 1
################

With the knowledge we know now, write a python program that:

   - loop that creates 10 random numbers and a random "heads"
   - store the random number as a *key* and the random head as the "value"


JSON and Redis
==============

Storing and Retrieving JSON
---------------------------

The binary-safe string data type used in Redis means a bit more "care" is needed for storing pure JSON. Check out the following examples:

.. code-block:: console

   >>> import json
   >>> d = {'a': 1, 'b': 2}
   >>> rd.set('k1', json.dumps(d))
   >>> json.loads(rd.get('k1'))

To get this to work - in some versions of Python - we may need to specify the encoding:

.. code-block:: console

   >>> json.loads(rd.get('k1').decode('utf-8'))
   Out[1]: {'a': 1, 'b': 2}


**Hashes**

Hashes provide another way of storing dictionary-like data in Redis.

- Hashes are useful when different fields are encoded in different ways; for example, a mix of binary and unicode data.
- Each field in a hash can be treated with a separate decoding scheme, or not decoded at all.
- Use *hset* to set a single field value in a hash; use *hmset* to set multiple fields at once.
- Similarly, use *hget* to get a single field within a hash, use *hmget* to get multiple fields, or use hgetall to get all of the fields.

.. code-block:: console

   >>> rd.hmset('k2', {'name': 'Charlie', 'email': 'charlie@tacc.utexas.edu'})
   >>> rd.hgetall('k2')
   Out[1]: {b'name': b'Charlie', b'email': b'charlie@tacc.utexas.edu'}
   >>> rd.hset('k2', 'name', 'Charlie Dey')
   >>> rd.hgetall('k2')
   Out[2]: {b'name': b'Charlie Dey', b'email': b'charlie@tacc.utexas.edu'}
   >>> rd.hget('k2', 'name')
   Out[3]: b'Charlie Dey'
   >>> rd.hmget('k2', 'name', 'email')
   Out[4]: [b'Charlie Dey', b'charlie@tacc.utexas.edu']


################
Quick Exercise 2
################

Modify your animal producer - your app that creates your animals - to write out 5 animals to the redis database, use a random number as the key and a hash as your value

################
Quick Exercise 3
################

Create another animal consumer  - your app that reads in the animals - to read in 5 random animals from the datbase using a random key

################
Quick Exercise 4
################

Modify your animal consumer to read in all the animals with a specific type of head

Questions
---------

   What happens when a key is not found?
   How can we adjust our code for this?


Containerizing Redis
====================

Using Docker, starting and running a Redis server can be accomplished in two easy steps. Assuming docker is running:

Pull the official Redis image for version 5.0.0:

.. code-block:: console
   
   $ docker pull redis:5.0.0

Start the redis server in a container:

.. code-block:: console

   $ docker run -p <your redis port>:6379 redis:5.0.0


Note: the above command will start the Redis container in the foreground which can be helpful for seeing logs, etc. However, you will have the need to start it in the background (detached or daemon mode)

################
Quick Exercise 5
################

Revisit Exercises 2, 3, and 4. Modify them to hit your Redis container instead

################
Quick Exercise 6
################

Kill your Redis container and restart it. Is your data still there?


Have a fun and safe Spring Break... see you all in a couple weeks.

