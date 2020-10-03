import os

from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as f:
    long_description = f.read()

setup(
    name='win2xcur',
    version='0.0.3',
    packages=find_packages(),
    install_requires=['Wand'],

    entry_points={
        'console_scripts': [
            'win2xcur = win2xcur.main.win2xcur:main',
            'x2wincur = win2xcur.main.x2wincur:main',
        ],
    },

    author='quantum',
    author_email='quantum2048@gmail.com',
    url='https://github.com/quantum5/win2xcur',
    description='win2xcur is a tool to convert Windows .cur and .ani cursors to Xcursor format.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='cur ani x11 windows win32 cursor xcursor',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Desktop Environment',
    ],
)
