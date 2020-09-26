from setuptools import setup

setup(
    name='win2xcur',
    version='0.3.1',
    packages=['win2xcur'],
    install_requires=['Wand'],

    entry_points={
        'console_scripts': [
            'win2xcur = win2xcur.main:main',
        ],
    },

    author='quantum',
    author_email='quantum2048@gmail.com',
)
