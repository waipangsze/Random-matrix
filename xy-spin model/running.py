import numpy as np
import os, sys, time
import multiprocessing
import xy_fermion
import main_xy_fermion

if __name__ == '__main__':
    '''
    There are three functions with different set of params
    '''
    params = [4, 0.5, 4]
    # params = [10, 0.5, 4.0] = [n, gamma, disorder]
    a = main_xy_fermion.cal_a_point
    # params = [10, 0.5, 40] = [n, gamma, size of disoder list]
    b = main_xy_fermion.ratio_vs_disorder
    # params = [4, 1.0, 0.5] = [n_max, gamma, disorder] for from 4 to n_max + 4]
    c = main_xy_fermion.finite_size_scaling
    main_xy_fermion.run(c, params)
