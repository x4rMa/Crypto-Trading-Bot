import json
from create_folders import Folder


class ReadJson:
    def __init__(self):
        self.data = {}

    def cleanupjson(self, jsonfile):
        # Code for cleaning up JSON file
        with open(jsonfile, "r") as f:
            s = f.read()
            s = s.replace("\t", "")
            s = s.replace("\n", "")
            s = s.replace(",}", "}")
            s = s.replace(",]", "]")
            data = json.loads(s)
            return data

    def readbalance(self):
        # Code for reading JSON file
        self.data = self.readbalancefile()
        for key, value in self.data.items():
            if key == "acc_balance":
                acc_balance = float(value)
                return acc_balance

    def readbalancefile(self):
        # Code for reading JSON file
        file_path = Folder().create_folder_link("JsonFiles", "balance.json")
        data = self.cleanupjson(file_path)
        return data

    def writebalancefile(self, data):
        # Code for writing JSON file
        file_path = Folder().create_folder_link("JsonFiles", "balance.json")
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)
