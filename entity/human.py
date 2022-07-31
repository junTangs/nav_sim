import random

from pygame.sprite import Sprite
import math
from nav_sim.utils.math_utils import normalize_2d
import pygame
from nav_sim.entity.manager import EntityManager
import numpy as np
from nav_sim.entity.obstacle import Obstacle
from nav_sim.entity.robot import Robot
from nav_sim.utils.math_utils import distance

import rvo2


class Human(Sprite):
    sim = None
    # orca config
    max_neighbors = 30
    neighbor_dist = 5
    time_horizon = 5
    time_horizon_obs = 5

    human_exist = False
    update_lock = False
    def __init__(self, config, dt, scare_trans, coord_trans) -> None:
        super().__init__()

        self.config = config

        self.x = 0
        self.y = 0
        self.r = 0
        self.vx = 0
        self.vy = 0
        self.theta = 0
        self.v_pref = 0
        self.safe_r = 0

        self.pref_vx = 0
        self.pref_vy = 0

        self.target = [0,0]
        self.t = 0


        self.dt = dt
        self.coord_trans = coord_trans
        self.scare_trans = scare_trans

        self.image = None
        self.display_image = None

        self.rect = None
        self.id = None

        self.agent_id = 0


        self.setup()

    def setup(self):
        self.x = self.config['x']
        self.y = self.config['y']
        self.r = self.config['r']
        self.theta = self.config["theta"]
        self.vx = math.cos(math.radians(self.config['theta']))
        self.vy = math.sin(math.radians(self.config['theta']))
        self.safe_r = self.config["safe_r"]
        self.target = self.config["target"]
        self.v_pref = self.config["v_pref"]

        angle = math.atan2(self.target[1] - self.y,self.target[0]-self.x)
        self.pref_vx = self.v_pref * math.cos(angle)
        self.pref_vy = self.v_pref * math.sin(angle)

        self.pref_vx,self.pref_vy = normalize_2d(self.pref_vx,self.pref_vy)

        self.image = pygame.image.load(self.config['image'])
        self.image = pygame.transform.smoothscale(self.image, self.scare_trans(self.r * 2, self.r * 2))
        self.display_image = pygame.transform.rotate(self.image, self.theta)
        self.rect = self.display_image.get_rect()
        self.rect.center = self.coord_trans(self.x,self.y)
        EntityManager.register(self)


    @classmethod
    def setup_orca(cls):
        # orca configure in first running
        cls.neighbor_dist = 1
        cls.time_horizon = 5
        cls.time_horizon_obs = 5


        humans = EntityManager.find_instance(Human)
        robot = EntityManager.find_instance(Robot)[0]

        if len(humans) !=0:
            obstacles = EntityManager.find_instance(Obstacle)

            cls.max_neighbors = EntityManager.counter(Human)+\
                                EntityManager.counter(Robot)+\
                                EntityManager.counter(Obstacle)

            params = cls.neighbor_dist, cls.max_neighbors, cls.time_horizon, cls.time_horizon_obs

            cls.sim = rvo2.PyRVOSimulator(humans[0].dt, *params, 1.2 * humans[0].r, humans[0].v_pref)

            for human in humans:
                human.agent_id = cls.sim.addAgent((human.x,human.y), *params, human.r + 0.01 + human.safe_r,
                                                  human.v_pref, (human.vx, human.vy))


            robot.agent_id = cls.sim.addAgent((robot.x, robot.y), *params, 1.5 * robot.r,
                                              robot.v_pref, (robot.vx, robot.vy))

            for obstacle in obstacles:
                x,y,r = obstacle.x,obstacle.y,obstacle.r
                pt = [(x + r,y+r),(x-r,y+r),(x-r,y-r),(x+r,y-r)]
                cls.sim.addObstacle(pt)
                cls.sim.processObstacles()


        cls.update_lock = True




    @classmethod
    def update_orca(cls):
        humans = EntityManager.find_instance(Human)
        robot = EntityManager.find_instance(Robot)[0]
        for human in humans:
            human.update_pref_v()
            cls.sim.setAgentPrefVelocity(human.agent_id,(human.pref_vx,human.pref_vy))
            cls.sim.setAgentPosition(human.agent_id, (human.x, human.y))

        cls.sim.setAgentPrefVelocity(robot.agent_id, (robot.vx, robot.vy))
        cls.sim.setAgentPosition(robot.agent_id, (robot.x, robot.y))

        cls.sim.doStep()

        for human in humans:
            if distance(human.x,human.y,human.target[0],human.target[1]) <=  0.2*human.r:
                    other = random.choice(humans)
                    human.target[0] = other.x
                    human.target[1] = other.y
                    continue
            human.x ,human.y = cls.sim.getAgentPosition(human.agent_id)
            human.vx,human.vy = cls.sim.getAgentVelocity(human.agent_id)
            human.theta = math.degrees(math.atan2(human.vy,human.vx))




    @classmethod
    def unlock_orca(cls):
        cls.update_lock = False

    @classmethod
    def update(cls):
        cls.update_orca()
        return

    def move(self,target):
        self.target = target
        self.update_pref_v()
        return

    def update_pref_v(self):
        angle = math.atan2(self.target[1] - self.y, self.target[0] - self.x)
        self.pref_vx = self.v_pref * math.cos(angle)
        self.pref_vy = self.v_pref * math.sin(angle)
        self.pref_vx, self.pref_vy = normalize_2d(self.pref_vx, self.pref_vy)
        return

    def draw(self, screen):
        # appearance
        self.display_image = pygame.transform.rotate(self.image, self.theta)
        self.rect = self.display_image.get_rect()
        self.rect.center = self.coord_trans(self.x,self.y)
        screen.blit(self.display_image, self.rect)
        x2,y2 = self.coord_trans(self.target[0],self.target[1])
        x1,y1 = self.coord_trans(self.x,self.y)
        pygame.draw.line(screen,(123,123,123),(x1,y1),(x2,y2),2)
        pygame.draw.circle(screen,(123,123,123),(x2,y2),5)

    def set(self, **kwargs):
        self.__dict__.update(kwargs)
        self.setup()




