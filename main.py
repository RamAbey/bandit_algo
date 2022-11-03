import bandit, simulation
from allocation import MidPoint, GradLower, Walrasian
from simulation import Simulation
from pyomo.opt import SolverFactory
import matplotlib.pyplot as plt


if __name__ == "__main__":
    allocation_name = str(input("Select Allocation: [midpoint / gradlower / walrasian]? "))
    iterations = int(input("Iterations? "))
    num_users = int(input("Num Users? "))
    num_items = int(input("Num Items? "))
    if allocation_name == "midpoint":
        allocation = MidPoint()
    elif allocation_name == "gradlower":
        allocation = GradLower()
    elif allocation_name == "walrasian":
        allocation = Walrasian()
    else:
        raise Exception("Allocation not implemented.")
    simulation = Simulation(allocation, num_users, num_items, solver=SolverFactory('glpk'))
    revenue = simulation.run_simulation(iterations)
    print("True Optimal: ", simulation.get_optimal())
    print("Max Achieved: ", max(revenue))