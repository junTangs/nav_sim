from nav_sim.envs import NavEnvV1
from nav_sim.entity import *


from gym.envs.registration import register

register(
        id='nav_env-v0',
        entry_point='nav_sim.envs.nav_env_1:NavEnvV1',
)


WRAPPER_FACTORTY = {}