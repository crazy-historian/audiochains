from setuptools import setup

README = ''

setup(
    name='runtime_audio_processing',
    description='runtime audio processing in chains of algorithms',
    version='0.9.0',
    license='',
    long_description=README,  # TODO: write markdown description!
    long_desctiption_content_type='text/markdown',
    url='https://github.com/crazy-historian/runtime_audio_processing',
    author='Maxim Zaitsev',
    author_email='zaitsev808@mail.ru',

    packages=[''],
    install_requires=[
        "numpy==1.20.0",
        "scipy>=1.7.1",
        "librosa>=0.8.1",
        "sounddevice>=0.4.2",
        "jsonschema>=4.1.0",
        "matplotlib>=3.4.3",
        "pytest~=6.2.5"
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest']  # TODO: figure out what is a setup requires, test requires
)
