from lib.debug import print_line as p
import os, errno
import csv

def tsv_get_column_index(data_file, column_name):

    rows = csv.reader(open(data_file, 'rb'), delimiter = "\t")
    for row in rows:
        for column in row:
            if column_name == column:
                return row.index(column)
        break

def force_symlink(source, target):
    try:
        os.symlink(source, target)
    except OSError, e:
        if e.errno != errno.EEXIST:
            raise
        os.remove(target)
        os.symlink(source, target)

def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def round_float(number, base = 30):
    return int(base * round(float(number) / base))

def list_chop(elements, n):
    """Divides list into n chunks. The last chunk may be smaller."""
    
    n = min(n, len(elements))
    chunk_size = len(elements) / n
    
    #p('list_size=%s,chunk_count=%s, chunk_size=%s' %\
    #  (len(elements), n, chunk_size))
    
    chunks = []
    while len(elements) > 0:
        chunk = []
        while len(chunk) < chunk_size and len(elements) > 0:
            chunk.append(elements.pop())
        chunks.append(chunk)

    return chunks
