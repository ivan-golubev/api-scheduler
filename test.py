import requests
import json

host = 'http://localhost:5000'
jobs_url = host + '/jobs'
jobs_del_url = jobs_url + '/{}'
jobs_query_url = jobs_url + '?q={}'
stop_server_url = host + '/shutdown'


def main():
    test_job_creation_removal()
    get_next_extime_daily_job()
    get_next_extime_hourly_job()
    get_next_extime_minute_job()
    get_next_extime_sixty_times_job()


def test_job_creation_removal():
    print("Testing job creation...")
    # create a couple of jobs
    job_id1 = requests.post(jobs_url, data="30 10 /bin/daily").text
    job_id2 = requests.post(jobs_url, data="24 * /bin/sixtyTimes").text
    jobs = json.loads(requests.get(jobs_url).text)
    assert job_id1 in jobs
    assert job_id2 in jobs
    print("Testing job creation... SUCCESS")

    print("Testing job removal...")
    # delete one of them
    requests.delete(jobs_del_url.format(job_id1))
    jobs = json.loads(requests.get(jobs_url).text)
    assert job_id1 not in jobs
    assert job_id2 in jobs
    print("Testing job removal... SUCCESS")
    # clear up
    requests.delete(jobs_url)


def get_next_extime_daily_job():
    print("Getting next exec time for a daily job with specified hour and minute")
    requests.post(jobs_url, data="30 10 /bin/daily")
    # should return a job for today
    jobs = json.loads(requests.get(jobs_query_url.format('10:15')).text)
    job_time, job_day, _ = jobs[0].split()
    assert job_time == '10:30' and job_day == 'today'

    # should return a job for tomorrow
    jobs = json.loads(requests.get(jobs_query_url.format('10:35')).text)
    job_time, job_day, _ = jobs[0].split()
    assert job_time == '10:30' and job_day == 'tomorrow'
    # clear up
    requests.delete(jobs_url)


def get_next_extime_hourly_job():
    print("Getting next exec time for an hourly job with specified minute")
    requests.post(jobs_url, data="45 * /bin/hourly")
    # should return a job for this hour
    jobs = json.loads(requests.get(jobs_query_url.format('10:15')).text)
    job_time, job_day, _ = jobs[0].split()
    assert job_time == '10:45' and job_day == 'today'

    # should return a job for the next hour
    jobs = json.loads(requests.get(jobs_query_url.format('10:50')).text)
    job_time, job_day, _ = jobs[0].split()
    assert job_time == '11:45' and job_day == 'today'
    # clear up
    requests.delete(jobs_url)


def get_next_extime_minute_job():
    print("Getting next exec time for an every minute job")
    requests.post(jobs_url, data="* * /bin/everyMinute")
    # should return a job to be executed the next minute
    jobs = json.loads(requests.get(jobs_query_url.format('5:45')).text)
    job_time, job_day, _ = jobs[0].split()
    assert job_time == '05:46' and job_day == 'today'
    # should return a job to be executed the next minute tomorrow
    jobs = json.loads(requests.get(jobs_query_url.format('23:59')).text)
    job_time, job_day, _ = jobs[0].split()
    assert job_time == '00:00' and job_day == 'tomorrow'
    # clear up
    requests.delete(jobs_url)


def get_next_extime_sixty_times_job():
    print("Getting next exec time for a job with sixty times execution")
    requests.post(jobs_url, data="* 21 /bin/sixtyTimes")
    # should return the job to be executed the next minute today
    jobs = json.loads(requests.get(jobs_query_url.format('21:05')).text)
    job_time, job_day, _ = jobs[0].split()
    assert job_time == '21:06' and job_day == 'today'

    # should return the job to be executed at 21:00 today
    jobs = json.loads(requests.get(jobs_query_url.format('03:22')).text)
    job_time, job_day, _ = jobs[0].split()
    assert job_time == '21:00' and job_day == 'today'

    # should return the job to be executed at 21:00 tomorrow
    jobs = json.loads(requests.get(jobs_query_url.format('22:00')).text)
    job_time, job_day, _ = jobs[0].split()
    assert job_time == '21:00' and job_day == 'tomorrow'

    # should return the job to be executed at 21:00 tomorrow
    jobs = json.loads(requests.get(jobs_query_url.format('21:59')).text)
    job_time, job_day, _ = jobs[0].split()
    assert job_time == '21:00' and job_day == 'tomorrow'
    # clear up
    requests.delete(jobs_url)

if __name__ == "__main__":
    main()
