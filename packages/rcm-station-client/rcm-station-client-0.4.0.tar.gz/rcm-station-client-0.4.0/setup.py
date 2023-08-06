#  Copyright (c) 2022 Pim Hazebroek
#  This program is made available under the terms of the MIT License.
#  For full details check the LICENSE file at the root of the project.

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rcm-station-client",
    version="0.4.0",
    author="Pim Hazebroek",
    author_email="rcm@pimhazebroek.nl",
    description="Collects measurement reports from various sensors and send them to the station-monitoring-service.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/residential-climate-monitoring/station-client",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'requests==2.27.1',
        'urllib3==1.26.9',
        'python-dotenv==0.20.0',
        'psutil==5.9.0',
        'adafruit-blinka==7.2.0',
        'adafruit-circuitpython-busdevice==5.1.8',
        'adafruit-circuitpython-sht31d==2.3.10',
        'adafruit-circuitpython-bme680==3.4.2',
        'adafruit-circuitpython-tsl2591==1.3.2',
        'adafruit-circuitpython-sgp30==2.4.0',
        # Remember to sync dependencies in requirements.txt
    ],
    extras_require={
        'build': [
            'setuptools==50.3.2',
            'pylint',
            'bump2version==1.0.0'
        ]
    },
    python_requires='>=3.7',
)
