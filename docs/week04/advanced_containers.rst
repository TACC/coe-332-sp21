Advanced Containers
===================

*Scenario:* You are a developer who has written some new code for reading and
parsing objects in JSON format. You now want to distribute that code for others
to use in what you know to be a stable production environment (including OS and
dependency versions). End users may want to use this application on their local
workstations, in the cloud, or on an HPC cluster.

In this section, we will build a Docker image from scratch for running our
Python code to parse JSON files. After going through this module, students
should be able to:

* Install and test code in a container interactively
* Write a Dockerfile from scratch
* Build a Docker image from a Dockerfile
* Push a Docker image to Docker Hub


Getting Set Up
--------------

The first step in a typical container development workflow entails installing
and testing an application interactively within a running Docker container.

.. note::

   We recommend doing this on the class ISP server. But, one of the most
   important features of Docker is that it is platform agnostic. These steps
   could be done anywhere Docker is installed.

To begin, make a folder for this section and gather the important files.
Specifically, you need two files from Homework01: ``generate_animals.py`` and
``read_animals.py``.

.. code-block:: console

   [isp02]$ cd ~/coe-332/
   [isp02]$ mkdir docker-exercise/
   [isp02]$ cd docker-exercise/
   [isp02]$ pwd
   /home/wallen/coe-332/docker-exercise

Now, we need an empty file called ``Dockerfile`` and a copy of your previous
homework files in here. Optionally, grab a copy of the homework files here:

.. code-block:: console

   [isp02]$ pwd
   /home/wallen/coe-332/docker-exercise
   [isp02]$ touch Dockerfile
   [isp02]$ wget https://raw.githubusercontent.com/tacc/coe-332-sp21/main/docs/week04/scripts/generate_animals.py
   [isp02]$ wget https://raw.githubusercontent.com/tacc/coe-332-sp21/main/docs/week04/scripts/read_animals.py
   [isp02]$ ls
   Dockerfile  generate_animals.py  read_animals.py

.. warning::

   It is important to carefully consider what files and folders are in the same
   ``PATH`` as a Dockerfile (known as the 'build context'). The ``docker build``
   process will index and send all files and folders in the same directory as
   the Dockerfile to the Docker daemon, so take care not to ``docker build`` at
   a root level.



Containerize Code Interactively
-------------------------------

There are several questions you must ask yourself when preparing to containerize
code for the first time:

1. What is an appropriate base image?
2. What dependencies are required for my program?
3. What is the install process for my program?
4. What environment variables may be important?

We can work through these questions by performing an **interactive installation**
of our Python scripts. Our development environment (the class ISP server) is a
Linux server running CentOS 7.7. We know our code works here, so that is how we
will containerize it. Use ``docker run`` to interactively attach to a fresh
`CentOS 7.7 container <https://hub.docker.com/_/centos?tab=tags&page=1&ordering=last_updated&name=7.7>`_.


.. code-block:: console

   [isp02]$ docker run --rm -it -v $PWD:/code centos:7.7.1908 /bin/bash
   [root@fbf511fa3447 /]#

Here is an explanation of the options:

.. code-block:: text

   docker run       # run a container
   --rm             # remove the container on exit
   -it              # interactively attach terminal to inside of container
   -v $PWD:/code    # mount the current directory to /code
   centos:7.7.1908  # image and tag from Docker Hub
   /bin/bash        # shell to start inside container


The command prompt will change, signaling you are now 'inside' the container.
And, new to this example, we are using the ``-v`` flag which mounts the contents
of our current directory (``$PWD``) inside the container in a folder in the root
directory called (``/code``).


Update and Upgrade
~~~~~~~~~~~~~~~~~~

The first thing we will typically do is use the CentOS package manager ``yum``
to update the list of available packages and install newer versions of the
packages we have. We can do this with:

.. code-block:: console

  [root@fbf511fa3447 /]# yum update
  ...

.. note::

  You will need to press 'y' followed by 'Enter' twice to download and install
  the updates




Install Required Packages
~~~~~~~~~~~~~~~~~~~~~~~~~

For our Python scripts to work, we need to install two dependencies: Python3 and
the 'petname' package.

