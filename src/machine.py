
class Machine:
   
    # 0 index for even ids, 1 index for odd ids
    operations: list[list[str]] = [['enhance', 'split', 'chop'],['trim', 'reverse' ]] 
    # initialize wear factors to 0
    wear_factors: dict = { 'enhance': 0, 'split': 0, 'chop': 0, 'trim': 0, 'reverse': 0 }
    
    # define constructor
    def __init__(self, id: int , operation: str , parent_id: int = None) -> None:
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
        

    def add_product(self, product: str) -> None:
        self.products.append(product)


#  ---------------------- OPERATIONS ---------------------- #
            
    def add(self) -> str:
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
        
    def work(self) -> None:
        string = self.add()                               # add products in machine's product list
        operation = getattr(self, self.operation)         # get the operation to be performed
        self.wear += Machine.wear_factors[self.operation] # add wear factor
        string = operation(string)                        # perform the operation
        self.operation = self.next_operations[0]          # set the next operation as current operation
        self.next_operations.remove(self.operation)       # remove the operation from the list
        self.next_operations.append(self.operation)       # add the operation to the end of the list

       
            
        