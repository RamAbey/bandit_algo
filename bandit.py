import numpy as np

class Bandit():

    def __init__(self, user, item, mu):
        self.user = user
        self.item = item
        self.mu = mu

    def set_mu(self, mu):
        self.mu = mu
        return self.mu

    def get_mu(self):
        return self.mu

    def pull_arm(self, price_offered):
        return 0 if self.mu <= price_offered else 1



class RandomBandit(Bandit):

    def __init__(self, user, item, mu, var):
        self.user = user
        self.item = item
        self.mu = mu
        self.var = var

    def set_var(self, var):
        self.var = var
        return self.var

    def get_var(self):
        return self.var

    def pull_arm(self, price_offered):
        return 0 if self.mu <= price_offered else 1



class BanditArray():

    def __init__(self, num_users, num_items, seed=0, random=False):
        self.bandit_arr = []
        for i in range(num_users):
            curr_row = []
            for j in range(num_items):
                if random:
                    curr_row.append( RandomBandit(user=i, item=j, mu=np.random.uniform(0.0, 1.0)) )
                else:
                    curr_row.append( Bandit(user=i, item=j, mu=np.random.uniform(0.0, 1.0)) )
            self.bandit_arr.append(curr_row)



class LearnedBandit():

    def __init__(self, user, item):
        self.user = user
        self.item = item
        self.high = 1.0
        self.low = 0.0
        self.dual = 0.5
        self.use_walrasian = False

    def signal(self, signal, price):
        """
        Modify high/low or alpha/beta based on response of bandit(user,item).get_price()
        """
        if signal < 0.5:
            self.low = max(self.low, price)
        else:
            self.high = min(self.high, price)



class LearnedBanditArray():

    def __init__(self, num_users, num_items):
        self.bandit_arr = []
        for i in range(num_users):
            curr_row = []
            for j in range(num_items):
                curr_row.append( LearnedBandit(user=i, item=j) )
            self.bandit_arr.append(curr_row)

    def get_bandit(self, user, item):
        return self.bandit_arr[user][item]