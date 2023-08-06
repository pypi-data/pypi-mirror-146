# import bisect
from ..utils import *


class Obj2Vec(object):

    def __init__(self):
        super(Obj2Vec, self).__init__()

    # def pretty(self, d, indent=0):
    #     for key, value in d.items():
    #         print('\t' * indent + str(key))
    #         for var, w in value.items():
    #             print('\t'* (indent + 1) + str(var) + " : " + str(w))

    def run_stats_on_graphs(
        self,
        stats_level,
        graph_name,
        graph,
        obj_features,
        nbr_nodes
    ):
        properties = []
        zeros = {}
        if (self.is_dnf_level and 'cc' in Config.Sequences.dnf_sequences) or (not self.is_dnf_level and 'cc' in Config.Sequences.bn_sequences):
            properties.append('cc')
            zeros['cc'] = [nbr_nodes, nbr_nodes - len(graph.keys())]
        if (self.is_dnf_level and 'degrees' in Config.Sequences.dnf_sequences) or (not self.is_dnf_level and 'degrees' in Config.Sequences.bn_sequences):
            properties.append('degrees')
            zeros['degrees'] = [nbr_nodes, nbr_nodes - len(graph.keys())]
        if (self.is_dnf_level and 'weights' in Config.Sequences.dnf_sequences) or (not self.is_dnf_level and 'weights' in Config.Sequences.bn_sequences):
            properties.append('weights')
            zeros['weights'] = [nbr_nodes*(nbr_nodes - 1), nbr_nodes*(nbr_nodes - 1) - self._meta[f'{graph_name}_edges_count']]
        if graph == {}:
            set_trivial_case_features(Config.Stats.rsf_stats if stats_level else Config.Stats.bn_stats, obj_features, graph_name, properties = properties)
        else:
            for _property, val  in  zeros.items(): 
                normalizer, len_zeros = val
                self.sequences[f'{graph_name}_{_property}']['zeros'] = len_zeros
                if stats_level in Config.Embeddings:
                    update_statistics(stats_level, f'{graph_name}_{_property}', obj_features, [0], normalizer, obs_count=len_zeros)
            for node, edges in graph.items():
                data = zeros.copy()
                if (self.is_dnf_level and 'cc' in Config.Sequences.dnf_sequences) or (not self.is_dnf_level and 'cc' in Config.Sequences.bn_sequences):
                    cc = get_clustering_coefficient(graph, set(edges.keys()))
                    self.sequences[f'{graph_name}_cc'][node] = cc
                    data['cc'][1] = [cc]
                if (self.is_dnf_level and 'degrees' in Config.Sequences.dnf_sequences) or (not self.is_dnf_level and 'degrees' in Config.Sequences.bn_sequences):
                    data['degrees'][1] = [self.sequences[f'{graph_name}_degrees'][node]]
                if (self.is_dnf_level and 'weights' in Config.Sequences.dnf_sequences) or (not self.is_dnf_level and 'weights' in Config.Sequences.bn_sequences):
                    data['weights'][1] = [w for _,w in edges.items()]

                for _property, val in data.items(): 
                    normalizer, val = val
                    if stats_level in Config.Embeddings:
                        update_statistics(stats_level, f'{graph_name}_{_property}', obj_features, val, normalizer)
            for _property in properties: 
                if stats_level in Config.Embeddings:
                    wrap_up_statistics(stats_level, f'{graph_name}_{_property}', obj_features)

