Docker Compose, Revisted
========================

Let's do a bit of rehash, docker-compose is a tool for defining and running multi-container Docker applications. With Compose, 
you use a YAML file to configure your application's services. Then, with a single command, you 
create and start all the services from your configuration.

Here, we will walk through the process of containerizing Flask and Redis, fire them up with docker-compose, and then have
our two services talk to each other.

When working with multiple containers, it can be difficult to manage the starting along with the configuration 
of variables and links.


Compose is a tool for defining and running multi-container Docker applications.


With Compose, you use a YAML file to configure your application’s services.


Then, with a single command, you create and start all the services from your configuration.

Why Docker-Compose?
-------------------

*  Orchestration!


*  Launch multiple containers with complex configurations at once


*  Define the structure of your app, not the commands needed to run it!

Using Compose
-------------

Using Compose is a three-step process:

*  Define images with Dockerfiles
*  Define the services in a docker-compose.yml as containers with all of your options (image, port mapping, links, etc.)
*  Run docker-compose up and Compose starts and runs your entire app.

Three step process to use … a bit more to actually build.

Docker Compose revolves around the docker-compose.yml file where all of your services and components of your system are defined

Let's start with Redis
----------------------

First, let's create our redis-docker and a config directory under that.

.. code-block:: console

   [isp02]$ mkdir redis-docker
   [isp02]$ mkdir redis-docker/config


Next, you'll need a redis config file, luckily we have one for you.

`redis.conf <https://github.com/TACC/coe-332-sp21/blob/main/docs/week09/redis.conf>`_

Copy this file into your redis-docker/config directory


The Docker-Compose File
-----------------------

Go to your Redis Docker directory
create a file called docker-compose.yml


.. code-block:: python3

    version: '3'
    services:
        redis:
            image: redis:latest
            ports:
                - <your port goes here>:6379
            volumes:
                - ./config/redis.conf:/redis.conf
            command: [ "redis-server", "/redis.conf" ]


Bring it Up
-----------

Bring up our system

.. code-block:: console

   docker-compose up -d


.. note::
   -d, puts it in daemon mode

Check to see if our systems are up

.. code-block:: console

   docker-compose ps


Boom! We have Redis running

* but Charlie!

* "docker-compose is about defining and running multi-container Docker applications"


Let's Add Another Service!
--------------------------

.. code-block::

    version: '3'
    services:
         web:
            build: .
            container_name: master_web
            ports:
               - 5001:5000
            volumes:
               - ./data/data_file.json:/datafile.json
        redis:
            image: redis:latest
            ports:
               - 6080:6379
            volumes:
               - ./config/redis.conf:/redis.conf
            command: [ "redis-server", "/redis.conf" ]


5001 is my port, how I access the service outside of the container.
5000 is the port *inside* the container

6080 is my redis port, how I access the service outside of the container.
6379 is the port *inside* the container


what does my Python Redis connection look like?
-----------------------------------------------

rd = redis.StrictRedis(host='redis', port=6379, db=7)
