"""
speed-rw
--------------
A app that analyse internet speed in Rwanda based on Twitter feebdacks.
"""
from setuptools import setup
from os import path


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='speed-rw',
    version='0.0.1',
    url='https://github.com/kenessajr/speed-rw',
    license='MIT',
    author='Remy Muhire',
    author_email='jeanremy1806@gmail.com',
    description=('Analyse internet speed based on Twitter feebdacks.'),
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'pytesseract==0.3.3',
        'numpy==1.18.2'
    ],
    extras_require={
        'test': [
            'pytest==4.1',
            'pytest-flake8==1.0.4',
            'pytest-cov==2.6.1'
        ]
    },
    test_suite="tests",
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3'
    ]
)
