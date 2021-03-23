Midterm Project, COE 332
========================

.. note::

    What is a UUID


    first some background. 
    A universally unique identifier is a 128-bit number used to identify information in computer systems, typically referred to as an UUID (thought, in Microsoft-speak it's called an GUID). When an UUID is generated using standard methods, for practical purposes, they are universally unique.

    -   UUIDS are composed of 128 bit numbers generated using standards-based algorithms that are "guaranteed" unique (i.e., the probability of collisions is so low that, to get to a 50% probability of collision, one would need to generate 2.7x10^18 UUIDs).
    -   There are 4 major versions of the standard 
        -   We will use UUID version 4 because: it generates uuid's with very low probability of collision without using sensitive data such as the MAC address of the server which is usually used in generating the UUID.
        
    -   The algorithms can and have been implemented in most major programming languages (yay standards!) and can generate uuid's very quickly.


    How do I generate a UUID in Python?

    .. code::
    
        >>> import uuid
        >>> uuid.uuid4()
        
        Out[1]: UUID('56849963-e90d-4322-a369-50870f0cf9fa')

        # return a string:
        >>> str(uuid.uuid4())
        Out[2]: '66a3acf3-8009-4cd3-8d40-c8ce42229f08'


You are Dr. Moreau and you have an island of bizzare creatures.
Now we're going to use flask to interact with our data

add the following to your JSON producer:
    - a timestamp labeled "created_on"
    - an unique identifier "uid"

In your Flask app,

    - have routes that
        - query a range of dates
        - selects a particular creature by its unique identifier
        - edits a particular creature by passing the UUID, and updated "stats"
        - deletes a selection of animals by a date rangees
        - returns the average number of legs per animal
        - returns a total count of animals

