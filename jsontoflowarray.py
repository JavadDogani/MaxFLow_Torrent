import json
import networkx as nx
from network_construction import NetworkConstruction
from max_flow_solver import MaxFlowSolver
from graph_visualization import GraphVisualization

class JsonToNetworkStructure:
    def __init__(self, json_file):
        self.json_file = json_file
        self.network = nx.DiGraph()
        self.start_nodes = []
        self.end_nodes = []
        self.capacities = []
        self.data=None
        self.c1=[]
    def load_network_data(self):
        with open(self.json_file, 'r') as f:
            self.data = json.load(f)
            return self.data

    def build_network(self):
        self.data = self.load_network_data()
        nodes = self.data['nodes']
        chunks = self.data['chunks']
        uplink_capacities = self.data['uplink_capacities']
        downlink_capacities = self.data['downlink_capacities']
        chunks_by_node = self.data['chunks_by_node']
        self.c1= chunks_by_node= self.data['chunks_by_node']

        # Create nodes in the network
        for node in range(nodes):
            self.network.add_node(f'{node}', capacity=uplink_capacities[node])

        # Create chunks
        for chunk in range(chunks):
            self.network.add_node(f'{chunk}')

        # Create links from source (stage 1) to nodes (stage 2)
        for node in range(nodes):
            self.network.add_edge('Source', f'Node_{node}', capacity=downlink_capacities[node])

        # Create links from nodes (stage 2) to chunks (stage 3)
        for node in range(nodes):
            for chunk in range(chunks):
                if chunk not in chunks_by_node[f'Node_{node}']['chunks']:
                    self.network.add_edge(f'Node_{node}', f'Chunk_{chunk}', capacity=1)

        # Create links from chunks (stage 3) to nodes (stage 4)
        for node in range(nodes):
            node_key = f'Node_{node}'
            if node_key in chunks_by_node:
                for chunk in chunks_by_node[node_key]['chunks']:
                    self.network.add_edge(f'Chunk_{chunk}', 'd'+node_key, capacity=uplink_capacities[node])

        # Create links from nodes (stage 4) to sink (stage 5)
        for node in range(nodes):
            self.network.add_edge(f'dNode_{node}', 'Sink', capacity=uplink_capacities[node])


    def get_edge_info(self):
        for edge in self.network.edges(data=True):
            u, v, attr = edge
            self.start_nodes.append(u)
            self.end_nodes.append(v)
            self.capacities.append(attr['capacity'])
    
    def are_neighbors(self, node1, node2):
        #self.data = self.load_network_data()
        print("111")
        #chunks_by_node = self.data['chunks_by_node']
        # Check if node1 is in the neighborhood of node2 or vice versa
        print("222")
        if node2 not in self.c1[f'Node_{node1}']['neighborhood']:
            return True    
        else:
            return False
# Example usage
    def Run(self):
        import os
        script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the script
        file = os.path.join(script_dir, self.json_file)  # Construct the full path to the JSON filenetwork_structure_builder = JsonToNetworkStructure(json_file)
        #print (json_file)
        network_structure_builder = JsonToNetworkStructure(file)
        network_structure_builder.build_network()
        network_structure_builder.get_edge_info()
        start_nodes, end_nodes, capacities = network_structure_builder.start_nodes, network_structure_builder.end_nodes, network_structure_builder.capacities
        import json

        # ... (the previous code)

        # Save the result arrays to a JSON file
        network_result = {
            "start_nodes": start_nodes,
            "end_nodes": end_nodes,
            "capacities": capacities
        }
        script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the script
        file = os.path.join(script_dir, "network.json")  # Construct the full path to the JSON filenetwork_structure_builder = JsonToNetworkStructure(json_file)

        with open(file, "w") as f:
            json.dump(network_result, f)
