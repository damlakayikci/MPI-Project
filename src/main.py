import init
from mpi4py import MPI
import sys
from machine import Machine 

# get input from the file
filename = "/Users/damlakayikci/Desktop/cmpe/okul/cmpe300/MPI-Project/src/input2.txt"

production_cycle, threshold, machine_count = init.get_input(filename)

args = ["work.py", str(production_cycle), str(threshold), str(machine_count)]

comm = MPI.COMM_SELF.Spawn(sys.executable, args=args, maxprocs=machine_count)

for p in range(production_cycle, 0, -1):
    for i in range(machine_count):
        msg = comm.recv(source=MPI.ANY_SOURCE, tag=p)
        print(f"---CENTER:: Received message  {msg}")
        sender = msg[0]
        receiver = msg[1]
        string = msg[2]
        comm.send([sender,string], dest=receiver-1, tag=p)
        print(f"---CENTER:: Sent message {msg} to {receiver} at production cycle {p}")

# Close the spawned processes
comm.Disconnect()
