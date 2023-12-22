from machine import Machine
import init
from mpi4py import MPI
from time import sleep

parent_comm = MPI.Comm.Get_parent()
rank = parent_comm.Get_rank()
filename = "/Users/damlakayikci/Desktop/cmpe/okul/cmpe300/MPI-Project/src/input1.txt"
init.get_input(filename)
# Now you can use the rank to identify the worker
print(f"I am machine {rank+1}")

Machine.machines[rank+1].work(parent_comm)


parent_comm.Disconnect()

