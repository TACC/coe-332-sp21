Final Project
=============

**Due Date: Friday, May 7th, by 11:00am CST**

The final project will consist of builing a REST API frontend to a time series database that allows for basic CRUD - Create, Read, Update, Delete - operations and
also allows users to submit analysis jobs. **At a minimum**, the system should support an analysis job to create a plot of the data; extra credit can be given if the system supports
additional types of analysis jobs, deploy over multiple systems, or has an innovative user interface. 

The project will also include two separate pieces of documentation: the first will provide **instructions for deploying the system** and the second should be **geared towards users/developers** who will interact with the system.

A.
--

Front-end API - A set of synchronous API endpoints providing the following functionality:
      * Data points retrieval endporints
      * Endpoint for creating new data points\
      * Jobs/graph submission and retrieval points
      * Submission of other kinds of analysis jobs - extra credit

B.
--

Back-end workers - Backend/worker processes to work the submitted jobs
      * Worker processes framework.
      * Analysis job itself (e.g., make a graph) 


C.
--

Use of Redis database and queue structures to link front-end and back-end processes. 
      * Note that if the API, Workers, and Redis server might run on a different servers, you'll need to provide a configuration description (or better yet a way of propagating config) 

D.
--

Github Repository
      * Repository/code organization - The code should be organized into modules and directories that make it easy to navigate as the project grows. An example repository layout is included at https://bitbucket.org/tacc-cic/coe332/src/master/archive/final_project_example/
      * Documentation
         * Deployment docs - instructions for how an operator should deploy the system.
         * Instructions for deploying to one VM
         * If you are going for extra credit, provide instructions for deploying to two (or more) VMs, with any necessary instructions for configuring IP addresses for databases, etc.
      * User docs - instructions for how to interact with your API. This should more or less be a (possibly updated version of) your HW 5, e.g., 
         * List of endpoints
         * Expected JSON responses
         * Examples of how to use your system from within curl and Python.

