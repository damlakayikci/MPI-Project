import init
from mpi4py import MPI
import sys
from machine import Machine 

# Get input and output file names from the command line
input_file = sys.argv[1]
output_file = sys.argv[2]

# initialize variables
filename = str(input_file)
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
            msg = "{}-{}-{}".format(wear_out_msg[0], wear_out_msg[1], production_cycle - int(wear_out_msg[2]) + 1)
            # print(f"---CENTER:: Received EMERGENCY message {wear_out_msg}") #TODO: remove this
            wear_outs.append(msg)

        msg = comm.recv(source=MPI.ANY_SOURCE, tag=p)  # receive message from any source on production cycle p
        if msg[0] == 1: # root machine should send the final product to the center
            print(f"---CENTER:: Received message  {msg}") # TODO: remove this
            f.write(msg[2] + "\n") 
        else: # other machines should send the message to their parents, parse the message and send to parent
            sender = msg[0]     # child id
            receiver = msg[1]   # parent id
            string = msg[2]     # product
        comm.send([sender,string], dest=receiver, tag=p)

# Disconnect the processes
comm.Disconnect()

# Write wear out messages to the output file
for wear_out in wear_outs:
    f.write(wear_out + "\n")
f.close()
