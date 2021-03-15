Containerizing Flask
====================

As we have discussed previously, Docker containers are critical to packaging a
(e.g. Flask) application along with all of its dependencies, isolating it from
other applications and services, and deploying it consistently and reproducibly
and platform-agnostically.

Here, we will walk through the process of containerizing Flask with Docker, then
curling it as a containerized microservice. After going through this module,
students should be able to:

* Assemble the different components needed for a containerized microservice into on directory
* Establish and document requirements (e.g. dependencies, Python packages) for the project
* Build and run in the background a containerized Flask microservice
* Map ports on the ISP server to ports inside a container, and curl the correct ports to return a response from the microservice

Organize Your App Directory
---------------------------

First, create a "web" directory, and change directories to it:

.. code-block:: console

   [isp02]$ mkdir web
   [isp02]$ cd web

Then, create a new ``app.py`` (or copy an existing one) into this folder. It
should have the following contents:

.. code-block:: python3
   ::linenos::

   from flask import Flask

   app = Flask(__name__)

   @app.route('/', methods = ['GET'])
   def hello_world():
       return 'Hello, world!\n'

   @app.route('/<name>', methods = ['GET'])
   def hello_name(name):
       return 'Hello, {}!\n'.format(name)

   if __name__ == '__main__':
       app.run(debug=True, host='0.0.0.0')


Establish Requirements
----------------------

Python uses a specific file called ``requirements.txt`` to capture the required
libraries and packages for a project. For our example here, create a file called
``requirements.txt`` and add the following line:

.. code-block:: console

   Flask==1.1.2



Build a Docker Image
--------------------

As we saw in a previous section, we write up the recipe for our application
install process in a Dockerfile. Create a file called ``Dockerfile`` for our
Flask microservice and add the following lines:

.. code-block:: console

   FROM ubuntu:latest
   RUN apt-get update -y
   RUN apt-get install -y python-pip python-dev build-essential
   COPY . /app
   WORKDIR /app
   RUN pip install -r requirements.txt
   ENTRYPOINT ["python"]
   CMD ["app.py"]


Here we see usage of the Docker ``ENTRYPOINT`` and ``RUN`` instructions, which
essentially specify a default command (``python app.py``) that should be run
when an instance of this image is instantiated.

Save the file and build the image with the following command:

.. code-block:: console

   [isp02]$ docker build -t <username>/flask-helloworld:latest .

.. warning:

   Don't forget to replace ``<username>`` with your Docker Hub username.


Run a Docker Container
----------------------

To create an instance of your image (a "container"), use the following command:

.. code-block:: console

   [isp02]$ docker run --name "give-your-container-a-name" -d -p <your port number>:5000 <username>/flask-helloworld:latest"

For example:

.. code-block:: console

   [isp02]$ docker run --name "charlies-helloworld-flask-app" -d -p 5050:5000 charlie/flask-helloworld:latest"

The ``-d`` flag detaches your terminal from the running container - i.e. it
runs the container in the background. The ``-p`` flag maps a port on the ISP
server (5050, in the above case) to a port inside the container (5000, in the
above case). In the above example, the Flask app was set up to use the
default port inside the container (5000), and we can access that through our
specified port on ISP (5050).

Check to see that things are up and running with:

.. code-block:: console

   [isp02]$ docker ps -a

The list should have a container with the name you gave it, an ``UP`` status,
and the port mapping that you specified.

If the above is not found in the list of running containers, try to debug with
the following:

.. code-block:: console

   [isp02]$ docker logs "your-container-name"
   -or-
   [isp02]$ docker logs "your-container-number"


Access Your Microservice
------------------------

Now for the payoff - you can curl your REST API / Flask microservice by hitting
the correct port on the ISP server. Following the example above, which was using
port 5050:

.. code-block:: console

   [isp02]$ curl localhost:5050/
   Hello, world!
   [isp02]$ curl localhost:5050/Charlie
   Hello, Charlie!


Clean Up
--------

Finally, don't forget to stop your running container and remove it.

.. code-block:: console

   [isp02]$ docker ps -a | grep charlie
   60be6788d73d   charlie/flask-helloworld:latest     "python app.py"   4 minutes ago   Up 4 minutes   0.0.0.0:5050->5000/tcp   charlies-helloworld-flask-app
   [isp02]$ docker stop 60be6788d73d
   60be6788d73d
   [isp02]$ docker rm 60be6788d73d
   60be6788d73d


EXERCISE
~~~~~~~~

.. note::

   This exercise will be reflected in Homework 03, part C.


Containerize your Dr. Moreau apps! Create a route that creates one random
animal. Post a link to your route to Slack. Have another classmate hit your
route, and build an animal.
