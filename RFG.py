from IFSGL import *
import random as rd


def random_fractal():
    # how many transformations ?
    t = rd.randint(2, 6)

    # define check_transformations
    master_list = {0:'Scale', }
    transformations = []
    for _ in range(t):
