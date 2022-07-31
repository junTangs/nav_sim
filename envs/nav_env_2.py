
from cmath import pi
import math
from re import S
from wsgiref.validate import validator
from nav_sim.envs.nav_env_1 import NavEnvV1
import json
from nav_sim.entity import Robot
from nav_sim.entity import Goal
from nav_sim.entity import Obstacle
from nav_sim.entity import Human
import random
from nav_sim.utils.math_utils import distance, clock_angle, norm
import pygame
from nav_sim.utils.env_utils import collide

class NavEnvV2(NavEnvV1):
    def __init__(self, config):
        super(NavEnvV2, self).__init__(config)

        
    def _setup_robot(self):
        # steup robot
        robot_config_path = self.config['robot_config_path']
        robot_config = json.load(open(robot_config_path))
        robot = Robot(robot_config, self.dt, self.scare, self.coord_trans)

        robot.x = 1
        robot.y = self.width//2

        robot.theta = 0
        self.robot = robot

    def _setup_obstacles(self):
        # setup obstacles
        # default obs config 
        obstacle_config = {
            "x":0,
            "y": 0,
            "r": 1,
            "image": "nav_sim/images/obstacle.png",
            "is_random": False
        }


        for i in range(0):
            obstacle = Obstacle(obstacle_config, self.dt,
                                self.scare, self.coord_trans)

            try_cnt = 0
            while (try_cnt != 10000):
                obstacle.x = random.uniform(0, self.length)
                obstacle.y = random.uniform(0, self.width)

                if distance(obstacle.x, obstacle.y, self.robot.x, self.robot.y) > obstacle.r + self.robot.r:
                    break
                try_cnt += 1
            if try_cnt == 10000:
                raise Exception('Obstacle is too close to robot')
            self.obstacles.add(obstacle)

    def _setup_humans(self):
        # setup crowds

        human_config =  {
            'x':5,
            "y":7,
            "theta": -56,
            "v_pref": 0.5,
            "r":0.25,
            "image":"nav_sim/images/human.png",
            "is_random": False,
            "target": [7,3],
            "safe_r": 0.1
        }
        
        n_h = 10
        
        for i in range(n_h):


            try_cnt = 0
            while (try_cnt != 10000):
                
                # a = i*2*math.pi/n_h + random.uniform(-0.1*math.pi,0.1*math.pi)
                # r = 3 
                # x = r*math.cos(a) + self.length//2
                # y = r*math.sin(a) + self.width//2
                
                # at = a + math.pi + random.uniform(-0.1*math.pi,0.1*math.pi)
                # tx = r*math.cos(at) + self.length//2
                # ty = r*math.sin(at) + self.width//2

                v = random.uniform(0.5,0.7)
                x = random.uniform(1, self.length-1)
                y = random.uniform(1, self.width-1)
                tx = random.uniform(1, self.length-1)
                ty = random.uniform(1, self.width-1)
                

                    
                    
                v = random.uniform(1,1.5)
                theta = random.uniform(0,180)
                
                human_config['x'] = x
                human_config['y'] = y
                human_config['target'] = [tx,ty]
                human_config['theta'] = theta
                human_config['v_pref'] = v

                
                human = Human(human_config, self.dt,
                            self.scare, self.coord_trans)
        
                if len(pygame.sprite.spritecollide(human, self.obstacles, False, collided=collide)) == 0 and \
                        len(pygame.sprite.spritecollide(human, self.humans, False, collided=collide)) == 0 :
                    break
                try_cnt += 1
            if try_cnt == 10000:
                raise Exception('Human is too close to other entities')
            self.humans.add(human)
            Human.setup_orca()

    def _setup_goals(self):
        # setup goals
        goal_config = {

            "x": 0,
            "y": 0,
            "r": 0.05,
            "image": "nav_sim/images/goal.png",
            "is_random": True
        }
        
        goal = Goal(goal_config, self.dt, self.scare, self.coord_trans)

        goal.x = self.length -1
        goal.y = self.width //2 
        self.goals.add(goal)
