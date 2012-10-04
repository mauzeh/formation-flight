"""
Keeps track of all events in the system and prints them for debugging
purposes.
"""

from pydispatch import dispatcher

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