# -*- coding:utf-8 -*-
import unittest
from unittest import TestCase
from worker.mytask2 import task1


class MyTask2TestCase(TestCase):
    def test_task1(self):
        #task1.apply_async(['http://www.baidu2.com'])
        task1.apply_async(['http://www.baidu.com'], exchange='for_mytask2_task1', routing_key='for_mytask2_task1')


if __name__ == '__main__':
    unittest.main()