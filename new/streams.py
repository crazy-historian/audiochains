import sounddevice as sd


class StreamWithChainOfMethods(sd.Stream):
    def __init__(self, chain_of_methods=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.chain_of_methods = chain_of_methods

    def from_json(self, filename):
        self.__init__()
        ...

    def from_yaml(self, filename):
        ...

    def set_chain(self):
        ...

    def set_methods(self):
        ...

    def apply(self):
        ...