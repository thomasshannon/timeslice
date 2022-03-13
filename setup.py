from setuptools import setup

setup(
    name='TimeSlice',
    version='1',
    packages=['timeslice'],
    url='https://github.com/thomasshannon/time-slice',
    license='MIT',
    author='Thomas Shannon',
    description='A command-line tool to create time slices from timelapse images',
    install_requires=[
        'Pillow',
        'numpy'
    ]
)
