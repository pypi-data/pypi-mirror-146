#  Copyright (c) 2021 Pim Hazebroek
#  This program is made available under the terms of the MIT License.
#  For full details check the LICENSE file at the root of the project.

"""
The SGP30 sensor - tVOC and eCO2 sensor
=========================================

See https://www.adafruit.com/product/3709

The first time this sensor is used, the setting `sgp30-init-baseline` should be set to true and the script should be run in the background
for approx. 12 hours. This will establish a baseline for the sensor which is then written to disk. It will store the baseline every hour.
Check the SGP30 datasheet for more details.
See https://cdn-learn.adafruit.com/assets/assets/000/050/058/original/Sensirion_Gas_Sensors_SGP30_Datasheet_EN.pdf
"""
import logging
import os
import sys
import time

import adafruit_sgp30

from constants import MODE_WRITE, MODE_READ, LINE_SEP, SENSOR_SGP30, UTF_8
from sensors.sensor import Sensor
from sensors.tmp_hum_sensor import TmpHumSensor
from settings import sgp30_baseline_file

SECONDS_IN_HOUR = 60 * 60
TWELVE_HOURS_IN_SECONDS = 12 * SECONDS_IN_HOUR
SECONDS_IN_WEEK = 7 * 24 * SECONDS_IN_HOUR


