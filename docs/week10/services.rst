Services
========

Services are the k8s resource one uses to expose APIs to other k8s pods and, ultimately, to the outside world. To
understand services we need to first discuss how k8s networking works.

k8s networking
--------------
k8s creates internal networks and attaches pod containers to them to facilitate communication between pods. For a number
of reasons, including security, these networks are not reachable from outside k8s.

.. note::

  We will be covering just the basics of k8s networking, enough for you to becomes proficient with the main concepts
  involved in deploying your application. Many details and advanced concepts will be omitted.

k8s assigns every pod an IP address on this private network. Pods that are on the same network can communicate with other
pods using their IP address.



Services
--------

