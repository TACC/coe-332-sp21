Introduction to the Flask Web Server Microframework
===================================================

Flask is a Python library and framework for building web servers. We
want to learn how to provide web services. Some of the defining
characteristics of flask make it a good fit for this project:

-  Flask is small, relatively easy to use and get setup initially.
-  Flask is "robust" - a great fit for REST APIs and "microservices".
-  When used correctly, Flask is performant enough to handle the traffic
   of sites with 100Ks users.

Wait. What is a microservice?
-----------------------------

Microservices - also known as the microservice architecture - is an
architectural style that structures an application as a collection of
services that are

-  Highly maintainable and testable
-  Loosely coupled
-  Independently deployable
-  Organized around business capabilities.

The microservice architecture enables the continuous delivery/deployment
of large, complex applications. It also enables an organization to
evolve its technology stack. Sites that use microservces include:

-  Netflix
-  Amazon
-  eBay

There is a `great article on DevTeam.Space about
microservces <https://www.devteam.space/blog/microservice-architecture-examples-and-diagram/>`__.

Setup and Installation
----------------------

The flask library is not part of the Python standard library but can be
installed standard tools like ``pip``. You will want to use your virtual
environment to do the Installation:

1. SSH to the VM.
2. Execute ``pip3 install --user flask``
3. Look at the command line interface (CLI) (``flask --help``)

A Hello World Flask App
-----------------------

Create a file called app.py and open it for editing.

1. Import the Flask class: ``from flask import Flask`` At the heart of
   every flask-based web program is a "Flask application" object. The
   application object holds the primary configuration and behaviors of
   the web program.