class SGP30(Sensor):
    """
    Concrete implementation of the SGP30 sensor.
    """

    def __init__(self):
        """
        Initialize the sensor. After the sensor is initialized, it will be in
        an initialization phase for about 15 seconds and only return default
        values of eCO2 400 ppm and TVOC 0 ppb.
        """
        super().__init__()
        self.tmp_hum_sensor = None
        self._sensor = adafruit_sgp30.Adafruit_SGP30(self._i2c)
        self._sensor.iaq_init()
        logging.debug('Initialized SGP30 sensor on address 0x58')

    @property
    def name(self):
        """
        :return: the name of the sensor
        """
        return SENSOR_SGP30

    @property
    def raw_ethanol(self):
        """
        :return: the (raw) Ethanol value in ticks
        """
        return self._sensor.Ethanol

    @property
    # pylint: disable=invalid-name
    def raw_H2(self):
        """
        :return: the (raw) H2 value in ticks
        """
        return self._sensor.H2

    @property
    # pylint: disable=invalid-name
    def TVOC(self):
        """
        :return: The TVOC value in ppb (parts per billion)
        """
        return self._sensor.TVOC

    @property
    # pylint: disable=invalid-name
    def eCO2(self):
        """
        :return: The eCO2 value in ppm (parts per million)
        """
        return self._sensor.eCO2

    @property
    def tmp_hum_sensor(self):
        """
        :return: the temperature/humidity sensor
        """
        return self._tmp_hum_sensor

    @tmp_hum_sensor.setter
    def tmp_hum_sensor(self, tmp_hum_sensor: TmpHumSensor):
        """
        Sets the temperature/humidity sensor
        """
        self._tmp_hum_sensor = tmp_hum_sensor

    def set_iaq_absolute_humidity(self, absolute_humidity):
        """
        Sets the absolute humidity for the compensation algorithm.
        :param absolute_humidity: the absolute humidity in g/m3
        """
        logging.debug(f'Enabling compensation algorithm with absolute humidity {absolute_humidity}')
        self._sensor.set_iaq_humidity(absolute_humidity)

    def set_iaq_relative_humidity(self, temperature, relative_humidity):
        """
        Sets the absolute humidity for compensation algorithm derived from
        temperature and relative humidity.
        :param temperature: the temperature in *C
        :param relative_humidity: the relative humidity in %
        """
        logging.debug(f'Enabling compensation algorithm with relative humidity {relative_humidity} and temperature {temperature}')
        self._sensor.set_iaq_relative_humidity(temperature, relative_humidity)

    def read(self):
        """
        Reads the sensor. The sensor is optimized for a sampling rate of 1Hz so
        we start reading measurements once every second for about 30 seconds to
        get a stable reading and be sure initialization phase is completed.
        """
        baseline = self._get_baseline()
        self._apply_baseline(baseline)
        if self.tmp_hum_sensor is not None:
            self.set_iaq_absolute_humidity(self.tmp_hum_sensor.absolute_humidity)

        logging.info('Reading SGP30 sensor...')
        elapsed_sec = 0
        while elapsed_sec < 30:
            self._sensor.iaq_measure()
            time.sleep(1)
            elapsed_sec += 1

        report = self._create_measurement_report()
        logging.info('Measurement: %s', report)
        return report

    def _get_baseline(self):
        """
        :return: the baseline, if none exists or current is too old, a new one is initialized before it is returned.
        """
        baseline = self._read_baseline()
        if baseline is None:
            self._init_baseline()
            baseline = self._read_baseline()
        return baseline

    def _init_baseline(self):
        """
        Initialize the baseline. Note: takes 12 hrs to run!
        """
        logging.info('Initializing SGP30 baseline...')
        self._sensor.iaq_init()
        elapsed_sec = 0
        start_time = time.time()
        while elapsed_sec < TWELVE_HOURS_IN_SECONDS:
            time.sleep(1)
            elapsed_sec = time.time() - start_time
            if self.tmp_hum_sensor is not None:
                self.set_iaq_absolute_humidity(self.tmp_hum_sensor.absolute_humidity)
            self._sensor.iaq_measure()
            if elapsed_sec % 60 <= 1:
                logging.info(f'eCO2 = {self._sensor.eCO2} ppm | TVOC = {self._sensor.TVOC} ppb')
                logging.info('**** Baseline values: eCO2 = 0x%x, TVOC = 0x%x', self._sensor.baseline_eCO2, self._sensor.baseline_TVOC)
                self._write_baseline({
                    'eCO2': self._sensor.baseline_eCO2,
                    'TVOC': self._sensor.baseline_TVOC,
                })
        logging.info('Baseline initialization complete')

    def _create_measurement_report(self):
        """
        Return a measurement report with the current values from the sensor.
        """
        measurements = {
            'raw-ethanol': self._sensor.Ethanol,
            'raw-H2': self._sensor.H2,
            'TVOC': self._sensor.TVOC,
            'eCO2': self._sensor.eCO2,
        }
        return measurements

    def _apply_baseline(self, baseline):
        """
        Apply the given baseline values to the sensor.

        :param baseline: the values for eCO2 and TVOC
        """
        self._sensor.set_iaq_baseline(baseline['eCO2'], baseline['TVOC'])
        logging.debug('Set eCO2 baseline: 0x%x', baseline['eCO2'])
        logging.debug('Set TVOC baseline: 0x%x', baseline['TVOC'])

    @staticmethod
    def _read_baseline():
        """
        Read the baseline values from file.
        :return: a dict with the values from the baseline file, or None when baseline too old or not found.
        """
        logging.debug('Reading IAQ baseline values from file')
        if not os.path.isfile(sgp30_baseline_file):
            logging.info('No baseline file')
            return None
        try:
            with open(sgp30_baseline_file, MODE_READ, encoding=UTF_8) as file:
                content = file.read().splitlines()
                timestamp = float(content[2])
                now = time.time()
                if now - timestamp >= SECONDS_IN_WEEK:
                    logging.warning('Baseline too old')
                    return None
                return {
                    'eCO2': int(content[0]),
                    'TVOC': int(content[1]),
                    'timestamp': timestamp
                }
        except Exception as exception:
            logging.exception('Failed to read baseline', exc_info=exception)
            sys.exit(1)

    @staticmethod
    def _write_baseline(baseline):
        """
        Write the baseline values to disk
        :param baseline: a dict with the baseline values for eCO2 and TVOC
        """
        logging.debug('Writing IAQ baseline values to file')
        try:
            with open(sgp30_baseline_file, MODE_WRITE, encoding=UTF_8) as file:
                eco2_baseline = str(baseline['eCO2']) + LINE_SEP
                tvoc_baseline = str(baseline['TVOC']) + LINE_SEP
                timestamp = str(time.time())
                file.writelines([eco2_baseline, tvoc_baseline, timestamp])
        except Exception as exception:
            logging.exception('Failed to write SGP30 baseline values to file', exc_info=exception)
            sys.exit(1)