.. code-block:: console

   [root@fbf511fa3447 /]# yum install python3
   ...
   [root@fbf511fa3447 /]# python3 --version
   Python 3.6.8
   [root@fbf511fa3447 /]# pip3 install petname==2.6
   ...
    UnicodeDecodeError: 'ascii' codec can't decode byte 0xe2 in position 32: ordinal not in range(128)
   ...
    Command "python setup.py egg_info" failed with error code 1 in /tmp/pip-build-8qhc6nih/petname/


Oh no! A ``UnicodeDecodeError`` happens sometimes on pip installs. We can fix
this by manually setting the character encoding with a couple environment
variables and trying again.

.. code-block:: console

   [root@fbf511fa3447 /]# export LC_CTYPE=en_US.UTF-8
   [root@fbf511fa3447 /]# export LANG=en_US.UTF-8
   [root@fbf511fa3447 /]# pip3 install petname
   ...
     Successfully installed petname-2.6

Success! Now all of our dependencies are installed and we can move on to the
JSON parsing code.



.. warning::

   An important question to ask is: Does the versions of Python and other
   dependencies match the versions you are developing with in your local
   environment? If not, make sure to install the correct version of Python.



Install and Test Your Code
~~~~~~~~~~~~~~~~~~~~~~~~~~

At this time, we should make a few small edits to the code that will make them
a lot more amenable to running in a container. There are two specific changes.
First, add a 'shebang' to the top of your scripts to make them executable
without calling the Python3 interpreter:

.. code-block:: python3

   #!/usr/bin/env python3

Second, instead of hard coding the filename 'animals.json' in each script, let's
make a slight modification so we can pass the filename on the command line. In
each script, add this line near the top:

.. code-block:: python3

   import sys

And change the ``with open...`` statements to these, as appropriate:

.. code-block:: python3

   with open(sys.argv[1], 'w') as f:          # in generate_animals.py
       json.dump(animal_dict, f, indent=2)    #

   with open(sys.argv[1], 'r') as f:          # in read_animals.py
       animal_dict = json.load(f)             #


.. tip::

   If you are using the sample files linked above, they already have these
   changes in them.

Since we are using simple Python scripts, there is not a difficult install
process. However, we can make them executable and add them to them user's `PATH`.

.. code-block:: console

   [root@fbf511fa3447 /]# cd /code
   [root@fbf511fa3447 /]# chmod +rx generate_animals.py
   [root@fbf511fa3447 /]# chmod +rx read_animals.py
   [root@fbf511fa3447 /]# export PATH=/code:$PATH

Now test with the following:

.. code-block:: console

   [root@fbf511fa3447 /]# cd /home
   [root@fbf511fa3447 /]# generate_animals.py animals.json
   [root@fbf511fa3447 /]# ls
   animals.json
   [root@fbf511fa3447 /]# read_animals.py animals.json
   {'head': 'bunny', 'body': 'yeti-ibex', 'arms': 8, 'legs': 12, 'tail': 20}


We now have functional versions of both scripts 'installed' in this container.
Now would be a good time to execute the `history` command to see a record of the
build process. When you are ready, type `exit` to exit the container and we can
start writing these build steps into a Dockerfile.


Assemble a Dockerfile
---------------------

After going through the build process interactively, we can translate our build
steps into a Dockerfile using the directives described below. Open up your copy
of ``Dockerfile`` with a text editor and enter the following:


The FROM Instruction
~~~~~~~~~~~~~~~~~~~~

We can use the FROM instruction to start our new image from a known base image.
This should be the first line of our Dockerfile. In our scenario, we want to
match our development environment with CentOS 7.7. We know our code works in
that environment, so that is how we will containerize it for others to use:

.. code-block:: text

   FROM centos:7.7.1908

Base images typically take the form `os:version`. Avoid using the '`latest`'
version; it is hard to track where it came from and the identity of '`latest`'
can change.

.. tip::

   Browse `Docker Hub <https://hub.docker.com/>`_ to discover other potentially
   useful base images. Keep an eye out for the 'Official Image' badge.


The RUN Instruction
~~~~~~~~~~~~~~~~~~~

We can install updates, install new software, or download code to our image by
running commands with the RUN instruction. In our case, our only dependencies
were Python3 and petname. So, we will use a few RUN instructions to install
them. Keep in mind that the the ``docker build`` process cannot handle
interactive prompts, so we use the ``-y`` flag with ``yum`` and ``pip3``.

