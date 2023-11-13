import json
import numpy as np
from ortools.graph.python import max_flow

class NetworkConstruction:
    def __init__(self, json_file):
        self.smf = max_flow.SimpleMaxFlow()
        self.json_file = json_file
        self.all_arcs = None
        self.network_info = self.load_network_from_json()

    def load_network_from_json(self):
        with open(self.json_file, 'r') as f:
            network_info = json.load(f)
        return network_info

    def create_network(self):
        start_nodes = self.network_info["start_nodes"]
        end_nodes = self.network_info["end_nodes"]
        capacities = self.network_info["capacities"]
        
        # Create a mapping between all unique node labels
        all_node_labels = set(start_nodes + end_nodes)
        node_label_to_id = {label: i for i, label in enumerate(all_node_labels)}
        
        # Map node labels to integer IDs in start_nodes and end_nodes
        start_node_ids = [node_label_to_id[label] for label in start_nodes]
        end_node_ids = [node_label_to_id[label] for label in end_nodes]
        
        self.all_arcs = self.smf.add_arcs_with_capacity(np.array(start_node_ids), np.array(end_node_ids), np.array(capacities))

    def modify_capacity(self, source, destination, new_capacity):
        for i, arc in enumerate(self.all_arcs):
            if self.smf.tail(arc) == source and self.smf.head(arc) == destination:
                self.smf.set_arc_capacity(arc, new_capacity)
                self.network_info["capacities"][i] = new_capacity
                print(f"Modified capacity of arc {source} to {destination} to {new_capacity}")
                return
        print(f"No arc found between source {source} and destination {destination}")

    def get_network_info(self):
        return self.network_info

    def solve_max_flow(self, source, sink):
        status = self.smf.solve(source, sink)
        return status, self.smf.optimal_flow(), self.smf.flows(self.all_arcs)
