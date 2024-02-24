import roof_util
import Chip as c
import Workload as w
import matplotlib.pyplot as plt
import itertools
import numpy as np
from typing import Dict
from prettytable import PrettyTable

def plot_roofline(compute: float,  # FLOPs/sec
                  mem_bw: float,  # bytes/sec
                  compute_req: float,  # FLOPs
                  color,
                  line,
                  linewidth,
                  xbase: float,
                  xbound: float):
    xs = np.logspace(xbase, xbound, num=200, endpoint=True, base=2, dtype=float, axis=0)
    ys = [roof_util.roof(op_intensity, compute, mem_bw, compute_req) for op_intensity in xs]
    plt.plot(xs, ys, f"{color}{line}", linewidth=linewidth)
    
def plot_workload(op_intensity: float,  # FLOPs/byte
                  throughput: float,  # work/sec
                  color,
                  point):
    plt.plot(op_intensity, throughput, f"{color}{point}", markersize=15)

def plot_scenario(chips: Dict[str, c.Chip],
                  workloads: Dict[str, w.Workload],
                  title: str,
                  xbase: float = 7,
                  xbound: float = 16):
    fig, ax = plt.subplots()
    # Rooflines
    for chip_name, chip in chips.items():
        for workload_name, workload in workloads.items():   
            plot_roofline( 
                compute=chip.compute,
                mem_bw=chip.mem_bw,
                compute_req=workload.compute_req,
                color=chip.color,
                line=workload.line,
                linewidth=1.0,
                xbase=xbase,
                xbound=xbound,
            )

    # Points
    units_of_work = list(workloads.values())[0].units_of_work
    results_table = PrettyTable(["Workload", "Chip", f"Throughput ({units_of_work}/sec)", "Operational Intensity (FLOPs/byte)"])
    results_table.align["Workload"] = "l"

    for chip_name, chip in chips.items():
        for workload_name, workload in workloads.items():   
            if workload.units_of_work != units_of_work:
                raise ValueError(f"Workload {workload_name} has units of work {workload.units_of_work} but expected {units_of_work}")

            throughput = roof_util.roof(
                op_intensity=workload.op_intensity,
                compute=chip.compute,
                mem_bw=chip.mem_bw,
                compute_req=workload.compute_req,
            )
            plot_workload(
                op_intensity=workload.op_intensity,
                throughput=throughput,
                color=chip.color,
                point=workload.point,
            )
            units_of_work = workload.units_of_work
            results_table.add_row([workload_name, chip_name, f"{throughput:.2f}", f"{workload.op_intensity:.2f}"])

    print(results_table)

    # Plot formatting
    plt.xlabel("Operational Intensity (FLOPs/byte)")
    plt.ylabel(f"Throughput ({units_of_work}/sec)")
    plt.title(title)
    ax.set_xscale("log", base=10)
    ax.set_yscale("log", base=10)
    roofline_legend = list(itertools.product(list(chips.keys()), list(workloads.keys())))
    point_legend = roofline_legend
    plt.legend(roofline_legend + point_legend)
    plt.grid(which="both")
    fig.set_figwidth(10)
    fig.set_figheight(15)
    plt.show()
