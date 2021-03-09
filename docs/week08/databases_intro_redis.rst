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

::
   $ redis-server

- sanity check:

::
   $ redis-cli ping

- working with redis in Python

::
   $ pip3 --user install redis

-lets do interactive python

::
   $ python3

first steps:
   >>> import redis
create a client connection to the Redis server and specify a database using the StrictRedis class:
   >>> rd = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)

- Some quick notes
   - We are using the IP of the gateway (127.0.0.1) on our localhost and the standard Redis port 6379).
   - Redis organizes collections into "databases" identified by an integer index. Here, we are specifying db=0; if that database does not exist it will be created for us.


Working with Redis
==================

The .set() and .get() Methods

   - We can create and/or update a key-value string pair using rd.set(key, value).
   - For example:
      - >>> rd.set('my_key', 'my_value')
      - Out[1]: True

This saved a key in the Redis server (db=0) with key my_key and value my_value. Note the method returned True, indicating that the request was successful.

