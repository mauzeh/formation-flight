def list_chop(points, chunk_size):
    """Divides list into chunks of chunk_size. The last chunk may be smaller."""
    
    n = chunk_size
    n = min(n, len(points));
    chunk_size = len(points) / n
    
    # Divide into equal chunks. Ignores any remaining (size % n) elements.
    origin_chunks = [list(t) for t in zip(*[iter(points)]*chunk_size)]
    
    # Add remaining elements (if any) as last chunk
    if len(points) % n > 0:
        origin_chunks.append(points[-1* (len(points) % n) :])

    return origin_chunks
