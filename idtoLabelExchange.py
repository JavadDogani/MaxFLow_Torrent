import json
import os

class IdtoLabelExchange:
    def __init__(self):
        self.data = None
        self.label_to_id = {}
        self.id_to_label = {}
        self.myset = None
        script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the script
        self.json_file = os.path.join(script_dir, "network.json")  # Construct the full path to the JSON file
        self.load_from_json()
        self.convert_labels_to_ids()
    
    def convert(self):
        data1 = {
        "start_nodes": self.getIdofstartNodes(),
        "end_nodes": self.getIdofEndNodes(),
        "capacities": self.getCapacity()
        }

        # Specify the output JSON file
        venv_path = os.path.abspath('./')
        output_file = os.path.join(venv_path, "output.json")
        #output_file = "output.json"

        # Write the data to the JSON file
        with open(output_file, "w") as json_file:
            json.dump(data1, json_file)

    def convert_labels_to_ids(self):
        unique_labels = set(self.data["start_nodes"] + self.data["end_nodes"])
        
        self.label_to_id["Source"] = 0
        self.label_to_id["Sink"] = len(unique_labels) - 1
        unique_labels.discard("Source")
        unique_labels.discard("Sink")

        i = 1
        for label in unique_labels:
            self.label_to_id[label] = i
            self.id_to_label[i] = label
            i += 1
        
    def getIdofstartNodes(self):
        Start_Id = [self.get_Id_by_Label(value) for value in self.data["start_nodes"]]
        return Start_Id
    def getIdofEndNodes(self):
        end_Id = [self.get_Id_by_Label(value) for value in self.data["end_nodes"]]
        return end_Id
    
    def getLabel(self):
        Label_List = [key for key in self.label_to_id.keys()]
        return Label_List

    def get_Id_by_Label(self, key):
        if key in self.label_to_id:
            return self.label_to_id[key]
        else:
            return None

    def getCapacity(self):
        return self.data["capacities"]

    def get_Label_by_Id(self, value):
        reversed_mapping = {v: k for k, v in self.label_to_id.items()}
        return reversed_mapping.get(value)

    def load_from_json(self):
        try:
            with open(self.json_file, "r") as json_file:
                self.data = json.load(json_file)
        except FileNotFoundError:
            print(f"File '{self.json_file}' not found in the current directory.")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in '{self.json_file}'")

    


