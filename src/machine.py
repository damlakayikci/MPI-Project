class Machine:
    def __init__(self, id, operations, parent_id=None):
        self.id = id
        self.operations = operations
        # self.maintenance_factor = maintenance_factor
        self.products = []
        self.wear = 0
        self.maintenance = 0
        self.parent_id = parent_id

    def add_product(self, product):
        self.products.append(product)