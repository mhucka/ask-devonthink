'''
ask-devonthink: ask DEVONthink for specific attribute values of selected items

Authors
-------

Michael Hucka <mhucka@caltech.edu> -- Caltech Library

Copyright
---------
Copyright (c) 2020 by Michael Hucka and the California Institute of Technology.
This code is open-source software released under the MIT license.  Please see
the file "LICENSE" for more information.
'''

# Package metadata ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#  ╭────────────────────── Notice ── Notice ── Notice ─────────────────────╮
#  |    The following values are automatically updated at every release    |
#  |    by the Makefile. Manual changes to these values will be lost.      |
#  ╰────────────────────── Notice ── Notice ── Notice ─────────────────────╯

__program__     = 'ask-devonthink'
__version__     = '0.0.1'
__description__ = 'Ask DEVONthink for specific attribute values of selected items'
__url__         = 'https://github.com/mhucka/ask-devonthink'
__author__      = 'Michael Hucka'
__email__       = 'mhucka@caltech.edu'
__license__     = 'BSD 3-clause'


# Miscellaneous utilities.
# .............................................................................

def print_version():
    print(f'{__program__} version {__version__}')
    print(f'Authors: {__author__}')
    print(f'URL: {__url__}')
    print(f'License: {__license__}')


# For Emacs users
# .............................................................................
# Local Variables:
# mode: python
# python-indent-offset: 4
# End:
