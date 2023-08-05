'Compiler using pythonnet. It is not for import, do not import it.'

import clr # type: ignore
clr.AddReference('System.Text.RegularExpressions') # type: ignore

from System.Text.RegularExpressions import Regex as _regex # type: ignore
from System.Text.RegularExpressions import RegexOptions as _options # type: ignore

__all__ = ('Regex', 'RegexOptions', 'compile')

class Regex:
    def __init__(self, *args, **kwargs):
        result = _regex(*args, **kwargs)

        for k in result.__dir__():
            if not k.startswith('__'):
                setattr(self, k, getattr(result, k))

    def __str__(self):
        return str(type(self))

class RegexOptions:
    pass

for k, v in _options.__dict__.items():
    if not k.startswith('__'):
        setattr(RegexOptions, k, v)

def compile(pattern: str, *options: RegexOptions): # type: ignore
    return Regex(pattern, *options)