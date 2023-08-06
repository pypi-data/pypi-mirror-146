#  Copyright (c) 2021 Pim Hazebroek
#  This program is made available under the terms of the MIT License.
#  For full details check the LICENSE file at the root of the project.

"""
The BME680 sensor - Temperature, Humidity, Pressure and Gas Sensor
=========================================

See https://www.adafruit.com/product/3660
"""
import logging

import adafruit_bme680

from constants import SENSOR_BME680
from sensors.tmp_hum_sensor import TmpHumSensor


class BME680(TmpHumSensor):
    """
    Concrete implementation of the BME680 sensor.
    """
    def __init__(self):
        """
        Initialize the sensor.
        """
        super().__init__()
        self._sensor = adafruit_bme680.Adafruit_BME680_I2C(self._i2c)

    @property
    def name(self):
        return SENSOR_BME680

    def read(self):
        """
        Reads the temperature, humidity, air pressure and VOC gas.
        """
        logging.info('Reading BME680 sensor')
        measurements = {
            'temperature': self.temperature,
            'humidity': self.relative_humidity,
            'air-pressure': self._sensor.pressure,
            'voc-gas': self._sensor.gas
        }
        logging.info('Measurement: %s', measurements)
        return measurements
