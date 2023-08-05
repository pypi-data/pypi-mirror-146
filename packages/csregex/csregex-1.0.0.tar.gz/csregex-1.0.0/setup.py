from setuptools import setup

from re import search

def _find_version():
    with open('csregex/__init__.py', 'r') as file:
        code = file.read()

    version = search(r'__version__ =.*', code)
    return version

exec(_find_version().group(), globals(), locals())

setup(
    name='csregex',
    version=__version__, # type: ignore
    description='C# Regex implemented in Python',
    long_description='# Example\n```python\nimport csregex\n\ncsa = regex.find_all(\'[^a]\', \'asdf\')\nlist(a)\n>>>[\'s\', \'\d\', \'f\']',
    long_description_content_type='text/markdown',
    packages=['csregex'],
    author='LUA9',
    maintainer='LUA9',
    url='https://github.com/LUA9/csregex',
    license='MIT'
)