from setuptools import setup, find_packages

setup(
    name         = 'Sunshine',
    version      = '1.0',
    description  = 'Lightweight json-database library for Python',
    url          = 'https://github.com/De4oult/Sunshine',
    author       = 'de4oult',
    author_email = 'kayra.dist@email.com',
    license      = 'MIT',
    packages     = find_packages('source'),
    zip_safe     = False
)