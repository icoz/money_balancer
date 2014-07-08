from copy import deepcopy
from unittest import TestCase
from random import randint, random

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
        return round(sum / len(self.buddies), 2)

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

    def get_buddies_debts2(self):
        avg = self.get_avg()
        credit = list()
        debit = list()
        for b in self.buddies:
            diff = round(self.buddies[b] - avg, 2)
            if diff > 0:  # если кто-то должен этому чуваку
                debit.append((diff, b))
            elif diff < 0:  # если это чувак кому-то должен
                credit.append((diff, b))
            else:  # этот чувак чист - никому не должен, но никто и ему не должен
                pass
        # им должны - сортировка по убыванию
        debit.sort(key=lambda x: x[0], reverse=True)
        # они должны - сортировка по возрастанию (т.к. числа отрицательные)
        credit.sort(key=lambda x: x[0])

        print('Дебит - ' + debit.__str__())
        print('Кредит - ' + credit.__str__())
        print('Скидываемся по {0}'.format(avg))

        # итоговый список
        buddies_debts = dict()
        # возвращаем долги
        while len(debit) > 0:
            dv, du = debit.pop(0)

            if buddies_debts.get(du) is None:
                buddies_debts[du] = dict()

            print('\nСобираем {0} денег для {1}'.format(dv, du))
            # собираем денег со всех должников
            while True:
                if len(credit) > 0:
                    cv, cu = credit.pop(0)

                    if buddies_debts.get(cu) is None:
                        buddies_debts[cu] = dict()

                    # смотрим сколько может нам вернуть должник
                    delta = round(dv + cv, 2)
                    print('{0} должен всего {1} денег'.format(cu, cv))
                    if delta > 0:  # чувак отдал все деньги, но дебет еще есть
                        # cu отдает du cv денег и отдыхает
                        print('{0} отдает {1} {2} денег'.format(cu, du, cv))
                        # кому - кто
                        buddies_debts[du][cu] = -cv
                        # кто - кому
                        buddies_debts[cu][du] = cv
                        # оставшийся дебет
                        dv = delta
                        print('Остается в дебете {0}'.format(dv))
                        pass
                    elif delta < 0:  # чувак покрыл дебет, но еще остался должен
                        # cu отдает du dv денег и попадает опять в список должников
                        credit.append((delta, cu))
                        print('{0} отдает {1} {2} денег и будет должен еще кому-нибудь {3}'.format(cu, du, dv, delta))
                        # кому - кто
                        buddies_debts[du][cu] = dv
                        # кто - кому
                        buddies_debts[cu][du] = -dv
                        break
                    else:  # дебет==кредит - они рассчитались друг с другом
                        # cu отдает du cv денег и они оба отдыхают
                        print('{0} отдает {1} {2} денег и все счастливы'.format(cu, du, cv))
                        # кому - кто
                        buddies_debts[du][cu] = dv
                        # кто - кому
                        buddies_debts[cu][du] = cv
                        break
                else:
                    print('Из-за ошибок округления в дебите осталось немного денег - {0}'.format(dv))
                    break

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

    def test_get_buddies_debts2(self):
        self.money.clear()
        buddies = {'user1': 34.76, 'user4': 745.36, 'user2': 286.32, 'user0': 723.32, 'user5': 775.38,
                   'user3': 643.0, 'user6': 399.61, 'user7': 284.18}
        self.money.add_buddies(buddies)
        res = self.money.get_buddies_debts()
        print(res)

    def test_get_buddies_debts3(self):
        """Генерируем случайные списки пользователей и денег."""
        self.money.clear()
        buddies = dict()

        for i in range(randint(5, 20)):
            u = 'user{0}'.format(i)
            m = round(random() * 1000, 2)
            buddies[u] = m

        print('Пати на {0} человек - '.format(len(buddies)) + buddies.__str__())
        self.money.add_buddies(buddies)
        res = self.money.get_buddies_debts2()
        print(res)