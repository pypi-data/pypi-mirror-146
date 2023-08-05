from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: MIT License',
    'Programming language :: Python :: 3'
]

setup(
    name='memcalc',
    version='0.0.1',
    description='calculator with essential math functions',
    long_description=open('README.md').read(),
    url='',
    author='David Balsys',
    author_email='davidbalsys@gmail.com',
    license='MIT',
    keywords='calculator',
    packages=find_packages(),
)
