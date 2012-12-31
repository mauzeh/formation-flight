"""Captures data and puts it into data/output.tsv"""
import csv
from lib import sim

writer = None

# Only print the header once. Useful when calling the sink multiple times.
print_header = True

def init(filename):
    global writer
    writer = csv.writer(open(filename, 'w'), delimiter = '\t')

def push(dictionary):
    global print_header, writer
    if print_header == True:
        writer.writerow(dictionary.keys())
    writer.writerow(dictionary.values())
    print_header = False
