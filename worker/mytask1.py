# -*- coding:utf -*-
import json

import requests
from celery import Celery
from celery.utils.log import task_logger

from worker import celeryconfig
import requests
app = Celery()
app.config_from_object(celeryconfig)


def back_off(retries):
    return 2 ** retries


@app.task(bind=True, acks_late=True)
def task1(self, url):
    task_logger.info(url)
    try:
        res = requests.get(url,timeout=5)
        assert res.status_code==200
        task_logger.debug(res.text)
        pass
    except Exception as e:
        raise self.retry(countdown=back_off(self.max_retries),max_retries=5)
    return url

@app.task(bind=True)
def ticket_task(self,datetime,from_station='SHH',to_station='GIW'):
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

                url = 'http://192.168.2.14:9002/weixin/message/send'
                data = dict(
                user='A363977771',
                content={"content": body},
                appid=5
                )
                res = requests.post(url,json=data)

                return res.text if res else 'error'


if __name__ == '__main__':
    app.worker_main(['mytask1', '-lDEBUG', '-nworker.mytask1', '-E', '-Qfor_mytask1_task1'])
