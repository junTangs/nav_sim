import json
from abc import ABCMeta, abstractmethod
import math
from gym import Env
from gym.spaces import Box,Discrete
from pygame.sprite import Group
import pygame
from utils.env_utils import collide
import numpy as np
from collections import deque
import random

class BaseNavEnv(Env,metaclass = ABCMeta):
    def __init__(self,config) -> None:
        super().__init__()
        self.config = config
        
        # stimulation parameters
        self.dt = self.config['dt'] # s
        self.t = 0 # s
        self.step_count = 0
        self.width = self.config['width'] # m:y
        self.length = self.config['length'] # m:x 
        self.max_distance = math.sqrt(self.width**2+self.length**2)
    
        
        self.l_scale = 0 # px/m
        self.w_scale = 0 # px/m
        
        # display parameters
        self.is_render = self.config['is_render']
        
        if self.is_render:
            self.fps = self.config['fps'] # frames per second
            self.display_size = [self.config['display_size']['width'],self.config['display_size']['height']] # pixels
            self.screen = None
        
        
        # entities 
        self.obstacles = Group()
        self.robot = None
        self.goals = Group()
        
        # states and action
        self.stack_frames = self.config['stack_frames']
        self.frames = None
        self.action_map = self.config['action_map']
        self.seed = self.config['seed']

        self.is_set_up = False
        
        # recoder 
        self.collide_flag = False
        self.collide_detail = None

        
        self.setup()
                        
    def setup(self):
        self.l_scale = self.display_size[0]/self.length
        self.w_scale =self.display_size[1]/self.width
        
        if self.is_render:
            self.screen = pygame.display.set_mode(self.display_size) # set screen
        
        init_states = self._states()
        BaseNavEnv.observation_space = Box(0,1,(self.stack_frames,len(init_states)))
        BaseNavEnv.action_space = Discrete(len(self.action_map))
        self.frames = deque([init_states]*self.stack_frames,maxlen=self.stack_frames)
        
        if self.seed is not None:
            random.seed(self.seed)
            np.random.seed(self.seed)

        self._setup()
        self.is_set_up = True
        
        
    def is_collide(self):

        results = pygame.sprite.spritecollide(self.robot,self.obstacles,False,collide)
        bound_results =  self.robot.x <= self.root.r or self.robot.x >= self.length - self.root.r or self.robot.y <= self.root.r or self.robot.y >= self.width - self.root.r
    
        if len(results)>=0:
            return True,{"collide":"obstacle","details":results}
        if bound_results:
            return True,{"collide":"bound","details":bound_results}
        return False,None
    
    def is_reach(self):
        results = pygame.sprite.spritecollide(self.robot,self.goals,True,collide)
        return len(results) > 0,results
    
    def is_finished(self):
        self.is_reach()
        return len(self.goals) == 0
            
    def reset(self):
        self.setup()
        return self.states()
    
    def is_done(self):
        if self.is_finished():
            return True,"finished"
        
        collide,details = self.is_collide()
        if collide:
            self.collide_flag = True
            self.collide_detail = details
            return True,"collide"

    def step(self,action):
        
        info = {"done_info":None,"time":0,"step":0}
        
        action = self.action(action)
        self.robot.move(action)
        
        # update states
        self.robot.update()
        for obstacle in self.obstacles:
            obstacle.update()
    
        for goal in self.goals:
            goal.update()
        
        done,info["done_info"] = self.is_done()
        
        reward = self.reward(self)
        
        # update frames
        self.frames.append(self._states())
        self.frames.popleft()
        self.t += self.dt
        self.step_count += 1
        
        info["time"] = self.t
        info["step"] = self.step_count
        
        return self.states(),reward,done,info
    

    def _setup(self):
        pass
        
    def render(self,mode = 'human'):
        if self.is_render:
            self.screen.fill((0,0,0))
            for obstacle in self.obstacles:
                obstacle.draw(self.screen)
            for goal in self.goals:
                goal.draw(self.screen)
            self.robot.draw(self.screen)
            if mode == "human":
                pygame.display.flip()
            elif mode == 'rgb_array':
                return pygame.surfarray.array3d(self.screen)
             
    def close(self):
        pygame.quit()
          
    def seed(self,seed):
        self.seed = seed
    
    def states(self):
        return np.concatenate(self.frames,axis=0)
    
    @abstractmethod
    def _states(self):
        pass
    
    @abstractmethod
    def reward(self,*args,**kwargs):
        pass
    
    def save(self,path):
        file = open(path,'w')
        json.dump(self.config,file)
        return 
    
    def load(self,path):
        file = open(path,'r')
        self.config = json.load(file)
        self.__dict__.update(self.config)
        return
    
    
    def action(self,action):
        return self.action_map[action]