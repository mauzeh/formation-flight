"""Captures data and puts it into data/output.tsv"""
import csv
from lib import sim
import os
import errno
from datetime import datetime

writer = None

# Only print the header once. Useful when calling the sink multiple times.
print_header = True

def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
        
def force_symlink(source, target):
    try:
        os.symlink(source, target)
    except OSError, e:
        if e.errno != errno.EEXIST:
            raise
        os.remove(target)
        os.symlink(source, target)

def init(directory):
    
    path = '%s/sink/%s.tsv' % (
        directory,
        datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )

    global writer
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

