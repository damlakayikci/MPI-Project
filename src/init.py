from machine import Machine

# global variables
# num_machines: int
# num_production_cycles: int
# threshold: int
# wear_factors: dict
# machines: list[Machine]

filename = "/Users/damlakayikci/Desktop/MPI-Project/src/input.txt"


# initialize root machine
root: Machine = Machine(1, ['add'])
machines = [root]

def get_input(filename):
    global machines
    with open(filename, 'r') as file:
        lines = file.readlines()

    # 1st line: Number of machines
    num_machines = int(lines[0])
    # 2nd line: Number of production cycles
    num_production_cycles = int(lines[1]) 
    # 3rd line: Wear factors for each operation
    wear_factor = lines[2].split(' ')
    operations = ['enhance', 'reverse', 'chop', 'trim', 'split']
    wear_factors = {}
    for i in range(5):
        wear_factors[operations[i]] = int(wear_factor[i])

   
    # 4th line: Threshold value for maintenance
    threshold = int(lines[3])

    leaves = []
    for i in range(num_machines ):
        leaves.append(i+1)
    for i in range(num_machines - 1):
        machine_info = lines[i+4].split(' ')
        child = int(machine_info[0])
        parent = int(machine_info[1])
        operations = machine_info[2:]
        machines.append(Machine(child, operations, parent))
        if parent in leaves:
            leaves.remove(parent)
    
    # Other lines
    for i in range(len(leaves)):   
        product = lines[3 + num_machines + i].strip()
        machines[leaves[i] - 1].add_product(product)

    return  machines, leaves



# read input from input.txt

machines, leaves = get_input(filename)

print(machines)
print(leaves)

# You can now use these variables to initialize your MPI processes
