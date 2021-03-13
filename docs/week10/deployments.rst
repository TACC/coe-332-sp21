Deployments
===========

Deployments are an abstraction and resource type in Kubernetes that can be used to represent long-running application
components, such as databases, REST APIs, web servers, or asynchronous worker programs. The key idea with deployments is
that they should *always be running*.

Imagine a program that runs a web server for a blog site. The blog website should alawys be available, 24 hours a day,
7 days a week. If the blog web server program crashes, it would ideally be restarted immediately so that the blog site
was available again. This is the main idea behind deployments.

Deployments are defined with a pod definition and a replication strategy, such as, "run 3 instances of this pod across
the cluster" or "run an instance of this pod on every worker node in the k8s cluster."

For this class, we will define deployments for our flask application and its associated components, as deployments
come with a number of advantages over defining "raw" pods. Deployments:

  * Can be used to run multiple instances of a pod, to allow for more computing to meet demands put on a system.
  * Are actively monitored by k8s for health -- if a pod in a deployment crashes or is otherwise deemed unhealthy, k8s
    will try to start a new one automatically.


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
              image: ubuntu:18.04
              command: ['sh', '-c', 'echo "Hello, Kubernetes!" && sleep 3600']

Let's break this down. Recall that the top four attributes are common to all k8s resource descriptions, however it is
worth noting:

  * ``apiVersion`` -- We need to use version ``apps/v1`` here. In k8s, different functionalities are packaged into
    different APIs. Deployments are part of the ``apps/v1`` API, so we must specify that here.
  * ``metadata`` -- The ``metadata.name`` gives our deployment object a name. This part is similar to when we defined pods.
    However, the ``labels`` concept is new. k8s uses labels to allow objects to refer to other objects in a decoupled way.
    A label in k8s is nothing more than a ``name: value`` pair that users create to organize objects and add information
    meaningful to the user. In this case, ``app`` is the name and ``hello-app`` is the value. Conceptually, you can think
    of label names like variables and labels values as the value for the variable. In some other deployment, we may choose
    to use label ``app: profiles`` to indicate that the deployment is for the "profiles" app.

Let's look at the ``spec`` stanza for the deployment above.

  * ``replicas`` -- Defines how many pods we want running at a time for this deployment, in this case, we are asking
    that just 1 pod be running at a time.
  * ``selector`` -- This is how we tell k8s where to find the pods to manage for the deployment. Note we are using labels
    again here, the ``app: hello-app`` label in particular.
  * ``template`` -- Deployments match one or more pod descriptions defined in the template. Note that in the ``metadata``
    of the template, we provide the same lable (``app: hello-app``) as we did in the ``matchLabels`` stanza of the
    ``selector``. This tells k8s that this spec is part of the deployment.
  * ``template.spec`` -- This is a pod spec, just like we worked with last time.

.. note::
  If the labels, selectors and matchLables seems confusing and complicated, that's understandable. These semantics allow
  for complex deployments that dynamically match different pods, but for the deployments in this class, you will not
  need this extra complexity. As long as you ensure the label in the ``template`` is the same as the label in the
  ``selector.matchLables`` your deployments will work. It's worth pointing out that the first use of the ``app: hello-app``
  label for the deployment iteself (lines 5 and 6 of the yaml) could be removed without impacting the end result.


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
Kubernetes!" message, just as was the case with our first pod.

Deleting Pods
-------------
However, there is a fundamental difference between the "hello" pod we created before and our "hello" deployment which
we have alluded to. This difference can be seen when we delete pods.

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
k8s worked to change it. Remember, deployments are for programs that should *always be running*.

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
              image: ubuntu:18.04
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

ImagePullPolicy
---------------

When defining a deployment, we can specify an ``ImagePullPolicy`` which instructs k8s about when and how to download
the image associated with the pod definition. For example, we can add ``imagePullPolicy: Always`` to our hello-deployment
as follows:

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
              imagePullPolicy: Always
              image: ubuntu:18.04
              command: ['sh', '-c', 'echo "Hello, Kubernetes!" && sleep 3600']

and now k8s will always try to download the latest version of ``ubuntu:18.04`` from Docker Hub every time it creates
a new pod for this deployment. Using ``imagePullPolicy: Always`` is nice during active development because you ensure
k8s is always deploying the latest version of your code. Other possible values include ``IfNotPresent`` which instruct
k8s to only pull the image if it doesn't already exist on the worker node.


Mounts, Volumes and Persistent Volume Claims
--------------------------------------------
Some applications need access to storage where they can save data that will persist across container starts and stops.
We saw how to solve this with Docker using a volume mount. In k8s, we use a combination of volume mounts, volumes and
persistent volume claims.

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
              image: ubuntu:18.04
              command: ['sh', '-c', 'echo "Hello, Kubernetes!" >> /data/out.txt && sleep 3600']
              volumeMounts:
              - name: hello-<username>-data
                mountPath: "/data"
          volumes:
          - name: hello-<username>-data
            persistentVolumeClaim:
              claimName: hello-<username>-data

