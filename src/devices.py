"""
A group of functions for getting advanced information about the input
or output device separately.
"""

import sounddevice as sd
from typing import Optional, List


def get_all_input_devices() -> List[int]:
    """
    Returns the list containing all input devices indices
    by checking an amount of input channels.
    """
    devices = sd.query_devices()
    input_devices = list()
    for num, dev in enumerate(devices):
        if dev['max_input_channels'] != 0:
            input_devices.append(num)
    return input_devices


def get_all_output_devices() -> List[int]:
    """
    Returns the list containing all output devices indices
    by checking an amount of output channels.
    """
    devices = sd.query_devices()
    output_devices = list()
    for num, dev in enumerate(devices):
        if dev['max_output_channels'] != 0:
            output_devices.append(num)
    return output_devices


def get_hostapi_with_devices(kind: str = None) -> dict[str: dict]:
    """
    Returns a dictionary where key is a name of audio system host api
    and corresponded value is dictionary containing information about all
    compatible devices

    :param kind: "input", "output" or None
    """
    devices_by_hostapi = dict()
    if kind == 'input':
        dev_numbers = get_all_input_devices()
    elif kind == 'output':
        dev_numbers = get_all_output_devices()
    else:
        dev_numbers = [_ for _ in range(len(sd.query_devices()))]

    hostapis = sd.query_hostapis()
    for hostapi in hostapis:
        devices = dict()
        for dev_num in dev_numbers:
            if dev_num in hostapi['devices']:
                devices[dev_num] = sd.query_devices(device=dev_num)
        devices_by_hostapi[hostapi['name']] = devices

    return devices_by_hostapi


def get_hostapi_by_device_name(device_name: str) -> Optional[str]:
    """
    If the device with the passed name exists,
    function returns the hostapi name related with particular device name,
    otherwise None

    """
    for num, device in enumerate(sd.query_devices()):
        if device_name == device['name']:
            return sd.query_hostapis(index=num)['name']
    return None


def get_device_index_by_name(device_name: str) -> Optional[int]:
    """
    If the device with the passed name exists,
    function returns the devices index related with particular device name,
    otherwise None
    """
    for num, device in enumerate(sd.query_devices()):
        if device_name == device['name']:
            return num
    return None
