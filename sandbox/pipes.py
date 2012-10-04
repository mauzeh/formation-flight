# cat emulator
import sys
import csv

if __name__ == '__main__':
    for row in csv.reader(sys.stdin, delimiter = '\t'):
        print row