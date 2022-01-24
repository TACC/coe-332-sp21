Introduction to Containers
==========================

Containers are an important common currency for app development, web services,
scientific computing, and more. Containers allow you to package an application
along with all of its dependencies, isolate it from other applications and
services, and deploy it consistently and reproducibly and *platform-agnostically*.
In this introductory module, we will learn about containers and their uses, in
particular the containerization platform **Docker**.

After going through this module, students should be able to:

* Describe what a container is
* Use essential docker commands
* Find and pull existing containers from Docker Hub
* Run containers interactively and non-interactively



What is a Container?
--------------------

* A container is a standard unit of software that packages up code and all its
  dependencies so the application runs quickly and reliably from one computing
  environment to another.
* Containers allow a developer to package up an application with all of the
  parts it needs, such as libraries and other dependencies, and ship it all out
  as one package.
* Multiple containers can run on the same machine and share the OS kernel with
  other containers, each running as isolated processes in user space, hence are
  *lightweight* and have *low overhead*.
* Containers ensure *portability* and *reproducibility* by isolating the
  application from environment.


How is a Container Different from a VM?
---------------------------------------

Virtual machines enable application and resource isolation, run on top of a
hypervisor (high overhead). Multiple VMs can run on the same physical
infrastructure - from a few to dozens depending on resources. VMs take up more
disk space and have long start up times (~minutes).

.. figure:: images/arch_vm.png
   :width: 400
   :align: center

   Applications isolated by VMs.

Containers enable application and resource isolation, run on top of the host
operating system. Many containers can run on the same physical infrastructure -
up to 1,000s depending on resources. Containers take up less disk space than VMs
and have very short start up times (~100s of ms).

.. figure:: images/arch_container.png
   :width: 400
   :align: center

   Applications isolated by containers.



Docker
------

