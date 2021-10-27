from PIL import Image
from weighting import *
from dinic import *


def get_fname(fpath):
    tmp = []
    i = len(fpath) - 1
    while fpath[i] != '.':
        i -= 1
    i -= 1
    while fpath[i] != '/':
        tmp.append(fpath[i])
        i -= 1
    res = ''
    for el in tmp[::-1]:
        res += el
    return res


def build_segmented(segmentation, size):
    pn = pixel_node(size)
    res = Image.new('1', size)
    pixels = res.load()
    for x in range(size[0]):
        for y in range(size[1]):
            color = segmentation[pn[(x, y)]]
            if color == 'white':
                pixels[x, y] = 255
    return res


def pixel_node(size):
    rel = {}
    i = 1
    for x in range(size[0]):
        for y in range(size[1]):
            rel[(x, y)] = i
            i += 1
    return rel


def histogram(intensities, vertices):
    res = {}
    for i in range(256):
        res[i] = 0
    for v in vertices:
        res[intensities[v]] += 1
    for i in res:
        res[i] /= len(vertices)
    return res


def vertices(coords, rel):
    res = set()
    for pixel in coords:
        if (pixel[0], pixel[1]) in rel:
            res.add(rel[(pixel[0], pixel[1])])
    return res


def node_intensities(size, pixels):
    rel = pixel_node(size)
    res = {}
    for x in range(size[0]):
        for y in range(size[1]):
            res[rel[(x, y)]] = pixels[x, y]
    return res


def graph_skeleton_4(relation, size, intensities, sigma=1):
    G = {}
    G['s'] = {}
    G['t'] = {}
    for pixel in relation:
        v = relation[pixel]
        G['s'][v] = [0, 0]
        G[v] = {}
        if pixel[0] > 0:
            u = relation[(pixel[0] - 1, pixel[1])]
            weight = boundary_penalty_adj(v, u, intensities, sigma)
            G[v][u] = [weight, 0]
        if pixel[1] > 0:
            u = relation[(pixel[0], pixel[1] - 1)]
            weight = boundary_penalty_adj(v, u, intensities, sigma)
            G[v][u] = [weight, 0]
        if pixel[0] < size[0] - 1:
            u = relation[(pixel[0] + 1, pixel[1])]
            weight = boundary_penalty_adj(v, u, intensities, sigma)
            G[v][u] = [weight, 0]
        if pixel[1] < size[1] - 1:
            u = relation[(pixel[0], pixel[1] + 1)]
            weight = boundary_penalty_adj(v, u, intensities, sigma)
            G[v][u] = [weight, 0]
        G[v]['t'] = [0, 0]
    return G


def graph_skeleton_8(relation, size, intensities, sigma=1):
    G = {}
    G['s'] = {}
    G['t'] = {}
    for pixel in relation:
        v = relation[pixel]
        G['s'][v] = [0, 0]
        G[v] = {}
        if pixel[0] > 0:
            u = relation[(pixel[0] - 1, pixel[1])]
            weight = boundary_penalty_adj(v, u, intensities, sigma)
            G[v][u] = [weight, 0]
        if pixel[0] > 0 and pixel[1] > 0:
            u = relation[(pixel[0] - 1, pixel[1] - 1)]
            weight = boundary_penalty_dia(v, u, intensities, sigma)
            G[v][u] = [weight, 0]
        if pixel[1] > 0:
            u = relation[(pixel[0], pixel[1] - 1)]
            weight = boundary_penalty_adj(v, u, intensities, sigma)
            G[v][u] = [weight, 0]
        if pixel[1] > 0 and pixel[0] < size[0] - 1:
            u = relation[(pixel[0] + 1, pixel[1] - 1)]
            weight = boundary_penalty_dia(v, u, intensities, sigma)
            G[v][u] = [weight, 0]
        if pixel[0] < size[0] - 1:
            u = relation[(pixel[0] + 1, pixel[1])]
            weight = boundary_penalty_adj(v, u, intensities, sigma)
            G[v][u] = [weight, 0]
        if pixel[0] < size[0] - 1 and pixel[1] < size[1] - 1:
            u = relation[(pixel[0] + 1, pixel[1] + 1)]
            weight = boundary_penalty_dia(v, u, intensities, sigma)
            G[v][u] = [weight, 0]
        if pixel[1] < size[1] - 1:
            u = relation[(pixel[0], pixel[1] + 1)]
            weight = boundary_penalty_adj(v, u, intensities, sigma)
            G[v][u] = [weight, 0]
        if pixel[1] < size[1] - 1 and pixel[0] > 0:
            u = relation[(pixel[0] - 1, pixel[1] + 1)]
            weight = boundary_penalty_dia(v, u, intensities, sigma)
            G[v][u] = [weight, 0]
        G[v]['t'] = [0, 0]
    return G


def gen_graph(image, obj, bck, prObj, prBck, intenses, neighbours=4,
              lamb=1, sigma=1):
    size = image.size
    pixels = image.load()
    rel_pn = pixel_node(size)
    if neighbours == 4:
        G = graph_skeleton_4(rel_pn, size, intenses, sigma)
    elif neighbours == 8:
        G = graph_skeleton_8(rel_pn, size, intenses, sigma)
    K = get_K(G, 's', 't')
    for v in G['s']:
        if v in obj:
            G['s'][v][0] = K
        elif v in bck:
            G['s'][v][0] = 0
        else:
            G['s'][v][0] = lamb * regional_penalty(prBck, intenses, v)
    for v in G:
        if v != 's' and v != 't':
            if v in obj:
                G[v]['t'][0] = 0
            elif v in bck:
                G[v]['t'][0] = K
            else:
                G[v]['t'][0] = lamb * regional_penalty(prObj, intenses, v)
    return G, K


def mod_graph(G, newObj, newBck, rel_pn, K, lamb, prObj, prBck, intensities):
    for pix in newObj:
        node = rel_pn[(pix[0], pix[1])]
        G['s'][node][0] += K + lamb * regional_penalty(prObj, intensities,
                                                       node)
        G[node]['t'][0] += lamb * regional_penalty(prBck, intensities, node)
    for pix in newBck:
        node = rel_pn[(pix[0], pix[1])]
        G['s'][node][0] += lamb * regional_penalty(prObj, intensities, node)
        G[node]['t'][0] += K + lamb * regional_penalty(prBck, intensities,
                                                       node)


def check_prob(distr):
    sum = 0
    for item in distr:
        sum += distr[item]
    return sum

# print(len(G))
# image = load_image('cross-gr-320.jpg')
# size = image.size
# pixels = image.load()
# rel_pn = pixel_node(size)
# intensities = node_intensities(size, rel_pn, pixels)
# skelet = graph_skeleton_4(rel_pn, size, intensities)
# hist = histogram(intensities, {7, 25})
# print(hist[intensities[25]])
