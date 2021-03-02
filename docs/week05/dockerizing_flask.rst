Dockerizing Flask
=================

This is going to be a practical walkthrough on the process of containerizing - Dockerizing - Flask

Step 1
------

create your web directory, and change directories to it

-  ``mkdir web``
-  ``cd web``


Step 2
------

save/create your ``app.py`` in this folder

::

    from flask import Flask
    app = Flask(__name__)

    @app.route('/', methods = ['GET'])
        def helloworld():
        return "Hello World!!!"
   
    # the next statement should always appear at the bottom of your flask app
    if __name__ == 'main':
    app.run(debug=True, host='0.0.0.0')

    
Step 3
------

create a requirments file - ``requirements.txt`` - in your web directory

``Flask==1.1.1``


Step 4
------

create your dockerfile

::

    FROM ubuntu:latest
    RUN apt-get update -y
    RUN apt-get install -y python-pip python-dev build-essential
    COPY . /app
    WORKDIR /app
    RUN pip install -r requirements.txt
    ENTRYPOINT ["python"]
    CMD ["app.py"]


Step 5
------

build your image

``docker build -t flask-helloworld:latest .``


Step 6
------

run the container

``docker run --name "give your container a name" -d -p <your portnumber>:5000 flask-helloworld``


Step 7
------

check to see if things are up and running

``docker ps -a``

if things are good, you should see your container running on your port...


Step 7a
-------

if things aren't quite right,

``docker logs "your container name"``

-or-

``docker logs "your container number"``


Step 8
------

curl your port

``curl localhost:<your portnumber>``

i.e ``curl localhost:5045``

Step 9
------

bring if down! Clean up after yourself
Find your container number, and pause it

``docker ps -a``
``docker stop <your container number>``


Homework Part b
---------------

### Homework ### Part B Containerize your Dr. Moreau apps! Create a route that creates one random animal. Post a link to your route to Slack. Have another classmate hit your route, and build an animal.

 




