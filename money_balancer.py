#!/usr/bin/python
# -*- coding: utf-8 -*-

from copy import deepcopy
from unittest import TestCase
from random import randint, random
import operator

__author__ = 'icoz'

""" Расчет кто по сколько скидывается.

        Задача: группа людей собирается на пати. У них есть коллективные расходы:
                они покупают еду, бухло, прочее. Все люди тратят деньги (или только часть людей).
                Необходимо определить кто по сколько должен скидываться.


        Вариант 0
        Общак.
        Все участники должны скидываются поровну, но в реальности каждый потратил разную сумму.
        Тот, кто должен, кладет деньги в общак.
        Тот, кому должны, берет деньги из общака.

        Вариант 1
        Персональный.
        Все участники должныскидываются поровну, но в реальности каждый потратил разную сумму
        В результате расчета имеем список, кто кому должен сколько денег ЛИЧНО.

        Вариант 2
        Общак. Исключения.
        Некоторые участники не употребляют определенные продукты (например алкоголь), т.е. они не скидываются
        на продукты, которые им не нужны.
        Каждый участник скидывается по разному, в зависимости от своих исключений.
        Включает в себя Вариант 0 (в случае отсутствия исключений).

        Пример:
            реальные затраты
            У1 - 100
            У2 - 150
            У3 - 50
            У4 - 0

            исключения
            У1 - 10 (У1 не пьет)
            У3 - 20 (У3 не ест)

        Вариант 3
        Персональный. Исключения.
"""


