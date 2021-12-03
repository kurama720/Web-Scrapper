from setuptools import setup


setup(
    name='databases',
    version='0.1',
    description='Includes MongoDB and PostgreSQL',
    install_requires=['pymongo', 'psycopg2'],
    packages=['mongo', 'postgre'],
)
