from unittest import result
from entity.sensor import Sensor
from utils.math_utils import distance,clock_angle


class GoalSensor(Sensor):
    def __init__(self, name) -> None:
        super().__init__(name)
        
        self.data = None
        
    def detect(self, robot_states: dict, obstacles: list,goals:list) -> dict:
        self.data = {"results":[]}
        result = {"type":"goal","results" : []}
        for goal in goals:
            d = distance(robot_states['x'],robot_states['y'],goal.x,goal.y)
            angle = clock_angle(robot_states['vx'],robot_states['vy'],goal.x - robot_states["x"],goal.y - robot_states["y"])
            result["results"].append({"id":goal.id,"distance":d,"angle":angle,"x":goal.x,"y":goal.y})
        
        self.data['results'] = result
        return result
            
            
            
            
        