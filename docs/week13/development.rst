Development Environment
=======================

Development of this API will be performed on the ISP server. The containers and
endpoints developed here will be ephemeral, only lasting long enough to test and
debug new features. They should never be seen by end users. There will be three
containerized components:

1. A Flask API front end for submitting / accessing jobs
2. A Redis database for storing job and queue information
3. A worker back end which runs the PSSP code


File Organization
-----------------

An example file organization scheme for developing this API may look like:

.. code-block:: text

    pssp-api/
    ├── data
    │   ├── dump.rdb
    │   └── redis.conf
    ├── docker
    │   ├── docker-compose.yml
    │   ├── Dockerfile.api
    │   ├── Dockerfile.db
    │   └── Dockerfile.wrk
    ├── README.md
    └── src
        ├── flask_api.py
        └── worker.py

In this example, the `data/` subfolder is mounted inside the Redis container. The
`redis.conf` configuration file is useful to have to customize how the database
behaves, and all the data is captured in regular intervals as `dump.rdb` for easy
backups.

The `docker/` subfolder contains a Dockerfile for each service, plus a `docker-compose.yml`
for orchestrating all services at once.

The `src/` folder contains the source Python scripts that are injected into the
API and worker containers. This is where the majority of the development will
occur.

.. tip::

   It is a very, very good idea to put this whole folder under version control.



Docker
------

We previously talked at great length about why it is a good idea to containerize
an app / service that you develop. One of the main reasons was for portability
to other machines. All the development / testing done in this development environment
will directly translate to our deployment environment (Kubernetes), as we will see
in the next module.

The development cycle for each of the three containerized components generally
follows the form:

1. Edit some source code (e.g. add a new Flask route)
2. Delete any running container with the old source code
3. Re-build the image with ``docker build``
4. Start up a new container with ``docker run``
5. Test the new code / functionality
6. Repeat

This 6-step cycle is great for iterating on each of the three containers
independently, or all at once. However, watch out for potential error sources.
For example if you take down the Redis container, a worker container that is in
the middle of watching the queue may also go down and will need to be restarted
(once a new Redis container is up).


Makefile
--------

Makefiles can be a useful automation tool for testing your services.
Many code projects use Makefiles to help with the compile and install process
(e.g. ``make && make install``). Here, we will set up a Makefile to help with the
6-step cycle above. Using certain keywords (called "targets") we will create
shortcuts to cleaning up running containers, re-building docker images, running
new containers, and deploying it all with docker-compose.

Targets are listed in a file called ``Makefile`` in this format:

.. code-block:: text

   target: prerequisite(s)
           recipe

Targets are short keywords, and recipes are shell commands. For example, a
simple target might look like:

.. code-block:: text

   ps-me:
           docker ps -a | grep wallen

With this text in a file called ``Makefile``, you simply need to type:

.. code-block:: console

    [isp02]$ make ps-me

And that will list all the docker containers with the username 'wallen' either
in the image name or the container name. Makefiles can be further abstracted with
variables to make them a little bit more flexible. Consider the following Makefile:

.. code-block:: text

   NAME ?= wallen

   all: ps-me im-me

   im-me:
           docker images | grep ${NAME}

   ps-me:
           docker ps -a | grep ${NAME}

Here we have added a variable ``NAME`` at the top so we can easily customize the
targets below. We have also added two new targets: ``im-me`` which lists images,
and ``all`` which does not contain any recipes, but does contain two prerequisites -
the other two targets. So these two are equivalent:

.. code-block:: console

   # make all targets
   [isp02]$ make all

   # or make them one-by-one
   [isp02]$ make ps-me
   [isp02]$ make im-me

   # Try this out:
   [isp02]$ NAME="redis" make all


EXERCISE
~~~~~~~~

Write a Makefile that, at a minimum:

1. Builds all necessary images for your app from Dockerfile(s)
2. Starts up new containers / services
3. Removes running containers in your namespace (be careful!)


Docker-Compose
--------------

Although it is not strictly necessary, it might also be useful to write Makefile
targets to run a ``docker-compose`` deployment of all of your services as a unit.
This behavior more closely mimics what it will be like to put services up in your
Kubernetes deployment environment. Be careful, however, about the order in which
docker-compose starts services. If the Redis DB service is not ready, your worker
service(s) may exit immediately with an error like 'Can not connect to database'.
