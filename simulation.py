import numpy as np
import matplotlib.pyplot as plt

from pyomo.environ import *
from pyomo.opt import SolverFactory

from bandit import *
from allocation import LearnedBanditArray

class Simulation():

    def __init__(self, allocation, num_users, num_items, solver):
        self.allocation = allocation
        self.num_users = num_users
        self.num_items = num_items
        self.capacities = [1 for _ in range(num_items)]
        self.revenue = []
        self.acceptances = []
        self.dissatisfaction = []
        self.regret = []
        self.solver = solver
        self.random=False
        self.learned_bandit_array = LearnedBanditArray(self.num_users, self.num_items)

    def set_bandit_array(self, seed=0):
        self.bandit_array = BanditArray(self.num_users, self.num_items, seed=seed, random=self.random)

    def get_optimal(self):
        pass
        
    def run_simulation(self, iterations, seed=0):
        self.set_bandit_array(seed=seed)
        model = ConcreteModel()
        # self.allocation.model = model
        model.Users = range(self.num_users)
        model.Items = range(self.num_items)
        if self.allocation.name == 'walrasian':
            model.dual = Suffix(direction=Suffix.IMPORT)
            model.x = Var(model.Users, model.Items, bounds=(0.0,1.0))
        else:
            model.x = Var(model.Users, model.Items, within=Binary)
        model.obj = Objective(
            expr=sum(self.learned_bandit_array.get_bandit(u, i).high*model.x[u,i] for u in model.Users for i in model.Items), sense=maximize)
        model.item_capacity = ConstraintList()
        temp_item_iter = 0
        for i in model.Items:
            model.item_capacity.add(
                sum(model.x[u,i] for u in model.Users) <= self.capacities[temp_item_iter]
            )
            temp_item_iter += 1
        model.user_capacity = ConstraintList()
        for u in model.Users:
            model.user_capacity.add(
                sum(model.x[u,i] for i in model.Items) <= 1
            )
        for iter in range(iterations):
            model.obj.expr = sum(self.learned_bandit_array.get_bandit(u, i).high*model.x[u,i] for u in model.Users for i in model.Items)
            self.solver.solve(model)
            solved_allocation = [(u, i) for u in model.Users for i in model.Items if model.x[u,i].value > 0.5]
            result = self.allocation.allocate(self.bandit_array, self.learned_bandit_array, solved_allocation)
            self.revenue.append(result['revenue'])
        

        return self.revenue


    def run_n_simulations(self, iterations, n):
        seeds = list(range(n))
        for seed in seeds:
            self.run_simulation(iterations, seed)



