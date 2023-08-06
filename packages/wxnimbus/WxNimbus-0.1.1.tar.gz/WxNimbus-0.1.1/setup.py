# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nimbus', 'nimbus.sinks', 'nimbus.sources', 'nimbus.transformers']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.0.1,<10.0.0',
 'PyAudio>=0.2.11,<0.3.0',
 'PySDL2>=0.9.11,<0.10.0',
 'numpy>=1.22.3,<2.0.0',
 'pyrtlsdr>=0.2.92,<0.3.0',
 'scipy>=1.8.0,<2.0.0']

entry_points = \
{'console_scripts': ['nimbus = nimbus.__main__:main']}

setup_kwargs = {
    'name': 'wxnimbus',
    'version': '0.1.1',
    'description': 'Nimbus is an open-source library and framework for real-time reading and decoding of data signals from NOAA polar satellites.',
    'long_description': '# Nimbus\nNimbus, named after Nimbus-1, the first satellite 🛰️ to transmit using the APT format, is an open-source framework that is easily composable and allows for both real-time and pre-recorded signal processing and image reconstruction of weather satellite data.\n\n## Usage\nNimbus has a command line wrapper for running commonly used settings, such as reading from an SDR and outputting to an image. There are several available Sources: reading from an SDR, reading from a .iq file, and reading from a .wav file. There are also several available outputs (called Sinks): output to a .wav file, output to a .iq file, output to a .png, output to audio (play sound), or output to a realtime window that renders the image row by row. \n\nThe general command line interface is as follows, where the wave, iq, and image files are optional, but you must pick a single source to read from and a satellite you are reading from (SDR is default if no other source is set). \n\n```\nnimbus [-h] [--wave WAVE_FILE] [--iq IQ_FILE] [--image IMAGE_FILE] [--audio] [--sat {15,18,19}] [source]\n```\nCurrently, only NOAA POES satellites (NOAA 15, 18, 19) are supported. Be on the lookout for GOES and METEOR support soon!\n\n## Examples\nFor some "copy paste" examples, here are some commonly used settings for the command line\n\nTo read NOAA 15 from an SDR and output a .wav file, a .iq file, a .png, play audio, and see the realtime rendering, run the following:\n```\nnimbus --image ./out.png --wave ./out.wav --iq ./out.iq --audio --sat 15\n```\n\nLet\'s say you didn\'t care about the wave file, iq file, and didn\'t want audio played. No problem! Just leave those options out:\n```\nnimbus --image ./out.png --sat 15\n```\n\nWhat if you don\'t have an SDR but have a .wav file from a NOAA pass? Easy! You can give the source as a path to the wavefile instead of leaving it blank.\n```\nnimbus example/path/to/wavefile.wav\n```\n\n\nGot an .iq file instead? No sweat for Nimbus. You can give the source as a path to the IQ file instead of leaving it blank.\n```\nnimbus example/path/to/iqfile.iq\n```\n\n\n## Demo\nOne thing that Nimbus can do that a lot of other programs do not do is providing real-time rendering from an SDR. This allows the user to make adjustments to satellite position if needed. Also, let\'s just be honest, it\'s kinda cool too. \n![real-time-demo](https://user-images.githubusercontent.com/32559461/162660124-d907e9eb-8290-4f05-af9a-3454110bb1c4.gif)\n\nCommand ran to generate demo:\n```\nnimbus examples/10080101_16bit.wav\n```\n\n\n## Installation\n### Install with pip\n```\npip install wxnimbus\n```\n\n### Installation from Git\n```\ngit clone https://github.com/Quinticx/nimbus.git\ncd nimbus \npoetry install \n```\n\n\n## Dependencies\n### Ubuntu\n```\nsudo apt install portaudio19-dev\n\n```\n\n## Background\nNOAA maintains several weather satellites responsible for weather analysis and forecasting, climate research and prediction, temperature measurements, and more. Among these satellites are the Polar Operational Environmental Satellites (POES) group. POES satellites have several sensors, such as a microwave imager, ultraviolet sensor, and more, that allow them to perform their daily duties in aiding weather researchers and forecasters across the country. \n\n## Satellite 🛰️ to Computer 💻\nPOES uses a communication protocol called automatic picture transmission (APT) to send image data to receivers on the ground. APT signals are composed of 2 image channels, telemetry information, and synchronization data. The signals are transmitted in a horizontal scan line which are sent at 2 lines per second, which is around 4160 baud. Once the APT signal is received, the image can be reconstructed from the transmitted lines.\n\nAPT encodes pixel intensity as one of 256 grayscale values. This signal is then amplitude modulated onto a 2.4kHz carrier, and the resulting AM waveform is frequency modulated onto a 137MHz carrier. To receive APT signals, a few components are needed: an appropriate antenna and a software-defined radio (SDR).\n\n### IQ Sampling\nMost SDRs use IQ sampling. IQ sampling is a technique that uses two 90 degree out-of-phase wave-forms to transform a single real signal into a complex signal. The resulting signal preserves the amplitude and phase, but allows an analog-to-digital converter (ADC) to sample at a much lower frequency. The SDR controls the frequency of the sampling wave-forms to tune the frequency band being sampled.\n\n### FM Demodulation \nTo unwrap the first layer of modulation, the signal needs to be frequency demodulated by a 137 MHz carrier wave. FM demodulation is accomplished by examining the phase change of consecutive IQ samples. If two samples have the same phase, then the frequency of the input is identical to the baseband frequency. If successive samples have increasing phases, then the input frequency is higher then the baseband frequency (the input is leading the baseband). Likewise if the phase is decreasing the frequency is lower (the input is lagging the baseband). By calculating the phase difference between each successive pair of samples (the derivative), we can retrieve the original signal.\n\n### AM Demodulation\nThe output of the FM Demodulation stage is a 256 level amplitude modulated signal. There are multiple ways to demodulate an AM waveform. A popular AM demodulation strategy is to utilize the Hilbert transform. The Hilbert transform takes a real AM signal and returns the complex analytic signal, the magnitude of which is the original signal. \n\n### APT Decoding\nAPT Data is encoded into scan lines that are transmitted at a rate of 2 per second. Each scan line contains 2080 pixels. Half of which are used for image data, and the remaining pixels are used for synchronization and satellite telemetry information. Decoding APT starts by locating a sync frame in the input signal, a 36 pixel long string of white and black pixels that corresponds to the start of the first video channel. Once the sync frame is established 47 pixels are skipped and then 909 pixels of image data are read. After the image data there are 45 pixels of telemetry data. The same sequence is repeated (with a different sync frame) for the second channel. Consecutive scan lines are stacked and the resulting image can be displayed.\n\n## Coming Soon\nSooner:\n1. Country border overlay on images \n\nLater:\n1. GOES Satellite 🛰️ support\n2. METEOR Satellite 🛰️ support\n',
    'author': 'Brianna Witherell',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Quinticx/nimbus',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