.. code-block:: text

   RUN yum update -y
   RUN yum install -y python3
   RUN pip3 install petname==2.6

Each RUN instruction creates an intermediate image (called a 'layer'). Too many
layers makes the Docker image less performant, and makes building less
efficient. We can minimize the number of layers by combining RUN instructions:


.. code-block:: text

   RUN yum update -y && yum install -y python3
   RUN pip3 install petname==2.6



The COPY Instruction
~~~~~~~~~~~~~~~~~~~~

There are a couple different ways to get your source code inside the image. One
way is to use a RUN instruction with ``wget`` to pull your code from the web.
When you are developing, however, it is usually more practical to copy code in
from the Docker build context using the COPY instruction. For example, we can
copy our scripts to the root-level `/code` directory with the following
instructions:

.. code-block:: text

   COPY generate_animals.py /code/generate_animals.py
   COPY read_animals.py /code/read_animals.py


And, don't forget to perform two more RUN instruction to make the scripts
executable:

.. code-block:: text

   RUN chmod +rx /code/generate_animals.py && \
       chmod +rx /code/read_animals.py

.. tip::

   In the above code block, the ``\`` character at the end of the lines causes the
   newline character to be ignored. This can make very long run-on lines with
   many commands separated by ``&&`` easier to read.


The ENV Instruction
~~~~~~~~~~~~~~~~~~~

Another useful instruction is the ENV instruction. This allows the image
developer to set environment variables inside the container runtime. In our
interactive build, we added the ``/code`` folder to the ``PATH``, and we also
had to set a few environment variables for the character set. We can do this
with ENV instructions as follows:

.. code-block:: text

   ENV LC_CTYPE=en_US.UTF-8
   ENV LANG=en_US.UTF-8

   ENV PATH "/code:$PATH"

.. warning::

   Be mindful where these instructions appear in your Dockerfile! The encoding
   environment variables must appear in the file before they are needed.


Putting It All Together
~~~~~~~~~~~~~~~~~~~~~~~

The contents of the final Dockerfile should look like:

.. code-block:: text
   :linenos:

   FROM centos:7.7.1908

   RUN yum update -y && yum install -y python3

   ENV LC_CTYPE=en_US.UTF-8
   ENV LANG=en_US.UTF-8

   RUN pip3 install petname==2.6

   COPY generate_animals.py /code/generate_animals.py
   COPY read_animals.py /code/read_animals.py

   RUN chmod +rx /code/generate_animals.py && \
       chmod +rx /code/read_animals.py

   ENV PATH "/code:$PATH"


Build the Image
---------------

Once the Dockerfile is written and we are satisfied that we have minimized the
number of layers, the next step is to build an image. Building a Docker image
generally takes the form:

.. code-block:: console

   [isp02]$ docker build -t <dockerhubusername>/<code>:<version> .

