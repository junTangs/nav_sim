from cmath import inf
import json
from abc import ABCMeta, abstractmethod
import math
from re import S, T
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
from nav_sim.utils.reward import REWARDS
from nav_sim.utils.state import STATES
from nav_sim.entity import Human
from nav_sim.utils.action import ActionXY,ActionVW
from nav_sim.entity.recorder import Recorder
import itertools

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
        self.states_wrapper = None
        self.seed = self.config['seed']
                        
        if self.seed is not None:
            random.seed(self.seed)
            np.random.seed(self.seed)

        self.speed_samples = self.config['speed_samples']
        self.rotation_samples = self.config['rotation_samples']
        self.kinematics = self.config["kinematics"]

        self.is_set_up = False

        
        # recoder 
        self.collide_flag = False
        self.collide_detail = None
        self.finish_flag = False


        # history recorder 
        self.recoder = None


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
        self.states_wrapper = STATES[self.config["state_wrapper"]](norm = self.config['is_running_norm'])


        self.is_set_up = False

        self.t = 0 # s
        self.step_count = 0

        # recoder and flag
        self.collide_flag = False
        self.collide_detail = None
        self.finish_flag = False

        self.recorder = Recorder()
        

        self._setup()
        
        if self.is_render:
            self.screen = pygame.display.set_mode(self.display_size,HWSURFACE) # set screen
        
        init_states = self._states()
        self.observation_space = Box(0,1,(self.stack_frames,len(init_states)))
        self.setup_action(self.robot.v_pref)
        self.frames = deque([init_states]*self.stack_frames,maxlen=self.stack_frames+1)


        self.reward_fn = REWARDS[self.config["reward_fn"]]()
        self.reward_fn.setup(self.goals,self.obstacles,self.humans,self.robot)
        self.is_set_up = True
        
        
    def is_collide(self):

        results = pygame.sprite.spritecollide(self.robot,self.obstacles,False,collide)
        bound_results =  self.robot.x <= self.robot.r or self.robot.x >= self.length - self.robot.r or self.robot.y <= self.robot.r or self.robot.y >= self.width - self.robot.r
        human_results = pygame.sprite.spritecollide(self.robot,self.humans,False,collide)

        if len(results)>0:
            return True,{"collide":"obstacle","details":results}
        if bound_results:
            return True,{"collide":"bound","details":bound_results}
        if len(human_results)>0:
            return True,{"collide":"human","details":human_results}
        return False,None
    
    def is_reach(self):
        results = pygame.sprite.spritecollide(self.robot,self.goals,False,collide)
        for result in results:
            result.reach()
        return len(results) > 0,results
    
    def is_finished(self):
        self.is_reach()
        goal_reach = [goal.is_reach for goal in self.goals]
        if all(goal_reach) is True:
            return True
        else:
            return False

    def reset(self):
        EntityManager.clear()
        self.setup()
        self.record()
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


    def record(self):
        # record trajectory
    
        # record robot trajectory
        wp = False if self.collide_flag else True
        data = {'x':self.robot.x,'y':self.robot.y,'t':self.t,'wp':wp}
        self.recorder.add_record("robot_trace",data)
        # record human trajectory
        for i,human in enumerate(self.humans):
            data = {'x':human.x,'y':human.y,'t':self.t,'wp':True}
            self.recorder.add_record(f"human_{i}_trace",data)
        
        

    def step(self,action):
        
        info = {"done_info":None,"time":0,"step":0}

        self.robot.move(action)
        
        # update states
        self.robot.update()
        for obstacle in self.obstacles:
            obstacle.update()
    
        for goal in self.goals:
            goal.update()

        Human.update()



        done,info["done_info"] = self.is_done()

        # update frames
        states = self._states()
        self.frames.append(states)
        self.frames.popleft()
        self.t += self.dt
        self.step_count += 1
        self.record()
        
        info["time"] = self.t
        info["step"] = self.step_count
        reward = self.reward()
        
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
          
    def states(self):
        return self.states_wrapper.wrapper(self.frames)
    
    @abstractmethod
    def _states(self):
        pass
    

    def reward(self):
        return self.reward_fn.reward(self.goals,self.obstacles,self.humans,self.robot,self.finish_flag,self.collide_flag)
    
    def save(self,path):
        file = open(path,'w')
        json.dump(self.config,file)
        return 
    
    def load(self,path):
        file = open(path,'r')
        self.config = json.load(file)
        self.__dict__.update(self.config)
        return

    def setup_action(self, v_pref):
        holonomic = True if self.kinematics == 'holonomic' else False
        speeds = [(np.exp((i + 1) / self.speed_samples) - 1) / (np.e - 1) * v_pref for i in
                  range(self.speed_samples)]
        if holonomic:
            rotations = np.linspace(0, 2 * np.pi, self.rotation_samples, endpoint=False)
        else:
            rotations = np.linspace(-np.pi / 4, np.pi / 4, self.rotation_samples)

        action_space = [ActionXY(0, 0) if holonomic else ActionVW(0, 0)]
        for rotation, speed in itertools.product(rotations, speeds):
            if holonomic:
                action_space.append(ActionXY(speed * np.cos(rotation), speed * np.sin(rotation)))
            else:
                action_space.append(ActionVW(speed, rotation))

        self.speeds = speeds
        self.rotations = rotations
        self.action_space = action_space

