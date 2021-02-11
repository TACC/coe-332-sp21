Docker Compose
==============

Up to this point, we have been looking at single-container applications - small
units of code that are containerized, executed *ad hoc* to generate or read a
JSON file, then exit on completion. But what if we want to do something more
complex? For example, what if our goal is to orchestrate a multi-container
application consisting of, e.g., a Flask app, a database, a message queue, an
authentication service, and more.

**Docker compose** is tool for managing multi-container applications. A YAML
file is used to define all of the application service, and a few simple commands
can be used to spin up or tear down all of the services.

In this module, we will get a first look at Docker compose. Later in this course
we will do a deeper dive into advanced container orchestration. After going
through this module, students should be able to:

* Translate Docker run commands into YAML files for Docker compose
* Run commands inside *ad hoc* containers using Docker compose



A Simple Example
----------------

Docker compose works by interpreting rules declared in a YAML file (typically
called ``docker-compose.yml``). The rules we will write will replace the
``docker run`` commands we have been using, and which have been growing quite
complex. For example, the commands we used to run our JSON parsing scripts in a
container looked like the following:

.. code-block:: console

   [isp02]$ docker run --rm -v $PWD:/data -u $(id -u):$(id -g) username/json-parser:1.0 generate_animals.py /data/animals.json
   [isp02]$ docker run --rm -v $PWD:/data -u $(id -u):$(id -g) username/json-parser:1.0 read_animals.py /data/animals.json

The above ``docker run`` commands can be loosely translated into a YAML file.
Navigate to the folder that contains your Python scripts and Dockerfile, then
create a new empty file called ``docker-compose.yml``:

.. code-block:: console

   [isp02]$ pwd
   /home/wallen/coe-332/docker-exercise
   [isp02]$ touch docker-compose.yml
   [isp02]$ ls -l
   total 12
   -rw-------. 1 wallen G-815499   0 Feb 10 20:46 docker-compose.yml
   -rw-------. 1 wallen G-815499 329 Feb  9 12:39 Dockerfile
   -rw-------. 1 wallen G-815499 703 Feb  9 11:16 generate_animals.py
   -rw-------. 1 wallen G-815499 236 Feb  9 11:16 read_animals.py
   drwx------. 2 wallen G-815499   6 Feb 10 20:44 test/


Next, open up ``docker-compose.yml`` with your favorite text editor and type /
paste in the following text:

.. code-block:: yaml

   ---
   version: "3"

   services:
       gen-anim:
           image: wallen/json-parser:1.0
           volumes:
               - ./test:/data
           user: "827385:815499"
           command: generate_animals.py /data/animals.json
       read-anim:
           image: wallen/json-parser:1.0
           volumes:
               - ./test:/data
           user: "827385:815499"
           command: read_animals.py /data/animals.json
   ...

The ``version`` key must be included and simply denotes that we are using
version 3 of Docker compose.

The ``services`` section defines the configuration of individual container
instances that we want to orchestrate. In our case, we define two called
``gen-anim`` for the generate_animals functionality, and ``read-anim`` for
the read_animals functionality.

Each of those services is configured with a Docker image (``wallen/json-parser:1.0``),
a mounted volume (equivalent to the ``-v`` option for ``docker run``), a user
namespace (equivalent to the ``-u`` option for ``docker run``), and a default
command to run.

Please note that the image name above should be changed to use your image. Also,
the user ID / group ID are specific to ``wallen`` - to find your user and group
ID, execute the Linux commands ``id -u`` and ``id -g``.

.. note::

   The top-level ``services`` keyword shown above is just one important part of
   Docker compose. Later in this course we will look at named volumes and
   networks which can be configured and created with Docker compose.

Running Docker Compose
----------------------

The Docker compose command line too follows the same syntax as other Docker
commands:

.. code-block:: console

   docker-compose <verb> <parameters>

Just like Docker, you can pass the ``--help`` flag to ``docker-compose`` or to
any of the verbs to get additional usage information. To get started on the
command line tools, try issuing the following two commands:

.. code-block:: console

   [isp02]$ docker-compose version
   [isp02]$ docker-compose config

The first command prints the version of Docker compose installed, and the second
searches your current directory for ``docker-compose.yml`` and checks that it
contains only valid syntax.

To run one of these services, use the ``docker-compose run`` verb, and pass the
name of the service as defined in your YAML file:

.. code-block:: console

   [isp02]$ ls test/     # currently empty
   [isp02]$ docker-compose run gen-anim
   [isp02]$ ls test/
   animals.json          # new file!
   [isp02]$ docker-compose run read-anim
   {'head': 'snake', 'body': 'marlin-tapir', 'arms': 10, 'legs': 9, 'tail': 19}


Now we have an easy way to run our *ad hoc* services consistently and
reproducibly. Not only does ``docker-compose.yml`` make it easier to run our
services, it also represents a record of how we intend to interact with this
container.



Essential Docker Compose Command Summary
----------------------------------------

+------------------------+------------------------------------------------+
| Command                | Usage                                          |
+========================+================================================+
| docker-compose version | Print version information                      |
+------------------------+------------------------------------------------+
| docker-compose config  | Validate docker-compose.yml syntax             |
+------------------------+------------------------------------------------+
| docker-compose up      | Spin up all services                           |
+------------------------+------------------------------------------------+
| docker-compose down    | Tear down all services                         |
+------------------------+------------------------------------------------+
| docker-compose build   | Build the images listed in the YAML file       |
+------------------------+------------------------------------------------+
| docker-compose run     | Run a container as defined in the YAML file    |
+------------------------+------------------------------------------------+


Additional Resources
--------------------

* `Docker Compose Docs <https://docs.docker.com/compose/>`_
