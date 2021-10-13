import sounddevice as sd
import json
import pyyaml as yaml

from jsonschema import validate
from schemas import stream_parameters_schema


class StreamWithChainOfMethods(sd.RawInputStream):
    def __init__(self, chain_of_methods=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.chain_of_methods = chain_of_methods

    def from_json(self, filename):
        with open(filename, 'r') as json_file:
            stream_config = json.load(json_file)
            validate(instance=stream_config, schema=stream_parameters_schema)
            self.__init__(
                samplerate=stream_config['framerate'],
                blocksize=stream_config['chunk'],
                channels=stream_config['channels'],
                device=stream_config['device'] or sd.default.device,
                chain_of_methods=None
            )

    def from_yaml(self, filename):
        with open(filename, 'r') as yaml_file:
            yaml.load(yaml_file)

    def set_chain(self):
        ...

    def set_methods(self):
        ...

    def apply(self):
        ...
