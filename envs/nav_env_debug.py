
from nav_sim.envs.nav_env_1 import NavEnvV1
import json
from nav_sim.entity import Robot
from nav_sim.entity import Goal
from nav_sim.entity import Obstacle
from nav_sim.entity import Human
import random
from nav_sim.utils.math_utils import distance,clock_angle,norm
import  pygame
from nav_sim.utils.env_utils import collide
from pprint import pprint



class NavEnvDebug(NavEnvV1):
    def __init__(self,config):
        super(NavEnvDebug, self).__init__(config)


    def _setup_robot(self):
        # steup robot
        robot_config_path = self.config['robot_config_path']
        robot_config = json.load(open(robot_config_path))
        robot = Robot(robot_config, self.dt, self.scare, self.coord_trans)

        # robot located on left bottom of env
        robot.x = self.length//2
        robot.y = self.width//2
        robot.theta = 0
        self.robot = robot

    def _setup_obstacles(self):
        # setup obstacles
        obstacle_config_path = self.config['obstacle_config_path']
        obstacle_configs = json.load(open(obstacle_config_path))

        if len(obstacle_configs["obstacles"]) != 0:
            for obstacle_config in obstacle_configs["obstacles"]:
                obstacle = Obstacle(obstacle_config, self.dt, self.scare, self.coord_trans)
                self.obstacles.add(obstacle)

    def _setup_humans(self):
        # setup crowds
        human_config_path = self.config['human_config_path']
        human_configs = json.load(open(human_config_path))
        if len(human_configs["humans"]) != 0:
            for human_config in human_configs["humans"]:
                human = Human(human_config, self.dt, self.scare, self.coord_trans)
                self.humans.add(human)
            Human.setup_orca()

    def _setup_goals(self):
        # setup goals
        goal_config = {
            "x":0,
            "y":0,
            "r":0.2,
            "image":"nav_sim/images/goal.png",
            "is_random": True
        }
        goal = Goal(goal_config, self.dt, self.scare, self.coord_trans)
        goal.x = self.length
        goal.y = self.width //2
        self.goals.add(goal)
        
    
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
        
        info["time"] = self.t
        info["step"] = self.step_count
        reward = self.reward()
        state = self.states()
        return state,reward,done,info