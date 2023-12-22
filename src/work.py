from machine import Machine
import init
from mpi4py import MPI
import sys

parent_comm = MPI.Comm.Get_parent()
rank = parent_comm.Get_rank()
_, filename = sys.argv
filename = str(filename)
num_production_cycles, threshold, num_machines= init.get_input(filename)
# Now you can use the rank to identify the worker
print(f"I am machine {rank+1}")

Machine.machines[rank+1].work(parent_comm, threshold)


parent_comm.Disconnect()

