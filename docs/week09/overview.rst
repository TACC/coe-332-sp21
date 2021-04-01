Week 9: Container Orchestration with Kubernetes
===============================================

In Week 9, we begin our study of container orchestration and the Kubernetes ("k8s") system. We have already built a
small HTTP application in the REST architecture using the flask framework. This HTTP application makes use of a database
to persist state. In the coming weeks, we will add more components to our application, and this is very typical of a
modern distributed system. As the number of components grows, the work required to deploy and maintain this system
increases. Container orchestration systems such as k8s aid us in this deployment and management effort by allowing us
to run our applications across a cluster of machines and use APIs to make changes to the application deployment over
time.

At the end of the next two weeks you will:

  * Understand container orchestration and the basic Kubernetes architecture.
  * Understand fundamental Kubernetes abstractions, including: ``pod``, ``deployment``, ``persistent volume``, and ``service``.
  * Write a basic script to deploy your flask application to a Kubernetes cluster in your own private namespace.

.. toctree::
   :maxdepth: 1

   docker_compose_services
   orchestration
   kubernetes_pod
