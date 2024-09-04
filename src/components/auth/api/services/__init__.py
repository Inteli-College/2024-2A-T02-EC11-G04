# Package metadata
__version__ = "1.0.0"
__author__ = "greentech"


# Packge modules, submodules and functions importing
from .auth_service import AuthService

# Defined importing for '*' wildcard
__all__ = ['AuthService']
