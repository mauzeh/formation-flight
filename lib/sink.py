"""Captures data and puts it into data/output.tsv"""
import csv
from lib import sim
from lib.util import make_sure_path_exists, force_symlink
import os
import errno
from datetime import datetime

writer = None

# Only print the header once. Useful when calling the sink multiple times.
print_header = True

def init(directory):
    
    path = '%s/%s.tsv' % (
        directory,
        datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )
    
    print "Sinking to %s" % path

    global writer, print_header
    print_header = True
    make_sure_path_exists(os.path.dirname(path))
    writer = csv.writer(open(path, 'w'), delimiter = '\t')
    
    # Update the symlink to point to the latest data file
    force_symlink(
        path,
        '%s/latest.tsv' % os.path.dirname(path)
    )

def push(dictionary):
    global print_header, writer
    if print_header == True:
        writer.writerow(dictionary.keys())
    writer.writerow(dictionary.values())
    print_header = False

