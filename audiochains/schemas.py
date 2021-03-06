"""
    The definition of allowed parameters naming as json schemas.
"""
stream_parameters_schema = {
    "type": "object",
    'properties': {
        "samplerate": {
            "type": ["integer", "null"],
            "enum": [8000, 16000, 22000, 22050, 44100, 44800]
        },
        'blocksize': {
            "type": ["integer", "null"]
        },
        'channels': {
            "type": ["integer", "null"],
            "enum": [1, 2]
        },
        "sampwidth": {
            "type": ["integer", "null"],
            "enum": [1, 2, 3, 4]
        },
        'device': {
            "anyOf": [
                {
                    "type": "integer"
                },
                {
                    "type": "array",
                    "maxItems": 2,
                    "items": {
                        "type": "number"
                    }
                },
                {
                    "type": "null"
                }
            ]
        },
        "dtype": {
            "type": ["string", "null"]
        },
        "latency": {
            "type": ["number", "string", "null"]
        },
        "callback": {
            "type": ["object", "null"]
        },
        "extra_settings": {
            "type": ["object", "null"]
        },
        "finished_callback": {
            "type": ["object", "null"]
        },
        "clip_off": {
            "type": ["boolean", "null"]
        },
        "dither_off": {
            "type": ["boolean", "null"]
        },
        "never_drop_input": {
            "type": ["boolean", "null"]
        },
        "prime_output_buffers_using_stream_callback:": {
            "type": ["boolean", "null"]
        },
    },
    "required": ["samplerate", "blocksize", "channels"],
    "additionalProperties": False
}
