import json
from abc import ABCMeta, abstractmethod
import math
from re import S
from gym import Env
from gym.spaces import Box,Discrete
from pygame.sprite import Group
import pygame
from nav_sim.utils.env_utils import collide
import numpy as np
from collections import deque
import random
from nav_sim.utils.math_utils import scare,xy_into_display
from functools import partial
from pygame.locals import *
from nav_sim.entity.manager import EntityManager
from nav_sim.utils.reward_utils import REWARD_FACTORY
from nav_sim.entity import Human

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

        # display parameters
        self.is_render = self.config['is_render']
        

        self.fps = self.config['fps'] # frames per second
        self.display_size = [self.config['display_size']['width'],self.config['display_size']['height']] # pixels
        self.screen = None
        # scare to display
        self.scare = partial(scare, src=(self.length, self.width), dst=self.display_size)
        self.coord_trans = partial(xy_into_display, display_size=self.display_size, size=(self.length, self.width))
        
        
        # entities 
        self.obstacles = Group()
        self.robot = None
        self.goals = Group()
        self.humans = Group()
        # states and action
        self.stack_frames = self.config['stack_frames']
        self.frames = None
        self.action_map = self.config['action_map']
        self.seed = self.config['seed']

        self.is_set_up = False
        
        # recoder 
        self.collide_flag = False
        self.collide_detail = None
        self.finish_flag = False

        # reward function
        self.reward_fn = None

        
        self.setup()
        
                        
    def setup(self):

        # entities
        self.obstacles = Group()
        self.robot = None
        self.goals = Group()
        self.humans = Group()

        # states and action
        self.stack_frames = self.config['stack_frames']
        self.frames = None
        self.action_map = self.config['action_map']
        self.seed = self.config['seed']

        self.is_set_up = False

        # recoder
        self.collide_flag = False
        self.collide_detail = None
        self.finish_flag = False

        self._setup()
        
        if self.is_render:
            self.screen = pygame.display.set_mode(self.display_size,HWSURFACE) # set screen
        
        init_states = self._states()
        BaseNavEnv.observation_space = Box(0,1,(self.stack_frames,len(init_states)))
        BaseNavEnv.action_space = Discrete(len(self.action_map))
        self.frames = deque([init_states]*self.stack_frames,maxlen=self.stack_frames+1)

        
        if self.seed is not None:
            random.seed(self.seed)
            np.random.seed(self.seed)

        self.reward_fn = REWARD_FACTORY[self.config["reward_fn"]]
        self.is_set_up = True
        
        
    def is_collide(self):

        results = pygame.sprite.spritecollide(self.robot,self.obstacles,False,collide)
        bound_results =  self.robot.x <= self.robot.r or self.robot.x >= self.length - self.robot.r or self.robot.y <= self.robot.r or self.robot.y >= self.width - self.robot.r

        if len(results)>0:
            return True,{"collide":"obstacle","details":results}
        if bound_results:
            return True,{"collide":"bound","details":bound_results}
        return False,None
    
    def is_reach(self):
        results = pygame.sprite.spritecollide(self.robot,self.goals,False,collide)
        return len(results) > 0,results
    
    def is_finished(self):
        self.is_reach()
        return len(self.goals) == 0
            
    def reset(self):
        EntityManager.clear()
        self.setup()
        return self.states()
    
    def is_done(self):
        if self.is_finished():
            self.finish_flag = True
            return True,"finished"
        
        collide,details = self.is_collide()
        if collide:
            self.collide_flag = True
            self.collide_detail = details
            return True,"collide"

        return False,"none"

    def step(self,action):
        
        info = {"done_info":None,"time":0,"step":0}
        
        action = self.action(action)
        self.robot.move(*action)
        
        # update states
        self.robot.update()
        for obstacle in self.obstacles:
            obstacle.update()
    
        for goal in self.goals:
            goal.update()

        Human.update()




        done,info["done_info"] = self.is_done()
        reward = self.reward()
        
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
            self.screen.fill((255,255,255))
            for obstacle in self.obstacles:
                obstacle.draw(self.screen)
            for goal in self.goals:
                goal.draw(self.screen)
            for human in self.humans:
                human.draw(self.screen)
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
        frames = [np.array(f).reshape(1,-1) for f in self.frames]
        states =  np.concatenate(frames,axis=0)
        return states
    
    @abstractmethod
    def _states(self):
        pass
    

    def reward(self,*args,**kwargs):
        return self.reward_fn(self,*args,**kwargs)
    
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
        return self.action_map[str(action)]

    def set_reward_fn(self,reward_fn:callable):
        self.reward_fn = reward_fn