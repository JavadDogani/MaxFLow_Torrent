import numpy as np
from ortools.graph.python import max_flow

class MaxFlowSolver:
    def __init__(self):
        self.smf = max_flow.SimpleMaxFlow()

    def solve_max_flow(self, start_nodes, end_nodes, capacities, source, sink):
        all_arcs = self.smf.add_arcs_with_capacity(start_nodes, end_nodes, capacities)
        status = self.smf.solve(source, sink)
        return status, self.smf.optimal_flow(), self.smf.flows(all_arcs)
