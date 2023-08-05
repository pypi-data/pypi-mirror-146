setup_text = "import pathlib\n" \
    "from setuptools import find_packages, setup\n" \
    "HERE = pathlib.Path(__file__).parent\n" \
    "README = (HERE / 'README.md').read_text()\n" \
    "setup(\n" \
    "    name='ts_tariffs',\n" \
    "    version='{}',\n" \
    "    description='Calculate bills from timeseries consumption data and different tariff structures',\n" \
    "    long_description=README,\n" \
    "    long_description_content_type='text/markdown',\n" \
    "    url='https://github.com/uts/tariff-module',\n" \
    "    author='Joe Wyndham',\n" \
    "    author_email='joseph.wyndham@uts.edu.au',\n" \
    "    license='GNU Lesser General Public License v2.1',\n" \
    "    classifiers=[\n" \
    "        'Programming Language :: Python :: 3',\n" \
    "        'Programming Language :: Python :: 3.9',\n" \
    "    ],\n" \
    "    packages=find_packages(exclude=('tests',)),\n" \
    "    include_package_data=True,\n" \
    "    install_requires=[\n" \
    "        'boto3 >= 1.18.44',\n" \
    "        'matplotlib >= 3.4.3',\n" \
    "        'numpy >= 1.21.2',\n" \
    "        'pandas >= 1.3.3',\n" \
    "        'scipy >= 1.7.1',\n" \
    "        'pyarrow >= 5.0.0',\n" \
    "        'pydantic >= 1.8.2',\n" \
    "   ]\n" \
    ")\n".format

init_text = '"""Timeseries Tariff Calculation""" \n' \
    '__version__ = "{}"\n'.format
