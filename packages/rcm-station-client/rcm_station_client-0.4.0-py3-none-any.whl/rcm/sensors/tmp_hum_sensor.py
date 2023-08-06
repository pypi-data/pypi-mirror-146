#  Copyright (c) 2021 Pim Hazebroek
#  This program is made available under the terms of the MIT License.
#  For full details check the LICENSE file at the root of the project.

"""
The module that defines the TmpHumSensor
"""

from abc import abstractmethod
from math import exp

from sensors.sensor import Sensor


class TmpHumSensor(Sensor):
    """
    A base class for sensors with temperature and humidity. The absolute humidity is derived from temperature and relative humidity.
    """

    def __init__(self):
        """
        Default constructor, the _sensor should be set by subclasses
        """
        super().__init__()
        self._sensor = None

    @property
    @abstractmethod
    def name(self):
        raise NotImplementedError

    @property
    def temperature(self):
        """
        :return: the temperature in *C
        """
        return self._sensor.temperature

    @property
    def relative_humidity(self):
        """
        :return: the relative humidity in %
        """
        return self._sensor.relative_humidity

    @property
    def absolute_humidity(self):
        """
        :return: the absolute humidity in g/m3, derived from the temperature and relative humidity.
        """
        numerator = (self.relative_humidity / 100.0) * 6.112 * exp((17.62 * self.temperature) / (243.12 + self.temperature))
        denominator = (273.15 + self.temperature)
        return 216.7 * (numerator / denominator)
