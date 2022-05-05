from envs import NavEnvV1
import json
import tqdm
from pprint import pprint
from entity.manager import EntityManager
from entity import Obstacle

import rvo2
sim = rvo2.PyRVOSimulator(1/60., 1.5, 5, 1.5, 2, 0.4, 2)

config_path = r'config/nav_env_v1_config_template/env.json'
config = json.load(open(config_path))
env = NavEnvV1(config)
env.reset()
pprint(EntityManager.ENTITIES_TABLE)
pprint(EntityManager.find_instance(Obstacle))

for i in range(10000):
    env.step(1)
    env.render()

