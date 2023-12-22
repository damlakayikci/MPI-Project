import init
from mpi4py import MPI
import sys
from machine import Machine 

# get input from the file
filename = "/Users/damlakayikci/Desktop/cmpe/okul/cmpe300/MPI-Project/src/input1.txt"
wear_outs = []
machine_count, production_cycle  = init.init(filename)

args = ["work.py", str(filename)]

comm = MPI.COMM_SELF.Spawn(sys.executable, args=args, maxprocs=machine_count)

for p in range(production_cycle, 0, -1):
    for i in range(machine_count):
        # Check for wear out messages
        flag = comm.iprobe(source=MPI.ANY_SOURCE, tag=0)
        if flag:
            wear_out_msg = comm.recv(source=MPI.ANY_SOURCE, tag=0)
            msg = "{}-{}-{}".format(wear_out_msg[0], wear_out_msg[1], production_cycle - int(wear_out_msg[2]))
            print(f"---CENTER:: Received EMERGENCY message {wear_out_msg}")
            wear_outs.append(msg)
        msg = comm.recv(source=MPI.ANY_SOURCE, tag=p)
        print(f"---CENTER:: Received message  {msg}")
        sender = msg[0]
        receiver = msg[1]
        string = msg[2]
        comm.send([sender,string], dest=receiver-1, tag=p)
        print(f"---CENTER:: Sent message {msg} to {receiver} at production cycle {p}")

# Close the spawned processes
comm.Disconnect()
