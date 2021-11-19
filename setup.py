from pathlib import Path
from setuptools import setup

project_path = Path(__file__).parent

README = str(Path(f'{project_path}/audiochains/test/test_config.json'))
with open(README, encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='audiochains',
    description='runtime audio processing in chains of algorithms',
    version='0.1.2',
    license='',
    long_description=long_description,
    long_desctiption_content_type='text/markdown',
    url='https://github.com/crazy-historian/runtime_audio_processing',
    author='Maxim Zaitsev',
    author_email='zaitsev808@mail.ru',

    packages=['audiochains', 'audiochains/test'],
    package_data={'audiochains/test': ['test_recording.wav', 'test_playback.wav', 'test_config.json']},
    include_package_data=True,
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
    tests_require=['pytest']
)
