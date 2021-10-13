import sounddevice as sd


def get_all_input_devices():
    devices = sd.query_devices()
    input_devices = dict()
    for num, dev in enumerate(devices):
        if dev['max_input_channels'] != 0:
            input_devices[num] = dev
    for key, value in input_devices.items():
        print(key, value)
    return input_devices


def get_all_output_devices():
    devices = sd.query_devices()
    output_devices = dict()
    for num, dev in enumerate(devices):
        output_channels = dev['max_output_channels']
        if output_channels != 0:
            output_devices[num] = dev
    for key, value in output_devices.items():
        print(key, value)


get_all_input_devices()
get_all_output_devices()
