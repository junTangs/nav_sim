from nav_sim.utils import state
from nav_sim.utils.state.state import State
import numpy as np


class DistSensorState(State):
    def __init__(self) -> None:
        super().__init__()

    def wrapper(self, frames, **kwargs) -> np.ndarray:
        # 0,1,2, 3,   4, 5, 6,  7  , 8,9,10,...
        # x,y,r,theta,vx,vy,v,omega,pref_v,gd,gangle
        robot_goal_frames = [np.array(f["robot_states"] +
                                      f["goal_dist"] +
                                      f["goal_angle"] +
                                      f["obs_states"]
                                      ).reshape(1, -1) for f in frames]


        state = np.concatenate(robot_goal_frames, axis=0)
        return {"states": state}
