from rq import Queue
from rq.job import Job
from worker import conn
from config import bot, token
import telebot


q = Queue(name="some_queue", connection=conn)


def add_to_queue(task, *args):
    # Enqueue the job
    job = q.enqueue(task, *args)
    return job


def get_job_status(job_id):
    job = Job.fetch(job_id, connection=conn)
    status = {
        "queued": job.is_queued,
        "finished": job.is_finished,
        "started": job.is_started,
        "failed": job.is_failed,
    }
    return status


def report_success(job, connection, result, *args, **kwargs):
    print('the report success message')
    try:
        userid = result['userid']
        answer = result['newuser']

        # bot = telebot.TeleBot(
        #     token,
        #     threaded=True
        # )
        bot.send_message(userid, text=answer)
    except:
        print('Failed to send message to user')
    return True

def report_failure(job, connection, type, value, traceback):
    print('the report failed message')
    pass