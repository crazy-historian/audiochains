class ChainOfMethods:
    """
    Implementation of Chain Of Command pattern for sequences of BlockAudioMethod.
    """
    def __init__(self, *chain):
        self.chain = chain

    def __call__(self, in_data):
        for block_method in self.chain:
            in_data = block_method(in_data)
        return in_data
