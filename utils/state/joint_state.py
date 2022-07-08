from nav_sim.utils.state.state import State
import numpy as np 


class JointState(State):
    def __init__(self) -> None:
        super().__init__()
        
        
    def wrapper(self, frames, **kwargs) -> np.ndarray:
        joint_frames = [np.array(f["robot_states"] +
                                f["goal_dist"] +
                                f["goal_angle"] +
                                f["obs_states"]
                                ).reshape(1, -1) for f in frames]
