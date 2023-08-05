'Pythonnet installer'

from subprocess import Popen
from pkgutil import iter_modules

__all__ = ('install_pythonnet', )

def install_pythonnet():
    packages = [package.name.lower() for package in iter_modules()]

    if not 'pythonnet' in packages:
        Popen(['pip', 'install', '--pre', 'pythonnet'])

    return None