"""
    The definition of allowed parameters naming as json schemas.
"""
stream_parameters_schema = {
    "type": "object",
    'properties': {
        "framerate": {
            "type": ["integer", "null"],
            "enum": [8000, 16000, 22000, 22050, 44100, 44800]
        },
        'chunk_size': {
            "type": ["integer", "null"]
        },
        'channels': {
            "type": ["integer", "null"],
            "enum": [1, 2]
        },
        'device_id': {
            "type": ["integer", "null"]
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
    "required": ["framerate", "chunk_size", "channels"],
    "additionalProperties": False
}
