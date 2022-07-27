
from cgi import print_environ_usage
from pygame.sprite import Sprite
import pygame
import math
from nav_sim.utils.math_utils import rotate
from nav_sim.utils.action import ActionXY,ActionVW
from nav_sim.entity.manager import EntityManager
from nav_sim.entity.sensor import Sensor
from collections import deque

class Robot(Sprite):
    def __init__(self,config,dt,scare_trans,coord_trans) -> None:
        super().__init__()
        self.config = config
        self.x = self.config['x']
        self.y = self.config['y']
        self.r = self.config['r'] # m
        self.v_pref = self.config["v_pref"]
        
        # inherit parameters
        self.vx = 0
        self.vy = 0
        self.theta = self.config['theta']
        self.v = 0 # m/s
        self.omega = 0 # rad/s
        
        self.last_vx = 0
        self.last_vy = 0
        self.last_theta = 0


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

        self.agent_id = 0

        
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
        self.x  += self.vx*self.dt
        self.y  += self.vy*self.dt
        

        
        self.trace.append((self.x,self.y))
        self.display_trace.append(self.coord_trans(self.x,self.y))

        if len(self.trace) > 250:
            self.trace.popleft()
            self.display_trace.popleft()

        return 
        
    def move(self,action):
        if isinstance(action,ActionXY):
            self.vx = action.vx
            self.vy = action.vy
            self.theta = math.degrees(math.atan2(self.vy,self.vx))
            self.v = self.vx**2 + self.vy**2
            self.omega = self.theta - self.last_theta
        else:
            theta =  math.radians(self.theta) + action.w
            self.omega = action.w
            self.v  = action.v
            self.vx = self.v * math.cos(theta)
            self.vy = self.v * math.sin(theta)
            self.theta = math.degrees(theta)

        self.last_vx = self.vx
        self.last_vy = self.vy 
        self.last_theta = self.theta
        
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
        return {'x':self.x,'y':self.y,'r':self.r,'theta':self.theta,"vx":self.vx,"vy":self.vy,"v":self.v,"omega":self.omega,"v_pref":self.v_pref}
        
    def detect(self,obsacles:list,humans:list,goals:list)-> dict:
        results = {}
        for sensor,sensor_instance in self.sensors.items():
            results[sensor] = sensor_instance.detect(self.states,obsacles,humans,goals)
            self.sensor_states[sensor] = sensor_instance.data
        return results
        
        
        
        
    