Docker is a containerization platform that uses OS-level virtualization to
package software and dependencies in deliverable units called containers. It is
by far the most common containerization platform today, and most other container
platforms are compatible with Docker. (E.g. Singularity and Shifter are two
containerization platforms you'll find in HPC environments).

We can find existing containers at:

1. `Docker Hub <https://hub.docker.com/>`_
2. `Quay.io <https://quay.io/>`_
3. `BioContainers <https://biocontainers.pro/#/>`_


Some Quick Definitions
----------------------

**CONTAINER**

A container is a standard unit of software that packages up code and all its
dependencies so the application runs quickly and reliably from one computing
environment to another. Containers includes everything from the operating
system, user-added files, metadata.

**IMAGE**

A Docker image is a read-only file used to produce Docker containers. It is
comprised of layers of other images, and any changes made to an image can only
be saved and propagated on by adding new layers. The "base image" is the
bottom-most layer that does not depend on any other layer and typically defines,
e.g., the operating system for the container. Running a Docker image creates an
instance of a Docker container.

**DOCKERFILE**

The Dockerfile is a recipe for creating a Docker image. They are simple, usually
short plain text files that contain a sequential set of commands (*a recipe*)
for installing and configuring your application and all of its dependencies. The
Docker command line interface is used to "build" an image from a Dockerfile.

**IMAGE REGISTRY**

The Docker images you build can be stored in online image registries, such as
`Docker Hub <https://hub.docker.com/>`_. (It is similar to the way we store
Git repositories on GitHub.) Image registries support the notion of tags on
images to identify specific versions of images. It is mostly public, and many
"official" images can be found.

Summing it Up
-------------

If you are developing an app or web service, you will almost certainly want to
work with containers. First you must either **build** an image from a
Dockerfile, or **pull** an image from a public registry. Then, you **run** (or
deploy) an instance of your image into a container. The container represents
your app or web service, running in the wild, isolated from other apps and
services.

.. figure:: images/docker_workflow.png
   :width: 600
   :align: center

   Simple Docker workflow.



Getting Started With Docker
---------------------------

Much like the ``git`` command line tools, the ``docker`` command line tools
follow the syntax: ``docker <verb> <parameters>``. Discover all the verbs
available by typing ``docker --help``, and discover help for each verb by typing
``docker <verb> --help``. Open up your favorite terminal, log in to the class
server, and try running the following:

.. code-block:: console

   [isp02]$ docker version
   Client: Docker Engine - Community
    Version:           20.10.3
    API version:       1.41
    Go version:        go1.13.15
    Git commit:        48d30b5
    Built:             Fri Jan 29 14:34:14 2021
    OS/Arch:           linux/amd64
    Context:           default
    Experimental:      true

   Server: Docker Engine - Community
    Engine:
     Version:          20.10.3
     API version:      1.41 (minimum version 1.12)
     Go version:       go1.13.15
     Git commit:       46229ca
     Built:            Fri Jan 29 14:32:37 2021
     OS/Arch:          linux/amd64
     Experimental:     false
    containerd:
     Version:          1.4.3
     GitCommit:        269548fa27e0089a8b8278fc4fc781d7f65a939b
    runc:
     Version:          1.0.0-rc92
     GitCommit:        ff819c7e9184c13b7c2607fe6c30ae19403a7aff
    docker-init:
     Version:          0.19.0
     GitCommit:        de40ad0


.. warning::

   Please let the instructors know if you get any errors on issuing the above
   command.

**EXERCISE**

Take a few minutes to run ``docker --help`` and a few examples of
``docker <verb> --help`` to make sure you can find and read the help text.


Working with Images from Docker Hub
-----------------------------------

To introduce ourselves to some of the most essential Docker commands, we will go
through the process of listing images that are currently available on the ISP
server, we will pull a 'hello-world' image from Docker Hub, then we will run the
'hello-world' image to see what it says.

List images on the ISP server with the ``docker images`` command. This peeks
into the Docker daemon, which is shared by all users on this system, to see
which images are available, when they were created, and how large they are:

.. code-block:: console

   [isp02]$ docker images
   REPOSITORY        TAG       IMAGE ID       CREATED         SIZE
   final_web         latest    dc4cda1aa2f1   8 months ago    749MB
   final_worker      latest    dc4cda1aa2f1   8 months ago    749MB
   flask             latest    58cdeed93a41   9 months ago    448MB
   master-web        latest    58cdeed93a41   9 months ago    448MB
   creatures         3         503cd4631565   9 months ago    446MB
   my_image          manisha   503cd4631565   9 months ago    446MB
   homework5         latest    f08364452cbd   9 months ago    490MB
   phuong            latest    f08364452cbd   9 months ago    490MB
   web_web           latest    a7d00df8fa6a   9 months ago    444MB
   web_worker        latest    a7d00df8fa6a   9 months ago    444MB
   redis             latest    4cdbec704e47   10 months ago   98.2MB
   ubuntu            latest    4e5021d210f6   10 months ago   64.2MB
   harmish/gnuplot   latest    b67698a87ae1   2 years ago     392MB


Pull an image from Docker hub with the ``docker pull`` command. This looks
through the Docker Hub registry and downloads the 'latest' version of that
image:

.. code-block:: console

   [isp02]$ docker pull hello-world
   Using default tag: latest
   latest: Pulling from library/hello-world
   0e03bdcc26d7: Pull complete
   Digest: sha256:31b9c7d48790f0d8c50ab433d9c3b7e17666d6993084c002c2ff1ca09b96391d
   Status: Downloaded newer image for hello-world:latest
   docker.io/library/hello-world:latest


Run the image we just pulled with the ``docker run`` command. In this case,
running the container will execute a simple shell script inside the container
that has been configured as the 'default command' when the image was built:

.. code-block:: console

   [isp02]$ docker run hello-world

   Hello from Docker!
   This message shows that your installation appears to be working correctly.

   To generate this message, Docker took the following steps:
    1. The Docker client contacted the Docker daemon.
    2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
       (amd64)
    3. The Docker daemon created a new container from that image which runs the
       executable that produces the output you are currently reading.
    4. The Docker daemon streamed that output to the Docker client, which sent it
       to your terminal.

   To try something more ambitious, you can run an Ubuntu container with:
    $ docker run -it ubuntu bash

   Share images, automate workflows, and more with a free Docker ID:
    https://hub.docker.com/

   For more examples and ideas, visit:
    https://docs.docker.com/get-started/


Check to see if any containers are still running using ``docker ps``:

.. code-block:: console

   [isp02]$ docker ps
   CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES


**EXERCISE**

The command ``docker ps`` shows only currently running containers. Pull up the
help text for that command and figure out how to show all containers, not just
currently running containers.


Pull Another Image
------------------

Navigate to the repositories of user ``wallen`` on Docker Hub
`here <https://hub.docker.com/u/wallen>`_.

Scroll down to find an image called ``wallen/bsd``, then click on that image.

Pull the image using the suggested command, then check to make sure it is
available locally:

.. code-block:: console

   [isp02]$ docker pull wallen/bsd:1.0
   ...
   [isp02]$ docker images
   ...
   [isp02]$ docker inspect wallen/bsd:1.0
   ...

.. tip::

   Use ``docker inspect`` to find some metadata available for each image.



Start an Interactive Shell Inside a Container
---------------------------------------------

Using an interactive shell is a great way to poke around inside a container and
see what is in there. Imagine you are ssh-ing to a different Linux server, have
root access, and can see what files, commands, environment, etc., are available.

Before starting an interactive shell inside the container, execute the following
commands on the ISP server (we will see why in a minute):

.. code-block:: console

   [isp02]$ whoami
   wallen
   [isp02]$ pwd
   /home/wallen
   [isp02]$ cat /etc/os-release
   NAME="CentOS Linux"
   VERSION="7 (Core)"
   ID="centos"
   ID_LIKE="rhel fedora"
   VERSION_ID="7"
   PRETTY_NAME="CentOS Linux 7 (Core)"
   ANSI_COLOR="0;31"
   CPE_NAME="cpe:/o:centos:centos:7"
   HOME_URL="https://www.centos.org/"
   BUG_REPORT_URL="https://bugs.centos.org/"

   CENTOS_MANTISBT_PROJECT="CentOS-7"
   CENTOS_MANTISBT_PROJECT_VERSION="7"
   REDHAT_SUPPORT_PRODUCT="centos"
   REDHAT_SUPPORT_PRODUCT_VERSION="7"

   [isp02]$ ls -l /usr/games/
   total 0

Now start the interactive shell:

.. code-block:: console

   [isp02]$ docker run --rm -it wallen/bsd:1.0 /bin/bash
   root@fc5b620c5a88:/#

Here is an explanation of the command options:

.. code-block:: text

  docker run      # run a container
  --rm            # remove the container when we exit
  -it             # interactively attach terminal to inside of container
  wallen/bsd:1.0  # image and tag on local machine
  /bin/bash       # shell to start inside container

Try the following commands and note what has changed:

.. code-block:: console

   root@fc5b620c5a88:/# whoami
   root
   root@fc5b620c5a88:/# pwd
   /
   root@fc5b620c5a88:/# cat /etc/os-release
   NAME="Ubuntu"
   VERSION="16.04.6 LTS (Xenial Xerus)"
   ID=ubuntu
   ID_LIKE=debian
   PRETTY_NAME="Ubuntu 16.04.6 LTS"
   VERSION_ID="16.04"
   HOME_URL="http://www.ubuntu.com/"
   SUPPORT_URL="http://help.ubuntu.com/"
   BUG_REPORT_URL="http://bugs.launchpad.net/ubuntu/"
   VERSION_CODENAME=xenial
   UBUNTU_CODENAME=xenial
   root@fc5b620c5a88:/# ls /usr/games/
   adventure   bcd       countmail  hack     morse      ppt     robots   teachgammon  worms
   arithmetic  boggle    cribbage   hangman  number     primes  rot13    tetris-bsd   wtf
   atc         caesar    dab        hunt     phantasia  quiz    sail     trek         wump
   backgammon  canfield  go-fish    mille    pig        rain    snake    wargames
   battlestar  cfscores  gomoku     monop    pom        random  snscore  worm

Now you are the ``root`` user on a different operating system inside a running
Linux container! You can type ``exit`` to escape the container.

**EXERCISE**

Before you exit the container, try running a few of the games (e.g. ``hangman``).



Run a Command Inside a Container
--------------------------------

Back out on the ISP server, we now know we have an image called
``wallen/bsd:1.0`` that has some terminal games inside it which would not
otherwise be available to us on the ISP server. They (and their dependencies)
are *isolated* from everything else. This image (``wallen/bsd:1.0``) is portable
and will run the exact same way on any OS that Docker supports.

In practice, though, we don't want to start interactive shells each time we need
to use a software application inside an image. Docker allows you to spin up an
*ad hoc* container to run applications from outside. For example, try:


.. code-block:: console

   [isp02]$ docker run --rm wallen/bsd:1.0 whoami
   root
   [isp02]$ docker run --rm wallen/bsd:1.0 pwd
   /
   [isp02]$ docker run --rm wallen/bsd:1.0 cat /etc/os-release
   NAME="Ubuntu"
   VERSION="16.04.6 LTS (Xenial Xerus)"
   ID=ubuntu
   ID_LIKE=debian
   PRETTY_NAME="Ubuntu 16.04.6 LTS"
   VERSION_ID="16.04"
   HOME_URL="http://www.ubuntu.com/"
   SUPPORT_URL="http://help.ubuntu.com/"
   BUG_REPORT_URL="http://bugs.launchpad.net/ubuntu/"
   VERSION_CODENAME=xenial
   UBUNTU_CODENAME=xenial
   [isp02]$ docker run --rm wallen/bsd:1.0 ls /usr/games
   adventure   bcd       countmail  hack     morse      ppt     robots   teachgammon  worms
   arithmetic  boggle    cribbage   hangman  number     primes  rot13    tetris-bsd   wtf
   atc         caesar    dab        hunt     phantasia  quiz    sail     trek         wump
   backgammon  canfield  go-fish    mille    pig        rain    snake    wargames
   battlestar  cfscores  gomoku     monop    pom        random  snscore  worm
   [isp02]$ docker run --rm -it wallen/bsd:1.0 hangman

The first four commands above omitted the ``-it`` flags because they did not
require an interactive terminal to run. On each of these commands, Docker finds
the image the command refers to, spins up a new container based on that image,
executes the given command inside, prints the result, and exits and removes the
container.

The last command, which executes the ``hangman`` game, requires an interactive
terminal so the ``-it`` flags were provided.


Essential Docker Command Summary
--------------------------------

+----------------+------------------------------------------------+
| Command        | Usage                                          |
+================+================================================+
| docker login   | Authenticate to Docker Hub using username and  |
|                | password                                       |
+----------------+------------------------------------------------+
| docker images  | List images on the local machine               |
+----------------+------------------------------------------------+
| docker ps      | List containers on the local machine           |
+----------------+------------------------------------------------+
| docker pull    | Download an image from Docker Hub              |
+----------------+------------------------------------------------+
| docker run     | Run an instance of an image (a container)      |
+----------------+------------------------------------------------+
| docker inspect | Provide detailed information on Docker objects |
+----------------+------------------------------------------------+
| docker rmi     | Delete an image                                |
+----------------+------------------------------------------------+
| docker rm      | Delete a container                             |
+----------------+------------------------------------------------+
| docker stop    | Stop a container                               |
+----------------+------------------------------------------------+
| docker build   | Build a docker image from a Dockerfile in the  |
|                | current working directory                      |
+----------------+------------------------------------------------+
| docker tag     | Add a new tag to an image                      |
+----------------+------------------------------------------------+
| docker push    | Upload an image to Docker Hub                  |
+----------------+------------------------------------------------+


Additional Resources
--------------------

* `Docker Docs <https://docs.docker.com/>`_
* `Best practices for writing Dockerfiles <https://docs.docker.com/develop/develop-images/dockerfile_best-practices/>`_
* `Docker Hub <https://hub.docker.com/>`_
* `Docker for Beginners <https://training.play-with-docker.com/beginner-linux/>`_
* `Play with Docker <https://labs.play-with-docker.com/>`_
