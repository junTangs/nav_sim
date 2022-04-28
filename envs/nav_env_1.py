from envs.base_env import BaseNavEnv
from utils.math_utils import distance,clock_angle,norm
from entity.robot import Robot
from entity.goal import Goal
from entity.obstacle import Obstacle
import pygame
from utils.env_utils import collide
from utils.reward_utils import reward_sparse
import numpy as np
import random
import json


class NavEnvV1(BaseNavEnv):
    def __init__(self,config) -> None:
        super().__init__(config)
    
    def _setup(self):
        # steup robot
        robot_config_path = self.config['robot_config_path']
        robot_config  = json.load(open(robot_config_path))
        robot = Robot(robot_config,self.dt,self.scare,self.coord_trans)
        
        if robot_config['is_random']:
            robot.x = random.uniform(0,self.length)
            robot.y = random.uniform(0,self.width)
            robot.theta = random.uniform(-180,180)
        self.robot = robot
        
        # setup obstacles
        obstacle_config_path = self.config['obstacle_config_path']
        obstacle_configs = json.load(open(obstacle_config_path))
        for obstacle_config in obstacle_configs["obstacles"]:
            obstacle = Obstacle(obstacle_config,self.dt,self.scare,self.coord_trans)
            
            if obstacle_config['is_random']:
                try_cnt  = 0
                while(try_cnt != 10000):
                    obstacle.x = random.uniform(0,self.length)
                    obstacle.y = random.uniform(0,self.width)

                    if distance(obstacle.x,obstacle.y,robot.x,robot.y) > obstacle.r+ robot.r:
                        break
                    try_cnt += 1
                if try_cnt == 10000:
                    raise Exception('Obstacle is too close to robot')
            self.obstacles.add(obstacle)
        
        # setup goals
        goal_config_path = self.config['goal_config_path']
        goal_configs = json.load(open(goal_config_path))
        for goal_config in goal_configs["goals"]:
            goal = Goal(goal_config,self.dt,self.scare,self.coord_trans)
            
            if goal_config['is_random']:
                try_cnt  = 0
                while(try_cnt != 10000):
                    goal.x = random.uniform(0,self.length)
                    goal.y = random.uniform(0,self.width)
                    if len(pygame.sprite.spritecollide(goal,self.obstacles,False,collide)) == 0:
                        break
                    try_cnt += 1
                if try_cnt == 10000:
                    raise Exception('Goal is too close to robot')
            self.goals.add(goal)
        return

    def _states(self):
        # format:  {"x":0,"y":0,"r":0,"v":0,"omega":0,"theta":0}
        robot_states = self.robot.states

        robot_states = [robot_states['x']/self.length,
                        robot_states['y']/self.width,
                        norm(robot_states['v'],self.robot.v_max,self.robot.v_min),
                        norm(robot_states['omega'],self.robot.omega_max,self.robot.omega_min),
                        norm(robot_states['theta'],180,-180)]
        
        # observation
        sensor_data = self.robot.detect(self.obstacles,self.goals)
        
        # format : [dist1,dist2,dist3,dist4,dist5,dist6,dist7,dist8] , range: (0,1) 
        obs_sensor_states = []
        # format :[dist1,dist2,dist3,dist4,dist5,dist6,dist7,dist8] , range: (0,1)
        goal_sensor_states_dist = []
        #format :[angle1,angle2,angle3,angle4,angle5,angle6,angle7,angle8] , range: (-1,1)
        goal_sensor_states_angle = []
        for sensor_name,data in sensor_data.items():
            if data['type'] == 'dist':
                # distance between robot and obstacle
                obs_sensor_states.append(data['results'])
            elif data['type'] == 'goal':
                # distance between robot and goal
                for goal in data['results']:
                    goal_sensor_states_dist.append(norm(goal['distance'],self.max_distance))
                    goal_sensor_states_angle.append(norm(goal['angle'],180,-180))

        return robot_states+obs_sensor_states+goal_sensor_states_dist+goal_sensor_states_angle
        
        
