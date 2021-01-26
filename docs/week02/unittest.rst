Unit Tests in Python
====================

In the previous module, we wrote a simple script with three functions used to
validate the state abbreviations in a JSON file. In this module, we will use the
Python ``unittest`` library to write unit tests for those functions.

After working through this module, students should be able to:

* Find the documentation for the Python ``unittest`` library
* Identify parts of code that should be tested and appropriate assert methods
* Write and run reasonable unit tests


Getting Started
---------------

Unit tests are designed to test small components (e.g. individual functions) of
your code. They should demonstrate that things that are expected to work
actually do work, and things that are expected to break raise appropriate errors.
The Python ``unittest`` unit testing framework supports test automation, set up
and shut down code for tests, and aggregation of tests into collections. It is
built in to the Python Standard Library and can be imported directly. Find the
`documentation here <https://docs.python.org/3/library/unittest.html>`_. The
best way to see how it works is to see it applied to a real example.

`Pull a copy  <https://raw.githubusercontent.com/TACC/coe-332-sp21/main/docs/week02/sample-json/json_ex.py>`_
of the Python script from the previous section if you don't have one already.

We need to make a small organizational change to this code in order to make it
work with the test suite (this is good organizational practice anyway). We will
move everything that is not already a function into a new ``main()`` function:

.. code-block:: python3
   :linenos:
   :emphasize-lines: 21-28,30,31

   import json

   def check_char_count(mystr):
       if ( len(mystr) == 2 ):
           return( f'{mystr} count passes' )
       else:
           return( f'{mystr} count FAILS' )

   def check_char_type(mystr):
       if ( mystr.isupper() and mystr.isalpha() ):
           return( f'{mystr} type passes' )
       else:
           return( f'{mystr} type FAILS' )

   def check_char_match(str1, str2):
       if ( str1[0] == str2[0] ):
           return( f'{str1} match passes' )
       else:
           return( f'{str1} match FAILS' )

   def main():
       with open('states.json', 'r') as f:
           states = json.load(f)

       for i in range(50):
           print(check_char_count( states['states'][i]['abbreviation'] ))
           print(check_char_type( states['states'][i]['abbreviation'] ))
           print(check_char_match( states['states'][i]['abbreviation'], states['states'][i]['name'] ))

   if __name__ == '__main__':
       main()

The last two lines make it so the ``main()`` function is only called if this
script is executed directly, and not if it is imported into another script.

Break a Function
----------------

The function in this example Python script are simple, but can be easily broken
if not used as intended. Use the Python interactive interpreter to import the
functions we wrote and find out what breaks them:

.. code-block:: python3

   >>> from json_ex import check_char_count        # that was easy!
   >>>
   >>> check_char_count('AA')    # this is supposed to pass
   'AA count passes'
   >>> check_char_count('AAA')   # this is supposed to fail
   'AAA count FAILS'
   >>> check_char_count(12)      # what if we send an int instead of a string?
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
     File "/home/wallen/test2/json_ex.py", line 4, in check_char_count
       if ( len(mystr) == 2 ):
   TypeError: object of type 'int' has no len()
   >>> check_char_count([12, 34])                   # ... uh oh
   '[12, 34] count passes'

Everything looked good until we sent our function a **list with two elements**.
The function we wrote just checks the length of whatever we sent as an argument,
but we never intended lists to pass. So now we need to do two things:

* Write up the above tests in an automated way
* Fix our function so lists don't pass through

Create a new file called ``test_json_ex.py`` and start writing code to automate
the above tests:

.. tip::

    It is common Python convention to name a test file the same name as the
    script you are testing, but with the ``test_`` prefix added at the
    beginning.


.. code-block:: python3
   :linenos:

   import unittest
   from json_ex import check_char_count

   class TestJsonEx(unittest.TestCase):

       def test_check_char_count(self):
           self.assertEqual(check_char_count('AA'), 'AA count passes')
           self.assertEqual(check_char_count('AAA'), 'AAA count FAILS')

   if __name__ == '__main__':
       unittest.main()

In the simplest case above, we do several things:

* Import the ``unittest`` framework
* Import the function (``check_char_count``) we want to test
* Create a class for testing our application (json_ex) and subclass ``unittest.TestCase``
* Define a method for testing a specific function (``check_char_count``) from our application
* Write tests to check that certain calls to our function return what we expect
* Wrap the ``unittest.main()`` function at the bottom so we can call this script

The key part of the above test are the ``assertEqual`` methods. The test will
only pass if the two parameters passed to that method are equal. Execute the
script to run the tests:

.. code-block:: console

   [isp02]$ python3 test_json_ex.py
   .
   ----------------------------------------------------------------------
   Ran 1 test in 0.000s

   OK

Success! Next, we can start to look at edge cases. If you recall above, sending
an ``int`` to this function raised a ``TypeError``. This is good and expected
behavior! We can use the ``assertRaises`` method to make sure that happens:

.. code-block:: python3

   def test_check_char_count(self):
       self.assertEqual(check_char_count('AA'), 'AA count passes')
       self.assertEqual(check_char_count('AAA'), 'AAA count FAILS')
       self.assertRaises(TypeError, check_char_count, 1)
       self.assertRaises(TypeError, check_char_count, True)
       self.assertRaises(TypeError, check_char_count, ['AA', 'BB'])

.. tip::

   How do we know what parameters to pass to the ``assertRaises`` method? Check
   `the documentation <https://docs.python.org/3/library/unittest.html#unittest.TestCase.assertRaises>`_
   of course!

