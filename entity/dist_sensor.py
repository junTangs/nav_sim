
import math
from utils.math_utils import line_circle_cross_cal
from entity.sensor import Sensor
import pygame 


class DistSensor(Sensor):
    COLOR = (255,0,0)
    def __init__(self,theta,max_distance,name,l_scare,w_scare) -> None:
        super().__init__(name)
        self.theta = theta
        self.max_distance = max_distance # m
        self.data = None
        self.l_scare = l_scare
        self.w_scare = w_scare
        
        


    def detect(self,robot_states:dict,obstacles:list) -> dict:
        x,y,r,theta = robot_states['x'],robot_states['y'],robot_states['r'],robot_states['theta']
        theta =+ self.theta
        
        results = 1e10
        for obstacle in obstacles:
            x_obs,y_obs,r_obs = obstacle.x,obstacle.y,obstacle.r
            d = line_circle_cross_cal(x,y,math.cos(theta),math.sin(theta),x_obs,y_obs,r_obs)
            if d != -1 and d < self.max_distance and d <= results:
                results = d
        
        results /= self.max_distance
        results = results if results <= 1 else 1
        self.data = {"x":x,"y":y,"r":r,"theta":theta,"results":results}
        return {"results":results,"theta":theta,"type":"dist"}
    

    def draw(self,screen):
        x1 = self.data['x']*self.l_scare
        y1 = self.data['y']*self.w_scare
        x2 = x1 + self.data['results']*self.max_distance*math.cos(self.data['theta'])*self.l_scare
        y2 = y1 + self.data['results']*self.max_distance*math.sin(self.data['theta'])*self.w_scare
        pygame.draw.line(screen,self.COLOR,(x1,y1),(x2,y2),1)
        