from nav_sim.utils import state
from nav_sim.utils.state.state import State
from nav_sim.utils.math_utils import norm, rotate_array
import numpy as np
from nav_sim.utils.norm import Normalization


class DistSensorState(State):
    def __init__(self,norm = False) -> None:
        super().__init__()
        self.is_nrom = norm
        self.norm = None


    def wrapper(self, frames, **kwargs) -> np.ndarray:
        # 0,1,2, 3,   4, 5, 6,  7  , 8,9,10,...
        # x,y,r,theta,vx,vy,v,omega,pref_v,gd,gangle

        robot_goal_frames = [np.array(f["robot_states"]+
                                      f["goal_dist"] +
                                      f["goal_angle"] +
                                      f["obs_states"]
                                      ).reshape(1, -1) for f in frames]


                
            

        state = np.concatenate(robot_goal_frames, axis=0)


        sensor = state[:,11:].reshape(-1,8)
        
        vx = state[:,4].reshape(-1,1)
        vy = state[:,5].reshape(-1,1)
        d = state[:,9].reshape(-1,1)
        angle = state[:,10].reshape(-1,1)
        r = state[:,2].reshape(-1,1)
        theta = state[:,3].reshape(-1,1)
        
        state = np.concatenate([d,angle,theta,vx,vy,r,sensor],axis = -1)
        
        if self.is_nrom:
            if self.norm is None:
                self.norm = Normalization(shape = state.shape)
            state = self.norm(state)


        return {"states": state}
