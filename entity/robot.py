
from pygame.sprite import Sprite
import pygame
import math
from utils.math_utils import rotate,trans_angle
from entity.manager import EntityManager
from entity.sensor import Sensor
from collections import deque

class Robot(Sprite):
    def __init__(self,config,dt,scare_trans,coord_trans) -> None:
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
        self.display_image = None
        self.rect = None

        self.coord_trans = coord_trans
        self.scare_trans = scare_trans
        
        self.sensors = {}
        self.sensor_states = {}


        self.trace = deque()
        self.display_trace = deque()
        
        self.setup()
    
    def setup(self):
        
        # appearance
        self.image = pygame.image.load(self.config['image'])
        self.image = pygame.transform.smoothscale(self.image,self.scare_trans(self.r*2,self.r*2))
        self.display_image = pygame.transform.rotate(self.image, self.theta)
        self.rect = self.display_image.get_rect()
        self.rect.center = self.coord_trans(self.x,self.y)


        for i, sensor_config in enumerate(self.config["sensor"]):
            sensor_type = sensor_config["type"]
            sensor_name = f"sensor_{sensor_type}#{i}"
            sensor = Sensor.FACTORY[sensor_type](sensor_config,sensor_name,self.scare_trans,self.coord_trans)
            self.sensors[sensor_name] = sensor


        EntityManager.register(self)
        
        
    def add_sensor(self,sensor):
        self.sensors[sensor.name] = sensor
        return
        
    def update(self):
        d_theta = math.degrees(self.omega*self.dt)
        self.vx ,self.vy = rotate(self.vx,self.vy,d_theta)
        theta_rad = math.atan2(self.vy,self.vx)
        self.theta = math.degrees(theta_rad)

        self.x  += self.v*self.dt*math.cos(theta_rad)
        self.y  += self.v*self.dt*math.sin(theta_rad)

        self.trace.append((self.x,self.y))
        self.display_trace.append(self.coord_trans(self.x,self.y))

        if len(self.trace) > 250:
            self.trace.popleft()
            self.display_trace.popleft()

        return 
        
    def move(self,v,omega):
        self.v = v
        self.omega = omega
        return
    
    def draw(self,screen):
        for sensor,sensor_instance in self.sensors.items():
            sensor_instance.draw(screen)

        if len(self.display_trace)>=2:
            pygame.draw.aalines(screen, (0, 0, 0), False, self.display_trace)
        # appearance
        self.display_image = pygame.transform.rotate(self.image, self.theta)
        self.rect = self.display_image.get_rect()
        self.rect.center = self.coord_trans(self.x,self.y)
        screen.blit(self.display_image, self.rect)




           
    @property
    def states(self):
        return {'x':self.x,'y':self.y,'r':self.r,'theta':self.theta,"vx":self.vx,"vy":self.vy,"v":self.v,"omega":self.omega}
        
    def detect(self,obsacles:list,goals:list)-> dict:
        results = {}
        for sensor,sensor_instance in self.sensors.items():
            results[sensor] = sensor_instance.detect(self.states,obsacles,goals)
            self.sensor_states[sensor] = sensor_instance.data
        return results
        
        
        
        
    