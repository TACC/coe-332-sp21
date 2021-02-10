YAML Reference
==============

This reference guide is meant to introduce you to YAML syntax. YAML is basically
JSON with a couple extra features, and meant to be a little more human readable.
We will be using YAML formatted configuration files in the Docker-compose and
Kubernetes sections, so it is important to become familiar with the syntax.


YAML Basics
-----------

YAML syntax is similar to Python dictionaries, and we will usually see them as
key:value pairs. Values can include strings, numbers, booleans, null, lists,
and other dictionaries.

Previously, we saw a simple JSON object in dictionary form like:

.. code-block:: json

   {
     "key1": "value1",
     "key2": "value2"
   }

That same object in YAML looks like:

.. code-block:: yaml

   ---
   key1: value1
   key2: value2
   ...

Notice that YAML documents all start with three hyphens on the top line (``---``),
and end with an optional three dots (``...``) on the last line. Key:value pairs
are separated by colons, but consecutive key:value pairs are NOT separated by
commas.

We also mentioned that JSON supports list-like structures. YAML does too. So the
following valid JSON block:

.. code-block:: json

   [
     "thing1", "thing2", "thing3"
   ]

Appears like this in YAML:

.. code-block:: yaml

   ---
   - thing1
   - thing2
   - thing3
   ...

Elements of the same list all appear with a hyphen ``-`` at the same indent
level.

We also previously saw this complex data structure in JSON:

.. code-block:: json

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

The same structure in YAML is:

.. code-block:: yaml

   ---
   department: COE
   number: 332
   name: Software Engineering and Design
   inperson: false
   instructors:
     - Joe
     - Charlie
     - Brandi
     - Joe
   prerequisites:
     - course: COE 322
       instructor: Victor
     - course: SDS 322
       instructor: Victor
   ...

The whole thing can be considered a dictionary. The key ``instructors`` contains
a value that is a list of names, and the key ``prerequisites`` contains a value
that is a list of two dictionaries. Booleans appear as ``false`` and ``true``
(lowercase only). A null / empty value would appear as ``null``.

Also, check out the list of states we worked with in the JSON section, but now
in YAML
`here <https://raw.githubusercontent.com/tacc/coe-332-sp21/main/docs/week04/scripts/states.yaml>`_.

More YAML
---------

There is a lot more to YAML, most of which we will not use in this course. Just
know that YAML files can contain:

* Comments
* Multi-line strings / text blocks
* Multi-word keys
* Complex objects
* Special characters
* Explicitly declared types
* A mechanism to duplicate / inherit values across a document ("anchors")



If we encounter a need for any of these, we can refer to the
`official YAML syntax <https://yaml.org/spec/1.2/spec.html>`_




Additional Resources
--------------------

* `YAML Spec <https://yaml.org/spec/1.2/spec.html>`_
* `YAML Validator <http://www.yamllint.com/>`_
* `JSON / YAML Converter <https://www.json2yaml.com/>`_
