import pyaudio

from globals import AVAILABLE_FREQUENCIES


class IMicrophone(pyaudio.PyAudio):
    def __init__(self, excepted_interfaces=None):
        super().__init__()
        self.microphones = {}
        self.names = set()
        self.interfaces = set()
        self.excepted_interfaces = excepted_interfaces or []
        #
        self.get_all_input_devices()
        self.sort_all_input_devices()

    def get_name_by_index(self, index):
        return self.get_device_info_by_index(index)['name']

    def get_all_input_devices(self):
        for i in range(self.get_device_count()):
            if self.check_malfunction(device_id=i):
                device_name = self.get_device_info_by_index(i)['name']
                device_host_api_id = self.get_device_info_by_index(i)['hostApi']
                device_host_api_info = self.get_host_api_info_by_index(device_host_api_id)

                if ("Микрофон" in device_name) or ("микрофон" in device_name) or ("Microphone" in device_name):
                    self.microphones[i] = {'name': device_name, 'index': i, 'interface': device_host_api_info['name']}

    def sort_all_input_devices(self):
        sorted_microphones = {}
        for device_num in self.microphones:
            device = self.microphones[device_num]

            if device['interface'] not in self.excepted_interfaces:
                self.names.add(device['name'])
                self.interfaces.add(device['interface'])
                sorted_microphones[device_num] = self.microphones[device_num]
        else:
            self.microphones = sorted_microphones

    def get_interfaces_by_name(self, name):
        interfaces = set()
        for device_num in self.microphones:
            device = self.microphones[device_num]
            if name == device['name']:
                interfaces.add(device['interface'])
            else:
                continue
        else:
            return interfaces

    def get_index_by_name_and_interface(self, name, interface):
        for device_num in self.microphones:
            device = self.microphones[device_num]
            if name == device['name'] and interface == device['interface']:
                return device['index']
        else:
            return None

    def get_index_by_name(self, name):
        for device_num in self.microphones:
            device = self.microphones[device_num]
            if name == device['name']:
                return device['index']
        else:
            return None

    def check_malfunction(self, device_id):
        for frequency in AVAILABLE_FREQUENCIES:
            try:
                if not self.is_format_supported(
                    rate=frequency,
                    input_device=device_id,
                    input_channels=1,
                    input_format=pyaudio.paInt16
                ):
                    return False
            except ValueError:
                return False
        else:
            return True

    def check_configuration(self, rate, num_of_channels, data_format):
        for i in range(self.get_device_count()):
            name = self.get_device_info_by_index(i)['name']
            device_host_api_id = self.get_device_info_by_index(i)['hostApi']
            device_host_api_info = self.get_host_api_info_by_index(device_host_api_id)['name']
            if ("Микрофон" in name) or ("микрофон" in name) or ("Microphone" in name):
                try:
                    output = self.is_format_supported(
                        rate=rate,
                        input_device=i,
                        input_channels=num_of_channels,
                        input_format=data_format
                    )
                except ValueError:
                    print(f'НЕ РАБОТАЕТ: {name}, {device_host_api_info}, НОМЕР: {i}')
                else:
                    if output:
                        print(f'РАБОТАЕТ: {name}, {device_host_api_info}, НОМЕР: {i}')
                    else:
                        print(f'НЕ РАБОТАЕТ: {name}, {device_host_api_info}, НОМЕР: {i}')


if __name__ == "__main__":
    micro = IMicrophone()
    for key in micro.microphones:
        print(micro.microphones[key])
    print('-' * 10)
    micro.check_configuration(
        rate=48000,
        num_of_channels=1,
        data_format=pyaudio.paInt16
    )
