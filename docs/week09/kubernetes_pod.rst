Kubernetes - Overview and Introduction to Pods
==============================================

In this section we give an overview of the Kubernetes system and introduce the first major Kubernetes abstraction, the Pod.

Kubernetes Overview
~~~~~~~~~~~~~~~~~~~
Kubernetes (k8s) is itself a distributed system of software components that run a cluster of one or more machines (physical
computers or virtual machines). Each machine in a k8s cluster is either a "master" or a "worker" node.

Users communicate with k8s by making requests to its API. The following steps outline how Kubernetes works at a high level:

 1) Requests to k8s API describe the user's *desired state* on the cluster; for example, the desire that 3 containers of
    a certain image are running.
 2) The k8s API schedules new containers to run on one or more worker nodes.
 3) After the container is started, the Kubernetes deployment controller, installed on each worker node, monitors the
    containers on the node.
 4) The k8s components, including the API and the deployment controllers, maintain both the *desired state* and the
    *actual state* in a distributed database. The components continuously coordinate together to make the actual state
    converge to the desired state.

.. figure:: ./images/k8s_overview.png
    :width: 1000px
    :align: center


Connecting to the TACC Kubernetes Instance
------------------------------------------
In this class, we will use TACC's FreeTail Kubernetes cluster for deploying our applications. To connect to it, use SSH
and your TACC username as follows:

.. code-block::

 $ ssh <tacc_username>@freetail.tacc.utexas.edu

You will be prompted for your TACC username and password, just as you are when connecting to isp02.


Hello, Kubernetes
-----------------

We will use the Kubernetes Command Line Interface (CLI) referred to as "kubectl" (pronounced "Kube control") to make
requests to the Kubernetes API. We could use any HTTP client, including a command-line client such as curl, but ``kubectl``
simplifies the process of formatting requests.

The ``kubectl`` software should already be installed and configured to use the Freetail K8s cluster. Let's verify that
is the case by running the following:

.. code-block:: bash

  $ kubectl version -o yaml

You should see output similar to the following:

.. code-block:: bash

    clientVersion:
      buildDate: "2021-01-13T13:28:09Z"
      compiler: gc
      gitCommit: faecb196815e248d3ecfb03c680a4507229c2a56
      gitTreeState: clean
      gitVersion: v1.20.2
      goVersion: go1.15.5
      major: "1"
      minor: "20"
      platform: linux/amd64
    serverVersion:
      buildDate: "2020-11-11T13:09:17Z"
      compiler: gc
      gitCommit: d360454c9bcd1634cf4cc52d1867af5491dc9c5f
      gitTreeState: clean
      gitVersion: v1.19.4
      goVersion: go1.15.2
      major: "1"
      minor: "19"
      platform: linux/amd64

This command made an API request to the TACC Freetail k8s cluster and returned information about the version
of k8s running there (under ``serverVersion``) as well as the version of the `kubectl`` that we are running (under
``clientVersion``).

.. note::

  The output of the ``kubectl`` command was yaml because we used the ``-o yaml`` flag. We could have asked for the output
  to be formatted in json with ``-o json``. The ``-o`` flag is widely available on ``kubectl`` commands.


Introduction to Pods
~~~~~~~~~~~~~~~~~~~~

Pods are a fundamental abstraction within Kubernetes and are the most basic unit of computing that can be deployed onto
the cluster. A pod can be thought of as generalizing the notion of a container: a pod contains one or more containers
that are tightly coupled and need to be scheduled together, on the same computer, with access to a shared file system
and a shared network address.

.. note::

  By far, the majority pods you will meet in the wild, including the ones used in this course, will only include one
  container. A pod with multiple containers can be thought of as an "advanced" use case.

To begin, we will define a pod with one container. As we will do with all the resources we want to create in k8s, we
will describe our pod in a yaml file.

Create a file called ``pod-basic.yml``, open it up in an editor and paste the following code in:

.. code-block:: yaml

    ---
    apiVersion: v1
    kind: Pod
    metadata:
      name: hello
    spec:
      containers:
        - name: hello
          image: busybox
          command: ['sh', '-c', 'echo "Hello, Kubernetes!" && sleep 3600']

Let's break this down. The top four stanzas are common to all k8s resource descriptions:

  * ``apiVersion`` -- describes what version of the k8s API we are working in. We are using ``v1``.
  * ``kind`` -- tells k8s what kind of resource we are describing, in this case a ``Pod``.
  * ``metadata`` -- in general, this is additional information about the resource we are describing that doesn't pertain
    to its operation. Here, we are giving our pod a ``name``, ``hello``.
  * ``spec`` -- This is where the actual description of the resource begins. The contents of this stanza vary depending
    on the ``kind`` of resource you are creating. We go into more details on this in the next section.


The Pod Spec
~~~~~~~~~~~~

In k8s, you describe resources you want to create or update using a ``spec``. The required and optional parameters
available depend on the ``kind`` of resource you are describing.

The pod spec we defined looked like this:

.. code-block:: yaml

    spec:
      containers:
        - name: hello
          image: busybox
          command: ['sh', '-c', 'echo "Hello, Kubernetes!" && sleep 3600']

There is just one stanza, the ``containers`` stanza, which is a list of containers (recall that pods can contain
multiple containers). Here we are definging just one container. We provide:

  * ``name`` -- this is the name of the container, similiar to the name attribute in Docker.
  *

In practice, we won't be creating many ``Pod`` resources directly -- we'll be creating other resources, such as
``deployments`` that are made up of ``Pod`` resources -- but it is important to understand pods and to be able to work
with pods using ``kubectl`` for debugging and other management tasks.


Additional Resources
~~~~~~~~~~~~~~~~~~~~

 * `k8s Pod Reference <https://kubernetes.io/docs/concepts/workloads/pods/>`_

