import numpy as np

from pyomo.environ import *
from pyomo.opt import SolverFactory

class Allocation:

    def __init__(self):
        pass

    def allocate(self, bandit_arr, learned_bandit_arr, allocation):
        revenue, acceptances = 0, 0
        for (user, item) in allocation:
            curr_bandit = learned_bandit_arr.get_bandit(user, item)
            price = self.get_price(curr_bandit)
            signal = bandit_arr.get_bandit(user, item).pull_arm(price)
            curr_bandit.process_signal(signal, price)
            revenue += signal*price
            acceptances += signal
        return {'revenue': revenue, 
                'acceptances': acceptances}

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
        if signal > 0.5:
            self.low = max(self.low, price)
        else:
            self.high = min(self.high, price)

    def get_spread(self):
        return self.high - self.low
    
    def set_use_walrasian(self):
        self.use_walrasian = True
    
    def get_use_walrasian(self):
        return self.use_walrasian

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

class GradLower(Allocation):

    name = 'gradlower'

    def get_price(self, learned_bandit):
        if learned_bandit.get_spread() < 1e-5:
            return learned_bandit.low
        return (learned_bandit.high + learned_bandit.low)/2


class Walrasian(Allocation):

    name = 'walrasian'

    def get_price(self, learned_bandit):
        if learned_bandit.get_spread() < 1e-5:
            return learned_bandit.dual
        return (learned_bandit.high + learned_bandit.low)/2


class SyncedWalrasian(Walrasian):

    name = 'syncedw'

    def __init__(self):
        self.walrasian_switch = False

    def get_price(self, learned_bandit, walrasian_switch):
        if walrasian_switch:
            return learned_bandit.dual
        return (learned_bandit.high + learned_bandit.low)/2

    def allocate(self, bandit_arr, learned_bandit_arr, allocation):
        revenue, acceptances = 0, 0
        if not self.walrasian_switch:
            walrasian_switch = True
            for (user, item) in allocation:
                curr_bandit = learned_bandit_arr.get_bandit(user, item)
                if curr_bandit.get_spread() < 1e-5:
                    curr_bandit.set_use_walrasian()
                if not curr_bandit.get_use_walrasian():
                    walrasian_switch = False
            if walrasian_switch:
                self.warlasian_switch = True
        for (user, item) in allocation:
            curr_bandit = learned_bandit_arr.get_bandit(user, item)
            price = self.get_price(curr_bandit, walrasian_switch)
            signal = bandit_arr.get_bandit(user, item).pull_arm(price)
            curr_bandit.process_signal(signal, price)
            revenue += signal*price
            acceptances += signal
        return {'revenue': revenue, 
                'acceptances': acceptances}


class ToleratedWalrasian(Walrasian):

    name = 'toleratedw'

    def get_price(self, learned_bandit):
        if learned_bandit.get_spread() < 1e-5:
            pass
        return (learned_bandit.high + learned_bandit.low)/2

class ClippedWalrasian(Walrasian):

    name = 'clippedw'

    def get_price(self, learned_bandit):
        if learned_bandit.get_spread() < 1e-5:
            pass
        return (learned_bandit.high + learned_bandit.low)/2

class SmoothedWalrasian(Walrasian):

    name = 'smoothedw'

    def get_price(self, learned_bandit):
        if learned_bandit.get_spread() < 1e-5:
            pass
        return (learned_bandit.high + learned_bandit.low)/2
