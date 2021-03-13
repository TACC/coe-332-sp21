
***********************
Homework 3 - Formalized
***********************

Filtering JSON Data by Example:

.. code-block:: python

    def get_data():
        with open("data_file.json", "r") as json_file:
            user_data == json.load(json_file)
    return user_data

    test = get_data();
    print (type(test))
    output = [x for x in test if x['head'] == 'snake']

A.
##

* Create 3 routes to your island animal JSON data, one has to be /animals, the other 2 should require a parameter for example:
    
    * /animals will return all of your animals
    * /animals/head/bunny will return all of your animals w/ bunny heads - here bunny would be a parameter
    * /animals/legs/6 will return all of your anmials w/ 6 legs - here 6 would be a paramter

create your flask server that connects to your flask port


B.
##

Containerize your Flask Apps.
Be sure to include your json data file in your Container

C.
##
Write a consumer similar to:

.. code-block:: python

    import requests

    response = requests.get(url="http://localhost:5050/animals")

    #look at the response code

    print(response.status_code)
    print(response.json())
    print(response.headers)


Share your url and routes to Slack, pick another student's url, and consume their data