# this file provides functions
# for weight calculation
from math import exp, log, sqrt


# weight of neighbors' edges
def boundary_penalty_adj(v, u, intensities, sigma=1):
    i_v = intensities[v]
    i_u = intensities[u]
    if i_v <= i_u:
        return 1
    return exp(-((i_v - i_u)**2)/(2*(sigma**2)))


def boundary_penalty_dia(v, u, intensities, sigma=1):
    i_v = intensities[v]
    i_u = intensities[u]
    if i_v <= i_u:
        return 1
    return exp(-((i_v - i_u)**2)/(2*(sigma**2)))/sqrt(2)


# component for weight of terminal edges
def regional_penalty(histogram, intensities, v, worse_case_hist):
    probability = histogram[intensities[v]]
    if probability == 0:
        probability = worse_case_hist
    return -log(probability)


# constants for weights
def get_K(G, s, t):
    big = -1
    for v in G:
        neighbouring_sum = 0
        if v != s and v != t:
            for u in G[v]:
                if u != t:
                    neighbouring_sum += G[v][u][0]
        if neighbouring_sum > big:
            big = neighbouring_sum
    return big + 1


def worse_than_worst(histogram):
    min = float('inf')
    for inten in histogram:
        if histogram[inten] < min and histogram[inten] != 0:
            min = histogram[inten]
    return min / 2
