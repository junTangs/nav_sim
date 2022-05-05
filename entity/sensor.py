from abc import ABCMeta, abstractmethod



class Sensor(metaclass = ABCMeta):
    FACTORY = {}
    def __init__(self,name) -> None:
        self.name = name
    
    @abstractmethod
    def detect(self,robot_states:dict,obstacles:list,humans:list,goals:list)->dict:
        pass
    
    
    
    def load(self,config:dict):
        self.__dict__.update(config)
        return

    def draw(self,screen):
        pass