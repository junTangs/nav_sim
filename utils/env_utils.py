from dis import dis
from pygame.sprite import Sprite
from .math_utils import distance


def collide(sprite1, sprite2):
    """
    判断两个精灵是否碰撞
    :param sprite1:
    :param sprite2:
    :return:
    """
    if distance(sprite1.x, sprite1.y, sprite2.x, sprite2.y) <= sprite1.r + sprite2.r:
        return True
    else:
        return False
    
    
    