We have added a ``volumeMounts`` stanza to ``spec.containers`` and we added a ``volumes`` stanza to the ``spec``.
These have the following effects:

  * The ``volumeMounts`` include a ``mountPath`` attribute whose value should be the path in the container that is to
    be provided by a volume instead of what might possibly be contained in the image at that path. Whatever is provided
    by the volume will overwrite anything in the image at that location.
  * The ``volumes`` stanza states that a volume with a given name should be fulfilled with a specific persistentVolumeClaim.
    Since the volume name (``hello-<username>-data``) matches the name in the ``volumeMounts`` stanza, this volume will be
    used for the volumeMount.
  * In k8s, a persistent volume claim makes a request for some storage from a storage resource configured by the k8s
    administrator in advance. While complex, this system supports a variety of storage systems without requiring the
    application engineer to know details about the storage implementation.

Note also that we have changed the command to redirect the output of the ``echo`` command to the file ``/data/out.txt``.
This means that we should not expect to see the output in the logs for pod but instead in the file inside the container.

However, if we create this new deployment and then list pods we see something curious:

.. code-block:: bash

  $ kubectl apply -f deployment-pvc.yml
  $ kubectl get pods
    NAME                                    READY   STATUS    RESTARTS   AGE
    hello-deployment-9794b4889-mk6qw        1/1     Running   1          62m
    hello-deployment-9794b4889-sx6jc        1/1     Running   1          78m
    hello-deployment-9794b4889-v2mb9        1/1     Running   1          62m
    hello-deployment-9794b4889-vp6mp        1/1     Running   1          62m
    hello-pvc-deployment-74f985fffb-g9zd7   0/1     Pending   0          4m22s

Our "hello-deployment" pods are still running fine but our new "hello-pvc-deployment" pod is still in "Pending" status. It
appears to be stuck. What could be wrong?

We can ask k8s to describe that pod to get more details:

.. code-block:: bash

  $ kubectl describe pods hello-pvc-deployment-74f985fffb-g9zd7
    Name:           hello-pvc-deployment-74f985fffb-g9zd7
    Namespace:      designsafe-jupyter-stage
    Priority:       0
    Node:           <none>
    Labels:         app=hello-pvc-app
                    pod-template-hash=74f985fffb
    <... some output omitted ...>
    Tolerations:     node.kubernetes.io/not-ready:NoExecute op=Exists for 300s
                     node.kubernetes.io/unreachable:NoExecute op=Exists for 300s
    Events:
      Type     Reason            Age    From               Message
      ----     ------            ----   ----               -------
      Warning  FailedScheduling  4m35s  default-scheduler  persistentvolumeclaim "hello-jstubbs-data" not found
      Warning  FailedScheduling  4m35s  default-scheduler  persistentvolumeclaim "hello-jstubbs-data" not found

At the bottom we see the "Events" section contains a clue: persistentvolumeclaim "hello-jstubbs-data" not found.

This is our problem. We told k8s to fill a volume with a persistent volume claim named "hello-jstubbs-data" but we
never created that persistent volume claim. Let's do that now!

Open up a file called ``hello-pvc.data`` and copy the following contents, being sure to replace ``<username>``
with your TACC username:

.. code-block:: yaml

    kind: PersistentVolumeClaim
    apiVersion: v1
    metadata:
      name: hello-<username>-data
    spec:
      accessModes:
        - ReadWriteOnce
      storageClassName: rbd
      resources:
        requests:
          storage: 1Gi

We will use this file to create a persistent volume claim against the storage that has been set up in the TACC k8s
cluster. In order to use this storage, you do need to know the storage class (in this case, "rbd", which is the storage
class for utilizing the Ceph storage system), and how much you want to request (in this case, just 1 Gig), but you
don't need to know how the storage was implemented.

We create this pvc object with the usual ``kubectl apply`` command:

.. code-block:: bash

  $ kubectl apply -f pvc.yml
    persistentvolumeclaim/hello-jstubbs-data created

Great, with the pvc created, let's check back on our pods:

.. code-block:: bash

  $ kubectl get pods
    NAME                                    READY   STATUS        RESTARTS   AGE
    hello-deployment-9794b4889-mk6qw        1/1     Running       46         46h
    hello-deployment-9794b4889-sx6jc        1/1     Running       46         46h
    hello-deployment-9794b4889-v2mb9        1/1     Running       46         46h
    hello-deployment-9794b4889-vp6mp        1/1     Running       46         46h
    hello-pvc-deployment-ff5759b64-sc7dk    1/1     Running       0          45s

Like magic, our "hello-pvc-deployment" now has a running pod without us making any additional API calls to k8s!
This is the power of the declarative aspect of k8s. When we created the hello-pvc-deployment, we told k8s to always
keep one pod with the properties specified running at all times, if possible, and k8s continues to try and implement our
wishes until we instruct it to do otherwise.

Exec Commands in a Running Pod
------------------------------

Because the command running within the "hello-pvc-deployment" pod redirected the echo statement to a file, the
hello-pvc-deployment-ff5759b64-sc7dk will have no logs. (You can confirm this is the case for yourself using the ``logs``
command as an exercise).

In cases like these, it can be helpful to run additional commands in a running pod to explore what is going on.
In particular, it is often useful to run shell in the pod container.

