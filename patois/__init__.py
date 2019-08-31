from __future__ import absolute_import, unicode_literals

import sys

if 'install' not in sys.argv \
        and 'egg_info' not in sys.argv \
        and 'init' not in sys.argv\
        and 'bdist_wheel' not in sys.argv:

    from .patois import Patois

__version__ = '0.4.0'
__author__ = 'Henri Blancke'
__email__ = 'blanckehenri@gmail.com'
