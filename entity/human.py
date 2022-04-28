from pygame.sprite import Sprite
import math
from utils.math_utils import rotate
import pygame
from entity.manager import EntityManager
from policy.orca.pyorca import Agent, get_avoidance_velocity, orca, normalized, perp
import numpy as np
from entity.obstacle import Obstacle


class Human(Sprite):
    def __init__(self, config, dt, scare_trans, coord_trans) -> None:
        super().__init__()

        self.config = config

        self.x = 0
        self.y = 0
        self.r = 0
        self.vx = 0
        self.vy = 0
        self.theta =0
        self.max_speed = 0

        self.t = 0


        self.dt = dt
        self.coord_trans = coord_trans
        self.scare_trans = scare_trans

        self.image = None
        self.display_image = None

        self.rect = None
        self.id = None
        self.agent = None
        self.setup()

    def setup(self):
        self.x = self.config['x']
        self.y = self.config['y']
        self.r = self.config['r']

        # configure orca
        self.theta = self.config["theta"]
        self.vx = math.cos(math.radians(self.config['theta']))
        self.vy = math.sin(math.radians(self.config['theta']))

        self.max_speed = self.config["max_speed"]
        x = self.r * np.array((np.cos(math.radians(self.config['theta'])), np.sin(math.radians(self.config['theta']))))  # + random.uniform(-1, 1)
        vel = normalized(-x) * self.max_speed
        self.agent = Agent((self.x,self.y),(self.vx,self.vy),self.r,self.max_speed,vel)

        self.image = pygame.image.load(self.config['image'])
        self.image = pygame.transform.smoothscale(self.image, self.scare_trans(self.r * 2, self.r * 2))
        self.display_image = self.image.copy()

        self.rect = self.display_image.get_rect()
        self.rect.center = self.coord_trans(self.x, self.y)

        self.agent = Agent((self.x,self.y),(self.vx,self.vy),self.r,self.max_speed)
        EntityManager.register(self)

    def update(self):
        humans  = filter(lambda x: x is not self,[human.agent for human in EntityManager.find_instance(Human)])
        obstacles = [Agent((obs.x,obs.y),(0,0),obs.r,0,(0,0)) for obs in EntityManager.find_instance(Obstacle)]

        new_vel,_  = orca(self.agent,humans+obstacles,5,self.dt)

        self.vx = new_vel[0]
        self.vy = new_vel[1]
        self.x += new_vel*self.dt
        self.y += new_vel*self.dt
        self.theta = math.degrees(math.atan2(self.vy,self.vx))
        return


    def move(self,theta):
        self.theta = theta
        x = self.r * np.array((np.cos(math.radians(self.theta)),
                               np.sin(math.radians(self.theta))))  # + random.uniform(-1, 1)
        vel = normalized(-x) * self.max_speed
        self.agent = Agent((self.x, self.y), (self.vx, self.vy), self.r, self.max_speed, vel)
        return


    def draw(self, screen):
        # appearance
        self.rect = self.display_image.get_rect()
        self.rect.center = self.coord_trans(self.x, self.y)
        screen.blit(self.display_image, self.rect)

    def set(self, **kwargs):
        self.__dict__.update(kwargs)
        self.setup()


if __name__ == "__main__":
    x =  np.array((np.cos(math.radians(90)), np.sin(math.radians(90))))  # + random.uniform(-1, 1)
    vel = normalized(-x)
    print(x,vel)
