import json


class Recorder:
    def __init__(self) -> None:
        self.container = {}


    def add_record(self,label,data):
        if label not in self.container:
            self.container[label] = []
        self.container[label].append(data)

    def get_record(self,label):
        if label not in self.container:
            return None
        else:
            return self.container[label]

    def save(self,path):
        with open(path,'w') as f:
            json.dump(self.container,f)
    
    def load(self,path):
        with open(path,'r') as f:
            self.container = json.load(f)