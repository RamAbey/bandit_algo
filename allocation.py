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

class MidPoint(Allocation):

    name = 'midpoint'

    def get_price(self, learned_bandit):
        return (learned_bandit.high + learned_bandit.low) // 2

    def allocate(self, bandit_arr, learned_bandit_arr, allocation):
        revenue, acceptances = 0, 0
        for (user, item) in allocation:
            curr_bandit = learned_bandit_arr.get_bandit(user, item)
            price = self.get_price(learned_bandit_arr, user, item)
            signal = bandit_arr.get_bandit(user, item).pull_arm(price)
            curr_bandit.process_signal(signal, price)
            revenue += signal*price
            acceptances += signal
            return {'revenue': revenue} #, acceptances


"""
class GradLower(Allocation):


class Walrasian(Allocation):


class SyncedWalrasian(Walrasian):


class ToleratedWalrasian(Walrasian):


class ClippedWalrasian(Walrasian):


class SmoothedWalrasian(Walrasian):
"""

