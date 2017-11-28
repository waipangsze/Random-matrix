import numpy as np
from numpy import linalg
import copy
import time
import sys
import itertools
import multiprocessing

def Hamiltonian(n, gamma, disorder):
    set_ensemble = int(1000/int(n/5.0))
    print("set_ensemble = ", set_ensemble)
    ensemble = np.zeros(2**n -1)
    ensemble_average = np.zeros(set_ensemble)

    stuff = [i+1 for i in range(n)]

    for se in range(set_ensemble):
        manybody_energy = np.zeros(2**n)
        delta_energy = np.zeros(2**n -1)
        Jx = 1.0 + gamma + disorder * np.random.uniform(-disorder, disorder, n - 1)
        Jy = 1.0 - gamma + disorder * np.random.uniform(-disorder, disorder, n - 1)
        tj = (Jx + Jy)/4.0
        deltaj = (Jx - Jy)/4.0

        A = np.diag(tj, k=1) + np.diag(tj, k=-1)
        B = np.diag(-tj, k=1) + np.diag(-tj, k=-1)
        C = np.diag(deltaj, k=1) + np.diag(-deltaj, k=-1)
        D = np.diag(-deltaj, k=1) + np.diag(deltaj, k=-1)

        H = np.hstack((np.vstack((A, D)), np.vstack((C, B))))

        # The eigenvalues in ascending order, each repeated according to its multiplicity.
        w = np.linalg.eigvalsh(H)
        w = w/n
        wneq = w[:n]

        # itertools.combinations returns an iterator.
        # This is like a list, except it just gives you one element at a time, on demand,
        # instead of creating them all at once. This saves memory.
        # Whether you can get what you want from that iterator depends on what you want to do.
        itercount = 0
        for L in range(0, len(stuff) + 1):
            for subset in itertools.combinations(stuff, L):
                copyw = copy.copy(wneq)
                for i in range(len(subset)):
                    copyw[subset[i]-1] *= -1
                manybody_energy[itercount] = np.sum(copyw)
                itercount += 1

        manybody_energy = np.sort(manybody_energy)/2
        delta_energy = manybody_energy[1:] - manybody_energy[:2**n-1]
        ensemble = np.vstack((ensemble, delta_energy))

    ensemble = ensemble[1:, :]
    r_n = np.zeros((set_ensemble, 2**n - 2))
    for p1 in range(set_ensemble):
        for p2 in range(2**n - 2):
            r_n[p1, p2] = min(ensemble[p1, p2], ensemble[p1, p2 + 1]) / max(ensemble[p1, p2], ensemble[p1, p2 + 1])

    # np.mean(a, axis=0) # =1 is mean row, =0 is mean coloumn
    average_rn = np.mean(r_n, axis=0)


    r_average = np.mean(average_rn)
    r_std = np.std(average_rn)
    np.savetxt('E_v2.txt', r_n)
    return n, r_average, r_std

def Hamiltonian_part_spectrum(n, gamma, disorder):
    ## we set a center energy and take energy spectrum around it
    ## may set as 100
    set_ensemble = int(1000/int(n/5.0))
    print("set_ensemble = ", set_ensemble)
    ensemble = np.zeros(2**n -1)
    ensemble_average = np.zeros(set_ensemble)

    stuff = [i+1 for i in range(n)]

    for se in range(set_ensemble):
        manybody_energy = np.zeros(2**n)
        delta_energy = np.zeros(2**n -1)
        Jx = 1.0 + gamma + disorder * np.random.uniform(-disorder, disorder, n - 1)
        Jy = 1.0 - gamma + disorder * np.random.uniform(-disorder, disorder, n - 1)
        tj = (Jx + Jy)/4.0
        deltaj = (Jx - Jy)/4.0

        A = np.diag(tj, k=1) + np.diag(tj, k=-1)
        B = np.diag(-tj, k=1) + np.diag(-tj, k=-1)
        C = np.diag(deltaj, k=1) + np.diag(-deltaj, k=-1)
        D = np.diag(-deltaj, k=1) + np.diag(deltaj, k=-1)

        H = np.hstack((np.vstack((A, D)), np.vstack((C, B))))

        # The eigenvalues in ascending order, each repeated according to its multiplicity.
        w = np.linalg.eigvalsh(H)
        w = w/n
        wneq = w[:n]

        # itertools.combinations returns an iterator.
        # This is like a list, except it just gives you one element at a time, on demand,
        # instead of creating them all at once. This saves memory.
        # Whether you can get what you want from that iterator depends on what you want to do.
        itercount = 0
        for L in range(0, len(stuff) + 1):
            for subset in itertools.combinations(stuff, L):
                copyw = copy.copy(wneq)
                for i in range(len(subset)):
                    copyw[subset[i]-1] *= -1
                manybody_energy[itercount] = np.sum(copyw)
                itercount += 1

        manybody_energy = np.sort(manybody_energy)/2
        delta_energy = manybody_energy[1:] - manybody_energy[:2**n-1]
        ensemble = np.vstack((ensemble, delta_energy))

    ensemble = ensemble[1:, :]
    r_n = np.zeros((set_ensemble, 2**n - 2))
    for p1 in range(set_ensemble):
        for p2 in range(2**n - 2):
            r_n[p1, p2] = min(ensemble[p1, p2], ensemble[p1, p2 + 1]) / max(ensemble[p1, p2], ensemble[p1, p2 + 1])

    # np.mean(a, axis=0) # =1 is mean row, =0 is mean coloumn
    average_rn = np.mean(r_n, axis=0)

    r_average = np.mean(average_rn)
    r_std = np.std(average_rn)

    ## Now, we have to calculate the part of spectrum
    part_spectrum = 70
    rlist = []

    for p0 in range(int(2**n - 2 - part_spectrum)):
        r_n = np.zeros((set_ensemble, part_spectrum))
        for p1 in range(set_ensemble):
            for p2 in range(part_spectrum):
                p3 = p0 + p2
                r_n[p1, p2] = min(ensemble[p1, p3], ensemble[p1, p3 + 1]) / max(ensemble[p1, p3], ensemble[p1, p3 + 1])
        part_average_rn = np.mean(r_n, axis=0)
        part_r_average = np.mean(part_average_rn)
        part_r_std = np.std(part_average_rn)
        rlist.append(part_r_average)


    return n, r_average, r_std, np.asarray(rlist)


