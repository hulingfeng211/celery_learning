# 项目目录
     celery_learning
    ├── REAME.md
    ├── test #单元测试模块
    │   ├── __init__.py
    │   ├── mytask1_test.py
    │   └── mytask2_test.py
    └── worker #工作模块
        ├── celeryconfig.py
        ├── celeryconfig.pyc
        ├── __init__.py
        ├── __init__.pyc
        ├── mytask1.py
        ├── mytask1.pyc
        ├── mytask2.py
        └── mytask2.pyc

# 为每个任务制定特定的队列
## 启动 flower 监控端

    celery flower --basic_auth=user1:pwd1,user2:pwd2 --broker='amqp://user:pwd@192.168.2.16:5672/test'
    -l DEBUG --broker_api='http://user:pwd@192.168.2.16:15672/api/'

## 启动celery worker

     celery worker --config=worker.celeryconfig  -Q for_mytask1_task1 -l DEBUG -n worker.mytask1

     celery worker --config=worker.celeryconfig  -Q for_mytask2_task1 -l DEBUG -n worker.mytask2

     #如果需要在一个机器上启动多个worker的话，通过-n参数指定新的节点名



     -Q:制定队列的名称如果有多个可以使用逗号(,)隔开
     -n:worker节点的名称
**启动后**

    george@worker:~/PycharmProjects/celery_learning$ celery worker --config=worker.celeryconfig  -Q for_mytask1_task1  -n worker.mytask1 -l info

     -------------- celery@worker.mytask1 v3.1.23 (Cipater)
    ---- **** -----
    --- * ***  * -- Linux-4.4.0-36-generic-x86_64-with-Ubuntu-16.04-xenial
    -- * - **** ---
    - ** ---------- [config]
    - ** ---------- .> app:         default:0x7f01e847ee10 (.default.Loader)
    - ** ---------- .> transport:   amqp://dev:**@192.168.2.16:5672/test
    - ** ---------- .> results:     disabled://
    - *** --- * --- .> concurrency: 4 (prefork)
    -- ******* ----
    --- ***** ----- [queues]
     -------------- .> for_mytask1_task1 exchange=for_mytask1_task1(direct) key=for_mytask1_task1


    [tasks]
      . worker.mytask1.task1
      . worker.mytask2.task1

    [2016-09-19 13:20:07,786: INFO/MainProcess] Connected to amqp://dev:**@192.168.2.16:5672/test
    [2016-09-19 13:20:07,804: INFO/MainProcess] mingle: searching for neighbors
    [2016-09-19 13:20:08,833: INFO/MainProcess] mingle: all alone
    [2016-09-19 13:20:08,873: WARNING/MainProcess] celery@worker.mytask1 ready.
    [2016-09-19 13:20:08,947: INFO/MainProcess] Events of group {task} enabled by remote.
    [2016-09-19 13:20:20,996: INFO/MainProcess] Received task: worker.mytask1.task1[af870ddf-6f28-490f-b6b2-fe532249ff0c]
    [2016-09-19 13:20:20,998: INFO/Worker-4] worker.mytask1.task1[af870ddf-6f28-490f-b6b2-fe532249ff0c]: http://www.baidu.com
    [2016-09-19 13:20:20,999: INFO/MainProcess] Task worker.mytask1.task1[af870ddf-6f28-490f-b6b2-fe532249ff0c] succeeded in 0.00126096399617s: u'http://www.baidu.com'
    [2016-09-19 13:20:34,354: INFO/MainProcess] Received task: worker.mytask1.task1[0ab0b196-5ee3-4de9-b493-292405d528b9]
    [2016-09-19 13:20:34,356: INFO/Worker-2] worker.mytask1.task1[0ab0b196-5ee3-4de9-b493-292405d528b9]: http://www.baidu.com
    [2016-09-19 13:20:34,356: INFO/MainProcess] Task worker.mytask1.task1[0ab0b196-5ee3-4de9-b493-292405d528b9] succeeded in 0.000635882999632s: u'http://www.baidu.com'

 ## 使用案例
 ## 案例一 每个任务使用单独的队列

 ## 案例二 定时执行任务
 >定时任务就是按照执行计划去执行特定的任务
 >执行定时任务可以选择在配置文件(`celeryconfig.py`)中配置定时任务的相关信息

    CELERYBEAT_SCHEDULE = {
    'add-every-30-seconds': {
        'task': 'worker.mytask1.ticket_task', #指定定时任务
        'schedule': timedelta(seconds=30),#指定定时策略
        'args': ('a','b','c'), #任务的参数
        'options':dict(exchange='default',routing_key='default') # 选项参数与apply_async一致 选项参数与apply_async一致,指定exchange和routing_key表示任务会定时发送到default交换机上然后再通过routing_key路由到对应的队列上，本case中会被路由到default.
        },
    }
 完整的配置内容如下:

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

 在启动worker的时候添加-B选项，定时执行任务

    celery worker --config=worker.celeryconfig   -l DEBUG -n worker.mytask1 -B

 样列代码:

    @app.task(bind=True)
      def ticket_task(self,datetime,from_station='SHH',to_station='GIW'):
      """
      到12306网站上查询上海到贵阳的K739车次的票务情况，如果存在卧铺则发送微信消息通知
      """
      url = 'https://kyfw.12306.cn/otn/lcxxcx/query?purpose_codes=ADULT&queryDate=2016-09-28&from_station=SHH&to_station=GIW'
      res = requests.get(url,verify=False)
      if res and res.status_code == 200:
          result = json.loads(res.text)
          k739_train = filter(lambda x:x.get('station_train_code')=="K739",result.get('data').get('datas'))
          if k739_train:
              train_info = k739_train[0]
              yw_num = train_info.get('yw_num')
              canwebby = train_info.get('canWebBuy')
              yz_num = train_info.get('yz_num')
              body = u"""
              硬卧:%s
              可购买:%s
              硬座数量:%s
              """%(yw_num,canwebby,yz_num)
              task_logger.info(body)
              if yw_num !=u'无':
                  url = 'http://localhost/weixin/message/send'
                  data = dict(
                  user='A363977771',
                  content={"content": body},
                  appid=5
                  )
                  res = requests.post(url,json=data)
                  return res.text if res else 'error'
 定时任务的执行情况

     [2016-09-23 11:06:12,834: INFO/Beat] Scheduler: Sending due task add-every-30-seconds (worker.mytask1.ticket_task)
     [2016-09-23 11:06:12,835: DEBUG/Beat] worker.mytask1.ticket_task sent. id->9d0d8880-5895-4de3-946d-ca4b3efac713##
     [2016-09-23 11:06:12,835: DEBUG/Beat] beat: Waking up in 29.99 seconds.
     [2016-09-23 11:06:12,838: INFO/MainProcess] Received task: worker.mytask1.ticket_task[9d0d8880-5895-4de3-946d-ca4b3efac713]
     [2016-09-23 11:06:12,838: DEBUG/MainProcess] TaskPool: Apply <function _fast_trace_task at 0x7fecd20b9050> (args:(u'worker.mytask1.ticket_task', u'9d0d8880-5895-4de3-946d-ca4b3efac713', [u'a', u'b', u'c'], {}, {u'utc': True, u'is_eager': False, u'chord': None, u'group': None, u'args': [u'a', u'b', u'c'], u'retries': 0, u'delivery_info': {u'priority': 0, u'redelivered': False, u'routing_key': u'default', u'exchange': u'default'}, u'expires': None, u'hostname': 'celery@worker.mytask1', u'task': u'worker.mytask1.ticket_task', u'callbacks': None, u'correlation_id': u'9d0d8880-5895-4de3-946d-ca4b3efac713', u'errbacks': None, u'timelimit': [None, None], u'taskset': None, u'kwargs': {}, u'eta': None, u'reply_to': u'2be4ff2e-904a-3d6d-bc49-6e6cad45ab5a', u'id': u'9d0d8880-5895-4de3-946d-ca4b3efac713', u'headers': {}}) kwargs:{})
     [2016-09-23 11:07:12,881: INFO/Worker-4] Starting new HTTPS connection (1): kyfw.12306.cn
     [2016-09-23 11:07:12,916: WARNING/Worker-4] /usr/local/lib/python2.7/dist-packages/requests/packages/urllib3/connectionpool.py:821: InsecureRequestWarning: Unverified HTTPS request is being made. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.org/en/latest/security.html
      InsecureRequestWarning)
     [2016-09-23 11:07:12,975: DEBUG/Worker-4] "GET /otn/lcxxcx/query?purpose_codes=ADULT&queryDate=2016-09-28&from_station=SHH&to_station=GIW HTTP/1.1" 200 None
     [2016-09-23 11:07:12,977: INFO/Worker-4] worker.mytask1.ticket_task[c4d43a06-ce70-4558-b402-7c2c5d0bc4c1]:
                硬卧:无
                可购买:Y
                硬座数量:298
     [2016-09-23 11:07:12,979: INFO/MainProcess] Task worker.mytask1.ticket_task[c4d43a06-ce70-4558-b402-7c2c5d0bc4c1] succeeded in 0.0983848370015s: None

