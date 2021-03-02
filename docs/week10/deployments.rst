Deployments
===========

Deployments are an abstraction and resource type in Kubernetes that can be used to represent long-running application
components, such as databases, REST APIs, or asynchronous worker programs. Deployments are defined with a pod
definition and a replication strategy, such as, "run 3 instances of this pod across the cluster" or "run an instance
of this pod on every worker node in the k8s cluster."

For this class, we will define deployments instead of pods, as they come with a number of advantages. Deployments:

  * Can be used to run multiple instances of a pod, to allow for more computing to meet demands put on a system.
  * Are actively monitored by k8s for health -- if a pod in a deployment crashes, k8s will try to start a new one
    automatically.


Creating a Basic Deployment
---------------------------

We will use yaml to describe a deployment just like we did in the case of pods. Copy and paste the following into a file
called ``deployment-basic.yml``

.. code-block:: yaml

    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: hello-deployment
      labels:
        app: hello-app
    spec:
      replicas: 1
      selector:
        matchLabels:
          app: hello-app
      template:
        metadata:
          labels:
            app: hello-app
        spec:
          containers:
            - name: hellos
              image: busybox
              command: ['sh', '-c', 'echo "Hello, Kubernetes!" && sleep 3600']

Let's break this down.


We create a deployment in k8s using the ``apply`` command, just like when creating a pod:

.. code-block:: bash

  $ kubectl apply -f basic-deploymnet.yml

If all went well, k8s response should look like:

.. code-block:: bash

  deployment.apps/hello-deployment created

We can list deployments, just like we listed pods:

.. code-block:: bash

  $ kubectl get deployments
    NAME               READY   UP-TO-DATE   AVAILABLE   AGE
    hello-deployment   1/1     1            1           1m

We can also list pods, and here we see that k8s has created a pod for our deployment for us:

.. code-block:: bash

  $ kubectl get pods
    NAME                               READY   STATUS    RESTARTS   AGE
    hello                              1/1     Running   0          29m
    hello-deployment-9794b4889-kms7p   1/1     Running   0          1m

Note that we see our "hello" pod from earlier as well as the pod "hello-deployment-9794b4889-kms7p" that k8s created
for our deployment. We can use all the kubectl commands associated with pods, including listing, describing and
getting the logs. In particular, the logs for our "hello-deployment-9794b4889-kms7p" pod prints the same "Hello,
Kubernetes!" message as our first pod.

Deleting Pods
-------------
However, there is one fundamental difference between the "hello" pod we created before and our "hello" deployment which
can be seen when we delete pods.

To delete a pod, we use the ``kubectl delete pods <pod_name>`` command. Let's first delete our hello deployment pod:

.. code-block:: bash

  $ kubectl delete pods hello-deployment-9794b4889-kms7p

It might take a little while for the response to come back, but when it does you should see:

.. code-block:: bash

  pod "hello-deployment-9794b4889-kms7p" deleted

If we then immediately list the pods, we see something interesting:

.. code-block:: bash

  $ kubectl get pods
    NAME                               READY   STATUS    RESTARTS   AGE
    hello                              1/1     Running   0         33m
    hello-deployment-9794b4889-sx6jc   1/1     Running   0          9s

We see a new pod (in this case, "hello-deployment-9794b4889-sx6jc") was created and started by k8s for our hello
deployment automatically! k8s did this because we instructed it that we wanted 1 replica pod to be running in the
deployment's ``spec`` -- this was the *desired* state -- and when that didn't match the actual state (0 pods)
k8s worked to change it.

What do you expect to happen if we delete the original "hello" pod? Will k8s start a new one? Let's try it

.. code-block:: bash

  $ kubectl delete pods hello
    pod "hello" deleted

  $ kubectl get pods
    NAME                               READY   STATUS    RESTARTS   AGE
    hello-deployment-9794b4889-sx6jc   1/1     Running   0          4m

k8s did not start a new one. This "automatic self-healing" is one of the major difference between deployments and pods.


Scaling a Deployment
--------------------
If we want to change the number of pods k8s runs for our deployment, we simply update the ``replicas`` attribute in
our deployment file and apply the changes. Let's modify our "hello" deployment to run 4 pods. Modify
``deployment-basic.yml`` as follows:

.. code-block:: yaml

    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: hello-deployment
      labels:
        app: hello-app
    spec:
      replicas: 4
      selector:
        matchLabels:
          app: hello-app
      template:
        metadata:
          labels:
            app: hello-app
        spec:
          containers:
            - name: hellos
              image: busybox
              command: ['sh', '-c', 'echo "Hello, Kubernetes!" && sleep 3600']

Apply the changes with:

.. code-block:: bash

  $ k apply -f deployment-basic.yml
    deployment.apps/hello-deployment configured

When we list pods, we see k8s has quickly implemented our requested change:

.. code-block:: bash

    $ k get pods
    NAME                               READY   STATUS    RESTARTS   AGE
    hello-deployment-9794b4889-mk6qw   1/1     Running   0          11s
    hello-deployment-9794b4889-sx6jc   1/1     Running   0          15m
    hello-deployment-9794b4889-v2mb9   1/1     Running   0          11s
    hello-deployment-9794b4889-vp6mp   1/1     Running   0          11s


EXERCISE
--------

1) Delete several of the hello deployment pods and see what happens.
2) Scale the number of pods associated with the hello deployment back down to 1.


Persistent Volume Claims and ConfigMaps
---------------------------------------
Some applications need access to storage where they can save data that will persist across container starts and stops.
We saw how to solve this with Docker using a volume mount. In k8s, we use a persistent volume claim.

Create a new file, ``deployment-pvc.yml``, with the following contents, replacing "<username>" with your username:

.. code-block:: yaml

    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: hello-pvc-deployment
      labels:
        app: hello-pvc-app
    spec:
      replicas: 1
      selector:
        matchLabels:
          app: hello-pvc-app
      template:
        metadata:
          labels:
            app: hello-pvc-app
        spec:
          containers:
            - name: hellos
              image: busybox
              command: ['sh', '-c', 'echo "Hello, Kubernetes!" > /data/out.txt && sleep 3600']
              volumeMounts:
              - name: hello-<username>-data
                mountPath: "/data"
          volumes:
          - name: hello-jstubbs-data
            persistentVolumeClaim:
              claimName: hello-<username>-data

We have added a ``volumeMounts`` stanza to ``spec.containers`` and we added a ``volumes`` stanza to the ``spec``.
Note also that we have changed the command to redirect the output of the ``echo`` command to a file.

Exec Into a Pod
---------------

Some times it can be helpful to "exec" into a running pod -- that is, open a shell in the container of a pod. To do this,
we use the following command: ``kubectl exec -it <pod_name> /bin/bash``




Additional Resources
====================

 * `Kubernetes Deployments Documentation <https://kubernetes.io/docs/concepts/workloads/controllers/deployment/>`_
