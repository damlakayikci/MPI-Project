from machine import Machine
import init
from mpi4py import MPI
import sys

parent_comm = MPI.Comm.Get_parent()                                 # get the parent communicator
rank = parent_comm.Get_rank()                                       # get the rank of the current machine

_, filename = sys.argv                                              # get the filename from the maim process
threshold = init.get_input(str(filename))                     # initialize the machines and get the threshold value

if rank != 0:                                                       # if not the center
    Machine.machines[rank].work(parent_comm, threshold)             # call work function for the current machine

parent_comm.Disconnect()
