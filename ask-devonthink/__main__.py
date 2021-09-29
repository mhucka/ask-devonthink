# TODO
# - add option to complain if requested field doesn't exist
# - accept a uuid or reference url on stdin, in which case, don't get selection
#   https://stackoverflow.com/questions/3762881/how-do-i-check-if-stdin-has-some-data


# See http://appscript.sourceforge.net/py-appscript/doc/osax-manual/04_notes.html
# for info about using OSAX

# Note: this code uses lazy loading.  Additional imports are made below.
import sys
from .__init__ import print_version, __program__


# Main body.
# .............................................................................

def main():
    '''Ask DEVONthink for metadata values of selected items.'''

    # Process arguments & handle early exits ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    if len(sys.argv) == 1:
        # If no args are given, we can't know if we should show dialogs or use
        # stdout for error messages.  Just we quit without saying anything.
        sys.exit(2)

    (help, print0, no_gui, no_numbers, version, fields) = parsed_arguments([
        ('-h', '--help', 'Print program help text and exit'),
        ('-0', '--print0', 'Terminate values with NUL instead of newline'),
        ('-g', '--no-gui', 'Do not use macOS GUI dialogs'),
        ('-n', '--no-index-numbers', 'Do not print index numbers'),
        ('-V', '--version', 'Print the program version info and exit'),
    ])

    if help:
        print(main.__doc__)
        sys.exit(0)

    if version:
        print_version()
        sys.exit(0)

    if not fields:
        fatal(f'Must name the metadata field(s) to request from DEVONthink.', no_gui)

    # Ask DEVONthink for the selection(s) ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    import appscript
    devonthink = appscript.app('DEVONthink 3')
    if not devonthink.isrunning():
        fatal('DEVONthink is not running', no_gui, use_system = True)
    windows = devonthink.think_window()
    if not windows:
        fatal(f'Could not get window info from DEVONthink.', no_gui)
    if len(windows) < 1:
        fatal(f'There are no DEVONthink windows open.', no_gui)
    front_window = windows[0]
    try:
        selected_docs = front_window.selection()
    except appscript.CommandError as ex:
        selected_docs = None
    if not selected_docs:
        fatal("There is no selection in DEVONthink's front window.", no_gui)

    # Loop through selections and print values ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # FIXME handle custom metadata:
    #   get it via custom_meta_data from Dt -- it comes back as json
    #   let user specify "mdcitekey" & interpret it as custom field "citekey"
    #   make sure to document that user has to look in Dt "identifier" to get correct field name
    #     eg my "location" is actually "page" bc I renamed it at some point

    with_number = (len(selected_docs) > 1) and not no_numbers
    line_ending = chr(0) if print0 else '\n'
    for index, selected in enumerate(selected_docs):
        for field in fields:
            if not hasattr(selected, field):
                continue
            attribute = getattr(selected, field)
            if isinstance(attribute, appscript.reference.Reference):
                value = attribute()
                prefix = f'{index}: ' if with_number else ''
                print(f'{prefix}{value}', end = line_ending, flush = True)


# Miscellaneous helpers.
# .............................................................................

def parsed_arguments(options):
    # Sanity check the options given on the command line.
    valid_options = [value for triple in options for value in triple[0:2]]
    if any(arg.startswith('-') and arg not in valid_options for arg in sys.argv[1:]):
        fatal(f'Unrecognized option in command line.')

    # Construct True/False liste based on whether corresponding option is given.
    values = []
    for index, opt in enumerate(options):
        # True if the arg is in argv, in the order the arg appears in options.
        opt_present = any(arg in [opt[0], opt[1]] for arg in sys.argv[1:])
        values.append(opt_present)

    # Values that are not recognized as options are assumed to be field names.
    fields = [arg for arg in sys.argv[1:] if not arg.startswith('-')]
    return values + ([fields] if fields else [None])


def alert(msg, no_gui, use_system = False):
    if no_gui:
        print('‼️  ' + msg)
    else:
        from osax import OSAX
        sa = OSAX("StandardAdditions",
                  name = "System Events" if use_system else "DEVONthink 3")
        sa.activate()
        sa.display_alert(__program__, buttons = ["OK"], message = msg)


def fatal(msg, no_gui, use_system = False):
    alert(msg, no_gui, use_system)
    sys.exit(1)


# Main entry point.
# .............................................................................

# The following entry point definition is for the console_scripts keyword
# option to setuptools.  The entry point for console_scripts has to be a
# function that takes zero arguments.
def console_scripts_main():
    main()

# The following allows users to invoke this using "python3 -m ask-devonthink".
if __name__ == '__main__':
    main()


# For Emacs users
# .............................................................................
# Local Variables:
# mode: python
# python-indent-offset: 4
# End:
