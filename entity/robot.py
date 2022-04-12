
from pygame.sprite import Sprite
import pygame
import math
from utils.math_utils import rotate,trans_angle
from entity.manager import EntityManager
from entity.dist_sensor import DistSensor
from entity.goal_sensor import GoalSensor

class Robot(Sprite):
    def __init__(self,config,dt,scare) -> None:
        super().__init__()
        self.config = config
        self.x = self.config['x']
        self.y = self.config['y']
        self.r = self.config['r'] # m
        
        # inherit parameters
        self.vx = math.cos(self.config['theta'])
        self.vy = math.sin(self.config['theta'])
        self.theta = self.config['theta']
        self.v = 0 # m/s
        self.omega = 0 # rad/s
        
        self.v_max = config['v_max']
        self.v_min = config['v_min']
        self.omega_max = config['omega_max']
        self.omega_min = config['omega_min']

        self.dt = dt 
        self.image = None
        self.rect = None
        self.l_scare = scare[0] # px/m : x axis
        self.w_scare = scare[1] # px/m : y axis
        
        self.sensors = {}
        self.sensor_states = {}
        
        
        self.setup()
    
    def setup(self):
        
        # appearance
        self.image = pygame.image.load(self.config['image'])
        self.image = pygame.transform.scale(self.image,(self.r*self.l_scare,self.r*self.w_scare))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x*self.l_scare,self.y*self.w_scare)
        self.image = pygame.transform.rotate(self.image,self.theta)

        for i, sensor_config in enumerate(self.config["sensor"]):
            if sensor_config["type"] == "dist":
                self.add_sensor(DistSensor(sensor_config["theta"],sensor_config["max_distance"],"dist_#{i}",self.l_scare,self.w_scare))
            elif sensor_config["type"] == "goal":
                self.add_sensor(GoalSensor("goal_#{i}"))

        EntityManager.register(self)
        
        
    def add_sensor(self,sensor):
        self.sensors[sensor.name] = sensor
        return
        
    def update(self):
        self.theta = trans_angle(self.theta + math.degrees(self.omega*self.dt))
        self.vx = self.v*math.cos(math.radians(self.theta))
        self.vy = self.v*math.sin(math.radians(self.theta))
        self.x = self.x + self.vx*self.dt
        self.y = self.y + self.vy*self.dt
        
        # appearance
        self.rect.center = (self.x,self.y)
        self.image = pygame.transform.rotate(self.image,self.theta)
        return 
        
    def move(self,v,omega):
        self.v = v
        self.omega = omega
        return
    
    def draw(self,screen):
        screen.blit(self.image,self.rect)
        for sensor,sensor_instance in self.sensors.items():
            sensor_instance.draw(screen)

           
    @property
    def states(self):
        return {'x':self.x,'y':self.y,'r':self.r,'theta':self.theta}
        
    def detect(self,obsacles:list,goals:list)-> dict:
        results = {}
        for sensor,sensor_instance in self.sensors.items():
            results[sensor] = sensor_instance.detect(self.states,obsacles,goals)
            self.sensor_states[sensor] = sensor_instance.data
        return results
        
        
        
        
    