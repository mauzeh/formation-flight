"""Contains functions to easily verbosely print variables.""" 

# Which severities can we print? Default to all
print_severities = [
    'notice',
    'critical'
]

# output table width (in chars)
width = 80

def print_table(headers = [], messages = []):

    assert len(headers) > 0 or len(messages) > 0

    print '%s%s%s' % ('+','-'*(width-2),'+')
    lines = []
    if len(headers) > 0:
        for datum in headers:
            lines.append('| % 25s: %s' % (datum[0], datum[1]))
        for line in lines:
            line_len = len(line)
            end_line = '' if line_len >= width else "|"
            print line + ' ' * (width - line_len - 1) + end_line
        print '%s%s%s' % ('+','-'*(width-2),'+')
    
    lines = []
    if len(messages) > 0:
        for datum in messages:
            lines.append('| % 25s: %s' % (datum[0], datum[1]))
        for line in lines:
            line_len = len(line)
            end_line = '' if line_len >= width else "|"
            print line + ' ' * (width - line_len - 1) + end_line
        print '%s%s%s' % ('+','-'*(width-2),'+')

def print_dictionary(dictionary):

    lines = []
    for key in sorted(dictionary.iterkeys()):
        lines.append((key, dictionary[key]))

    headers = [('Dictionary', '%d element(s)' % len(dictionary))]
    print_table(headers, lines)

def print_object(obj, headers = []):

    lines = []

    if len(headers) == 0:
        headers.append(('Object', obj.__class__.__name__))
    
    try:
        # Define this method if you want to customize the debug output
        lines = obj.get_debug_lines()
    except AttributeError:
        # Otherwise the dict will be printed
        lines = []
        for key in obj.__dict__:
            lines.append((key, obj.__dict__[key]))
    print_table(headers, lines)

# Ugly, but really handy
#import sim

def print_line(severity, message = None):

    if message is None:
        message = severity
        severity = 'debug'
    
    # if not in debug mode, do not print anything except severity "critical"
    if severity in print_severities:
        print 't = %4d :: %s' % (sim.time, message)
