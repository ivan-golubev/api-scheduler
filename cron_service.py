# /usr/bin/python

from pprint import pformat
from job import Job
import json


class CronService():
    def __init__(self):
        self.job_ctr = 1
        self.jobs = {}

    def get_jobs(self, query):
        if not query:
            print("returning all jobs:\n{}\n".format(pformat(self.jobs)))
            return json.dumps( {k: str(v) for k, v in self.jobs.items()} )
        else:
            h, m = CronService.parse_query(query)
            result = [j.get_next_execution(h, m) for j in self.jobs.values()]
            return json.dumps(result)

    @staticmethod
    def parse_query(query):
        try:
            return map(int, query.split(':'))
        except ValueError:
                raise Exception('Invalid input command format')

    def create_job(self, data):
        job_id = self.job_ctr
        self.job_ctr += 1
        self.jobs[job_id] = Job(data)
        print("CREATED: /jobs/{}\n".format(job_id))
        return str(job_id)

    def delete_job(self, job_id):
        del self.jobs[job_id]
        return "DELETED: /jobs/{}\n".format(job_id)

    def delete_all_jobs(self):
        self.jobs = {}
        result = "DELETED all jobs"
        print(result)
        return result