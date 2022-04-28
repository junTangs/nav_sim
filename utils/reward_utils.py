REWARD_FACTORY = {}



def sparse_reward(instance,*args,**kwargs):
    collide = instance.collide_flag
    finish = instance.finish_flag

    if finish:
        return 1
    elif collide:
        return -1
    else:
        return 0
    
REWARD_FACTORY["sparse"] = sparse_reward