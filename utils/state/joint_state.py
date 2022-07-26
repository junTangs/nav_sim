from curses import noraw
from nav_sim.utils.state.state import State
import numpy as np 


class JointState(State):
    def __init__(self,norm = False) -> None:
        super().__init__()
        
        
    def wrapper(self, frames, **kwargs) -> np.ndarray:

        frame = frames[-1]

        joint_frame = frame["robot_states"]+frame["goal_x"]+frame["goal_y"]
        for hs in frame["humans_states"]:
            joint_frame+= hs

        return np.array(joint_frame)
