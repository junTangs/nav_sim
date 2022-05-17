STATE_WRAPPER_FACTORTY  = {}
import numpy as np
import matplotlib.pyplot as plt

def rs_s_g_wrapper(frames):
    frames = [np.array(f["robot_states"]+\
                       f["obs_states"]+\
                       f["goal_dist"]+\
                       f["goal_angle"]).reshape(1, -1) for f in frames]
    states = np.concatenate(frames, axis=0)
    return states

STATE_WRAPPER_FACTORTY["rs_s_g"] = rs_s_g_wrapper