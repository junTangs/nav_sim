from entity import *
from entity import robot
import json
import pygame 
from pygame.sprite import Sprite,Group
from pprint import pprint
from pygame.locals import *
from utils.math_utils import *
from utils.env_utils import *
from functools import partial

DISPLAY_SIZE = (800,800)
ENV_SIZE = (10,10)


scare_trans = partial(scare,dst = DISPLAY_SIZE,src = ENV_SIZE)
coord_trans = partial(xy_into_display, display_size=DISPLAY_SIZE, size=ENV_SIZE)

robot_config = json.load(open(r"config\nav_env_v1_config\robot.json"))
robot = robot.Robot(robot_config,dt = 1,scare_trans = scare_trans,coord_trans = coord_trans)


obstacles = Group()
obstacle_config = json.load(open(r"config\nav_env_v1_config\obstacle.json"))
pprint(obstacle_config)

for obstacle in obstacle_config["obstacles"]:
    obstacles.add(Obstacle(obstacle,dt = 0.1,scare_trans = scare_trans,coord_trans = coord_trans))

screen = pygame.display.set_mode(DISPLAY_SIZE ,DOUBLEBUF|HWSURFACE)  # set screen

goal_config = json.load(open(r"config\nav_env_v1_config\goal.json"))
goals = Group()
pprint(goal_config)
for goal in goal_config["goals"]:
    goals.add(Goal(goal,0.1,scare_trans= scare_trans,coord_trans = coord_trans))


RUN_FLAG= True

while RUN_FLAG:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

    robot.move(0.01,0.01)
    robot.update()
    robot.detect(obstacles,goals)

    screen = pygame.display.set_mode(DISPLAY_SIZE,DOUBLEBUF|HWSURFACE)  # set screen
    screen.fill((255,255,255))

    robot.draw(screen)
    for obstacle in obstacles:
        obstacle.draw(screen)
    for goal in goals:
        goals.draw(screen)

    pygame.display.update()

