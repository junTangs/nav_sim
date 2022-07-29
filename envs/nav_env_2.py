
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



class NavEnvV2(NavEnvV1):
    def __init__(self,config):
        super(NavEnvV2, self).__init__(config)


    def _setup_robot(self):
        # steup robot
        robot_config_path = self.config['robot_config_path']
        robot_config = json.load(open(robot_config_path))
        robot = Robot(robot_config, self.dt, self.scare, self.coord_trans)

        # robot located on left bottom of env
        robot.x = 5
        robot.y = 5
        robot.theta = 0
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
        if len(human_configs["humans"]) != 0:
            for human_config in human_configs["humans"]:
                human = Human(human_config, self.dt, self.scare, self.coord_trans)

                if human_config['is_random']:
                    try_cnt = 0
                    while (try_cnt != 10000):
                        human.x = random.uniform(0, self.length)
                        human.y = random.uniform(0, self.width)
                        human.target[0] = random.uniform(0, self.length)
                        human.target[1] = random.uniform(0, self.width)
                        human.v_pref = 0.1

                        if len(pygame.sprite.spritecollide(human, self.obstacles, False, collided=collide)) == 0 and \
                                len(pygame.sprite.spritecollide(human, self.humans, False, collided=collide)) == 0 and \
                                distance(human.x, human.y, self.robot.x, self.robot.y) > human.r + self.robot.r:
                            break
                        try_cnt += 1
                    if try_cnt == 10000:
                        raise Exception('Human is too close to other entities')
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
        
        target = [[1,self.length -1],[1,1],[self.length -1,self.width -1],[1,self.width -1]]
        pos = random.choice(target)
        goal = Goal(goal_config, self.dt, self.scare, self.coord_trans)
        goal.x = pos[0]
        goal.y = pos[1]
        self.goals.add(goal)