Run it again to see what happens:

.. code-block:: console

   [isp02]$ python3 test_json_ex.py
   F
   ======================================================================
   FAIL: test_check_char_count (__main__.TestJsonEx)
   ----------------------------------------------------------------------
   Traceback (most recent call last):
     File "test_json_ex.py", line 11, in test_check_char_count
       self.assertRaises(TypeError, check_char_count, ['AA', 'BB'])
   AssertionError: TypeError not raised by check_char_count

   ----------------------------------------------------------------------
   Ran 1 test in 0.001s

   FAILED (failures=1)


Our test failed because we are trying to assert that sending our function a list
should result in a TypeError. But, that's not what happened - in fact sending
our function a list resulted in a pass without error.

Fix a Function
--------------

We need to modify our function in ``json_ex.py`` to handle edge cases better. We
don't want to pass anything sent to this function other than a two-character
**string**. So, let's modify our function and add an assert statement to make
sure the thing passed to the function is in fact a string:

.. code-block:: python3
   :emphasize-lines: 3

   def check_char_count(mystr):

       assert isinstance(mystr, str), 'Input to this function should be a string'

       if ( len(mystr) == 2 ):
           return( f'{mystr} count passes' )
       else:
           return( f'{mystr} count FAILS' )


Assert statements are a convenient way to put checks in code with helpful print
statements for debugging. Run ``json_ex.py`` again to make sure it is still
working, then run the test suite again:

.. code-block:: console

   [isp02]$ python3 test_json_ex.py
   F
   ======================================================================
   FAIL: test_check_char_count (__main__.TestJsonEx)
   ----------------------------------------------------------------------
   Traceback (most recent call last):
     File "test_json_ex.py", line 9, in test_check_char_count
       self.assertRaises(TypeError, check_char_count, 1)
   AssertionError: Input to this function should be a string

   ----------------------------------------------------------------------
   Ran 1 test in 0.001s

   FAILED (failures=1)

Whoops! The test is still failing. This is because we are trying to enforce a
``TypeError`` when we send our function an ``int``. However, with the new assert
statement in our function, we are raising an ``AssertionError`` before the
``TypeError`` ever has a chance to crop up. We must modify our tests to now look
for ``AssertionErrors``.

.. code-block:: python3
   :emphasize-lines: 4-6

   def test_check_char_count(self):
       self.assertEqual(check_char_count('AA'), 'AA count passes')
       self.assertEqual(check_char_count('AAA'), 'AAA count FAILS')
       self.assertRaises(AssertionError, check_char_count, 1)
       self.assertRaises(AssertionError, check_char_count, True)
       self.assertRaises(AssertionError, check_char_count, ['AA', 'BB'])

Then run the test suite one more time:

.. code-block:: console

   [isp02]$ python3 test_json_ex.py
   .
   ----------------------------------------------------------------------
   Ran 1 test in 0.001s

   OK

Success! The test for our first function is passing. Our test suite essentially
documents our intent for the behavior of the ``check_char_count()`` function.
And, if ever we change the code in that function, we can see if the behavior we
intend still passes the test.

Another Function, Another Test
------------------------------

The next function in our original code is ``check_char_type()``, which checks to
see that the passed string consists of uppercase letters only. This function is
already pretty fail safe because it is using built-in string methods
(``isupper()`` and ``isalpha()``) to do the checking. These already have
internal error handling, so we can probably get away with a few simple tests and
no changes to our original function.

Add the following lines to the ``test_json_ex.py``:

.. code-block:: python3
   :linenos:
   :emphasize-lines: 3,14-22

   import unittest
   from json_ex import check_char_count
   from json_ex import check_char_type

   class TestJsonEx(unittest.TestCase):

       def test_check_char_count(self):
           self.assertEqual(check_char_count('AA'), 'AA count passes')
           self.assertEqual(check_char_count('AAA'), 'AAA count FAILS')
           self.assertRaises(AssertionError, check_char_count, 1)
           self.assertRaises(AssertionError, check_char_count, True)
           self.assertRaises(AssertionError, check_char_count, ['AA', 'BB'])

        def test_check_char_type(self):
            self.assertEqual(check_char_type('AA'), 'AA type passes')
            self.assertEqual(check_char_type('Aa'), 'Aa type FAILS')
            self.assertEqual(check_char_type('aa'), 'aa type FAILS')
            self.assertEqual(check_char_type('A1'), 'A1 type FAILS')
            self.assertEqual(check_char_type('a1'), 'a1 type FAILS')
            self.assertRaises(AttributeError, check_char_type, 1)
            self.assertRaises(AttributeError, check_char_type, True)
            self.assertRaises(AttributeError, check_char_type, ['AA', 'BB'])

   if __name__ == '__main__':
       unittest.main()

The ``isupper()`` and ``isalpha()`` methods only work on strings - if you try
them on anything else, they will automatically return an ``AttributeError``. We
can confirm this with our tests.

Run the tests again to be sure you have two passing tests:

.. code-block:: console

   [isp02]$ python3 test_json_ex.py
   ..
   ----------------------------------------------------------------------
   Ran 2 tests in 0.000s

   OK


EXERCISE
~~~~~~~~

Focusing on the ``assertEqual()`` and ``assertRaises()`` methods, write
reasonable tests for the final function - ``check_char_match()``.



Additional Resources
--------------------

* `Python unittest documentation <https://docs.python.org/3/library/unittest.html>`_
* `Exceptions in Python <https://docs.python.org/3/library/exceptions.html>`_
