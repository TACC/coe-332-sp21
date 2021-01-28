Homework 01
===========

**Due Date: Thursday, Feb 4, by 11:00am CST**

The Island of Dr. Moreau
------------------------

You are Dr. Moreau and you will randomly create 20 bizarre animals. Each animal
should have the following:

* A head randomly chosen from this list: snake, bull, lion, raven, bunny
* A body made up of two animals randomly chosen using the ``petname`` library
* A random number of arms; must be an even number and between 2-10, inclusive
* A random number of legs; must be a multiple of three and between 3-12, inclusive
* A non-random number of tails that is equal to the sum of arms and legs

Each of the 20 individual animals should be accessible from a list of
dictionaries. Use the ``json`` library to dump your data structure into an
``animals.json`` file. For example, your assembled data structure may look like:

.. code-block:: console

   {
     "animals": [
       {
         "head": "snake",
         "body": "sheep-bunny",
         "arms": 2,
         "legs": 12,
         "tail": 14
       },
       {
         "head": "snake",
         "body": "parrot-bream",
         "arms": 6,
         "legs": 6,
         "tail": 12
       },
       ... etc

Next, create a new Python script to read in ``animals.json`` and print the
details of one animal at random to screen.

What to Turn In
---------------

Your final homework should be turned in via GitHub. Create a repository under
your GitHub account for this class. Make a subfolder called ``homework01``. That
folder should contain three files:

* ``generate_animals.py``, which generates ``animals.json``
* ``animals.json``, which contains 20 bizarre animals as described above
* ``read_animals.py``, which reads ``animals.json`` and prints one animal at random to screen

The TA will git clone your repository on the due date / time, navigate to your
``homework01`` folder, and inspect your code and output. The TA will try to run
your code by typing ``python3 generate_animals.py`` followed by
``python3 read_animals.py``. Additionally, ``animals.json`` will be entered into
into a JSON validator to check if it is valid JSON.


Additional Resources
--------------------

* `The petname library <https://pypi.org/project/petname/>`_
* `Random numbers <https://docs.python.org/3.6/library/random.html#functions-for-integers>`_
* `JSON dump <https://docs.python.org/3.6/library/json.html#basic-usage>`_
* `Validate JSON with JSONLint <https://jsonlint.com/>`_
* Please find us in the class slack channel if you have any questions!
