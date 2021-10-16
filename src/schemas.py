stream_parameters_schema = {
    "type": "object",
    'properties':
        {
            "framerate": {
                "type": "integer",
                "enum": [8000, 16000, 22000, 22050, 44100, 44800]
            },
            'chunk_size': {
                "type": "integer"
            },
            'channels': {
                "type": "integer",
                "enum": [1, 2]
            },
            'device_id': {
                "type": ["integer", "null"]
            }
        }
}
