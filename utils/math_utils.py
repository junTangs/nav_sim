import math



def rotate(x,y,degree):
    x_new = x*math.cos(math.radians(degree)) - y*math.sin(math.radians(degree))
    y_new = x*math.sin(math.radians(degree)) + y*math.cos(math.radians(degree))
    return x_new,y_new

