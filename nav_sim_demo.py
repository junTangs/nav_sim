from envs import NavEnvV1
import json



config_path = r'config/nav_env_v1_config_template/env.json'
config = json.load(open(config_path))
env = NavEnvV1(config)
env.reset()
print(env.action_space)
for i in range(10000):
    print(env.step(env.action_space.sample()))
    env.render()