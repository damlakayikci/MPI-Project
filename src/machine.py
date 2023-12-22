from mpi4py import MPI

class Machine:
   
    # 0 index for even ids, 1 index for odd ids
    operations: list[list[str]] = [['enhance', 'split', 'chop'],['trim', 'reverse' ]] 
    # initialize wear factors to 0
    wear_factors: dict = { 'enhance': 0, 'split': 0, 'chop': 0, 'trim': 0, 'reverse': 0 }

    machines: dict = {} # dictionary to keep the machines
    
    # define constructor
    def __init__(self, id: int , operation: str, production_cycle: int, parent_id: int = None) -> None:
        self.id: int = id
        operations = Machine.operations[id%2].copy() 
        for op in operations:
            if op == operation:
                self.operation: str = operation # operation to be performed
                operations.remove(op)
                self.next_operations: list[str] = operations # add the other operations to the list
                break
        self.products: list[str] = []
        self.wear: int = 0
        self.parent_id: int = parent_id
        self.children: list[int] = []
        self.production_cycle: int = production_cycle
        
    def add_child(self, child_id: int) -> None:
        self.children.append(child_id)

    def add_product(self, product: str) -> None:
        self.products.append(product)


#  ---------------------- OPERATIONS ---------------------- #
            
    def add(self) -> str:
        # Sort the list based on the first element of each sublist
        self.products.sort(key=lambda x: x[0])

        # Remove the first element from each sublist and create a new list
        self.products = [item[1] for item in self.products]


        return ''.join(map(str, self.products))

    # duplicate the first and the last letter of the product
    def enhance(self, string: str) -> str:
        return string[0] + string + string[-1]

    # reverse the product
    def reverse(self, string: str) -> str:
        return string[::-1]

    # remove the last letter from the product
    def chop(self, string: str) -> str:
        if len(string) == 1:
            return string
        return string[:-1]

    # remove the first and the last letters from the product
    def trim(self, string: str) -> str:
        if len(string) <= 2:
            return string
        return string[1:-1]

    # split the product into two parts, and discards the right part. 
    def split(self, string: str) -> str:
        if len(string) % 2 == 0:                 # if the length of the string is even, split from the middle
            return string[:len(string)//2]
        else:                                    # else, split from the middle + 1
            return string[:len(string)//2 + 1]
        
    #  ---------------------- OPERATIONS ---------------------- #
        
    def work(self, comm, threshold) -> None:

        if self.production_cycle == 0:                    # if production cycle is over, return
            return
        
        if self.children != []:                           # if machine has children, wait for them to finish
            for child_id in self.children:
                recv = comm.recv(source=0, tag=self.production_cycle)
                # print("\n-RECEIVED:: Machine {} received message from {} at production cycle {}\n".format(self.id, child_id, self.production_cycle))
                self.products.append([recv[0], recv[1]])                # add the product to the machine's product list
                
        string = self.add()                               # add products in machine's product list
        if self.id == 1:                                  # if machine is root, print the product
            # print("\n-ROOT:: Machine {}'s product is {} at production cycle {}\n".format(self.id, string, self.production_cycle))
            comm.send([self.id, 1,string], dest=0, tag=self.production_cycle) # TODO: 1 yerine ne yazacagimi bilmiyorum
        else:
            operation = getattr(self, self.operation)         # get the operation to be performed
            self.wear += Machine.wear_factors[self.operation] # add wear factor
            string = operation(string)                        # perform the operation

            # print("Machine {} performed {} operation on {} and wear factor is {} at production cycle {}".format(self.id, self.operation, string, self.wear, self.production_cycle))

            if self.wear >= threshold:                        # if wear factor is greater than threshold, send the product to the parent
                wear_factor = Machine.wear_factors[self.operation]
                cost =(self.wear - threshold+1) * wear_factor
                message = [self.id, cost, self.production_cycle]
                comm.isend(message, dest=0, tag=0)
                self.wear = 0                                 # reset the wear factor
            
            self.operation = self.next_operations[0]          # set the next operation as current operation
            self.next_operations.remove(self.operation)       # remove the operation from the list
            self.next_operations.append(self.operation)       # add the operation to the end of the list

            comm.send([self.id,self.parent_id, string], dest=0, tag=self.production_cycle)
            # print("\n-SENT:: Machine {} sent message to {} at production cycle {}\n".format(self.id, self.parent_id, self.production_cycle))
            
        self.production_cycle -= 1
        if self.children != []:                          # if machine has children, empty its product list
            self.products = []
        else: # TODO: dogru mu bilmiyorum
            self.products = []
            self.add_product([0,string])                 # else, add the product to its product list
            
        self.work(comm, threshold)                       # call work function recursively for other production cycles

       
            
        