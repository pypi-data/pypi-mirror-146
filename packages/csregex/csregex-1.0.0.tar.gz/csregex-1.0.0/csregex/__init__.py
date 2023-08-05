'C# Regex implemented in Python'
from . import package, compiler

package.install_pythonnet() # Don't remove it

__all__ = ('compiler', 'is_match', 'match', 'find_all', 'sub', 'split')
__version__ = '1.0.0'

def escape(pattern: str, string: str, *options): # type: ignore
    return compiler.compile(pattern, *options).Escape(string)

def is_match(pattern: str, string: str, *options: compiler.RegexOptions): # type: ignore
    return compiler.compile(pattern, *options).IsMatch(string)

def match(pattern: str, string: str, *options: compiler.RegexOptions): # type: ignore
    return compiler.compile(pattern, *options).Match(string)

def sub(pattern: str, replace: str, string: str, *options: compiler.RegexOptions): # type: ignore
    return compiler.compile(pattern, *options).Replace(string, replace)

def split(pattern: str, string: str, *options: compiler.RegexOptions): # type: ignore
    yield from compiler.compile(pattern, *options).Split(string)

def find_all(pattern: str, string: str, *options: compiler.RegexOptions): # type: ignore
    yield from [match.Value for match in compiler.compile(pattern, *options).Matches(string)]