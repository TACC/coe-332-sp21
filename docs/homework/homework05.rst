Homework 05
===========

**Due Date: Thursday, April 8, by 11:00am CST**

A.
--

Recall the following example pod from class:

.. code-block:: yaml

    ---
    apiVersion: v1
    kind: Pod
    metadata:
      name: hello
    spec:
      containers:
        - name: hello
          image: ubuntu:18.04
          command: ['sh', '-c', 'echo "Hello, Kubernetes!" && sleep 3600']

Modify the above to create a pod in Kubernetes to print a message "Hello, $NAME", where ``$NAME`` is an environment
variable. Give this pod a label, ``greeting: personalized``.

  1. Include the yaml file used and the command issued to create the pod.
  2. Issue a command to get the pod using an appropriate ``selector``. Copy and paste the command used and the output.
  3. Check the logs of the pod. What is the output? Is that what you expected?
  4. Delete the pod. What command did you use?


B.
--

Our first pod above was a little sad because no value was specifed for our ``$NAME`` variable. Let's fix that here!
Let's update our pod definition to include a value for the variable, ``$NAME``. We can add any number of environment
variables and values using the ``env`` stanza inside the ``containers`` spec, like so:

.. code-block:: yaml

  ---

  # some stuff here...

  spec:
    containers:
      - name: # stuff...
        image: # stuff...
        env:
          - name: "VAR_1"
            value: "VALUE_1"
          - name: "VAR_2"
            value: "VALUE_2"
          . . .

Give the variable ``$NAME`` the value of your own name.

  1. Include the yaml file used and the command issued to create the pod.
  2. Check the logs of the pod. What is the output? Copy and paste the command used and the output.
  3. Delete the pod. What command did you use?

C.
--

This time, let's create a deployment with the above properties, instead of a pod. We'll also add the pod's IP address
to the message. Create a deployment that uses the ``ubuntu:18.04`` image and prints the personalized message,
"Hello, $NAME from IP <pod_ip_address>", where ``$NAME`` is an environment variable. To add the pod's IP address to the
message, we will inject another environment variable, but this time we will have k8s populate the value for us.

We can use the Kubernetes Downward API to expose pod information to itself via environment variables. Instead of using
the ``value`` field, we use ``valueFrom`` with a ``fieldRef`` stanza that specifies a ``fieldPath`` property. The value
of the ``fieldPath`` property should be a reference to the k8s property of interest.

From the k8s documentation, the following information is available through environment variables (see the
`docs <https://kubernetes.io/docs/tasks/inject-data-application/downward-api-volume-expose-pod-information/#the-downward-api>`_
for more details):

  * ``status.podIP`` - the pod's IP address
  * ``spec.serviceAccountName`` - the pod's service account name, available since v1.4.0-alpha.3
  * ``spec.nodeName`` - the node's name, available since v1.4.0-alpha.3
  * ``status.hostIP`` - the node's IP, available since v1.7.0-alpha.1

Thus, for example, the following code snippet included in the ``env`` section would create an environment variable,
``$POD_IP``, with value equal to the pod's IP address (as assigned by k8s).

.. code-block:: yaml

  env:
    - name: POD_IP
      valueFrom:
        fieldRef:
          fieldPath: status.podIP

Include the following in your submission:

  1. Include the yaml file used to create a deployment with 3 replica pods, and include the command issued to create the
     deployment.
  2. First, use kubectl to get all the pods in the deployment and their IP address. Copy and paste the command used and the
     output.
  3. Now, check the logs associated with each pod in the deployment. Does it match what you got in 2? Copy and paste the
     commands and the output.

