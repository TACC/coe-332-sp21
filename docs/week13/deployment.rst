Deployment Environment
======================

Our deployment environment for this API will be the class Kuberentes cluster. It
could just as easily be AWS, or Azure, or Google Cloud, or another Kuberenets
cluster. Remember if you containerize everything, it becomes extremely portable.
In contrast to our development environment, the Kubernetes deployment is meant
to be long-lasting, always available, and consumable by the public. We will have
`test` and `prod` deployments, so that new changes can be seen by developers in
the `test` deployment environment (sometimes also called "staging") before
finally making their way to the `prod` (production) deployment environment.


File Organization
-----------------

To support the deployment environment, our file organization grows to the
following:

.. code-block:: text

    pssp-api/
    ├── data
    │   ├── dump.rdb
    │   └── redis.conf
    ├── docker
    │   ├── docker-compose.yml
    │   ├── Dockerfile.api
    │   ├── Dockerfile.db
    │   └── Dockerfile.wrk
    ├── kubernetes
    │   ├── prod
    │   │   ├── api-deployment.yml
    │   │   ├── api-service.yml
    │   │   ├── db-deployment.yml
    │   │   ├── db-pvc.yml
    │   │   ├── db-service.yml
    │   │   └── wrk-deployment.yml
    │   └── test
    │       ├── api-deployment.yml
    │       ├── api-service.yml
    │       ├── db-deployment.yml
    │       ├── db-pvc.yml
    │       ├── db-service.yml
    │       └── wrk-deployment.yml
    ├── Makefile
    ├── README.md
    └── src
        ├── flask_api.py
        └── worker.py

Here you will find 12 new yaml files with somwhat descriptive names. Six are
organized into a 'test' directory, and six are organized into a 'prod' directory.

These yaml files closely follow the naming convention and content we have seen
in previous lectures.

Testing
-------

The purpose of this testing / staging environment is to see the entire API
exactly as it appears in production before actually putting new code changes
into production.

Generally the process to get code into testing follows these steps:

1. Develop / test code in the development environment (ISP) as described in the
   previous module
2. Push code to GitHub and tag it with an appropriate version number (avoid
   using "latest")
3. Push images to Docker Hub - Kubernetes needs to pull from here. Make sure the
   Docker image tag matches the GitHub tag so you always know what exact version
   of code is running.
4. Edit the appropriate testing deployment(s) with the new tags and apply the
   changes. Pods running within a deployment under the old tag number should be
   automatically terminated.

The yaml files above can be applied one by one, or the entire directory at a time
like the following:

.. code-block:: console

   [isp02]$ kubectl apply -f kubernetes/test/

Kuberenets will apply all the files found in the test folder. Be careful, however,
about the order in which things are applied. For example, the Redis DB deployment
needs the PVC to exist in order to deploy successfully. But, Kubernetes is usually
pretty smart about this kind of thing, so it should keep retrying all deployments,
services, and pvcs until everything is happy and connected.


Once deployed, you should rigorously test all services using the python debug pod
and, if applicable, the NodePort Service connection to the outside world. We will
see more on automating integration tests later in this unit.


Production
----------

If everything with the test / staging deployment looks good and passes tests,
follow the same steps for your production environment. Kubernetes is fast at
stopping / starting containers, and the services should provide pretty seemless
access to the underlying API. If larger-scale changes are needed and significant
downtime is anticipated, it would be a good idea to post an outage notice to
users.
