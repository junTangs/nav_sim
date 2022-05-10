REWARD_FACTORY = {}
from nav_sim.utils.math_utils import distance,gaussian
from numba import njit



@njit
def att_filed(x1,y1,x2,y2,a):
    return 0.5*a*distance(x1,y1,x2,y2)**2
@njit
def rep_filed(x1,y1,x2,y2,r,a):
    dist = distance(x1,y1,x2,y2)
    # if dist <= r:
    #     return 0.5*a*(1/dist - 1/r)**2
    # else:
    #     return 0
    return gaussian(dist,r)

def cal_apf(goals,obstacles,humans,robot):
    att = 0
    rep = 0
    for g in goals:
         att += att_filed(g.x,g.y,robot.x,robot.y,1)

    for obs in obstacles:
        rep = 5*max(rep_filed(obs.x,obs.y,robot.x,robot.y,obs.r,1),rep)
    for h in humans:
        rep  = 5*max(rep_filed(h.x,h.y,robot.x,robot.y,h.r,1),rep)
    rep = min(5,rep)
    return att+rep


def sparse_reward(instance,*args,**kwargs):
    collide = instance.collide_flag
    finish = instance.finish_flag

    if kwargs.get("init",False):
        instance.rwd_hst["lst_poten"] = cal_apf(instance.goals,instance.obstacles,instance.humans,instance.robot)
        instance.rwd_hst["v"] = instance.robot.v
        instance.rwd_hst["omega"] = instance.robot.omega
        return 0
    else:
        poten =  cal_apf(instance.goals,instance.obstacles,instance.humans,instance.robot)
        r = 10*(instance.rwd_hst["lst_poten"] - poten)
        r -= abs(instance.robot.v - instance.rwd_hst["v"]) ** 2 + abs(instance.robot.omega - instance.rwd_hst["omega"]) ** 2

        instance.rwd_hst["lst_poten"] = poten
        instance.rwd_hst["v"] = instance.robot.v
        instance.rwd_hst["omega"] = instance.robot.omega

        if collide:
            return  -10
        if finish:
            return  500

        return r


def cal_poten(min_dist_sensor,dist,a,b):
    atten = 0.5*a*dist**2
    rep = b*gaussian(min_dist_sensor,0.3)
    return atten+rep


def sparse_rewardII(instance,*args,**kwargs):
    collide = instance.collide_flag
    finish = instance.finish_flag
    states = kwargs.get("states")

    x = states[0]
    y = states[1]
    v = states[2]
    w = states[3]
    theta = states[4]
    obs_sensor = states[5:5+8]
    dist = states[-2]
    angle = states[-1]


    if kwargs.get("init",False):
        instance.rwd_hst["lst_poten"] =cal_poten(min(obs_sensor),dist,10,10)
        instance.rwd_hst["v"] = v
        instance.rwd_hst["omega"] = w
        return 0
    else:
        poten =  cal_poten(min(obs_sensor),dist,10,10)
        r = 10*(instance.rwd_hst["lst_poten"] - poten)
        r -= abs(v - instance.rwd_hst["v"]) ** 2 + abs(w - instance.rwd_hst["omega"]) ** 2

        instance.rwd_hst["lst_poten"] = poten
        instance.rwd_hst["v"] = v
        instance.rwd_hst["omega"] = w

        if collide:
            return  -10
        if finish:
            return  500

        return r



REWARD_FACTORY["sparse"] = sparse_rewardII