from allocation import *
from simulation import Simulation
from pyomo.opt import SolverFactory


if __name__ == "__main__":
    allocation_name = str(input("Select Allocation: [midpoint / gradlower / walrasian]? "))
    if allocation_name == "midpoint":
        allocation = MidPoint()
    elif allocation_name == "gradlower":
        allocation = GradLower()
    elif allocation_name == "walrasian":
        walrasian_allocation_name = str(input("Select Allocation: [walrasian / toleratedw / syncedw / clippedw / smoothedw]? "))
        if walrasian_allocation_name == 'walrasian':
            allocation = Walrasian()
        elif walrasian_allocation_name == "toleratedw":
            allocation = ToleratedWalrasian()
        elif walrasian_allocation_name == "syncedw":
            allocation = SyncedWalrasian()
        elif walrasian_allocation_name == "clippedw":
            allocation = ClippedWalrasian()
        elif walrasian_allocation_name == "smoothedw":
            allocation = SmoothedWalrasian()
        else:
            raise Exception(walrasian_allocation_name + " allocation not implemented")
    else:
        raise Exception(allocation_name + " allocation not implemented.")
    iterations = int(input("Iterations? "))
    num_users = int(input("Num Users? "))
    num_items = int(input("Num Items? "))
    simulation = Simulation(allocation, num_users, num_items, solver=SolverFactory('glpk'))
    revenue = simulation.run_simulation(iterations)
    print("True Optimal: ", simulation.get_optimal())
    print("Max Achieved: ", max(revenue))