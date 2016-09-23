# -*- coding:utf -*-
from celery import Celery
from celery.utils.log import task_logger

from worker import celeryconfig

app = Celery()
app.config_from_object(celeryconfig)


@app.task(bind=True, acks_late=True)
def task1(self, url):
    task_logger.info(url)
    return url

if __name__ == '__main__':
    app.worker_main(['mytask2', '-lDEBUG', '-nworker.mytask2', '-E', '-Qfor_mytask2_task1'])
