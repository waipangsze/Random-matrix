import numpy as np
import os
import sys
import time
import multiprocessing
import xy_fermion
import main_xy_fermion

if __name__ == '__main__':
    a = main_xy_fermion.cal_a_point
    b = main_xy_fermion.ratio_vs_disorder
    c = main_xy_fermion.finite_size_scaling
    main_xy_fermion.run(a)
