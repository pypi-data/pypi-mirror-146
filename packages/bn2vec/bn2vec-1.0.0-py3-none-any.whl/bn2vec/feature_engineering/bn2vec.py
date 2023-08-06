from bn2vec import np, pd
from bn2vec.utils import *
from bn2vec.feature_engineering.dnf2vec import Dnf2Vec
from bn2vec.feature_engineering.obj2vec import Obj2Vec


class Bn2Vec(Obj2Vec):
    # mode: 
    # lossy -> two stage compression (stats)
    # relaxed -> single stage compression (stats)
    def __init__(self, bn):
        # turns out this features are strongly related to the influence graph
        # a set of BNs with the same influence graph will have the same following features :(
        self.sequences = {
            'compdnfp_cdegrees':{'zeros':0}, # component-dnf positive - clause degrees
            'compdnfn_cdegrees':{'zeros':0}, # component-dnf negative - clause degrees
            'compdnfp_vdegrees':{'zeros':0}, # component-dnf positive - variable degrees
            'compdnfn_vdegrees':{'zeros':0}, # component-dnf negative - variable degrees
            'compdnfp_weights':{'zeros':0}, # component-dnf positive - weights
            'compdnfn_weights':{'zeros':0}, # component-dnf negative - weights
            'compgp_degrees':{'zeros':0},  # component graph positive - degrees
            'compgn_degrees':{'zeros':0},  # component graph negative - degrees
            'compgos_degrees':{'zeros':0}, # component graph opposite sign - degrees
            'compgp_weights':{'zeros':0},  # component graph positive - weights
            'compgn_weights':{'zeros':0},  # component graph negative - weights
            'compgos_weights':{'zeros':0}, # component graph opposite sign - weights
            'compgp_cc': {'zeros':0},      # component graph positive - clustering coefficients
            'compgn_cc': {'zeros':0},      # component graph negative - clustering coefficients
            'compgos_cc':{'zeros':0},      # component graph opposite sign - clustering coefficients
            'dnfgp_degrees': {'zeros':0},  # dnf graph positive - degrees
            'dnfgp_weights': {'zeros':0},  # dnf graph positive - weights
            'dnfgp_cc': {'zeros':0},       # dnf graph positive - clustering coefficient
            'dnfgn_degrees': {'zeros':0},  # dnf graph negative - degrees
            'dnfgn_weights': {'zeros':0},  # dnf graph negative - weights
            'dnfgn_cc': {'zeros':0},       # dnf graph negative - clustering coefficient
            'dnfgos_degrees': {'zeros':0}, # dnf graph opposite sign - degrees
            'dnfgos_weights': {'zeros':0}, # dnf graph opposite sign - weights
            'dnfgos_cc': {'zeros':0}       # dnf graph opposite sign - clustering coefficient
        }
        self.dnf_features_meta = []
        self.bn_features = {
            'rsf':pd.Series(dtype='float64'),
            'lsf':pd.Series(dtype='float64'),
            'ptrns':pd.Series(dtype='float64'),
            'igf':pd.Series(dtype='float64')
        }
        self.dnfs_data = {}

        self.compdnf = {
            'compdnfp':{}, # component-dnf positive
            'compdnfn':{} # component-dnf negative
        }
        self.compg = {
            'compgp': {}, # component graph positive
            'compgn': {}, # component graph negative
            'compgos': {} # component graph opposite sign
        }
        self.dnfg = {
            'dnfgp': {}, # dnf graph positive
            'dnfgn': {}, # dnf graph negative
            'dnfgos': {}, # dnf graph opposite sign
        }
        self._meta = {
            'compdnfp_edges_count':0,
            'compdnfn_edges_count':0,
            'compgp_edges_count': 0,
            'compgn_edges_count': 0,
            'compgos_edges_count': 0,
            'dnfgp_edges_count': 0,
            'dnfgn_edges_count': 0,
            'dnfgos_edges_count': 0
        }

        self.bn = bn
        self.len_bn = len(bn)
        self.is_dnf_level = False
        super(Bn2Vec, self).__init__()

    def update_compdnf_graphs(
        self,
        compdnf_graph_name,
        comp_name,
        nbr_literals,
        literal
    ) -> None:
        if compdnf_graph_name not in Config.Graphs.bn_graphs:
            return

        if 'vdegrees' in Config.Sequences.bn_sequences:
            self.sequences[f'{compdnf_graph_name}_vdegrees'][literal] = self.sequences[f'{compdnf_graph_name}_vdegrees'].get(literal, 0) + 1/self.len_bn

        if comp_name in self.compdnf[compdnf_graph_name]:
            self.compdnf[compdnf_graph_name][comp_name][literal] = 1/nbr_literals
        else:
            self.compdnf[compdnf_graph_name][comp_name] = {literal: 2/nbr_literals}

        if 'weights' in Config.Sequences.bn_sequences:
            if f'{comp_name}_{literal}' not in self.sequences[f'{compdnf_graph_name}_weights'].keys():
                self.sequences[f'{compdnf_graph_name}_weights'][f'{comp_name}_{literal}'] = 1/self.len_bn
                self._meta[f'{compdnf_graph_name}_edges_count'] += 1

    def update_compg_graphs(
        self,
        compg_graph_name,
        weight,
        literal,
        co_literal
    ):
        if compg_graph_name not in Config.Graphs.bn_graphs:
            return

        for _, key in enumerate(((literal, co_literal), (co_literal, literal))):
            degrees_normalizer = self.len_bn
            if 'weights' in Config.Sequences.bn_sequences:
                if _ == 0:
                    seq = f'{key[0]["name"]}_{key[1]["name"]}' if key[0]["name"] < key[1]["name"] else f'{key[1]["name"]}_{key[0]["name"]}'
                    self.sequences[f'{compg_graph_name}_weights'][seq] = self.sequences[f'{compg_graph_name}_weights'].get(seq, 0) + weight
            if key[0]["name"] in self.compg[compg_graph_name].keys():
                if key[1]["name"] in self.compg[compg_graph_name][key[0]["name"]].keys():
                    self.compg[compg_graph_name][key[0]["name"]][key[1]["name"]] += weight
                else:
                    self.compg[compg_graph_name][key[0]["name"]][key[1]["name"]] = weight
                    self._meta[f'{compg_graph_name}_edges_count'] += 1
                    if 'degrees':
                        self.sequences[f'{compg_graph_name}_degrees'][key[0]["name"]] = self.sequences[f'{compg_graph_name}_degrees'].get(key[0]["name"],0) + 1/degrees_normalizer
            else:
                self.compg[compg_graph_name][key[0]["name"]] = {key[1]["name"]: weight}
                self._meta[f'{compg_graph_name}_edges_count'] += 1
                if 'degrees' in Config.Sequences.bn_sequences:
                    self.sequences[f'{compg_graph_name}_degrees'][key[0]["name"]] = self.sequences[f'{compg_graph_name}_degrees'].get(key[0]["name"],0) + 1/degrees_normalizer

    def update_compg_compdnf_graphs(
        self,
        comp_name,
        nbr_literals,
        literals,
    ):
        weight = 1/self.len_bn
        # vg_graphs_names = list(vg_graphs.keys())
        for i_literal in range(nbr_literals):
            literal_iscanonical = literals[i_literal].iscanonical
            literal = literals[i_literal].obj if literal_iscanonical else list(literals[i_literal].symbols)[0].obj
            compdnf_graphs_names = list(self.compdnf.keys())
            compdnf_graph_name = compdnf_graphs_names[0] if literal_iscanonical else compdnf_graphs_names[1]
            self.update_compdnf_graphs(
                compdnf_graph_name,
                comp_name,
                nbr_literals,
                literal
            )

            for i_co_literal in range(i_literal + 1, nbr_literals):
                # use the right graph for the right pair of literals (e.g: with positive pair we use VGP)
                co_literal_iscanonical = literals[i_co_literal].iscanonical
                compg_graph_name = ('compgp' if literal_iscanonical else 'compgn') if literal_iscanonical == co_literal_iscanonical else 'compgos'
                co_literal = literals[i_co_literal].obj if co_literal_iscanonical else list(literals[i_co_literal].symbols)[0].obj
                    
                _literal = {
                    'name': literal,
                    'iscanonical': literal_iscanonical
                }
                _co_literal = {
                    'name': co_literal,
                    'iscanonical': co_literal_iscanonical
                }

                self.update_compg_graphs(
                    compg_graph_name,
                    weight,
                    _literal,
                    _co_literal
                )

    def update_dnfg_graphs(
        self,
        i_comp,
        pos_literals,
        neg_literals
    ) -> None:
        degrees_normalizer = (self.len_bn - 1) if self.len_bn > 1 else np.inf
        for i_co_comp in range(i_comp + 1, self.len_bn):
            pos_co_literals, neg_co_literals = divide_by_sign(list(self.bn[i_co_comp][1].literals))
            cg_graphs_data = [
                ('dnfgp', pos_literals, pos_co_literals),
                ('dnfgn', neg_literals, neg_co_literals),
                ('dnfgos', pos_literals, pos_co_literals),
                ('dnfgos', neg_literals, neg_co_literals)
            ]
            for graph_name, lits, co_lits in cg_graphs_data:
                if graph_name not in Config.Graphs.bn_graphs:
                    continue
                weights_normalizer = len(set(lits).union(set(co_lits)))
                weight = len(set(lits).intersection(set(co_lits))) / weights_normalizer if weights_normalizer > 0 else 0
                if weight == 0:
                    continue
                for _,key in enumerate([(i_comp, i_co_comp), (i_co_comp, i_comp)]):
                    if 'weights' in Config.Sequences.bn_sequences:
                        if _ == 0:
                            seq = f'{key[0]}_{key[1]}' if key[0] < key[1] else f'{key[1]}_{key[0]}'
                            self.sequences[f'{graph_name}_weights'][seq] = self.sequences[f'{graph_name}_weights'].get(seq,0) + weight
                    if key[0] in self.dnfg[graph_name].keys():
                        if key[1] not in self.dnfg[graph_name][key[0]].keys():
                            self._meta[f'{graph_name}_edges_count'] += 1
                            if 'degrees' in Config.Sequences.bn_sequences:
                                self.sequences[f'{graph_name}_degrees'][key[0]] = self.sequences[f'{graph_name}_degrees'].get(key[0],0) + 1/degrees_normalizer
                        self.dnfg[graph_name][key[0]][key[1]] = np.round(weight, decimals = 3)
                    else:
                        if 'degrees' in Config.Sequences.bn_sequences:
                            self.sequences[f'{graph_name}_degrees'][key[0]] = 1/degrees_normalizer
                        self.dnfg[graph_name][key[0]] = {key[1]:weight}
                        self._meta[f'{graph_name}_edges_count'] += 1

    def generate_patterns(self, comp_name, dnf_sequences):
        ptrns = {}
        for vg in ['vgp', 'vgn', 'vgos']:
            weights = dnf_sequences[f'{vg}_weights']
            for ptrn_name, val in weights.items():
                if ptrn_name != 'zeros': ptrns[f'{comp_name}_{ptrn_name}'] = val
        return ptrns

    def aggregate_dnf_features(self, dnf, comp_name):
        gen = Dnf2Vec(dnf, comp_name=comp_name)
        dnf_graphs, dnf_sequences, dnf_features = gen.generate_features()
        self.dnfs_data[comp_name] = {'dnf_graphs':dnf_graphs, 'dnf_sequences':dnf_sequences, 'dnf_features':dnf_features}
        self.bn_features['rsf'] = pd.concat([self.bn_features['rsf'], dnf_features])
        for _, obs in dnf_features.items():
            # LSF
            if 'lsf' in Config.Embeddings:
                # if self.ishead: self.dnf_features_meta.append(_)
                update_statistics('lsf', str.join("_", _.split("_")[1:]), self.bn_features['lsf'], [obs], self.len_bn)
            # RSF
            # if 'rsf' in Config.embeddings:
            #     rsf_feature_name = f"{comp_name}_{_}"
            #     self.bn_features['rsf'] = self.bn_features['rsf'].append(pd.Series({rsf_feature_name:obs}))


        # if self.ishead: self.ishead = False 

        # PTRNS
        if 'ptrns' in Config.Embeddings:
            self.bn_features['ptrns'] = pd.concat([self.bn_features['ptrns'], pd.Series(self.generate_patterns(comp_name, dnf_sequences), dtype='float64')])

    def generate_features(self):
        # self.ishead = True

        for idnf in range(self.len_bn):
            # print(self.bn[idnf])
            comp_name, dnf = self.bn[idnf]
            literals = list(dnf.literals)
            len_dnf = len(literals)

            # aggregate DNF features : 
            self.aggregate_dnf_features(dnf, comp_name)

            self.update_compg_compdnf_graphs(idnf, len_dnf, literals)
            pos_literals, neg_literals = divide_by_sign(literals)
            self.update_dnfg_graphs(idnf, pos_literals, neg_literals)

            graphs = []
            nbr_pos = len(pos_literals)
            if 'compdnfp' in Config.Graphs.bn_graphs and 'cdegrees' in Config.Sequences.bn_sequences: graphs.append(('compdnfp', nbr_pos))
            if 'compdnfn' in Config.Graphs.bn_graphs and 'cdegrees' in Config.Sequences.bn_sequences: graphs.append(('compdnfn', len_dnf - nbr_pos))
            for graph, nbr_lits in graphs:
                self.sequences[f'{graph}_cdegrees'][comp_name] = nbr_lits/self.len_bn
                if 'igf' in Config.Embeddings:
                    update_statistics('igf', f"{graph}_cdegrees", self.bn_features['igf'], [nbr_lits/self.len_bn], self.len_bn)

        # aggregate DNF features : 
        # print(self.dnf_features_meta)
        # if 'lsf' in Config.embeddings:
        #     for feature in self.bn_features['lsf']: 
        #         self.wrap_up_statistics('lsf', feature, self.bn_features['lsf'])

        # VC sequences : 
        graphs = []
        if 'compdnfp' in Config.Graphs.bn_graphs: graphs.append('compdnfp')
        if 'compdnfn' in Config.Graphs.bn_graphs: graphs.append('compdnfn')
        for graph in graphs:
            if 'cdegrees' in Config.Sequences.bn_sequences:
                len_zeros = self.len_bn - (len(self.sequences[f'{graph}_cdegrees'].keys()) - 1)
                self.sequences[f'{graph}_cdegrees']['zeros'] = len_zeros
                if 'igf' in Config.Embeddings:
                    update_statistics('igf', f"{graph}_cdegrees", self.bn_features['igf'], [0], self.len_bn, obs_count=len_zeros)
                    wrap_up_statistics('igf', f"{graph}_cdegrees", self.bn_features['igf'])
            if 'vdegrees' in Config.Sequences.bn_sequences:
                if 'igf' in Config.Embeddings:
                    update_statistics('rsf', f"{graph}_vdegrees", self.bn_features['igf'], [v for k,v in self.sequences[f'{graph}_vdegrees'].items() if k != 'zeros'], self.len_bn)
                    wrap_up_statistics('rsf', f"{graph}_vdegrees", self.bn_features['igf'])

            if 'weights' in Config.Sequences.bn_sequences:
                len_zeros = self.len_bn**2 - self._meta[f'{graph}_edges_count']
                self.sequences[f'{graph}_weights']['zeros'] = len_zeros
                if 'igf' in Config.Embeddings:
                    update_statistics('igf', f"{graph}_weights", self.bn_features['igf'], [0], self.len_bn**2, len_zeros)
                    update_statistics('igf', f"{graph}_weights", self.bn_features['igf'], [v for k,v in self.sequences[f'{graph}_weights'].items() if k != 'zeros'], self.len_bn**2)
                    wrap_up_statistics('igf', f"{graph}_weights", self.bn_features['igf'])



        # COMPG/DNFG sequences : 
        # graphs = [(graphname, graph) for graphname, graph in self.compg.items()]
        # graphs.extend([(graphname, graph) for graphname, graph in self.dnfg.items()])

        # for graph_name, graph in graphs:
        #     self.run_stats_on_graphs(graph_name, graph, self.sequences, self.features, self.bn_features, self.len_bn)

        graphs = []
        if 'compgp' in Config.Graphs.bn_graphs: graphs.append(('compgp', self.compg['compgp'], self.len_bn))
        if 'compgn' in Config.Graphs.bn_graphs: graphs.append(('compgn', self.compg['compgn'], self.len_bn))
        if 'compgos' in Config.Graphs.bn_graphs: graphs.append(('compgos', self.compg['compgos'], self.len_bn))
        if 'dnfgp' in Config.Graphs.bn_graphs: graphs.append(('dnfgp', self.dnfg['dnfgp'], self.len_bn))
        if 'dnfgn' in Config.Graphs.bn_graphs: graphs.append(('dnfgn', self.dnfg['dnfgn'], self.len_bn))
        if 'dnfgos' in Config.Graphs.bn_graphs: graphs.append(('dnfgos', self.dnfg['dnfgos'], self.len_bn))

        for graph_name, graph, nbr_nodes in graphs:
            self.run_stats_on_graphs('igf', graph_name, graph, self.bn_features['igf'], nbr_nodes)
        
        mx = lambda x,col: ((f'moment{x}' == col and f'moment{x}' in Config.Stats.lsf_stats) or (f'moment{x}' != col))
        if 'lsf' in Config.Embeddings:
            self.bn_features['lsf'] = pd.Series({col:val for col,val in self.bn_features['lsf'].items() 
            if "pmf" not in col and mx(1,col.split("_")[1] if 'ratio' in col else col.split("_")[3]) and 
            mx(2,col.split("_")[1] if 'ratio' in col else col.split("_")[3]) and mx(3,col.split("_")[1] if 'ratio' in col else col.split("_")[3])}, dtype='float64')

        mx = lambda x,col: (f'moment{x}' in col and f'moment{x}' in Config.Stats.bn_stats) or (f'moment{x}' not in col)
        self.bn_features['igf'] = pd.Series({
            col: np.round(val, decimals = 1) if ('ratio' not in col) and ('entropy' not in col) else val 
            for col,val in self.bn_features['igf'].items() if ("pmf" not in col) and mx(1, col) and mx(2, col) and mx(3, col)
        }, dtype='float64')
        graphs = {'compdnf': self.compdnf, 'compg':self.compg, 'dnfg':self.dnfg} if Config.Memory.memorize_bn_graphs else {}
        seqs = self.sequences if Config.Memory.memorize_bn_sequences else {}
        return graphs, seqs, self.dnfs_data, self.bn_features


