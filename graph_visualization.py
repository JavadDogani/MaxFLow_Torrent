import networkx as nx
import matplotlib.pyplot as plt
from idtoLabelExchange import IdtoLabelExchange
import os
class GraphVisualization:
    def visualize_graph(self, network_builder, source_label, sink_label):
        G = nx.DiGraph()
        network_info = network_builder.get_network_info()
        start_nodes = network_info["start_nodes"]
        end_nodes = network_info["end_nodes"]
        capacities = network_info["capacities"]
        solution_flows = network_builder.solve_max_flow(source_label, sink_label)[2]

        for i in range(len(start_nodes)):
            source_id = start_nodes[i]
            sink_id = end_nodes[i]
            capacity = capacities[i]
            flow = solution_flows[i]
            G.add_edge(source_id, sink_id, capacity=capacity, flow=flow)

        pos = self.custom_layout(G, source_label, sink_label)
        labels = {(u, v): f"{d['flow']} / {d['capacity']}" for u, v, d in G.edges(data=True)}
        edge_colors = [d['flow'] / d['capacity'] for u, v, d in G.edges(data=True)]

        # Set node labels for source and sink
        convert_data = IdtoLabelExchange()
        node_labels = {node_id: convert_data.get_Label_by_Id(node_id) for node_id in list(set(start_nodes + end_nodes))}

        # Adjust the font size for labels and text
        font_size = 8  # Adjust this value as needed

        nx.draw(G, pos, labels=node_labels, node_size=500, node_color='lightblue', font_size=font_size)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=font_size)
        nx.draw(G, pos, edge_color=edge_colors, edge_cmap=plt.cm.Reds, width=2.0, edge_vmin=0.0, edge_vmax=1.0)
        script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the script
        file_name = os.path.join(script_dir, "max_flow.png") 
        plt.savefig(file_name)
        plt.show()

    def custom_layout(self, G, source_label, sink_label):
        pos = {}
        levels = self.get_levels(G, source_label, sink_label)
        level_height = 1.0

        for level in levels:
            x_pos = 0 if level[0] == source_label else 2 if level[0] == sink_label else 1
            spacing = 2.0  # Adjust this spacing value
            for node in level:
                pos[node] = (x_pos, -level_height)
                x_pos += spacing
            level_height += 1

        return pos

    def get_levels(self, G, source_label, sink_label):
        levels = []
        current_level = [source_label]

        while current_level:
            next_level = []
            for node in current_level:
                neighbors = list(G.successors(node))
                next_level.extend(neighbors)
            levels.append(current_level)
            current_level = next_level

        return levels
