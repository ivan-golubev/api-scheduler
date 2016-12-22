# /usr/bin/python

from flask import Flask
from flask import request
from cron_service import CronService
from multiprocessing import Process

app = Flask(__name__)

cron_service = CronService()


@app.route("/jobs", methods=['GET', 'POST', 'DELETE'])
def jobs():
    if request.method == 'GET':
        return cron_service.get_jobs(request.args.get('q', ''))
    elif request.method == 'POST':
        return cron_service.create_job(request.data)
    else:
        return cron_service.delete_all_jobs()


@app.route("/jobs/<int:job_id>", methods=['DELETE'])
def delete_job(job_id):
    return cron_service.delete_job(job_id)


@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


def start_server():
    app.run()

if __name__ == "__main__":
    start_server()