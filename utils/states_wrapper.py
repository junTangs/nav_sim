STATE_WRAPPER_FACTORTY  = {}
import numpy as np
import matplotlib.pyplot as plt

def rs_s_g_wrapper(frames):
    frames = [np.array(f["robot_states"]+\
                       f["obs_states"]+\
                       f["goal_dist"]+\
                       f["goal_angle"]).reshape(1, -1) for f in frames]


    states = np.concatenate(frames, axis=0)
    return {"states":states}

STATE_WRAPPER_FACTORTY["rs_s_g"] = rs_s_g_wrapper


def rs_d_g_wrapper(frames):
    states  = [np.array(f["robot_states"]+\
                       f["goal_dist"]+\
                       f["goal_angle"]).reshape(1, -1) for f in frames]


    maps = [np.expand_dims(f["map"],0) for f in frames]
    states = np.concatenate(states, axis=0)
    maps = np.concatenate(maps, axis=0)
    return {"states":states,"density_maps":maps}
STATE_WRAPPER_FACTORTY["rs_d_g"] = rs_d_g_wrapper
