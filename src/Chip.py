from dataclasses import dataclass

@dataclass
class Chip:
    compute: float  # FLOPs/sec
    mem_bw: float  # bytes/sec
    color: str  # color type for plotting
