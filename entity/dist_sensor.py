
import math
from nav_sim.utils.math_utils import line_circle_cross_cal,trans_angle
from nav_sim.entity.sensor import Sensor
import pygame 


class DistSensor(Sensor):
    COLOR = (123,123,123)
    def __init__(self,config,name,scare_trans,coord_trans) -> None:
        super().__init__(name)
        self.theta = config["theta"]
        self.max_distance = config["max_distance"] # m
        self.data = None
        self.scare_trans = scare_trans
        self.coord_trans = coord_trans


    def detect(self,robot_states:dict,obstacles:list,humans:list,goals:list) -> dict:
        x,y,r,theta = robot_states['x'],robot_states['y'],robot_states['r'],robot_states['theta']
        theta += self.theta
        theta = trans_angle(theta)

        
        results = self.max_distance
        for obstacle  in obstacles:
            x_obs,y_obs,r_obs = obstacle.x,obstacle.y,obstacle.r
            d = line_circle_cross_cal(x,y,math.cos(math.radians(theta)),math.sin(math.radians(theta)),x_obs,y_obs,r_obs)

            if d != -1 and d < self.max_distance and d <= results:
                results = d

        for human in humans:
            x_h, y_h, r_h = human.x, human.y, human.r
            d = line_circle_cross_cal(x,y,math.cos(math.radians(theta)),math.sin(math.radians(theta)),x_h,y_h,r_h)
            if d != -1 and d < self.max_distance and d <= results:
                results = d



        results = min(self.max_distance,results)
        results = max(0,results)

        self.data = {"x":x,"y":y,"r":r,"theta":theta,"results":results}
        return {"results":results,"theta":theta,"type":"dist"}
    

    def draw(self,screen):

        x1,y1 = self.coord_trans(self.data["x"],self.data["y"])
        x2 = self.data["x"] + self.data["results"]*self.max_distance*math.cos(math.radians(self.data["theta"]))
        y2 = self.data["y"] + self.data["results"]*self.max_distance*math.sin(math.radians(self.data["theta"]))
        x2,y2 = self.coord_trans(x2,y2)
        pygame.draw.aaline(screen,self.COLOR,(x1,y1),(x2,y2),10)
        pygame.draw.circle(screen,self.COLOR,(x2,y2),5)

Sensor.FACTORY["dist"] = DistSensor