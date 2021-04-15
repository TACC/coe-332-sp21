Homework 07
===========

**Due Date: Tuesday, April 27, by 11:00am CST**

This homework assignment builds on the exercises done in class in the
`Messaging Systems <https://coe-332-sp21.readthedocs.io/en/main/week11/messaging.html#private-vs-public-objects>`_
section as well as the Week 12 material for deploying a worker to k8s.
At the end of those exercises, we ended up with three files, ``api.py``, ``worker.py`` and ``jobs.py``.

A.
--

In the first in-class exercise from Week 12, you updated the Dockerfile for your flask application to include the
new source code files in your Docker image and to include an entrypoint and a command that could be used for running
both the flask web server and the worker.

  1. Complete this exercise if needed and include the Dockerfile in your
     homework submission. Update the code to use the IP address of your test Redis service. Be sure to build the
     Docker image and push it to the Docker Hub.

  2. With your new image on Docker Hub, create a deployment for the flask API and a separate deployment for the worker.
     (Creating a worker deployment was the second exercise from Week 12.) Name the files
     ``<username>-hw7-flask-deployment.yml`` and ``<username>-hw7-worker-deployment.yml`` and
     include them and the commands you used to create the deployments with your homework submission.

  3. Verify that your flask API and worker are working properly: in your python debug container, create some jobs by
     making a POST request with ``curl`` to your flask API. Confirm
     that the jobs go to "complete" status by checking the Redis database in a Python shell. Include the following with
     your submission:

     a. The curl statements used and the responses (output) returned by your flask APi (these should include job id's).
     b. The Python statements (code) you issued to check the status of the jobs and the output from the statements.

B.
--

1. Update the worker deployment you wrote in A.2) to pass the worker's IP address in as an environment variable, ``WORKER_IP``.
   Recall that we learned how to do this in hw 5 using the following snippet:

.. code-block:: yaml

    env:
      - name: WORKER_IP
        valueFrom:
          fieldRef:
            fieldPath: status.podIP

Include the updated deployment file with your homework submission.


2. In the ``worker.py`` file we did in class, the ``execute_job`` function looked like this:

.. code-block:: python

    def execute_job(jid):
        jobs.update_job_status(jid, 'in progress')
        time.sleep(15)
        jobs.update_job_status(jid, 'complete')

Update ``jobs.py`` and/or ``worker.py`` so that when the job status is updated to ``in progress``, the
worker's IP address is saved as new key in the job record saved in Redis. The key can be called ``worker`` and its value
should be the worker's IP address as a string. Think through the best way to add this functionality in terms of the changes made to
``jobs.py`` and/or ``worker.py``.

C.
--

Scale your worker deployment to 2 pods. In a python shell from within your python debug container, create 10 more jobs
by making POST requests using curl to your flask API. Verify that the jobs go to "complete" status by checking the
Redis database in a Python shell. Also, note which worker worked each job. Include the following with your submission:

     a. The curl statements used and the responses (output) returned by your flask APi (these should include job id's).
     b. The Python statement (code) you issued to check the status of the job and the output from the statement.
     c. How many jobs were worked by each worker?
