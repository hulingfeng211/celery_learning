# -*- coding:utf-8 -*-
from datetime import timedelta
from kombu import Queue,Exchange

BROKER_URL="amqp://dev:dev12345@192.168.2.16:5672/test"
CELERY_IMPORTS = ('worker.mytask1', 'worker.mytask2','celery.task.http')
CELERY_ENABLE_UTC  = True
CELERY_TIMEZONE = 'Asia/Shanghai'

CELERY_ACCEPT_CONTENT = ['json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'

#CELERY_RESULT_BACKEND = 'amqp:'
CELERY_RESULT_BACKEND = 'redis://192.168.2.14:6379/8'

CELERY_QUEUES = (
    Queue('default',Exchange('default'),routing_key='default'),
    Queue('for_mytask1_task1',Exchange('for_mytask1_task1'),routing_key='for_mytask1_task1'),
    Queue('for_mytask2_task1',Exchange('for_mytask2_task1'),routing_key='for_mytask2_task1'),
)

CELERy_ROUTES = {
    'worker.mytask1.task1':{'queue':'for_mytask1_task1','routing_key':'for_mytask1_task1'},
    'worker.mytask2.task1':{'queue':'for_mytask2_task1','routing_key':'for_mytask2_task1'},
    'worker.mytask2.ticket_task':{'queue':'default','routing_key':'default'}
}

CELERYBEAT_SCHEDULE = {
    'add-every-30-seconds': {
        'task': 'worker.mytask1.ticket_task',
        'schedule': timedelta(seconds=30),
        'args': ('a','b','c'),
        'options':dict(exchange='default',routing_key='default')
    },
}