class MoneyBalancer(object):
    def __init__(self):
        # список участников и потраченых денег
        # {имя: сумма, }
        self.buddies = dict()
        # список стафа
        # {имя: сумма, }
        self.stuff = dict()
        # список исключений (участники и стаф, цена стафа берется из списка стафа)
        # {имя: имя_стафа, }
        self.exclusion = dict()

    # Поштучное добавление #

    def add_buddy(self, name, money):
        """Добавление участника и суммы, которую он реально потратил."""
        # TODO: в списке должны быть уникальные имена, если повторно добавить участника, то надо сложить его деньги
        self.buddies[name] = money

    def add_stuff(self, name, money):
        """Добавление названия стафа и суммы, которую на него потратили."""
        # TODO: в списке должны быть уникальные имена, если повторно добавить стаф, то надо сложить его стоимость
        self.stuff[name] = money

    def add_exclusion(self, name, stuff_name):
        """Добавление названия стафа и суммы, которую на него потратили."""
        # в списке могут быть неуникальные имена, т.к. у одного участника может быть несколько исключений
        self.stuff[name] = stuff_name

    # Массовое добавление #

    def add_buddies(self, buddies):
        """Добавление списка участников и реально потраченных ими сумм."""
        if not isinstance(buddies, dict):
            raise ValueError('buddies must be dict')
        for name in buddies:
            self.buddies[name] = buddies[name]

    def add_stuffs(self, stuff):
        """Добавление списка стафа и реально потраченных на них сумм."""
        if not isinstance(stuff, dict):
            raise ValueError('stuff must be dict')
        for name in stuff:
            self.stuff[name] = stuff[name]

    def add_exclusions(self, ex):
        """Добавление списка исключений - участники и стаф."""
        if not isinstance(ex, dict):
            raise ValueError('exclusions must be dict')
        for name in ex:
            self.exclusion[name] = ex[name]

    # Суммы #

    def get_avg_buddies(self):
        """Средняя сумма затрат по всем участникам."""
        return round(self.get_total_buddies() / len(self.buddies), 2)

    def get_total_buddies(self):
        """Полная сумма по всем участникам."""
        amount = 0.0
        for buddy in self.buddies:
            amount += self.buddies[buddy]
        return round(amount, 2)

    def get_total_stuff(self):
        """Полная сумма по всему стафу."""
        amount = 0.0
        for s in self.stuff:
            amount += self.stuff[s]
        return round(amount, 2)

    def get_total_exclusions(self):
        """Полная сумма по всем исключениям."""
        amount = 0.0
        for ex in self.exclusion:
            amount += self.exclusion[ex]
        return round(amount, 2)

    # Прочее #

    def get_buddies(self):
        """Получение списка участников."""
        return deepcopy(self.buddies)

    def clear(self):
        """Очистка."""
        self.buddies = dict()
        self.exclusion = dict()

    #  Методики расчета #

    def get_buddies_debts(self):
        """Расчет Варианта 1 по методу icoz'a """
        avg = self.get_avg_buddies()
        credit = list()
        debit = list()
        for b in self.buddies:
            diff = self.buddies[b] - avg
            if diff > 0:  # если кто-то должен этому чуваку
                debit.append((diff, b))
            elif diff < 0:  # если это чувак кому-то должен
                credit.append((diff, b))
            else:  # этот чувак чист - никому не должен, но никто и ему не должен
                pass
        # теперь оптимально распределим кто кому сколько должен отдать
        buddies_debts = dict()
        while True:
            credit.sort(key=lambda x: x[0])
            debit.sort(key=lambda x: x[0], reverse=True)
            lv, lu = credit.pop(0)
            hv, hu = debit.pop(0)
            val = hv + lv
            if buddies_debts.get(hu) is None:
                buddies_debts[hu] = dict()
            if buddies_debts.get(lu) is None:
                buddies_debts[lu] = dict()
            if val > 0:  # если этому чуваку кто-то еще должен
                debit.append((val, hu))
                buddies_debts[hu][lu] = -lv  # positive
                buddies_debts[lu][hu] = lv
            elif val < 0:  # если этот чувак еще кому-то должен
                credit.append((val, lu))
                buddies_debts[hu][lu] = hv  # positive
                buddies_debts[lu][hu] = -hv
            else:  # кредит с дебетом сошлись
                buddies_debts[hu][lu] = hv  # positive
                buddies_debts[lu][hu] = lv
            if len(credit) == 0 or len(debit) == 0:
                break
        del credit
        del debit
        return buddies_debts

    def get_zero_variant2(self):
        """"Расчет по методу "общак" без исключений. """
        # участники с положительной разницей берут из общака
        # участники с отрицательной разницей кладут в общак
        avg = self.get_avg_buddies()

        buddies_debts = list()
        # сортируем по именам
        for b in sorted(self.buddies.items(), key=operator.itemgetter(0)):
            buddies_debts.append((b[0], b[1] - avg))

        return buddies_debts

    def get_first_variant(self):
        """Расчет по методу "персональный"  без исключений. """
        avg = self.get_avg_buddies()

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
        debit.sort(key=lambda x: (x[0], x[1]), reverse=True)
        # они должны - сортировка по возрастанию (т.к. числа отрицательные)
        credit.sort(key=lambda x: (x[0], x[1]))

        print('Дебит - ' + debit.__str__())
        print('Кредит - ' + credit.__str__())
        print('Скидываемся по {0}'.format(avg))

        # разделим кто-кому и кому-кто
        debit_debts = dict()
        credit_debts = dict()

        # возвращаем долги
        while len(debit) > 0:
            dv, du = debit.pop(0)

            if debit_debts.get(du) is None:
                debit_debts[du] = dict()

            print('\nСобираем {0} денег для {1}'.format(dv, du))
            # собираем денег со всех должников
            while True:
                if len(credit) > 0:
                    cv, cu = credit.pop(0)

                    if credit_debts.get(cu) is None:
                        credit_debts[cu] = dict()

                    # смотрим сколько может нам вернуть должник
                    delta = round(dv + cv, 2)
                    print('{0} должен всего {1} денег'.format(cu, cv))
                    if delta > 0:  # чувак отдал все деньги, но дебет еще есть
                        # cu отдает du cv денег и отдыхает
                        print('{0} отдает {1} {2} денег'.format(cu, du, cv))
                        # кому - кто
                        debit_debts[du][cu] = -cv
                        # кто - кому
                        credit_debts[cu][du] = cv
                        # оставшийся дебет
                        dv = delta
                        print('Остается в дебете {0}'.format(dv))
                        pass
                    elif delta < 0:  # чувак покрыл дебет, но еще остался должен
                        # cu отдает du dv денег и попадает опять в список должников
                        credit.append((delta, cu))
                        print('{0} отдает {1} {2} денег и будет должен еще кому-нибудь {3}'.format(cu, du, dv, delta))
                        # кому - кто
                        debit_debts[du][cu] = dv
                        # кто - кому
                        credit_debts[cu][du] = -dv
                        break
                    else:  # дебет==кредит - они рассчитались друг с другом
                        # cu отдает du cv денег и они оба отдыхают
                        print('{0} отдает {1} {2} денег и все счастливы'.format(cu, du, cv))
                        # кому - кто
                        debit_debts[du][cu] = dv
                        # кто - кому
                        credit_debts[cu][du] = cv
                        break
                else:
                    print('Из-за ошибок округления в дебите осталось немного денег - {0}'.format(dv))
                    break

        del credit
        del debit

        return {'d': debit_debts,
                'c': credit_debts}

    def calculate_obshchak(self):
        """"Расчет по методу "общака" с исключениями или без."""
        assert len(self.buddies) > 1, 'Кол-во участников должно быть не меньше двух'

        print('Участники - {0} человек - '.format(len(self.buddies)) + self.buddies.__str__())
        print('Исключения - {0} человек - '.format(len(self.exclusion)) + self.exclusion.__str__())

        # среднее значение со всеми вычтенными исключениями
        # такое кол-во денег приходится на каждого участника
        avg_val_all = round((self.get_total_buddies() - self.get_total_exclusions()) / len(self.buddies), 2)

        # начальные персональные средние для всех участников
        avg_list = {name: avg_val_all for name in self.buddies}

        print('Среднее значение на всех (учитывая исключения) - {0}'.format(avg_val_all))
        print('Общие средние - {0}'.format(avg_list.__str__()))

        # цикл по всем исключениям
        for name_ex in self.exclusion:
            # среднее значение по текущему исключению
            # кол-во участников на 1 меньше, т.к. сумма исключения раскидывается на всех, кроме участника исключения
            avg_val_ex = round(self.exclusion[name_ex] / (len(self.buddies) - 1), 2)
            # добавить среднее от исключения всем, кроме участника исключения
            for name in avg_list:
                if name != name_ex:
                    avg_list[name] += avg_val_ex

        print('Персональные средние - {0}'.format(avg_list.__str__()))

        # считаем долги
        # из суммы каждого участника вычитаем его персональное среднее
        buddies_debts = dict()
        for name in self.buddies:
            buddies_debts[name] = self.buddies[name] - avg_list[name]

        del avg_list
        return buddies_debts

    def calculate_personal(self):
        """Расчет по методу "персональный"  с исключениями и без."""
        # первоначальный расчет по методу общака
        # имеем данные кто сколько должен отдать/получить
        obshchak = self.calculate_obshchak()
        print('Общак - {0}'.format(obshchak.__str__()))

        # но деньги крутятся не в общаке, а передаются p2p

        # положительные суммы
        # этим участникам должны денег
        # они получают
        debit = [(name, obshchak[name]) for name in obshchak if obshchak[name] > 0]
        # отрицательные суммы
        # эти участники должны денег
        # они отдают
        credit = [(name, obshchak[name]) for name in obshchak if obshchak[name] <= 0]

        # TODO: вопрос с сортировкой: цель - уменьшить кол-во передач денег из рук в руки
        # им должны - сортировка по убыванию
        debit.sort(key=lambda x: (x[0], x[1]), reverse=True)
        # они должны - сортировка по возрастанию (т.к. числа отрицательные)
        credit.sort(key=lambda x: (x[0], x[1]))

        print('Дебит - ' + debit.__str__())
        print('Кредит - ' + credit.__str__())

        # разделим кто-кому и кому-кто
        debit_debts = dict()
        credit_debts = dict()

        # возвращаем долги
        while len(debit) > 0:
            du, dv = debit.pop(0)

            if debit_debts.get(du) is None:
                debit_debts[du] = dict()

            print('\nСобираем {0} денег для {1}'.format(dv, du))
            # собираем денег со всех должников
            while True:
                if len(credit) > 0:
                    cu, cv = credit.pop(0)

                    if credit_debts.get(cu) is None:
                        credit_debts[cu] = dict()

                    # смотрим сколько может нам вернуть должник
                    delta = round(dv + cv, 2)
                    print('{0} должен всего {1} денег'.format(cu, cv))
                    if delta > 0:  # чувак отдал все деньги, но дебет еще есть
                        # cu отдает du cv денег и отдыхает
                        print('{0} отдает {1} {2} денег'.format(cu, du, cv))
                        # кому - кто
                        debit_debts[du][cu] = -cv
                        # кто - кому
                        credit_debts[cu][du] = cv
                        # оставшийся дебет
                        dv = delta
                        print('Остается в дебете {0}'.format(dv))
                        pass
                    elif delta < 0:  # чувак покрыл дебет, но еще остался должен
                        # cu отдает du dv денег и попадает опять в список должников
                        credit.append((cu, delta))
                        print('{0} отдает {1} {2} денег и будет должен еще кому-нибудь {3}'.format(cu, du, dv, delta))
                        # кому - кто
                        debit_debts[du][cu] = dv
                        # кто - кому
                        credit_debts[cu][du] = -dv
                        break
                    else:  # дебет==кредит - они рассчитались друг с другом
                        # cu отдает du cv денег и они оба отдыхают
                        print('{0} отдает {1} {2} денег и все счастливы'.format(cu, du, cv))
                        # кому - кто
                        debit_debts[du][cu] = dv
                        # кто - кому
                        credit_debts[cu][du] = cv
                        break
                else:
                    print('Из-за ошибок округления в дебите осталось немного денег - {0}'.format(dv))
                    break

        del credit
        del debit

        return {'d': debit_debts,
                'c': credit_debts}


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
        ret = self.money.get_avg_buddies()
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

    def test_obshchak(self):
        self.money.clear()
        # участники
        buddies = {
            'user1': 100,
            'user2': 100,
            'user3': 150,
            'user4': 50,
            'user5': 200
        }
        # исключения (user1 не пьет =()
        ex = {
            'user1': 50
        }

        self.money.add_buddies(buddies)
        self.money.add_exclusions(ex)

        res = self.money.calculate_obshchak()
        print(res)

    def test_personal(self):
        self.money.clear()
        # участники
        buddies = {
            'user1': 100,
            'user2': 100,
            'user3': 150,
            'user4': 50,
            'user5': 200
        }
        # исключения (user1 не пьет =()
        ex = {
            'user1': 50
        }

        self.money.add_buddies(buddies)
        self.money.add_exclusions(ex)

        res = self.money.calculate_personal()
        print(res)