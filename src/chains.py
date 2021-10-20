class ChainOfMethods:
    def __init__(self, *chain):
        self.chain = chain

    def __call__(self, in_data):
        for block_method in self.chain:
            in_data = block_method(in_data)
        return in_data
