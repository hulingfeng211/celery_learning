# -*- coding:utf-8 -*-


from tornado.gen import IOLoop, coroutine,Task
from tornado.web import RequestHandler, Application,asynchronous
from tornado.options import options, parse_command_line, define
import os

import tcelery
from worker.mytask1 import task1



# print os.environ['http_proxy']
# print os.environ['https_proxy']
# print os.environ['HTTP_PROXY']
# print os.environ['HTTPS_PROXY']


class IndexHandler(RequestHandler):

    #@asynchronous
    #@coroutine
    #@asynchronous
    @coroutine
    def get(self, *args, **kwargs):
        result = yield  Task(task1.apply_async,args=['http://www.baidu.com'], exchange='for_mytask1_task1',
                                           routing_key='for_mytask1_task1')
        #result = task1.apply_async(args=['http://www.baidu.com'], exchange='for_mytask1_task1',routing_key='for_mytask1_task1')
        #task1.apply_async(args=['http://www.baidu.com'], exchange='for_mytask1_task1',routing_key='for_mytask1_task1')
        print str(result.result)


if __name__ == '__main__':
    parse_command_line()
    settings = {'DEBUG': True}
    app = Application(handlers=[(r'/', IndexHandler)], **settings)
    app.listen(3333)
    tcelery.setup_nonblocking_producer()
    IOLoop.current().start()

    """import pika

    connection = pika.BlockingConnection(pika.URLParameters(
        'amqp://dev:dev!23$5@192.168.2.16:5672/test'))
    channel = connection.channel()
    channel.queue_declare(queue='for_mytask1_task1',durable=1)
    channel.basic_publish(exchange='for_mytask1_task1',
                          routing_key='for_mytask1_task1',
                          body='http://www.baidu.com')
    print(" [x] Sent 'Hello World!'")
    connection.close()"""
