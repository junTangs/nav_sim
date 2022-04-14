from envs import NavEnvV1
import json
import tqdm
from pprint import pprint
from entity.manager import EntityManager


config_path = r'config/nav_env_v1_config_template/env.json'
config = json.load(open(config_path))
env = NavEnvV1(config)
env.reset()
pprint(EntityManager.ENTITIES_TABLE)
for i in tqdm.trange(10000000):
    s_,r,d,info = env.step(env.action_space.sample())
    env.render()
    if d :
        env.reset()
