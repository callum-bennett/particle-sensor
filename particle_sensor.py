from pms5003 import PMS5003
import time

class ParticleSensor:
    def __init__(self, clientId, device="/dev/ttyAMA0", baudrate=9600, pin_enable="GPIO22", pin_reset="GPIO27"):
        self.deviceId = clientId
        self.sensor = PMS5003(device=device, baudrate=baudrate, pin_enable=pin_enable, pin_reset=pin_reset)

    def read(self):
        data = self.sensor.read()

        return {
            'deviceId': self.deviceId,
            'timestamp': int(time.time() * 1000),
            'pm1_0': data.pm_ug_per_m3(1.0),
            'pm2_5': data.pm_ug_per_m3(2.5),
            'pm10': data.pm_ug_per_m3(10),
            'pm1_0_atm': data.pm_ug_per_m3(1.0, True),
            'pm2_5_atm': data.pm_ug_per_m3(2.5, True),
            'pm10_atm': data.pm_ug_per_m3(None, True),
            'particles_0_3um': data.pm_per_1l_air(0.3),
            'particles_0_5um': data.pm_per_1l_air(0.5),
            'particles_1_0um': data.pm_per_1l_air(1.0),
            'particles_2_5um': data.pm_per_1l_air(2.5),
            'particles_5_0um': data.pm_per_1l_air(5.0),
            'particles_10um': data.pm_per_1l_air(10)
        }