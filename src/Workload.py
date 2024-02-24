from dataclasses import dataclass
from functools import cached_property

@dataclass
class Workload:
    compute_req: float  # Total floating point operations
    mem_movement_req: float  # Total bytes to move to/from memory
    units_of_work: str  # description of workload output
    line: str  # line type for plotting
    point: str  # point type for plotting
        
    @cached_property
    def op_intensity(self) -> float:  # FLOPs/byte
        return self.compute_req / self.mem_movement_req
