from jsonschema import validate

stream_parameters_schema = {
    "type": "object",
    'properties':
        {
            "recording": {
                "type": "object",
                "properties": {
                    "framerate": {
                        "type": "integer",
                        "enum": [8000, 16000, 22000, 22050, 44100, 44800]}
                    ,
                    'chunk_size': {"type": "number"},
                    'channels': {"type": "number"},
                    'device_id': {"type": "integer"},
                    'duration': {"type": "integer"},
                }
            }
        }
}

test_config = {
    'recording': {
        'framerate': 44800,
        'chunk_size': 1024,
        'channels': 1,
        'device_id': 1,
        'duration': None,
        'silence': [0, 500],
        'whisper': [501, 1000],
        'normal': [1001, 2000],
        'loud': [2001, 5000]
    },
    'playback': {
        'file_name': 'test.wav',
        'chunk_size': 1024
    }
}

test = {
    'recording': {
        'framerate': 8001
    }

}

print(validate(instance=test, schema=stream_parameters_schema))
