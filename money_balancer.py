from copy import deepcopy
from unittest import TestCase

__author__ = 'icoz'


class MoneyBalancer(object):
    def __init__(self):
        self.buddies = dict()

    def add_buddy(self, name, money):
        self.buddies[name] = money

    def get_avg(self):
        sum = 0.0
        for buddy in self.buddies:
            sum += self.buddies[buddy]
        return sum / len(self.buddies)

    def get_buddies(self):
        return deepcopy(self.buddies)


class TestMoneyBalancer(TestCase):
    def setUp(self):
        self.money = MoneyBalancer()
        pass

    def test_add_buddy(self):
        self.money.add_buddy('user1', 0)
        self.money.add_buddy('user2', 100)
        self.money.add_buddy('user3', 43)
        self.money.add_buddy('user4', 0)
        self.money.add_buddy('user5', 12)
        pass

    def test_get_buddies(self):
        ret = self.money.get_buddies()
        val = {
            'user1': 0,
            'user2': 100,
            'user3': 43,
            'user4': 0,
            'user5': 12
        }
        self.assertDictEqual(val, ret)


    def test_get_avg(self):
        ret = self.money.get_avg()
        self.assertEqual(31, ret)