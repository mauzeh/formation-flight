"""
Keeps track of all events in the system and prints them for debugging
purposes.
"""

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

def print_object(obj):

    headers = []
    lines = []

    headers.append(('Object', obj.__class__.__name__))
    
    lines = []
    for key in obj.__dict__:
        lines.append((key, obj.__dict__[key]))
    print_table(headers, lines)