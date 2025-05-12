from setuptools import setup, find_packages

setup(
    name='akamalablib',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        # These libraries are currently all you need.
    ],
    author='Hiroyuki Akama',
    author_email='akamalab01@gmail.com',
    description='A Mathematica-like custom library for array operations and more in Python',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/hilolani/akamalablib',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)