2. Create a Flask application object passing ``__name__`` to the
   constructor\ ``:``\ app =
   Flask(\ **name**)\ ``Note that``\ **name**\ \` is a special python
   variable that gets set to either the module's actual name OR
   "**main**\ " in the case where the module was executed directly by
   the python interpreter.
3. Launch the development server using the ``app.run`` method if the
   app.py module is executed from the command line:

::

    from flask import Flask

    app = Flask(__name__)

    # the next statement should usually appear at the bottom of a flask app
    if __name__ == '__main__':
        app.run(debug=True, host='0.0.0.0')

Notes:

-  The ``debug=True`` tell flask to print verbose debug statements while
   the server is running.
-  The ``host=0.0.0.0`` instructs the server to listen on all network
   interfaces; basically this means you can reach the server from inside
   and outside the host VM.

Run the Flask App and Make an Initial Request
---------------------------------------------

There are 2 main ways of starting the flask service. For now, we would
like you to start the service using a unique port number. The
``-p 5000`` indicates that flask is running on port 5000. You will need
to use your own assigned port.

::

    [charlie@isp02 ~]$ export FLASK_APP=app.py
    [charlie@isp02 ~]$ export FLASK_ENV=development
    [charlie@isp02 ~]$ flask run -h localhost -p 5000
     * Serving Flask app "app.py" (lazy loading)
     * Environment: development
     * Debug mode: on
     * Running on http://localhost:5000/ (Press CTRL+C to quit)
     * Restarting with stat
     * Debugger is active!
     * Debugger PIN: 182-299-771

That's it! We now have a server up and running. Some notes:

-  Note that the program took over our shell; we could have put it in
   the background, but for now we want to leave it in the foreground.
   (Multiple PIDs are started for the flask app when started in daemon
   mode; to get them, find all processes listening on the port 5000
   socket with ``lsof -i:5000``).
-  If we make changes to our flask app while the server is running, the
   server will detect those changes automatically and "reload"; you will
   see a log to the effect of ``Detected change in <file>``.
-  We can stop the program with ``Ctrl+C`` just like any other (python)
   program.
-  If we stop our flask program, the server will no longer be listening
   and our requests will fail.

Let's try to talk to it. Note this line:

::

     * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)

That tells us our server is listening on all interfaces on the default
Flask port, port 5000.

A Word on Ports
~~~~~~~~~~~~~~~

Ports are a concept from networking that allow multiple services or
programs to be running at the same time, listening for messages over the
internet, on the same computer.

-  For us, ports will always be associated with a specific IP address.
   In general, we specify a port by combining it with an IP separated by
   a colon (:) character. For example, ``129.114.97.16:5000``.
-  One and only one program can be listening on a given port at a time.
-  Some ports are designated for specific activities; Port 80 is
   reserved for HTTP, port 443 for HTTPS (encrypted HTTP) but other
   ports can be used for HTTP/HTTPS traffic.

In a separate terminal window, SSH to the VM again.

We'll use the command line HTTP client ``curl`` to make a request to our
Flask app on port 5000;

curl Basics:
~~~~~~~~~~~~

You can think of ``curl`` as a command-line version of a web browser: it
is just an HTTP client.

-  The basic syntax is ``curl <some_url>:<some_port>``. This will make a
   GET request to the URL and port print the message response.
-  Curl will default to using port 80 for http and port 443 for https.
-  You can specify the HTTP verb to use with the ``-X`` flag; e.g.,
   ``curl -X GET <some_url>`` (though ``-X GET`` is redundant because
   curl defaults to making a GET request.

-  You can set "verbose mode" with the ``-v`` flag, which will then show
   additional information such as the headers passed back and forth
   (more on this later).

To make a request , type the following:

::

      $ curl localhost:5000

You should see:

::

    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
    <title>404 Not Found</title>
    <h1>Not Found</h1>
    <p>The requested URL was not found on the server.  If you entered the URL manually please check your spelling and try again.</p>

Our server is sending us HTML! It's sending a 404 that it could not find
the resource we requested. It's time to add some routes.

Routes in Flask
---------------

In a Flask app, you define the URLs in your application using the
``app.route`` decorator.

-  ``app.route`` is a decorator - place it on the line before the
   declaration of a python function.
-  ``app.route`` requires a string argument which is the path of the URL
   (not including the base\_url);
-  ``app.route`` takes an argument ``methods`` which should be a list of
   strings containing the names of valid HTTP methods.
-  When the URL + HTTP method combination is requested, Flask will call
   the decorated function.

(Warning - tangent!) What is a Python decorator?
------------------------------------------------

-  A decorator is a function that takes another function as an input and
   returns a different function then extends the behavior in some way.
-  The decorator must return a function which includes a call to the
   original function plus the extended behavior.
-  The typical structure of a decorator is as follows:

::

    def my_decorator(some_func):
        def func_to_return():
            # extend the behavior of some_fun by doing some processing before it is called (optional)
            do_something_before()
            # call the original function
            some_func(*args, **kwargs)
            # extend the behavior of some_fun by doing some processing after it is called (optional)
            do_something_after()
        return func_to_return

As an example, consider this test program:

::

    def print_dec(f):
        def func_to_return(*args, **kwargs):
            print("args: {}; kwargs: {}".format(args, kwargs))
            val = f(*args, **kwargs)
            print("return: {}".format(val))
            return val
        return func_to_return

    @print_dec
    def foo(a):
        return a+1


    result = foo(2)
    print("Got the result: {}".format(result))

Our print decorator gets executed automatically when we call ``foo(2)``.

Defining the Hello World Route
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Let's define a hello world route for the base url. To do so, add the
following code *before* the ``if __name__`` line:

::

    @app.route('/', methods=['GET'])
    def hello_world():
        return "Hello world\n"

Back in the other SSH terminal, execute the curl command again (you may
need to restart the flask app); you should see:

::

      $ curl localhost:5000
    Hello world

Routes with URL Parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~

Flask makes it easy to create Routes (or URLs) with variable in the URL.
Here are the basics:

-  We put the variable name in angled brackets (``<>``) within the
   app.route() decorator statement; for example ``@app.route(/<year>``)
   for a variable ``year``.
-  We make the variable a parameter to the decorated function and use it
   just like any other variable.

In the following example, we create a route with a variable:

::

    @app.route('/<name>', methods=['GET'])
    def hello_name(name):
        return "Hello {}\n".format(name)

HW parts A & B
----------------

Using your creature creator dataset, use your get\_data() function that
reads in your data set into a dictionary.

::

    def get_data():
    ....

You job is to create an API to manage that database. We need to think
through the following:

-  What are the nouns in our application?
-  What are the routes we want to define?
-  What data format do we want to return?

### Homework #### Part A Create some new GET routes for the nouns
identified in the database above. Find yout nouns, make at least 3
routes to retrieve the nouns from your json data #### Part B Write tests
for your routes
