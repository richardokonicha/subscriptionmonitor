import os

import redis
from rq import Worker, Queue, Connection

listen = ['some_queue', 'default']

redis_url = os.getenv('REDISTOGO_URL', 'redis://default:redispw@localhost:55000/4')

conn = redis.from_url(redis_url, db=4)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work(with_scheduler=True)
