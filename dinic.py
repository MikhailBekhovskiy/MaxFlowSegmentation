import time


# 1. general utility
# we modify graph so that skew function model of a flow is feasible:
# for (u,v) that so (v,u) doesn't exist we add (v,u) with 0-capacity
# initially, flow through these edges equals 0 as well
# further we assume (and provide) that f(u,v) = -f(v,u)
# while creating additional edges,
# this allows us to maintain uniform structure
# for the sake of residual network's simplicity
def add_antiparallel(G):
    for v in G:
        for u in G[v]:
            if v not in G[u]:
                G[u][v] = [0, 0]
    # print("Graph prepared")


# 2. max-flow utility
# this function not only modifies flow values,
# but reforms residual network accordingly as well
# returns list of saturated edges
def push_flow(G, res, layered, path, value):
    sat = []
    for i in range(len(path) - 1):
        v = path[i]
        u = path[i+1]
        G[v][u][1] += value
        G[u][v][1] -= value
        res[v][u] -= value
        if res[v][u] == 0:
            sat.append((v, u))
            del res[v][u]
            layered[v][0].discard(u)
            layered[u][1].discard(v)
        if v in res[u]:
            res[u][v] += value
        else:
            res[u][v] = value
    # print(f'Pushed flow {min}')
    return sat


# Assuming skew nature of our flow, generating residual network is quite simple
def res_gen(G):
    residual = {}
    for v in G:
        residual[v] = {}
        for u in G[v]:
            res_cap = G[v][u][0] - G[v][u][1]
            if res_cap > 0:
                residual[v][u] = res_cap
    return residual


def BFSmod(G, s):
    levels = {}
    reachable = {}
    for v in G:
        levels[v] = -1
        reachable[v] = False
    levels[s] = 0
    queue = [s]
    while queue != []:
        v = queue.pop(0)
        for u in G[v]:
            if levels[u] == -1:
                levels[u] = levels[v] + 1
                reachable[u] = True
                queue.append(u)
    return reachable


def min_cut(g_f, s, t):
    reach = BFSmod(g_f, s)
    segmentation = {}
    for v in reach:
        if v != s and v != t:
            if reach[v] is True:
                segmentation[v] = 'white'
            else:
                segmentation[v] = 'black'
    print('Min-cut found')
    return segmentation


# 2.1 Dinic' utility
# Extended BFS populates parents' tree with all possible edges
# between consecutive levels
def BFS_ext(G, s):
    levels = {}
    parents = {}
    for v in G:
        levels[v] = -1
        parents[v] = set()
    levels[s] = 0
    queue = [s]
    while queue != []:
        head = queue.pop(0)
        for tail in G[head]:
            if levels[tail] == -1:
                levels[tail] = levels[head] + 1
                parents[tail].add(head)
                queue.append(tail)
            elif levels[tail] == levels[head] + 1:
                parents[tail].add(head)
    return parents


# BFS parents' tree may be considered a reversed graph. thus by running
# BFS second time on parents' tree from sink yields us clean layered network
# with natural direction of edges
# since BFS parents' tree includes all the vertices of the original graph,
# we have to manually delete vertices with no outgoing edges
def lay_gen(G, s, t):
    unculled = BFS_ext(G, s)
    culled = BFS_ext(unculled, t)
    for v in list(culled.keys()):
        if v != t and culled[v] == set():
            del culled[v]
    if culled == {t: set()}:
        return {}
    res = {}
    for v in culled:
        res[v] = [culled[v], unculled[v]]
    return res


# Choosing ANY path in layered network
def get_path(layered, g_f, s, t):
    min = float('inf')
    path = [s]
    elem = s
    while elem != t:
        v = elem
        u = list(layered[elem][0])[0]
        if g_f[v][u] < min:
            min = g_f[v][u]
        path.append(u)
        elem = u
    # print(f'Path found: {path}')
    return path, min


# 2.1.1 cleaning layered network
# whether right-end vertex has incoming edges left in the network check
# requires going through all remaining vertices.
# (level-based check)
def right_pass(L, Q_r):
    while Q_r != []:
        v = Q_r.pop(0)[1]
        if v in L:
            if L[v][1] == set():
                for u in L[v][0]:
                    Q_r.append((v, u))
                    L[u][1].discard(v)
                del L[v]


# as in the previous function selecting incoming edges may prove to be
# time consuming.
def left_pass(L, Q_l):
    while Q_l != []:
        v = Q_l.pop(0)[0]
        # print(L)
        if v in L:
            if L[v][0] == set():
                income = L[v][1]
                del L[v]
                for head in income:
                    Q_l.append((head, v))
                    L[head][0].discard(v)


def cleaning(L, sat):
    Q_l = list(sat)
    Q_r = list(sat)
    right_pass(L, Q_r)
    left_pass(L, Q_l)
    if L == {}:
        # print("End of phase")
        return 'vanished'
    # print('Continuing phase')
    return 'continue'


def dinic(G, s, t):
    time1 = time.perf_counter()
    add_antiparallel(G)
    G_f = res_gen(G)
    L = lay_gen(G_f, s, t)
    time2 = time.perf_counter()
    print(f'initialization done in {time2 - time1}')
    time1 = time.perf_counter()
    while L != {}:
        # print(L)
        path, val = get_path(L, G_f, s, t)
        # print(path)
        sat = push_flow(G, G_f, L, path, val)
        # print(sat)
        # print(L)
        res = cleaning(L, sat)
        if res == 'vanished':
            L = lay_gen(G_f, s, t)
    time2 = time.perf_counter()
    print(f'Max-flow found in {time2 - time1}')
    return G_f


def flow_value(G, s):
    res = 0
    for u in G[s]:
        res += G[s][u][1]
    return res


# G = {'s': {'a': [13, 0], 'c': [1, 0], 'b': [1, 0]},
#      'a': {'d': [2, 0], 'e': [1, 0]},
#     'c': {'a': [12, 0], 'g': [2, 0]},
#     'b': {'c': [7, 0], 'f': [4, 0]},
#     'd': {'e': [3, 0]},
#     'e': {'g': [3, 0], 't': [9, 0]},
#     'g': {'t': [9, 0]},
#     'f': {'t': [4, 0]},
#     't': {}
#     }
# print(min_cut(dinic(G, 's', 't'), 's'))
# L = {1: {4, 5, 6}, 4: {7}, 5: {7}, 6: {7}, 7: set()}
# sat = [(1, 4), (4, 7)]
# L[1].discard(4)
# L[4].discard(7)
# print(cleaning(L, sat))
# print(L)