The ``-t`` flag is used to name or 'tag' the image with a descriptive name and
version. Optionally, you can preface the tag with your **Docker Hub username**.
Adding that namespace allows you to push your image to a public registry and
share it with others. The trailing dot '``.``' in the line above simply
indicates the location of the Dockerfile (a single '``.``' means 'the current
directory').

To build the image, use:

.. code-block:: console

   [isp02]$ docker build -t username/json-parser:1.0 .

.. note::

   Don't forget to replace 'username' with your Docker Hub username.


Use ``docker images`` to ensure you see a copy of your image has been built. You can
also use `docker inspect` to find out more information about the image.

.. code-block:: console

   [isp02]$ docker images
   REPOSITORY           TAG        IMAGE ID       CREATED          SIZE
   wallen/json-parser   1.0        632f9f174274   33 minutes ago   507MB
   ...
   centos               7.7.1908   08d05d1d5859   15 months ago    204MB

.. code-block:: console

   [isp02]$ docker inspect username/json-parser:1.0


If you need to rename your image, you can either re-tag it with ``docker tag``, or
you can remove it with ``docker rmi`` and build it again. Issue each of the
commands on an empty command line to find out usage information.



Test the Image
--------------

We can test a newly-built image two ways: interactively and non-interactively.
In interactive testing, we will use ``docker run`` to start a shell inside the
image, just like we did when we were building it interactively. The difference
this time is that we are NOT mounting the code inside with the ``-v`` flag,
because the code is already in the container:

.. code-block:: console

   [isp02]$ docker run --rm -it username/json-parser:1.0 /bin/bash
   ...
   [root@c5cf05edddcd /]# ls /code
   generate_animals.py  read_animals.py
   [root@c5cf05edddcd /]# cd /home
   [root@c5cf05edddcd home]# pwd
   /home
   [root@c5cf05edddcd home]# generate_animals.py test.json
   [root@c5cf05edddcd home]# ls
   test.json
   [root@c5cf05edddcd home]# read_animals.py test.json
   {'head': 'snake', 'body': 'camel-oyster', 'arms': 8, 'legs': 12, 'tail': 20}

Here is an explanation of the options:

.. code-block:: text

   docker run      # run a container
   --rm            # remove the container when we exit
   -it             # interactively attach terminal to inside of container
   username/...    # image and tag on local machine
   /bin/bash       # shell to start inside container


Everything looks like it works! Next, exit the container and test the code
non-interactively. Notice we are calling the container again with ``docker run``,
but instead of specifying an interactive (``-it``) run, we just issue the command
as we want to call it on the command line. Also, notice the return of the ``-v``
flag, because we need to create a volume mount so that our data (``animals.json``)
will persist outside the container.

.. code-block:: console

   [isp02]$ mkdir test
   [isp02]$ cd test
   [isp02]$ pwd
   /home/wallen/coe-332/docker-exercise/test
   [isp02]$ docker run --rm -v $PWD:/data username/json-parser:1.0 generate_animals.py /data/animals.json
   [isp02]$ ls -l
   total 4
   -rw-r--r-- 1 root root 2325 Feb  8 14:30 animals.json


A new file appeared! The file ``animals.json`` was written by a the Python
script inside the container, and because we mounted our current location as a
folder called '/data' (``-v $PWD:/data``), and we made sure to write the output
file to that location in the container (``generate_animals.py /data/animals.json``),
then we get to keep the file.

Alas, there is an issue. The new file is owned by ``root``, simply because it is
``root`` who created the file inside the container. This is one minor Docker
annoyance that we run in to from time to time. The simplest fix is to use one
more ``docker run`` flag to specify the user and group ID namespace that should
be used inside the container.

.. code-block:: console

   [isp02]$ rm animals.json
   rm: remove write-protected regular file ‘animals.json’? y
   [isp02]$ docker run --rm -v $PWD:/data -u $(id -u):$(id -g) username/json-parser:1.0 generate_animals.py /data/animals.json
   [isp02]$ ls -l
   total 4
   -rw-r--r-- 1 wallen G-815499 2317 Feb  8 14:40 animals.json

Much better! And finally, we can test the ``read_animals.py`` script on the file
we just created:

.. code-block:: console

   [isp02]$ docker run --rm -v $PWD:/data username/json-parser:1.0 read_animals.py /data/animals.json
   {'head': 'lion', 'body': 'rhino-duck', 'arms': 6, 'legs': 12, 'tail': 18}

This time, we still mount the volume with ``-v`` so that the ``read_animals.py``
script has access to the input file inside the container. But we don't use the
``-u`` flag because we are not writing any new files and user namespace does not
need to be enforced.



Share Your Docker Image
-----------------------

Now that you have containerized, tested, and tagged your code in a Docker image,
the next step is to disseminate it so others can use it.

Docker Hub is the *de facto* place to share an image you built. Remember, the
image must be name-spaced with either your Docker Hub username or a Docker Hub
organization where you have write privileges in order to push it:

.. code-block:: console

   [isp02]$ docker login
   ...
   [isp02]$ docker push username/json-parser:1.0


You and others will now be able to pull a copy of your container with:

.. code-block:: console

   [isp02]$ docker pull username/json-parser:1.0


As a matter of best practice, it is highly recommended that you store your
Dockerfiles somewhere safe. A great place to do this is alongside the code
in, e.g., GitHub. GitHub also has integrations to automatically update your
image in the public container registry every time you commit new code.

For example, see: `Set up automated builds <https://docs.docker.com/docker-hub/builds/>`_




Additional Resources
--------------------

* `Docker for Beginners <https://training.play-with-docker.com/beginner-linux/>`_
* `Play with Docker <https://labs.play-with-docker.com/>`_
