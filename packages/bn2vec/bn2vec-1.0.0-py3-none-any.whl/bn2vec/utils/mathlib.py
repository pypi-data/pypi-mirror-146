import numpy as np
import bisect

from bn2vec.utils.configparser import Config


def get_clustering_coefficient(
    graph: dict,
    edges: set
):
    len_edges = len(edges)
    nbr_of_possible_edges = len_edges*(len_edges-1)
    nbr_of_edges = 0
    for edge in edges:
        nbr_of_edges += len(set(graph[edge].keys()).intersection(edges))
    return nbr_of_edges/nbr_of_possible_edges if nbr_of_possible_edges > 0 else 1


def divide_by_sign(
    literals: tuple
):
    pos = []
    neg = []
    for lit in literals:
        if lit.iscanonical:
            pos.append(lit)
        else:
            neg.append(list(lit.symbols)[0])
    return pos, neg


def linear_interpolation(
    xp: float,
    x: float,
    pcumm: float,
    cumm: float,
    p_i: float = 0.25
):
    if xp is None:
        if x == 0:
            return x
        elif x != 0:
            xp, pcumm = 0, 0
    if pcumm == cumm:
        return x
    xdiff = x - xp
    pdiff = cumm - pcumm
    bias = xp
    slope = xdiff/pdiff
    return slope*(p_i - pcumm) + bias


def set_trivial_case_features(
    features,
    dnf_features,
    graph,
    properties
):
    for feature in features:
        for _property in properties:
            dnf_features[f'{graph}_{_property}_{feature}'] = 0


def update_statistics(
    stats_level,
    feature,
    curr_stats,
    new_data,
    data_count,
    obs_count=1
):
    stats = Config.Stats.rsf_stats if stats_level == 'rsf' else (Config.Stats.lsf_stats if stats_level == 'lsf' else Config.Stats.bn_stats)
    for obs in new_data:
        obs = np.round(float(obs), decimals=2)
        if 'min' in stats:
            ford, sord = (obs,obs) if curr_stats.get(f'{feature}_min', np.inf) == np.inf else sorted((obs, curr_stats[f'{feature}_min']))
            curr_stats[f'{feature}_min'] = ford
        else:
            sord = obs
        if '2nd-order-stat' in stats:
            curr_stats[f'{feature}_2nd-order-stat'] = sord if curr_stats.get(f'{feature}_2nd-order-stat', np.inf) > sord else curr_stats[f'{feature}_2nd-order-stat']
        if 'max' in stats:
            curr_stats[f'{feature}_max'] = obs if curr_stats.get(f'{feature}_max', -np.inf) < obs else curr_stats[f'{feature}_max']
        for i in range(1, 4):
            curr_stats[f'{feature}_moment{i}'] = curr_stats.get(f'{feature}_moment{i}',0) + obs_count*(obs**i) /data_count
        if 'mode' in stats or 'entropy' in stats or '25%' in stats or '50%' in stats or '75%' in stats:
            if 'ratio' not in feature and 'entropy' not in feature:
                if f'{feature}_pmf' in curr_stats.keys():
                    try:
                        oldval = curr_stats[f'{feature}_pmf']['pmf'][obs]
                    except Exception:
                        notin = True
                        oldval = 0

                    notin = obs not in curr_stats[f'{feature}_pmf']['pmf']
                    curr_stats[f'{feature}_pmf']['pmf'][obs] = oldval + obs_count/data_count
                    if notin: bisect.insort(curr_stats[f'{feature}_pmf']['order'], obs)
                else:
                    curr_stats[f'{feature}_pmf'] = {"order":[obs], "pmf":{obs: obs_count/data_count}}


def wrap_up_statistics(
    stats_level,
    feature,
    curr_stats
):
    stats = Config.Stats.rsf_stats if stats_level == 'rsf' else (Config.Stats.lsf_stats if stats_level == 'lsf' else Config.Stats.bn_stats)
    if 'max' in stats and 'min' in stats and 'range' in stats:
        curr_stats[f'{feature}_range'] = curr_stats[f'{feature}_max'] - curr_stats[f'{feature}_min']
    # the sorting has to be changed.
    if 'mode' in stats or 'entropy' in stats or '25%' in stats or '50%' in stats or '75%' in stats:
        if 'ratio' in feature or 'entropy' in feature:
            seq = curr_stats[feature]
            norm = len(seq)
            bins = norm if norm > 2 else int(np.round(2*norm/3))
            p,x = np.histogram(seq, bins=bins)
            p = p/norm
            x = np.hstack((x[:-2],x[-1]))
            curr_stats[f'{feature}_pmf'] = tuple(zip(x,p))
    # if self.mode == 'lossy': curr_stats[f'{feature}_median'] = curr_stats[f'{feature}_pmf'][len(curr_stats[f'{feature}_pmf'])//2][0]
    if 'std' in stats:
        curr_stats[f'{feature}_std'] = np.sqrt(np.round(curr_stats[f'{feature}_moment2'], decimals=4) - np.round(curr_stats[f'{feature}_moment1']**2, decimals = 4)) 
    if 'mode' in stats:
        curr_stats[f'{feature}_mode'] = (np.nan, -np.inf)
    # curr_stats[f'{feature}_coeff_var'] = curr_stats[f'{feature}_std']/curr_stats[f'{feature}_moment1'] if curr_stats[f'{feature}_moment1'] != 0 else 0
    xp = None
    cumm = 0
    quartiles = {25:False, 50:False, 75:False}
#     if feature == "cg_cc": print(curr_stats[f'{feature}_pmf'])
#     if 'cc' in feature: print(feature, curr_stats[f'{feature}_pmf'])
#     if 'cg_weights' in feature : print(curr_stats[f'{feature}_pmf'])
    if 'mode' in stats or 'entropy' in stats or '25%' in stats or '50%' in stats or '75%' in stats:
        for x in curr_stats[f'{feature}_pmf']['order']:
            p = curr_stats[f'{feature}_pmf']['pmf'][x]
            if 'entropy' in stats:
                curr_stats[f'{feature}_entropy'] = curr_stats.get(f'{feature}_entropy', 0) - p*np.log2(p) if p != 0 else 0
            if 'mode' in stats:
                if p > curr_stats[f'{feature}_mode'][1]: curr_stats[f'{feature}_mode'] = (x,p)
            cumm += p
            for quartile, reached in quartiles.items():
    #             print(quartile)
                if f'{quartile}%' in stats:
                    if not reached and cumm >= quartile/100 :
                        quartiles[quartile] = True
                        curr_stats[f'{feature}_{quartile}%'] = linear_interpolation(xp, x, cumm - p, cumm, p_i = quartile/100)
        #                 if 'vgp_weights' in feature: 
        #                     print(x,cumm, xp, cumm - p, quartile, curr_stats[f'{feature}_{int(quartile*100)}%'])
        #                     print(curr_stats[f'{feature}_pmf'])
                    else:
                        xp = x
    if '25%' in stats and '75%' in stats and 'IQ-range' in stats:
        curr_stats[f'{feature}_IQ-range'] = curr_stats[f'{feature}_75%'] - curr_stats[f'{feature}_25%']

    if 'mode' in stats:
        curr_stats[f'{feature}_mode'] = curr_stats[f'{feature}_mode'][0]
