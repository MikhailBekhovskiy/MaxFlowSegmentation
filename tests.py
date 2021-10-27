from dinic import *
import time


def line_transformer(line):
    bufnum = None
    res = []
    for letter in line:
        if letter == '\n':
            if bufnum is not None:
                res.append(bufnum)
            return res
        if letter == ' ' and bufnum is not None:
            res.append(bufnum)
            bufnum = None
        if letter != ' ' and bufnum is None:
            bufnum = int(letter)
        elif letter != ' ' and bufnum is not None:
            bufnum = bufnum * 10 + int(letter)
    return res


def parse_test(fname):
    res = []
    with open('MaxFlow-tests/' + fname, 'r') as f:
        for line in f:
            res.append(line_transformer(line))
    return res


def graph_gen(parsed):
    G = {}
    for line in parsed[1:]:
        u = line[0]
        v = line[1]
        cap = line[2]
        if u not in G:
            G[u] = {}
        if v not in G:
            G[v] = {}
        G[u][v] = [cap, 0]
    return G


fnames = ['test_1', 'test_2', 'test_3', 'test_4', 'test_5', 'test_6',
          'test_d1', 'test_d2', 'test_d3', 'test_d4', 'test_d5',
          'test_rd01', 'test_rd02', 'test_rd03', 'test_rd04', 'test_rd05',
          'test_rd06', 'test_rd07',
          'test_rl01', 'test_rl02', 'test_rl03', 'test_rl04', 'test_rl05',
          'test_rl06', 'test_rl07', 'test_rl08', 'test_rl09', 'test_rl10'
          ]

for fn in fnames:
    fname = fn+'.txt'
    stored = parse_test(fname)
    G = graph_gen(stored)
    time1 = time.perf_counter()
    G_final = dinic(G, 1, stored[0][0])
    time2 = time.perf_counter()
    mfv = flow_value(G, 1)
    time_res = time2 - time1
    with open('testing.txt', 'a') as w:
        w.write('Results for ' + fname + ': ' + '\n')
        w.write('\t' + 'Max-flow value: ' + str(mfv) + '\n')
        w.write('\t' + 'Calculations time: ' + '{:10.7f}'.format(time_res) +
                's' + '\n')
