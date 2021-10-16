class ChainOfMethods:
    def __init__(self, *chain):
        self.chain = chain

    def __call__(self, in_data):
        for callback_filter in self.chain:
            in_data = callback_filter(in_data)
        return in_data
