Services
========

Services are the k8s resource one uses to expose HTTP APIs, databases and other components that communicate
on a network to other k8s pods and, ultimately, to the outside world. To
understand services we need to first discuss how k8s networking works.

k8s Networking Overview
-----------------------

.. note::

  We will be covering just the basics of k8s networking, enough for you to become proficient with the main concepts
  involved in deploying your application. Many details and advanced concepts will be omitted.

k8s creates internal networks and attaches pod containers to them to facilitate communication between pods. For a number
of reasons, including security, these networks are not reachable from outside k8s.

We can learn the IP address on this internal network for a specific pod with the following command:

.. code-block:: bash

  $ kubectl get pods <pod_name> -o wide

For example:

.. code-block:: bash

  $ kbectl get pods hello-deployment-9794b4889-mk6qw -o wide
    NAME                               READY   STATUS    RESTARTS   AGE   IP             NODE   NOMINATED NODE   READINESS GATES
    hello-deployment-9794b4889-mk6qw   1/1     Running   277        11d   10.244.3.176   c01    <none>           <none>

This tells us k8s assigned an IP address of ``10.244.3.176`` to our hello-deployment pod.

k8s assigns every pod an IP address on this private network. Pods that are on the same network can communicate with other
pods using their IP address.

Ports
-----
To communicate with a program running on a network, we use of ports. We saw how our flask program used port 5000 to
communicate HTTP requests from clients. We can expose ports in our k8s deployments by defining a ``ports`` stanza in
our ``template.spec.containers`` object. Let's try that now.

Create a file called ``hello-flask-deployment.yml`` and copy the following contents

.. code-block:: yaml

    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: helloflask
      labels:
        app: helloflask
    spec:
      replicas: 1
      selector:
        matchLabels:
          app: helloflask
      template:
        metadata:
          labels:
            app: helloflask
        spec:
          containers:
            - name: helloflask
              imagePullPolicy: Always
              image: jstubbs/hello-flask
              env:
              - name: FLASK_APP
                value: "app.py"
              ports:
              - name: http
                containerPort: 5000

Much of this will look familiar. We are creating a deployment that matches the pod description given in the ``template.spec``
stanza. The pod description uses an image, ``jstubbs/hello-flask``. This image runs a very simple flask server that
responds with simple text messages to a few endpoints.

The ``ports`` attribute is a list of k8s port descriptions. Each port in the list includes:

  * ``name`` -- the name of the port, in this case, ``http``. This could be anything we want really.
  * ``containerPort`` -- the port inside the container to expose, in this case ``5000``. This needs to match the port
    that the containerized program (in this case, flask server) is binding to.

Let's create the helloflask deployment using ``kubectl apply``

.. code-block:: bash

  $ kubectl apply -f hello-flask-deployment.yml
    deployment.apps/hello-flask-deployment configured

With our deployment created, we should see a new pod.

*Exercise.* Determine the IP address of the new pod for the hello-flask-deployment.

*Solution.*

.. code-block:: bash

  $ kubectl get pods
    NAME                                    READY   STATUS    RESTARTS   AGE
    hello-deployment-9794b4889-w4jlq        1/1     Running   0          56m
    hello-pvc-deployment-6dbbfdc4b4-sxk78   1/1     Running   231        9d
    helloflask-86d4c7d8db-2rkg5             1/1     Running   0          5m10s


  $ kubectl get pods helloflask-86d4c7d8db-2rkg5 -o wide
    NAME                          READY   STATUS    RESTARTS   AGE     IP            NODE   NOMINATED NODE   READINESS GATES
    helloflask-86d4c7d8db-2rkg5   1/1     Running   0          6m27s   10.244.7.95   c05    <none>           <none>

  Therefore, the IP address is 10.244.7.95

We found the IP address for our flask container, but if we try to communicate with it from the k8s master node, we will
get an error:

.. code-block:: bash

  $ curl 10.244.7.95:5000
    curl: (7) Failed connect to 10.244.7.95:5000; Network is unreachable

This is because the 10.244.*.* private k8s network is not available from the outside, not even from the master node.
However, it *is* available from other pods in the namespace.


A Debug Deployment
------------------

For exploring and debugging k8s deployments, it can be helpful to have a basic container on the network. We can
create a deployment for this purpose.

For example, let's create a deployment using the official python 3.9 image. We can run a sleep command and then, once
the container pod is running, we can use ``exec`` to launch a shell inside the container.


EXERCISE
^^^^^^^^

1. Create a new "debug" deployment using the following definition:

.. code-block:: yaml

    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: py-debug-deployment
      labels:
        app: py-app
    spec:
      replicas: 1
      selector:
        matchLabels:
          app: py-app
      template:
        metadata:
          labels:
            app: py-app
        spec:
          containers:
            - name: py39
              image: python:3.9
              command: ['sleep', '999999999']

(Hint: paste the contenat into a new file called ``deployment-python-debug.yml``  and then use the ``kubectl apply``
command).

2. Exec into the running pod for this deployment. (Hint: then find the pod name and then use the ``kubectl exec``
command, running the shell (``/bin/bash``) command in it).

Once we have a shell running inside our debug deployment pod, we can try to access our flask server. Recall that
the IP and port for the flask server were determined above to be 10.244.7.95:5000 (yours will likely be different).

If we try to access it using curl from within the debug container, we get:

.. code-block:: bash

    root@py-debug-deployment-5cc8cdd65f-xzhzq: $ curl 10.244.7.95:5000
    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
    <title>404 Not Found</title>
    <h1>Not Found</h1>
    <p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>

That's a different error from before, and that's good! This time, the error is from flask, and it indicates that flask
doesn't have a route for the root path (``/``).

The ``jstubbs/hello-flask`` image does have a route for the path  ``/hello-service``. If we try that one, we should
get a response:

.. code-block:: bash

  root@py-debug-deployment-5cc8cdd65f-xzhzq: $ curl 10.244.7.95:5000/hello-service
  Hello world

Great! k8s networking from within the private network is working!


Services
--------

We saw above how pods can use the IP address of other pods to communicate. However, that is not a great solution because
we know the pods making up a deployment come and go. Each time a pod is destroyed and a new one created it gets a new
IP address. Moreover, we can scale the number of replica pods for a deployment up and down to handle more or less load.

How would an application that needs to communicate with a pod know which IP address to use? If there are 3 pods comprising
a deployment, which one should it use? This problem is referred to as the *service discovery problem* and k8s has a
solution for it.. the ``Service`` abstraction.

A k8s service provides an abstract way of exposing an application running as a collection of pods on a single IP address
and port. Let's define a service for our hello-flask deployment.


Copy and paste the following code into a file called ``hello-flask-service.yml``:

.. code-block:: yaml

    apiVersion: v1
    kind: Service
    metadata:
      name: hello-service
    spec:
      type: ClusterIP
      selector:
        app: helloflask
      ports:
      - name: helloflask
        port: 5000
