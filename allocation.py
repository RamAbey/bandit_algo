import numpy as np

from pyomo.environ import *
from pyomo.opt import SolverFactory

class Allocation:

    def __init__(self):
        self.model=None

    def allocate():
        pass

    def get_price():
        pass

    def pull_arm(price_offered):
        pass

class LearnedBandit():

    def __init__(self, user, item):
        self.user = user
        self.item = item
        self.high = 1.0
        self.low = 0.0
        self.dual = 0.5
        self.use_walrasian = False

    def process_signal(self, signal, price):
        if signal < 0.5:
            self.low = max(self.low, price)
        else:
            self.high = min(self.high, price)

class LearnedBanditArray():

    def __init__(self, num_users, num_items):
        self.learned_bandit_arr = []
        for i in range(num_users):
            curr_row = []
            for j in range(num_items):
                curr_row.append( LearnedBandit(user=i, item=j) )
            self.learned_bandit_arr.append(curr_row)

    def get_bandit(self, user, item):
        return self.learned_bandit_arr[user][item]


class MidPoint(Allocation):

    name = 'midpoint'

    def get_price(self, learned_bandit):
        return (learned_bandit.high + learned_bandit.low)/2 - 1e-10

    def allocate(self, bandit_arr, learned_bandit_arr, allocation):
        revenue, acceptances = 0, 0
        for (user, item) in allocation:
            curr_bandit = learned_bandit_arr.get_bandit(user, item)
            price = self.get_price(curr_bandit)
            signal = bandit_arr.get_bandit(user, item).pull_arm(price)
            curr_bandit.process_signal(signal, price + 1e-9)
            revenue += signal*price
            acceptances += signal
        return {'revenue': revenue, 
                'acceptances': acceptances}


"""
class GradLower(Allocation):


class Walrasian(Allocation):


class SyncedWalrasian(Walrasian):


class ToleratedWalrasian(Walrasian):


class ClippedWalrasian(Walrasian):


class SmoothedWalrasian(Walrasian):
"""

