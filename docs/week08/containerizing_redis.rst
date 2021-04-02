Containerizing Redis
====================

Up to this point, we have been interacting with a shared Redis database instance
directly on the class ISP server. Next, we will each containerize an instance of
Redis, figure out how to interact with it by forwarding the port, and connect it
to our Flask app.

After going through this module, students should be able to:

* Start a Redis container, connecting the appropriate inside port to a port on ISP
* Connect to the container from within a Python script
* Mount a volume inside the container for data persistence


Start a Redis Container
-----------------------

Docker Hub has a wealth of official, public images. It is a good idea to pull
the existing Redis image rather than build it ourself, because it has all of the
functionality we need as a base image.

Pull the official Redis image for version 5.0.0:

.. code-block:: console

   [isp02]$ docker pull redis:5.0.0
   5.0.0: Pulling from library/redis
   Digest: sha256:481678b4b5ea1cb4e8d38ed6677b2da9b9e057cf7e1b6c988ba96651c6f6eff3
   Status: Image is up to date for redis:5.0.0
   docker.io/library/redis:5.0.0

Start the Redis server in a container:

.. code-block:: console

   [isp02]$ docker run -p <your-redis-port>:6379 redis:5.0.0
   1:C 31 Mar 2021 16:48:11.939 # oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
   ...
   1:M 31 Mar 2021 16:48:11.972 * Ready to accept connections


The above command will start the Redis container in the foreground which can be
helpful for debugging, seeing logs, etc. However, you will have the need to
start it in the background (detached or daemon mode).

.. code-block:: console

   [isp02]$ docker run -d -p <your-redis-port>:6379 redis:5.0.0
   3a28cb265d5e09747c64a87f904f8184bd8105270b8a765e1e82f0fe0db82a9e


Connect to the Container from Python
------------------------------------

Only one small change is needed in our Python scripts to connect to this
containerized version of Redis. Since Docker is smart about port forwarding to
the localhost, you simply need to change the port you connect to when setting
up the Redis client.


.. code-block:: python3

   >>> import redis
   >>> rd=redis.StrictRedis(host='127.0.0.1', port=<your-redis-port>, db=0)



Exercise 1
~~~~~~~~~~

Revisit the Exercises from the `previous module <databases_intro_redis.html>`_
Modify them to hit your Redis container instead.

Exercise 2
~~~~~~~~~~

Kill your Redis container and restart it. Is your data still there?

.. tip::

   Use ``docker ps`` to find the container ID, then ``docker rm -f <containerID>``


Exercise 3
~~~~~~~~~~

Alright, so when we took down our Redis container, and then brought it back...
we lost our data? What can we do about this?

Mount a **volume** in your running container:

.. code-block:: console

   $ docker run -d -p <your port>:6379 -v <data-dir>:/data redis:5.0.0


Additional Resources
--------------------

* `Redis Image on Docker Hub <https://hub.docker.com/_/redis>`_
