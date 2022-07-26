import math
from numba import njit
import numpy as np
@njit
def rotate(x,y,degree):
    x_new = x*math.cos(math.radians(degree)) - y*math.sin(math.radians(degree))
    y_new = x*math.sin(math.radians(degree)) + y*math.cos(math.radians(degree))
    return x_new,y_new

@njit
def rotate_array(x,y,degree):
    x_new = x*np.cos(np.radians(degree)) - y*np.sin(np.radians(degree))
    y_new = x*np.sin(np.radians(degree)) + y*np.cos(np.radians(degree))
    return x_new,y_new



@njit
def distance(x1,y1,x2,y2):
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)

@njit
def manhattan_distance(x1,y1,x2,y2):
    return abs(x1 - x2)+abs(y1 - y2)

@njit
def gaussian(x,sigma = 10):
    return math.e**(-x**2/(2*sigma**2))

@njit
def line_circle_cross_cal(x,y,dir_x,dir_y,c_x,c_y,r):
    # M = P-C
    m_0 = x - c_x
    m_1 = y - c_y
    
    # b = M.dir
    b = m_0*dir_x + m_1*dir_y
    # c = M.M - r*r
    c = m_0*m_0 + m_1*m_1 - r*r
    # d = b*b -c 
    d = b*b - c
    
    if c > 0 and b > 0 :
        return -1
    
    
    if d <0 :
        return -1
    elif d ==0 :
        return -b
    elif d > 0 :
        return min(-b+math.sqrt(d),-b-math.sqrt(d))

# @njit
def clock_angle(x1,y1,x2,y2):
    the_norm1 = math.sqrt(x1**2 + y1**2)
    the_norm2 = math.sqrt(x2**2 + y2**2)
    the_norm = the_norm1 * the_norm2

    
    dot = x1*x2 + y1*y2
    cross = x1*y2 - x2*y1
    rho = math.asin(cross / the_norm)
    theta = math.acos(dot / the_norm)
    theta = math.degrees(theta)
    return theta if rho > 0 else -theta

@njit
def norm(x,max_x,min_x = 0):
    return (x-min_x)/(max_x-min_x)

@njit
def recover_norm(norm_x,max_x,min_x = 0):
    return norm_x*(max_x - min_x)+min_x

@njit
def trans_angle(angle):
    return 180 - (180-angle)%360


@njit
def symmetic_y_a(x,y,a):
    return x,2*a-y

def scare(x,y,src,dst):
    return x*(dst[0]/src[0]),y*(dst[1]/src[1])


def xy_into_display(x,y,display_size,size):
    x,y = scare(x,y,size,display_size)
    return symmetic_y_a(x,y,display_size[1]//2)

@njit
def normalize_2d(x,y):
    sq = x**2+y**2
    return x/math.sqrt(sq),y/math.sqrt(sq)

if __name__ == "__main__":
    for i in range(100000):
        line_circle_cross_cal(0,0,1,1,0,0,1)