# Returns the roof value as a throughput (units of work X per second).
def roof(op_intensity: float,  # FLOPs/byte
         compute: float,  # FLOPs/sec
         mem_bw: float,  # bytes/sec
         compute_req: float) -> float:  # FLOPs/X; X/sec
    # Compute X/sec = (FLOPs/sec) / (FLOPs/X)
    compute_roof = compute / compute_req
    # Memory X/sec = (FLOPs/byte) * (bytes/sec) / (FLOPs/X)
    mem_roof = op_intensity * mem_bw / compute_req
    return min(compute_roof, mem_roof)
