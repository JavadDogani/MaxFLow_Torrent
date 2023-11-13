import os
from network_construction import NetworkConstruction
from max_flow_solver import MaxFlowSolver
from idtoLabelExchange import IdtoLabelExchange
from graph_visualization import GraphVisualization
from jsontoflowarray import JsonToNetworkStructure
def main():
    Torrent2Network_convertor=JsonToNetworkStructure("torrent.json")
    Torrent2Network_convertor.Run()
    convert_data=IdtoLabelExchange()
    convert_data.convert()
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the script
    json_file = os.path.join(script_dir, "output.json")  # Construct the full path to the JSON file

    network_builder = NetworkConstruction(json_file)
    max_flow_solver = MaxFlowSolver()
    graph_visualizer = GraphVisualization()
    
    network_builder.create_network()
    a= network_builder.get_network_info()

    start_nodes=a["start_nodes"]
    end_nodes=a["end_nodes"]
    capacities=a["capacities"]
    
    # Modify the capacity of the arc between nodes 0 and 2 to 25
    #network_builder.modify_capacity(0, 2, 25)

    # Solve the max flow problem
    source, sink = convert_data.get_Id_by_Label("Source"),convert_data.get_Id_by_Label("Sink")
    status, max_flow, solution_flows = network_builder.solve_max_flow(source, sink)

    if status != network_builder.smf.OPTIMAL:
        print("There was an issue with the max flow input.")
        print(f"Status: {status}")
        exit(1)
    print("Max flow:", max_flow)
    print("\nArc    Flow / Capacity")
    for arc, flow, capacity in zip(network_builder.all_arcs, solution_flows, network_builder.network_info["capacities"]):
        print(convert_data.get_Label_by_Id(network_builder.smf.tail(arc)),"/", convert_data.get_Label_by_Id(network_builder.smf.head(arc)) ,"  ",flow ," / ",capacity)
    print("Source side min-cut:", network_builder.smf.get_source_side_min_cut())
    print("Sink side min-cut:", network_builder.smf.get_sink_side_min_cut())

    graph_visualizer.visualize_graph(network_builder, source, sink)  # Pass source and sink

    print("____________________")
    Torrent2Network_convertor.Run()

    #print (Torrent2Network_convertor.are_neighbors("Node_1", "Node_2"))

if __name__ == "__main__":
    main()

