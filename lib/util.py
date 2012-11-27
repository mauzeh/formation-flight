from lib.debug import print_line as p

def list_chop(elements, n):
    """Divides list into n chunks. The last chunk may be smaller."""
    
    n = min(n, len(elements))
    chunk_size = len(elements) / n
    
    p('list_size=%s,chunk_count=%s, chunk_size=%s' %\
      (len(elements), n, chunk_size))
    
    chunks = []
    while len(elements) > 0:
        chunk = []
        while len(chunk) < chunk_size and len(elements) > 0:
            chunk.append(elements.pop())
        chunks.append(chunk)
    p(chunks)

    return chunks