In general, one can run a command in a pod using the following:

.. code-block:: bash

  $ kubectl exec <options> <pod_name> -- <command>

To run a shell, we will use:

.. code-block:: bash

  $ kubectl exec -it <pod_name> -- /bin/bash

The ``-it`` flags might look familiar from Docker -- they allow us to "attach" our standard input and output to the
command we run in the container. The command we want to run is ``/bin/bash`` for a shell.

Let's exec a shell in our "hello-pvc-deployment-ff5759b64-sc7dk" pod and look around:

.. code-block:: bash

  $ k exec -it  hello-pvc-deployment-5b7d9775cb-xspn7 -- /bin/bash
    root@hello-pvc-deployment-5b7d9775cb-xspn7:/#

Notice how the shell prompt changes after we issue the ``exec`` command -- we are now "inside" the container, and our
prompt has changed to "root@hello-pvc-deployment-5b7d9775cb-xspn" to indicate we are the root user within the container.

Let' issue some commands to look around:

.. code-block:: bash

  $ pwd
    /
    # cool, exec put us at the root of the container's file system

  $ ls -l
    total 8
    drwxr-xr-x   2 root root 4096 Jan 18 21:03 bin
    drwxr-xr-x   2 root root    6 Apr 24  2018 boot
    drwxr-xr-x   3 root root 4096 Mar  4 01:06 data
    drwxr-xr-x   5 root root  360 Mar  4 01:12 dev
    drwxr-xr-x   1 root root   66 Mar  4 01:12 etc
    drwxr-xr-x   2 root root    6 Apr 24  2018 home
    drwxr-xr-x   8 root root   96 May 23  2017 lib
    drwxr-xr-x   2 root root   34 Jan 18 21:03 lib64
    drwxr-xr-x   2 root root    6 Jan 18 21:02 media
    drwxr-xr-x   2 root root    6 Jan 18 21:02 mnt
    drwxr-xr-x   2 root root    6 Jan 18 21:02 opt
    dr-xr-xr-x 887 root root    0 Mar  4 01:12 proc
    drwx------   2 root root   37 Jan 18 21:03 root
    drwxr-xr-x   1 root root   21 Mar  4 01:12 run
    drwxr-xr-x   1 root root   21 Jan 21 03:38 sbin
    drwxr-xr-x   2 root root    6 Jan 18 21:02 srv
    dr-xr-xr-x  13 root root    0 May  5  2020 sys
    drwxrwxrwt   2 root root    6 Jan 18 21:03 tmp
    drwxr-xr-x   1 root root   18 Jan 18 21:02 usr
    drwxr-xr-x   1 root root   17 Jan 18 21:03 var
    # as expected, a vanilla linux file system.
    # we see the /data directory we mounted from the volume...

  $ ls -l data/out.txt
    -rw-r--r-- 1 root root 19 Mar  4 01:12 data/out.txt
    # and there is out.txt, as expected

  $ cat data/out.txt
    Hello, Kubernetes!
    # and our hello message!

  $ exit
    # we're ready to leave the pod container

.. note::
  To exit a pod from within a shell (i.e., ``/bin/bash``) type "exit" at the command prompt.

.. note::
  The ``exec`` command can only be used to execute commands in *running* pods.


Persistent Volumes Are... Persistent
------------------------------------

The point of persistent volumes is that they live beyond the length of one pod. Let's see this in action. Do the
following:

  1. Delete the "hello-pvc" pod. What command do you use?
  2. After the pod is deleted, list the pods again. What do you notice?
  3. What contents do you expect to find in the ``/data/out.txt`` file? Confirm your suspicions.


*Solution*.

.. code-block:: bash

  $ kubectl delete pods hello-pvc-deployment-5b7d9775cb-xspn7
    pod "hello-pvc-deployment-5b7d9775cb-xspn7" deleted

  $ kubectl get pods
    NAME                                    READY   STATUS              RESTARTS   AGE
    hello-deployment-9794b4889-mk6qw        1/1     Running             47         47h
    hello-deployment-9794b4889-sx6jc        1/1     Running             47         47h
    hello-deployment-9794b4889-v2mb9        1/1     Running             47         47h
    hello-deployment-9794b4889-vp6mp        1/1     Running             47         47h
    hello-pvc-deployment-5b7d9775cb-7nfhv   0/1     ContainerCreating   0          46s
    # wild -- a new hello-pvc-deployment pod is getting created automatically!

  # let's exec into the new pod and check it out!
  $ k exec -it hello-pvc-deployment-5b7d9775cb-7nfhv -- /bin/bash

  $ cat /data/out.txt
    Hello, Kubernetes!
    Hello, Kubernetes!




Additional Resources
--------------------

 * `Kubernetes Deployments Documentation <https://kubernetes.io/docs/concepts/workloads/controllers/deployment/>`_
 * `Persistent Volumes <https://kubernetes.io/docs/concepts/storage/persistent-volumes/>`_
 * `Ceph RDB Storage class in k8s <https://kubernetes.io/docs/concepts/storage/storage-classes/#ceph-rbd>`_
