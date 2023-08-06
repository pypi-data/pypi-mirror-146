#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=7.0'
    , 'bump2version==0.5.11'
    , 'watchdog==0.9.0'
    , 'flake8==3.7.8'
    , 'tox==3.14.0'
    , 'coverage==4.5.4'
    , 'Sphinx==1.8.5'
    , 'twine==1.14.0'
    , 'Click==7.1.2'
    , 'asn1crypto==1.4.0'
    , 'wheel==0.33.6'
    , 'azure-common==1.1.27'
    , 'azure-core==1.17.0'
    , 'azure-storage-blob==12.8.1'
    , 'boto3==1.18.30'
    , 'botocore==1.21.30'
    , 'certifi==2021.5.30'
    , 'cffi==1.14.6'
    , 'chardet==4.0.0'
    , 'charset-normalizer==2.0.4'
    , 'cryptography==3.4.8'
    , 'idna==3.2'
    , 'isodate==0.6.0'
    , 'pycryptodomex==3.10.1'
    , 'jmespath==0.10.0'
    , 'pyOpenSSL==20.0.1'
    , 'msrest==0.6.21'
    , 'pytz==2021.1'
    , 'oauthlib==3.1.1'
    , 'requests-oauthlib==1.3.0'
    , 'oscrypto==1.2.1'
    , 'six==1.16.0'
    , 'pycparser==2.20'
    , 'pyarrow==5.0.0'
    , 'PyJWT==2.1.0'
    , 'python-dateutil==2.8.2'
    , 'requests==2.26.0'
    , 'snowflake-connector-python==2.6.2'
    , 's3transfer==0.5.0'
    , 'snowflake-sqlalchemy==1.3.3'
    , 'SQLAlchemy==1.4.29'
    , 'urllib3==1.26.6']

test_requirements = []

setup(
    author="Md Kamruz Zaman Rana",
    author_email='mrkfw@mail.missouri.edu',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Snowflake helper library",
    entry_points={
        'console_scripts': [
            'kzr_snowflake=kzr_snowflake.cli:main',
        ],
    },
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='kzr_snowflake',
    name='kzr_snowflake',
    packages=find_packages(include=['kzr_snowflake', 'kzr_snowflake.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/kzraryan-mu/kzr_snowflake',
    version='0.0.8',
    zip_safe=False,
)
