import json
import multiprocessing
import threading
import time
import traceback

from run.exception.local_exceptions import NumberProcessException
from run.redis_connector import RedisPool


# rpop from redis given key as list name
# return rpop result
def single_start(key, pid, func):
    """
    read list-key from redis,
    pop list element,
    call function with popped element as param
    :param key: model name defined in tool and model
    :param pid: process id
    :param func: call model function
    """
    print('process start: 【' + str(pid) + '】')
    pool = RedisPool()
    conn = pool.connector()

    while True:
        val = conn.brpop(key)
        print(pid, val[1])

        # do ack
        # do persistance work

        try:
            val_json = json.loads(val[1])
            func(val_json)
            # do exception work
        except:
            traceback.print_exc()
            # record failed vals
            err_json = {"val": val[1], "timestamp": int(round(time.time() * 1000))}
            conn.lpush('failed_' + key, json.dumps(err_json))


def start(key: str, func, np: int = 5):
    """
    call np number of processes,
    do func work, func params read from redis
    :param key: model name defined in tool and model
    :param func: call model function
    :param np: number of processes, default 5
    """

    if np < 1:
        raise NumberProcessException(np)
        return

    for i in range(np):
        p = multiprocessing.Process(target=single_start, kwargs={"key": key, "pid": i, "func": func})
        p.start()

        time.sleep(0.5)
