#  Copyright (c) 2022 Pim Hazebroek
#  This program is made available under the terms of the MIT License.
#  For full details check the LICENSE file at the root of the project.

"""
The SHT31-D sensor - High precision Temperature & Humidity sensor
=================================================================

See https://www.adafruit.com/product/2857
"""
import logging

import adafruit_sht31d

from constants import SENSOR_SHT31_D
from sensors.tmp_hum_sensor import TmpHumSensor
from util.bool import strtobool

_PRIMARY_ADDRESS = 0x44
_SECONDARY_ADDRESS = 0x45


class SHT31D(TmpHumSensor):
    """Concrete implementation of SHT31-D sensor."""

    def __init__(self):
        """
        Initialize the SHT31D sensor. It will automatically check the settings to choose the I2C address to use.
        """
        super().__init__()
        address = self._get_address()
        self._sensor = adafruit_sht31d.SHT31D(self._i2c, address)
        logging.debug(f'Initialized SHT31-D sensor on address {address}')

    @property
    def name(self):
        """
        :return: the name of the sensor
        """
        return SENSOR_SHT31_D

    def read(self):
        """
        Reads the temperature and relative humidity.
        """
        logging.info('Reading SHT31-D sensor')
        measurements = {
            'temperature': self.temperature,
            'humidity': self.relative_humidity
            # 'absolute_humidity': self.absolute_humidity
        }
        logging.info('Measurement: %s', measurements)
        return measurements

    def _get_address(self):
        """Determine the I2C address to use"""
        return _SECONDARY_ADDRESS \
            if 'secondary_address' in self._settings.keys() and strtobool(self._settings['secondary_address']) \
            else _PRIMARY_ADDRESS
