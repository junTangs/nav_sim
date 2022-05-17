from envs import NavEnvV1
import json
import tqdm
from pprint import pprint
from entity.manager import EntityManager
from entity import Obstacle,Human


config_path = r'/home/juntang/桌面/code/config/env_config/env.json'
config = json.load(open(config_path))
env = NavEnvV1(config)
env.reset()
for i in tqdm.trange(10000):
    s = env.step(0)
    print(s)
    env.render()

