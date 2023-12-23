import init
from mpi4py import MPI
import sys
from machine import Machine 


input_file = sys.argv[1]
output_file = sys.argv[2]

# get input from the file
filename = str(input_file)
# filename = "/Users/damlakayikci/Desktop/cmpe/okul/cmpe300/MPI-Project/src/input1.txt"
wear_outs = []
machine_count, production_cycle  = init.init(filename)

# Spawn the processes
args = ["work.py", str(filename)]
comm = MPI.COMM_SELF.Spawn(sys.executable, args=args, maxprocs=machine_count+1)

# open the output file
f = open(output_file, "w")

for p in range(production_cycle, 0, -1):
    for i in range(machine_count):
        # Check for wear out messages
        flag = comm.iprobe(source=MPI.ANY_SOURCE, tag=0) # TODO: check hepsini alıyor mu
        if flag:
            wear_out_msg = comm.recv(source=MPI.ANY_SOURCE, tag=0)
            msg = "{}-{}-{}".format(wear_out_msg[0], wear_out_msg[1], production_cycle - int(wear_out_msg[2]) + 1) # TODO: wear out message'da son elemana 1 ekledim ama neden bilmiyorum
            print(f"---CENTER:: Received EMERGENCY message {wear_out_msg}")
            wear_outs.append(msg)
        msg = comm.recv(source=MPI.ANY_SOURCE, tag=p) 
        if msg[0] == 1: # root machine
            print(f"---CENTER:: Received message  {msg}")
            f.write(msg[2] + "\n")
        # print(f"---CENTER:: Received message  {msg}")
        else:
            sender = msg[0]
            receiver = msg[1]
            string = msg[2]
        comm.send([sender,string], dest=receiver, tag=p)
        # print(f"---CENTER:: Sent message {msg} to {receiver} at production cycle {p}")

# Close the spawned processes
comm.Disconnect()

# Write wear out messages to the output file
for wear_out in wear_outs:
    f.write(wear_out + "\n")
f.close()
