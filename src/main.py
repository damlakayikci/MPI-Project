import init
from mpi4py import MPI
import sys
from machine import Machine 

# get input from the file
filename = "/Users/damlakayikci/Desktop/cmpe/okul/cmpe300/MPI-Project/src/input1.txt"
leaves, threshold, machine_count = init.get_input(filename)

comm = MPI.COMM_SELF.Spawn(sys.executable, args=["work.py"], maxprocs=machine_count)

production_cycle = 10
for i in range(machine_count):
    msg = comm.recv(source=MPI.ANY_SOURCE, tag=production_cycle)
    print(f"---CENTER:: Received message  {msg}")
    sender = msg[0]
    receiver = msg[1]
    string = msg[2]
    comm.send([sender,string], dest=receiver-1, tag=production_cycle)

# Close the spawned processes
comm.Disconnect()
