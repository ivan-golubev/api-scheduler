README
------

Installation:
------------
1. install python 2.7

2. install requests:

> pip install requests


To launch the app, run this in bash console:

> chmod +x run.sh
> ./run.sh

Then you may access the server in your favourite browser:
http://localhost:5000/jobs

Testing
-------
To run tests execute in bash console:
> python test.py

REST API
--------

1. create job: POST /jobs, BODY: "30 10 /bin/daily", response:(job id): 2

2. get all jobs: GET /jobs

3. remove job: DELETE /jobs/<job_id>

4. get next expected runtime for jobs: GET /jobs?q="hh:mm"

This service just implements the API and is not suitable for production in itself.
To tune it for production usage follow the instructions at http://flask.pocoo.org/docs/0.11/deploying/#deployment