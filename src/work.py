from machine import Machine
import init
from mpi4py import MPI
import sys

parent_comm = MPI.Comm.Get_parent()
rank = parent_comm.Get_rank()

_, filename = sys.argv
filename = str(filename)
num_production_cycles, threshold, num_machines= init.get_input(filename)

print(f"I am machine {rank+1}")
if rank != 0:
    Machine.machines[rank].work(parent_comm, threshold)


parent_comm.Disconnect()

