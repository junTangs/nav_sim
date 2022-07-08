from nav_sim.utils.state.state import State
import numpy as np 


class JointState(State):
    def __init__(self) -> None:
        super().__init__()
        
        
    def wrapper(self, frames, **kwargs) -> np.ndarray:

        frame = frames[-1]
        joint_frame = np.array(frame["robot_states"]+frame["goal_x"]+frame["goal_y"]+frame["human_pos"])
        return joint_frame
