# -*- coding:utf-8 -*-
import unittest
from unittest import TestCase
from worker.mytask1 import task1,ticket_task


class MyTask1TestCase(TestCase):
    def test_task1(self):
        task1.apply_async(args=['http://169.24.1.100'],exchange='for_mytask1_task1',routing_key='for_mytask1_task1')

    def test_ticket_task(self):
        ticket_task.apply_async(args=['a','b','c'], exchange='for_mytask1_task1', routing_key='for_mytask1_task1')


if __name__ == '__main__':
    unittest.main()