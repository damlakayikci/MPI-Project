from mpi4py import MPI

class Machine:
    # Class variables
    operations: list[list[str]] = [['enhance', 'split', 'chop'],['trim', 'reverse' ]]     # 0 index for even ids, 1 index for odd ids
    wear_factors: dict = { 'enhance': 0, 'split': 0, 'chop': 0, 'trim': 0, 'reverse': 0 } # initialize wear factors to 0
    machines: dict = {}                                                                   # dictionary to keep the machines
    
    # Constructor
    def __init__(self, id: int , operation: str, production_cycle: int, parent_id: int = None, original_string=None) -> None:
        self.id: int = id
        operations = Machine.operations[id%2].copy() 
        for op in operations:
            if op == operation:
                self.operation_index: int = operations.index(op) # index of the operation to be performed
                self.operation: str = operations[self.operation_index] # operation to be performed
                break
        self.products = []
        self.wear: int = 0
        self.parent_id: int = parent_id
        self.children: list[int] = []
        self.production_cycle: int = production_cycle
        self.original_string = original_string
        
    def add_child(self, child_id: int) -> None:
        self.children.append(child_id)

    def add_product(self, product: str) -> None:
        self.products.append(product)

#  <<<<<<<<<<<<<<<<<<<<<< OPERATIONS ---------------------- #
            
    def add(self) -> str:
        self.products.sort(key=lambda x: x[0])              # Sort the list by the first element of each sublist which denotes the child id
        self.products = [item[1] for item in self.products] # Remove the first element from each sublist 
        return ''.join(map(str, self.products))             # Join the list elements into a string

    def enhance(self, string: str) -> str:                  # duplicate the first and the last letter of the product
        return string[0] + string + string[-1]

    def reverse(self, string: str) -> str:                  # reverse the product
        return string[::-1]

    def chop(self, string: str) -> str:                     # remove the last letter from the product
        if len(string) == 1:
            return string
        return string[:-1]
   
    def trim(self, string: str) -> str:                     # remove the first and the last letters from the product
        if len(string) <= 2:
            return string
        return string[1:-1]

    def split(self, string: str) -> str:                    # split the product into two parts, and discard the right part
        if len(string) % 2 == 0:                            # if the length of the string is even, split from the middle
            return string[:len(string)//2]
        else:                                               # else, split from the middle + 1
            return string[:len(string)//2 + 1]
        
#  ---------------------- OPERATIONS >>>>>>>>>>>>>>>>>>>>>> #

    # main work function    
    def work(self, comm, threshold) -> None:
        if self.production_cycle == 0:                                  # if production cycle is over, return
            return
        
        if self.children != []:                                         # if machine has children, wait for them to finish
            for child_id in self.children:
                recv = comm.recv(source=0, tag=self.production_cycle)   # FIXME !!!
                self.products.append([recv[0], recv[1]])                # add the product to the machine's product list
                
        string = self.add()                                             # add products in machine's product list
        if self.id == 1:                                                # if machine is root send the final product to the center
            comm.send([self.id, 1, string], dest=0, tag=self.production_cycle) # (msg[1] is left as 1 since root machine has no parent)
        else:
            operation = getattr(self, self.operation)                   # get the operation to be performed
            self.wear += Machine.wear_factors[self.operation]           # add wear factor
            string = operation(string)                                  # perform the operation

            if self.wear >= threshold:                                  # if wear factor is greater than threshold,
                wear_factor = Machine.wear_factors[self.operation]
                cost =(self.wear - threshold+1) * wear_factor
                message = [self.id, cost, self.production_cycle]        
                comm.isend(message, dest=0, tag=0)                      # send a non-blocking message to the center
                self.wear = 0                                           # reset the wear factor

            if self.id % 2 == 1:                                        # change the operation                   
                self.operation_index = (self.operation_index + 1) % 2
                self.operation = Machine.operations[1][self.operation_index]
            else:
                self.operation_index = (self.operation_index + 1) % 3
                self.operation = Machine.operations[0][self.operation_index]
                
            comm.send([self.id,self.parent_id, string], dest=0, tag=self.production_cycle)
            
        self.production_cycle -= 1                                      # decrement production cycle
        if self.children != []:                                         # if machine has children, empty its product list
            self.products = []
        else:                                                           # else, add the original product to its product list
            self.products = []
            self.products = [[0, self.original_string]]
            
        self.work(comm, threshold)                                      # call work function recursively for other production cycles

       
        