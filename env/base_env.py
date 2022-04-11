import json
from gym import Env
from pygame.sprite import Group
import pygame


class BaseNavEnv(Env):
    def __init__(self,config) -> None:
        super().__init__()
        self.config = config
        
        # stimulation parameters
        self.dt = self.config['dt'] # s
        self.width = self.config['width'] # m
        self.length = self.config['length'] # m
        self.height = self.config['height'] # m
        
        self.l_scale = 0 # m/pixel
        self.w_scale = 0 # m/pixel
        
        # display parameters
        self.is_render = self.config['is_render']
        
        if self.is_render:
            self.fps = self.config['fps'] # frames per second
            self.display_size = self.config['display_size'] # pixels
            self.screen = None
        
        
        # entities 
        self.obstacles = Group()
        self.robot = None
    
          
    def setup(self):
        self.l_scale = self.length/self.display_size[0]
        self.w_scale = self.width/self.display_size[1]
        
        if self.is_render:
            self.screen = pygame.display.set_mode(self.display_size) # set screen
        
    
    def reset(self):
        pass
    
    def step(self,action):
        pass
    
    def render(self):
        pass
    
    def close(self):
        pass
    
    def seed(self,seed):
        pass
    
    def states(self):
        pass
    
    def reward(self,*args,**kwargs):
        pass
    
    
    def save(self,path):
        file = open(path,'w')
        json.dump(self.config,file)
        return 