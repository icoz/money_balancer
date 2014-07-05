from copy import deepcopy
from unittest import TestCase

__author__ = 'icoz'


class MoneyBalancer(object):
    def __init__(self):
        self.buddies = dict()

    def add_buddy(self, name, money):
        self.buddies[name] = money

    def add_buddies(self, buddies):
        if not isinstance(buddies, dict):
            raise ValueError('buddies must be dict')
        for name in buddies:
            self.buddies[name] = buddies[name]

    def get_avg(self):
        sum = 0.0
        for buddy in self.buddies:
            sum += self.buddies[buddy]
        return sum / len(self.buddies)

    def get_buddies(self):
        return deepcopy(self.buddies)

    def get_buddies_debts(self):
        avg = self.get_avg()
        self.credit = list()
        self.debit = list()
        for b in self.buddies:
            diff = self.buddies[b] - avg
            if diff > 0:  # если кто-то должен этому чуваку
                self.debit.append((diff, b))
            elif diff < 0:  # если это чувак кому-то должен
                self.credit.append((diff, b))
            else:  # этот чувак чист - никому не должен, но никто и ему не должен
                pass
        # теперь оптимально распределим кто кому сколько должен отдать
        buddies_debts = dict()
        while True:
            self.credit.sort(key=lambda x: x[0])
            self.debit.sort(key=lambda x: x[0], reverse=True)
            lv, lu = self.credit.pop(0)
            hv, hu = self.debit.pop(0)
            val = hv + lv
            if buddies_debts.get(hu) is None:
                buddies_debts[hu] = dict()
            if buddies_debts.get(lu) is None:
                buddies_debts[lu] = dict()
            if val > 0:  # если этому чуваку кто-то еще должен
                self.debit.append((val, hu))
                buddies_debts[hu][lu] = -lv  # positive
                buddies_debts[lu][hu] = lv
            elif val < 0:  # если этот чувак еще кому-то должен
                self.credit.append((val, lu))
                buddies_debts[hu][lu] = hv  # positive
                buddies_debts[lu][hu] = -hv
            else:  # кредит с дебетом сошлись
                buddies_debts[hu][lu] = hv  # positive
                buddies_debts[lu][hu] = lv
            if len(self.credit) == 0 or len(self.debit) == 0:
                break
        del self.credit
        del self.debit
        return buddies_debts

    def clear(self):
        self.buddies = dict()


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
        self.money.clear()
        val = {
            'user1': 0,
            'user2': 100,
            'user3': 43,
            'user4': 0,
            'user5': 12
        }
        self.money.add_buddies(val)
        ret = self.money.get_buddies()
        self.assertDictEqual(val, ret)

    def test_get_avg(self):
        self.test_add_buddy()
        ret = self.money.get_avg()
        self.assertEqual(31, ret)

    def test_get_buddies_debts(self):
        self.money.clear()
        buddies = {
            'user1': 0,
            'user2': 100,
            'user3': 43,
            'user4': 0,
            'user5': 12
        }
        self.money.add_buddies(buddies)
        ret = self.money.get_buddies_debts()
        val = {
            'user1': {'user2': -31.0},
            'user2': {'user1': 31.0, 'user4': 31.0, 'user5': 7.0},
            'user3': {'user5': 12.0},
            'user4': {'user2': -31.0},
            'user5': {'user2': -7.0, 'user3': -12.0}
        }
        self.assertDictEqual(ret, val)