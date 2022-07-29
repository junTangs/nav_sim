import numpy as np

from nav_sim.envs.base_env import BaseNavEnv
from nav_sim.utils.math_utils import distance,clock_angle,norm
from nav_sim.entity import Robot
from nav_sim.entity import Goal
from nav_sim.entity import Obstacle
from nav_sim.entity import Human
import pygame
from nav_sim.utils.env_utils import collide
from nav_sim.utils.math_utils import norm
import random
import json
import math

class NavEnvV1(BaseNavEnv):
    def __init__(self,config) -> None:
        super().__init__(config)
    
    def _setup(self):

        self._setup_robot()
        self._setup_obstacles()
        self._setup_humans()
        self._setup_goals()
        return


    def _setup_robot(self):
        # steup robot
        robot_config_path = self.config['robot_config_path']
        robot_config = json.load(open(robot_config_path))
        robot = Robot(robot_config, self.dt, self.scare, self.coord_trans)

        if robot_config['is_random']:
            robot.x = random.uniform(0, self.length)
            robot.y = random.uniform(0, self.width)
            robot.theta = random.uniform(-180, 180)
        self.robot = robot

    def _setup_obstacles(self):
        # setup obstacles
        obstacle_config_path = self.config['obstacle_config_path']
        obstacle_configs = json.load(open(obstacle_config_path))

        if len(obstacle_configs["obstacles"]) != 0:
            for obstacle_config in obstacle_configs["obstacles"]:
                obstacle = Obstacle(obstacle_config, self.dt, self.scare, self.coord_trans)

                if obstacle_config['is_random']:
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
        human_config_path = self.config['human_config_path']
        human_configs = json.load(open(human_config_path))
        if len(human_configs["humans"])!= 0:
            for human_config in human_configs["humans"]:
                human = Human(human_config, self.dt, self.scare, self.coord_trans)

                if human_config['is_random']:
                    try_cnt = 0
                    while (try_cnt != 10000):
                        human.v_pref = random.uniform(0.3,0.7)
                        human.r = 0.25
                        human.x = random.uniform(0, self.length)
                        human.y = random.uniform(0, self.width)
                        human.target[0] = random.uniform(0, self.length)
                        human.target[1] = random.uniform(0, self.width)
                        if len(pygame.sprite.spritecollide(human,self.obstacles,False,collided=collide)) == 0 and\
                            len(pygame.sprite.spritecollide(human,self.humans,False,collided=collide)) == 0 and\
                            distance(human.x,human.y,self.robot.x,self.robot.y) > human.r + self.robot.r and\
                            distance(human.x,human.y,human.target[0],human.target[1]) >= 2:
                            break
                        try_cnt += 1
                    if try_cnt == 10000:
                        raise Exception('Human is too close to other entities')
                self.humans.add(human)
            Human.setup_orca()

    def _setup_goals(self):
        # setup goals
        goal_config_path = self.config['goal_config_path']
        goal_configs = json.load(open(goal_config_path))
        for goal_config in goal_configs["goals"]:
            goal = Goal(goal_config, self.dt, self.scare, self.coord_trans)

            if goal_config['is_random']:
                try_cnt = 0
                while (try_cnt != 10000):
                    goal.x = random.uniform(0, self.length)
                    goal.y = random.uniform(0, self.width)
                    if len(pygame.sprite.spritecollide(goal, self.obstacles, False, collide)) == 0 and \
                      distance(goal.x,goal.y,self.robot.x,self.robot.y) > 0.5*self.length:
                        break
                    try_cnt += 1
                if try_cnt == 10000:
                    raise Exception('Goal is too close to robot')
            self.goals.add(goal)

    def _states(self):
        # format:  {"x":0,"y":0,"r":0,"v":0,"omega":0,"theta":0}
        robot_states = self.robot.states

        if not self.config["is_norm"]:
            robot_states = [
                            robot_states['x'],
                            robot_states['y'],
                            robot_states['r'],
                            robot_states['theta'],
                            robot_states['vx'],
                            robot_states['vy'],
                            robot_states['v'],
                            robot_states['omega'],
                            robot_states['v_pref']
                            ]
        else:
            robot_states = [
                norm(robot_states['x'],self.length),
                norm(robot_states['y'],self.width),
                1,
                norm(robot_states['theta'],180,-180),
                robot_states['vx']/robot_states['v_pref'],
                robot_states['vy']/robot_states['v_pref'],
                robot_states['v']/robot_states['v_pref'],
                norm(robot_states['omega'],180,-180),
                1
                ]
            

        
        # observation
        sensor_data = self.robot.detect(self.obstacles,self.humans,self.goals)
        
        # format : [dist1,dist2,dist3,dist4,dist5,dist6,dist7,dist8] , range: (0,max_distance) 
        obs_sensor_states = []
        # format :[dist1,dist2,dist3,dist4,dist5,dist6,dist7,dist8] , range: (0,max_distance)
        goal_sensor_states_dist = []
        #format :[angle1,angle2,angle3,angle4,angle5,angle6,angle7,angle8] , range: (-180,180)
        goal_sensor_states_angle = []
        # format: [pos_x,pos_y,......] range: (x_range,y_range)
        humans_states = []

        goal_sensor_states_x = []
        goal_sensor_states_y = []

        for sensor_name,data in sensor_data.items():
            if data['type'] == 'dist':
                # distance between robot and obstacle
                # data has been normalized 
                obs_sensor_states.append(data['results'])

                    
            elif data['type'] == 'goal':
                # distance between robot and goal
                for goal in data['results']:
                    
                    if not self.config["is_norm"]:
                        goal_sensor_states_dist.append(goal['distance'])
                        goal_sensor_states_angle.append(goal['angle'])
                        goal_sensor_states_x.append(goal["x"])
                        goal_sensor_states_y.append(goal["y"])
                    else:
                        goal_sensor_states_dist.append(norm(goal['distance'],self.max_distance))
                        goal_sensor_states_angle.append(norm(goal['angle'],180,-180))
                        goal_sensor_states_x.append(norm(goal["x"],self.length))
                        goal_sensor_states_y.append(norm(goal["y"],self.width))
                        
            elif data['type'] == "human":
                # human states
                for hs in data["results"]:
                    humans_states.append(hs)
                map = data["map"]

        return {"robot_states":robot_states,
                "obs_states":obs_sensor_states,
                "goal_dist":goal_sensor_states_dist,
                "goal_angle":goal_sensor_states_angle,
                "goal_x":goal_sensor_states_x,
                "goal_y":goal_sensor_states_y,
                "humans_states":humans_states,
                "map":map}
        
        
