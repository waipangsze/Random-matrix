import numpy as np
import os, sys, time
import multiprocessing
import xy_fermion, sys_info
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams["savefig.directory"]=os.chdir(os.getcwd())

def cal_a_point(params):
    """
    calculate a point
    :return:
    """
    n, gamma, disorder = params
    timestr = time.strftime("%Y%m%d_%H%M%S")
    print('n, gamma, disorder = ', params)
    n, r, ra = xy_fermion.Hamiltonian(n, gamma, disorder)
    print(n, r, ra)
    filename = ("1d_a_point_n_%s_gamma_%s_disorder_%s_"+timestr+".csv") % (n, gamma, disorder)
    print(' File name = \n', filename)
    f1 = open(filename, 'wb')
    np.savetxt(f1, r[np.newaxis], delimiter=',')
    f1.close()

def ratio_vs_disorder(params):
    '''
    Calculate the r ration vs list of disorder
    m = a list of disorder from 0.01 to 4.0
    :return:
    '''
    n, gamma, m = params
    timestr = time.strftime("%Y%m%d_%H%M%S")
    cores = multiprocessing.cpu_count()
    print('Total cores = ', cores)
    pool = multiprocessing.Pool(processes=cores)

    list_disorder = np.linspace(0.01, 4.0, m)
    print('n, gamma, list_disorder \n = ', n, gamma, list_disorder)

    tasks = [(n, gamma, list_disorder[x]) for x in range(m)]
    filename = ("1d_n_%s_gamma_%s_ratio_vs_disorder_"+timestr+".csv") % (n, gamma)
    print(' File name = \n', filename)
    f1 = open(filename, 'wb')
    r = pool.starmap(xy_fermion.Hamiltonian, tasks)
    r = np.asarray(r)
    print(r.shape, list_disorder[np.newaxis].T.shape)
    np.savetxt(f1, np.hstack([r, list_disorder[np.newaxis].T]), delimiter=',')
    f1.close()

    pool.close()
    pool.join()

    print('r, list_disorder = \n ', np.hstack([r, list_disorder[np.newaxis].T]))

def finite_size_scaling(params):
    # plot from N= 4 to xx , for gamma = 0.1 and disorder = 0.5, 3.0
    n_max, gamma, disorder = params # if 4, 1.0, 0.5  then from 4 to n_max + 4
    timestr = time.strftime("%Y%m%d_%H%M%S")
    cores = multiprocessing.cpu_count()
    print('Total cores = ', cores)
    pool = multiprocessing.Pool(processes=cores)
    list_n = [i+4 for i in range(n_max + 1)]
    list_n = np.asarray(list_n)
    list_n = list_n[0::2] # [4, 6, 8, ... , n_max+4]
    print("list n = ", list_n,"\n gamma = ", gamma, "\n disorder = ", disorder)

    tasks = [(list_n[x], gamma, disorder) for x in range(list_n.shape[0])]
    print(' Tasks list [list_n, gamma, disorder] = \n', tasks)
    filename = ("1d_finite_size_scaling_gamma_%s_disorder_%s_"+timestr+".csv")%(gamma, disorder)
    print(' File name = \n', filename)
    f1 = open(filename, 'wb')
    r = pool.starmap(xy_fermion.Hamiltonian, tasks)
    r = np.asarray(r)
    np.savetxt(f1, r, delimiter=',')
    f1.close()

    pool.close()
    pool.join()

    print('r =\n ', r)

def run(f, params):
    print('='*50)
    print('Start with ', time.asctime(time.localtime(time.time())))
    t1 = time.time()
    print('='*50)

    f(params)

    print('='*50)
    t2 = time.time()
    print('time = ', t2 - t1, ' s ')
    print('time = ', (t2 - t1) / 60, ' mins ')
    print('time = ', (t2 - t1) / (60*60), 'hours')
    print('time = ', (t2 - t1) / (60*60*24), ' days')
    print('End with ', time.asctime(time.localtime(time.time())))
    print('='*50)
    sys_info.sysinfo()
