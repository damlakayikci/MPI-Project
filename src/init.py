from machine import Machine

# initialize function to create the machines and return the threshold value for work.py
def get_input(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    # 1st line: Number of Machine.machines
    num_machines = int(lines[0])

    # 2nd line: Number of production cycles
    num_production_cycles = int(lines[1]) 

    Machine.machines[1] = Machine(1, ['add'], num_production_cycles, None) # initialize root machine

    # 3rd line: Wear factors for each operation
    wear_factor = lines[2].split(' ')
    operations = ['enhance', 'reverse', 'chop', 'trim', 'split']
    for i in range(5):
        Machine.wear_factors[operations[i]] = int(wear_factor[i])
   
    # 4th line: Threshold value for maintenance
    threshold = int(lines[3])

    leaves = [i+1 for i in range(num_machines)] # a list to keep the leaves
    parents_not_created = []  # a list to keep parents in case their children are created before them
    for i in range(num_machines - 1):
        # parse each line
        machine_info = lines[i+4].split(' ')
        child_id = int(machine_info[0])
        parent_id = int(machine_info[1])
        operation = machine_info[2].strip()

        # create machine object and add it to the dictionary
        Machine.machines[child_id] = Machine(child_id, operation, num_production_cycles, parent_id)
        
        # add the child to the parent's children list if parent is created already
        if Machine.machines[parent_id] != None:
            Machine.machines[parent_id].add_child(child_id)
        else: # else, add it to the list to add later
            parents_not_created.append((parent_id, child_id))
        if parent_id in leaves: # remove parent from the leaves list
            leaves.remove(parent_id)
    
    # add the children of the parents in the list to be added
    for parent_id, child_id in parents_not_created:
        Machine.machines[parent_id].add_child(child_id)
        
    # Other lines
    for i in range(len(leaves)):   
        product = lines[3 + num_machines + i].strip()
        Machine.machines[leaves[i]].add_product([0,product]) # add the product to the leaf machine's product list
        Machine.machines[leaves[i]].original_string = product

    return threshold

# initialize function to return the number of machines and the number of production cycles for main.py
def init(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    num_machines = int(lines[0])
    num_production_cycles = int(lines[1])
    return num_machines, num_production_cycles




