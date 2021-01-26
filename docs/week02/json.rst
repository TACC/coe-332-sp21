Working with JSON
=================

In this hands-on module, we will learn how to work with the JSON data format.
JSON (javascript object notation) is a powerful, flexible, and lightweight data
format that we see a lot throughout this course, especially when working with
web apps and REST APIs.

After going through this module, students should be able to:

* Identify and write valid JSON
* Load JSON into an object in a Python script
* Loop over and work with elements in a JSON object
* Write JSON to file from a Python script


Sample JSON
-----------

Analogous to Python dictionaries, JSON is typically composed of key:value pairs.
The universality of this data structure makes it ideal for exchanging
information between programs written in different languages and web apps. A
simple, valid JSON  object may look like this:

.. code-block:: json

   {
     "key1": "value1",
     "key2": "value2"
   }

Although less common in this course, simple arrays of information (analogous to
Python lists) are also valid JSON:

.. code-block:: JSON

   [
     "thing1", "thing2", "thing3"
   ]

JSON offers a lot of flexibility on the placement of white space and newline
characters. Types can also be mixed together, forming complex data structures:

.. code-block:: JSON

   {
     "department": "COE",
     "number": 332,
     "name": "Software Engineering and Design",
     "inperson": false,
     "instructors": ["Joe", "Charlie", "Brandi", "Joe"],
     "prerequisites": [
       {"course": "COE 322", "instructor": "Victor"},
       {"course": "SDS 322", "instructor": "Victor"}
     ]
   }

On the class server, navigate to your home directory and make a new folder for
this class. Within that folder, make a subfolder for today's module:

.. code-block:: bash

   [local]$ ssh username@isp02.tacc.utexas.edu
   (enter password)
   [isp02]$ mkdir coe-332/
   [isp02]$ cd coe-332/
   [isp02]$ mkdir week02-json && cd week02-json

Download this sample JSON files into that folder using the ``wget`` command, or
click `this link <https://raw.githubusercontent.com/TACC/coe-332-sp21/main/docs/week02/sample-json/states.json>`_
and cut and paste the contents into a file called ``states.json``:

.. code-block:: bash

   [isp02]$ wget https://raw.githubusercontent.com/TACC/coe-332-sp21/main/docs/week02/sample-json/states.json

Plug this file (or some of the above samples) into an online JSON validator
(e.g. `JSONLint <https://jsonlint.com/>`_). Try making manual changes to some of
the entries to see what breaks the JSON format.

Load JSON into a Python Script
------------------------------

The ``json`` Python library is part of the Python Standard Library, meaning it
can be imported without having to be installed by pip. Start editing a new
Python script using your method of choice:

.. code-block:: bash

    [isp02]$ vim json_ex.py


.. warning::

   Do not name your Python script "json.py". If you ``import json`` when there
   is a script called "json.py" in the same folder, it will import that instead
   of the actual ``json`` library.

The code you need to read in the JSON file of state names and abbreviations into
a Python object is:

.. code-block:: python3
   :linenos:

   import json

   with open('states.json', 'r') as f:
       states = json.load(f)

Only three simple lines! We ``import json`` from the standard library so that we
can work with the ``json`` class. We use the safe ``with open...`` statement to
open the file we downloaded read-only into a filehandle called ``f``. Finally,
we use the ``load()`` method of the ``json`` class to load the contents of the
JSON file into our new ``states`` object.

EXERCISE
~~~~~~~~

Try out some of these calls to the ``type()`` function on the new ``states``
object that you loaded. Also ``print()`` each of these as necessary to be sure
you know what each is. Be able to explain the output of each call to ``type()``
and ``print()``.

.. code-block:: python3
   :linenos:

   import json

   with open('states.json', 'r') as f:
       states = json.load(f)

   type(states)
   type(states['states'])
   type(states['states'][0])
   type(states['states'][0]['name'])
   type(states['states'][0]['name'][0])

   print(states)
   print(states['states'])
   print(states['states'][0])
   print(states['states'][0]['name'])
   print(states['states'][0]['name'][0])

.. tip::

   Consider doing this in the Python interpreter's interactive mode instead if
   in a script.

Working with JSON
-----------------

As we have seen, the JSON object we loaded contains state names and
abbreviations. In the US, official state abbreviations are unique, two-letter
identifiers. Let's write a few functions to help us validate whether our state
abbreviations follow the rules or not.

First, write a function to check whether there are exactly two characters in
each of the abbreviations. Call that function, and have it return a message
about whether the abbreviation passes or fails the test.

.. code-block:: python3
   :linenos:
   :emphasize-lines: 3-7,12-13

   import json

   def check_char_count(mystr):
       if ( len(mystr) == 2 ):
           return( f'{mystr} count passes' )
       else:
           return( f'{mystr} count FAILS' )

   with open('states.json', 'r') as f:
       states = json.load(f)

   for i in range(50):
       print(check_char_count( states['states'][i]['abbreviation']))



Next, write a function to check whether both characters are actually uppercase
letters, and not something else like a number or a special character or a
lowercase letter. Again, have it return a pass or fail message as appropriate.

.. code-block:: python3
   :linenos:
   :emphasize-lines: 9-13,20

   import json

   def check_char_count(mystr):
       if (len(mystr) == 2):
           return( f'{mystr} count passes' )
       else:
           return( f'{mystr} count FAILS' )

   def check_char_type(mystr):
       if (mystr.isalpha() and mystr.isupper()):
           return( f'{mystr} type passes' )
       else:
           return( f'{mystr} type FAILS' )

   with open('states.json', 'r') as f:
       states = json.load(f)

   for i in range(50):
       print(check_char_count( states['states'][i]['abbreviation']))
       print(check_char_type( states['states'][i]['abbreviation']))



EXERCISE
~~~~~~~~

Write a third function to check that the first character of each abbreviation
matches the first character of the corresponding state. Return pass or fail
messages as appropriate.


Write JSON to File
------------------

Finally, in a new script, we will create an object that we can write to a new
JSON file.

.. code-block:: python3
   :linenos:

   import json

   data = {}
   data['class'] = 'COE332'
   data['title'] = 'Software Engineering and Design'
   data['subjects'] = []
   data['subjects'].append( {'week': 1, 'topic': ['linux', 'python']} )
   data['subjects'].append( {'week': 2, 'topic': ['json', 'unittest', 'git']} )

   with open('class.json', 'w') as out:
       json.dump(data, out, indent=2)

Notice that most of the code in the script above was simply assembling a normal
Python dictionary. The ``json.dump()`` method only requires two arguments - the
object that should be written to file, and the filehandle. The ``indent=2``
argument is optional, but it makes the output file looks a little nicer and
easier to read.

Inspect the output file and paste the contents into an online JSON validator.

Additional Resources
--------------------

* `Reference for the JSON library <https://docs.python.org/3.6/library/json.html>`_
* `Validate JSON with JSONLint <https://jsonlint.com/>`_
