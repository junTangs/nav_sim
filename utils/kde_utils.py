import  math
import numpy as np
from numba import njit
@njit
def gaussian_kernel(x,xc,bandwidth = 0.1):
    return (1/math.sqrt(2*math.pi))*math.e**(-((x - xc)/bandwidth)**2/2)

@njit
def kernel_density_estimate_2d(sample,x,bandwidth = 0.1):
    n = len(sample)
    res = 0
    if n == 0:
        return 0
    for i,x_i in enumerate(sample):
        k1 =  gaussian_kernel(x[0],x_i[0],bandwidth)
        k2 =  gaussian_kernel(x[1],x_i[1],bandwidth)
        res += k1*k2
    res/= n
    return res


@njit
def gaussian_np(x,y,x0,y0,sigma):
    return 255*1/(2*np.pi*sigma**2)*np.exp(-((x-x0)**2+(y-y0)**2)/(2*sigma**2))


def gaussian_kernel(height, width, x0:int, y0:int, sigma):
    x = np.arange(width)
    y = np.arange(height)
    x, y = np.meshgrid(x, y)
    return gaussian_np(x,y,x0,y0,sigma)


def density_map(height, width, samples, bandwidth = 0.1):
    res = np.zeros((width, height))
    if len(samples) == 0:
        return res
    for i in range(0,len(samples),2):
        res += gaussian_kernel(height, width, samples[i], samples[i + 1], bandwidth)

    return res



if __name__ == "__main__":
    import matplotlib.pyplot as plt
    res  = density_map(128,128,[64,64,10,10,50,50],10)
    print(res)
    plt.imshow(res)
    plt.show()