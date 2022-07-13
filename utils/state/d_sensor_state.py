from nav_sim.utils import state
from nav_sim.utils.state.state import State
from nav_sim.utils.math_utils import rotate_array
import numpy as np


class DistSensorState(State):
    def __init__(self) -> None:
        super().__init__()

    def wrapper(self, frames, **kwargs) -> np.ndarray:
        # 0,1,2, 3,   4, 5, 6,  7  , 8,9,10,...
        # x,y,r,theta,vx,vy,v,omega,pref_v,gd,gangle

        robot_goal_frames = [np.array(f["robot_states"]+
                                      f["goal_dist"] +
                                      f["goal_angle"] +
                                      f["obs_states"]
                                      ).reshape(1, -1) for f in frames]


        state = np.concatenate(robot_goal_frames, axis=0)

        gd = state[:,9].reshape(-1,1)
        angle = state[:,10].reshape(-1,1)
        vx,vy= rotate_array(state[:,4],state[:,5],state[:,3])
        vx = vx.reshape(-1,1)
        vy = vy.reshape(-1,1)
        r = state[:,2].reshape(-1,1)
        v_pref = state[:,8].reshape(-1,1)
        sensor = state[:,11:].reshape(-1,8)

        state = np.concatenate([vx,vy,r,gd,angle,v_pref,sensor],axis=-1)
        return {"states": state}
