from nav_sim.utils.reward.reward import Reward
from nav_sim.utils.math_utils import distance,gaussian
from numba import njit


@njit
def att_filed(x1,y1,x2,y2,a):
    return 0.5*a*distance(x1,y1,x2,y2)**2

@njit
def rep_filed(x1,y1,x2,y2,r,r2,a):
    dist = distance(x1,y1,x2,y2) - (r + r2)
    # if dist <= r:
    #     return 0.5*a*(1/dist - 1/r)**2
    # else:
    #     return 0
    return gaussian(dist,r2)

def cal_apf(goals,obstacles,humans,robot):
    att = 0
    rep = 0
    for g in goals:
         att += att_filed(g.x,g.y,robot.x,robot.y,1)

    for obs in obstacles:
        rep = 5*max(rep_filed(obs.x,obs.y,robot.x,robot.y,obs.r,robot.r,1),rep)
    for h in humans:
        rep  = 5*max(rep_filed(h.x,h.y,robot.x,robot.y,h.r,robot.r,1),rep)
    rep = min(5,rep)
    return att+rep



class ApfReward(Reward):
    def __init__(self) -> None:
        super().__init__()
        
        self.lst_poten = 0
        self.vx = 0
        self.vy = 0
        
        self.__is_setup = False
    
    def setup(self, goals, obstacles, humans, robot,**kwargs):
        self.lst_poten = cal_apf(goals,obstacles,humans,robot)

        self.__is_setup = True
        return
        
    def reward(self, goals, humans, obstacles, robot, finish, collide,**kwargs) -> float:
        if collide:
            return  -10
        if finish:
            return  500
        
        poten =  cal_apf(goals,obstacles,humans,robot)
        r = 10*(self.lst_poten - poten)
        r -= abs(robot.vx - self.vx)+ abs(robot.vy - self.vy)

        self.lst_poten = poten
        self.vx = robot.vx
        self.vy = robot.vy

        return r
