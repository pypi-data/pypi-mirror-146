from functools import reduce

from bn2vec import np, pd
from bn2vec.utils import *
from bn2vec.feature_engineering.obj2vec import Obj2Vec


class Dnf2Vec(Obj2Vec):

    def __init__(self, dnf, comp_name):
        # note that the VC graph is a special case of the VG and the CG graphs where two identical vars (resp. clauses) connect.
        # e.g: the clauses' degrees in the VC can be seen as the weight of the edge between two identical clauses in the CG.
        # these special cases aren't encoded in teh VG & CG graphs, instead we define them in the VC graphs.
        self.sequences = {
            'vcp_cdegrees': {'zeros':0}, # variable-clause positive - clause degrees
            'vcn_cdegrees': {'zeros':0}, # variable-clause negative - clause degrees
            'vcp_vdegrees': {'zeros':0}, # variable-clause positive - variable degrees
            'vcn_vdegrees': {'zeros':0}, # variable-clause negative - variable degrees
            'vcp_weights': {'zeros':0}, # variable-clause positive - weights
            'vcn_weights': {'zeros':0}, # variable-clause negative - weights
            'vgp_degrees': {'zeros':0}, # variable graph positive  - degrees
            'vgn_degrees': {'zeros':0}, # variable graph negative  - degrees
            'vgos_degrees':{'zeros':0}, # variable graph opposite sign - degrees
            'vgp_weights': {'zeros':0}, # variable graph positive - weights
            'vgn_weights': {'zeros':0}, # variable graph negative - weights
            'vgos_weights':{'zeros':0}, # variable graph opposite sign - weights
            'vgp_cc':      {'zeros':0}, # variable graph positive - clustering coefficients
            'vgn_cc':      {'zeros':0}, # variable graph negative - clustering coefficients
            'vgos_cc':     {'zeros':0}, # variable graph opposite sign - clustering coefficients
            'cgp_degrees': {'zeros':0}, # clause graph positive - degrees
            'cgn_degrees': {'zeros':0}, # clause graph negative - degrees
            'cgp_weights': {'zeros':0}, # clause graph positive - weights
            'cgn_weights': {'zeros':0}, # clause graph negative - weights
            'cgp_cc':      {'zeros':0}, # clause graph positive - clustering coefficient
            'cgn_cc':      {'zeros':0} # clause graph negative - clustering coefficient
        }
        self.vc = {
            'vcp':{}, # variable-clause positive
            'vcn':{} # variable-clause negative
        } 
        self.vg = {
            'vgp':{}, # variable graph positive
            'vgn':{}, # variable graph negative
            'vgos':{} # variable graph opposite sign
        }
        self.cg = {
            'cgp':{}, # clause graph positive
            'cgn':{} # clause graph negative
        }
        self._meta = {
            'vcp_edges_count':0,
            'vcn_edges_count':0,
            'vgp_edges_count': 0,
            'vgn_edges_count': 0,
            'vgos_edges_count': 0,
            'cgp_edges_count': 0,
            'cgn_edges_count': 0
        }

        self.dnf = dnf
        self.comp_name = comp_name
        self.clauses = [dnf] if dnf.args == () or dnf.operator == "&" else list(dnf.args)
        self.len_clauses = len(self.clauses)
        # should be optimized!
        self.total_nbr_pos, self.total_nbr_neg = reduce(lambda a,b: (a[0] + 1, a[1]) if b.iscanonical else (a[0], a[1] + 1), list(dnf.literals), (0,0))
        self.len_symbols = self.total_nbr_pos + self.total_nbr_neg
        self.dnf_features = {
            'cv-pos-ratio': self.len_clauses/self.total_nbr_pos if self.total_nbr_pos != 0 else 0,
            'cv-neg-ratio': self.len_clauses/self.total_nbr_neg if self.total_nbr_neg != 0 else 0
        }
        self._meta['len_symbols'] = self.len_symbols
        self.is_dnf_level = True
        super(Dnf2Vec, self).__init__()


    def update_vc_graphs(
        self,
        vc_graph_name,
        clause_name,
        nbr_literals,
        literal
    ) -> None:
        if vc_graph_name not in Config.Graphs.dnf_graphs:
            return

        if 'vdegrees' in Config.Sequences.dnf_sequences:
            self.sequences[f'{vc_graph_name}_vdegrees'][literal] = self.sequences[f'{vc_graph_name}_vdegrees'].get(literal, 0) + 1/self.len_clauses

        if clause_name in self.vc[vc_graph_name]:
            self.vc[vc_graph_name][clause_name][literal] = 1/nbr_literals
        else:
            self.vc[vc_graph_name][clause_name] = {literal: 2/nbr_literals}

        if 'weights' in Config.Sequences.dnf_sequences:
            if f'{clause_name}_{literal}' not in self.sequences[f'{vc_graph_name}_weights'].keys():
                self.sequences[f'{vc_graph_name}_weights'][f'{clause_name}_{literal}'] = 1/self.len_clauses
                self._meta[f'{vc_graph_name}_edges_count'] += 1

    def get_vg_degrees_normalizer(
        self,
        vg_graph_name,
        literal
    ) -> int:
        if vg_graph_name == 'vgp':
            degrees_normalizer = (self.total_nbr_pos - 1) if self.total_nbr_pos > 1 else np.inf
        elif vg_graph_name == 'vgn':
            degrees_normalizer = (self.total_nbr_neg - 1) if self.total_nbr_neg > 1 else np.inf
        elif vg_graph_name == 'vgos':
            if literal['iscanonical'] is True:
                degrees_normalizer = self.total_nbr_neg if self.total_nbr_neg > 0 else np.inf
            else:
                degrees_normalizer = self.total_nbr_pos if self.total_nbr_pos > 0 else np.inf
        return degrees_normalizer

    def update_vg_graphs(
        self,
        vg_graph_name,
        weight,
        literal,
        co_literal
    ):
        if vg_graph_name not in Config.Graphs.dnf_graphs:
            return

        for _, key in enumerate(((literal, co_literal), (co_literal, literal))):
            degrees_normalizer = self.get_vg_degrees_normalizer(
                vg_graph_name,
                key[0]
            )
            if 'weights' in Config.Sequences.dnf_sequences:
                if _ == 0:
                    seq = f'{key[0]["name"]}_{key[1]["name"]}' if key[0]["name"] < key[1]["name"] else f'{key[1]["name"]}_{key[0]["name"]}'
                    self.sequences[f'{vg_graph_name}_weights'][seq] = self.sequences[f'{vg_graph_name}_weights'].get(seq, 0) + weight
            if key[0]["name"] in self.vg[vg_graph_name].keys():
                if key[1]["name"] in self.vg[vg_graph_name][key[0]["name"]].keys():
                    self.vg[vg_graph_name][key[0]["name"]][key[1]["name"]] += weight
                else:
                    self.vg[vg_graph_name][key[0]["name"]][key[1]["name"]] = weight
                    self._meta[f'{vg_graph_name}_edges_count'] += 1
                    if 'degrees':
                        self.sequences[f'{vg_graph_name}_degrees'][key[0]["name"]] = self.sequences[f'{vg_graph_name}_degrees'].get(key[0]["name"],0) + 1/degrees_normalizer
            else:
                self.vg[vg_graph_name][key[0]["name"]] = {key[1]["name"]: weight}
                self._meta[f'{vg_graph_name}_edges_count'] += 1
                if 'degrees' in Config.Sequences.dnf_sequences:
                    self.sequences[f'{vg_graph_name}_degrees'][key[0]["name"]] = self.sequences[f'{vg_graph_name}_degrees'].get(key[0]["name"],0) + 1/degrees_normalizer

    def update_vg_vc_graphs(
        self,
        clause_name,
        nbr_literals,
        literals,
    ):
        weight = 1/self.len_clauses
        # vg_graphs_names = list(vg_graphs.keys())
        for i_literal in range(nbr_literals):
            literal_iscanonical = literals[i_literal].iscanonical
            literal = literals[i_literal].obj if literal_iscanonical else list(literals[i_literal].symbols)[0].obj
            vc_graphs_names = list(self.vc.keys())
            vc_graph_name = vc_graphs_names[0] if literal_iscanonical else vc_graphs_names[1]
            self.update_vc_graphs(
                vc_graph_name,
                clause_name,
                nbr_literals,
                literal
            )

            for i_co_literal in range(i_literal + 1, nbr_literals):
                # use the right graph for the right pair of literals (e.g: with positive pair we use VGP)
                co_literal_iscanonical = literals[i_co_literal].iscanonical
                vg_graph_name = ('vgp' if literal_iscanonical else 'vgn') if literal_iscanonical == co_literal_iscanonical else 'vgos'
                co_literal = literals[i_co_literal].obj if co_literal_iscanonical else list(literals[i_co_literal].symbols)[0].obj
                    
                _literal = {
                    'name': literal,
                    'iscanonical': literal_iscanonical
                }
                _co_literal = {
                    'name': co_literal,
                    'iscanonical': co_literal_iscanonical
                }

                self.update_vg_graphs(
                    vg_graph_name,
                    weight,
                    _literal,
                    _co_literal
                )

    def update_cg_graphs(
        self,
        i_clause,
        pos_literals,
        neg_literals
    ) -> None:
        degrees_normalizer = (self.len_clauses - 1) if self.len_clauses > 1 else np.inf
        for i_co_clause in range(i_clause + 1, self.len_clauses):
            pos_co_literals, neg_co_literals = divide_by_sign(list(self.clauses[i_co_clause].literals))
            cg_graphs_data = [('cgp', pos_literals, pos_co_literals), ('cgn', neg_literals, neg_co_literals)]
            for graph_name, lits, co_lits in cg_graphs_data:
                if graph_name not in Config.Graphs.dnf_graphs:
                    continue
                weights_normalizer = len(set(lits).union(set(co_lits)))
                weight = len(set(lits).intersection(set(co_lits))) / weights_normalizer if weights_normalizer > 0 else 0
                if weight == 0:
                    continue
                for _,key in enumerate([(i_clause, i_co_clause), (i_co_clause, i_clause)]):
                    if 'weights' in Config.Sequences.dnf_sequences:
                        if _ == 0:
                            seq = f'{key[0]}_{key[1]}' if key[0] < key[1] else f'{key[1]}_{key[0]}'
                            self.sequences[f'{graph_name}_weights'][seq] = self.sequences[f'{graph_name}_weights'].get(seq,0) + weight
                    if key[0] in self.cg[graph_name].keys():
                        if key[1] not in self.cg[graph_name][key[0]].keys():
                            self._meta[f'{graph_name}_edges_count'] += 1
                            if 'degrees' in Config.Sequences.dnf_sequences:
                                self.sequences[f'{graph_name}_degrees'][key[0]] = self.sequences[f'{graph_name}_degrees'].get(key[0],0) + 1/degrees_normalizer
                        self.cg[graph_name][key[0]][key[1]] = np.round(weight, decimals = 3)
                    else:
                        if 'degrees' in Config.Sequences.dnf_sequences:
                            self.sequences[f'{graph_name}_degrees'][key[0]] = 1/degrees_normalizer
                        self.cg[graph_name][key[0]] = {key[1]:weight}
                        self._meta[f'{graph_name}_edges_count'] += 1

    def generate_features(self):
        is_rsf_or_lsf = 'rsf' in Config.Embeddings or 'lsf' in Config.Embeddings

        # VC sequences : 
        if is_rsf_or_lsf:
            vc = []
            if 'vcp' in Config.Graphs.dnf_graphs: vc.append(('vcp', self.total_nbr_pos))
            if 'vcn' in Config.Graphs.dnf_graphs: vc.append(('vcn', self.total_nbr_neg))
            for graph, nbr_nodes in vc:
                if nbr_nodes == 0:
                    properties = []
                    if 'cdegrees' in Config.Sequences.dnf_sequences: properties.append('cdegrees')
                    if 'vdegrees' in Config.Sequences.dnf_sequences: properties.append('vdegrees')
                    if 'weights' in Config.Sequences.dnf_sequences: properties.append('weights')
                    set_trivial_case_features(Config.Stats.rsf_stats, self.dnf_features, graph, properties = properties)

        for i_clause in range(self.len_clauses):
            clause = self.clauses[i_clause]
            nbr_pos = 0
            literals = list(clause.literals)
            len_clause = len(clause.literals)
            
            self.update_vg_vc_graphs(i_clause, len_clause, literals)
            pos_literals, neg_literals = divide_by_sign(literals)
            self.update_cg_graphs(i_clause, pos_literals, neg_literals)

            # VC sequences : 
            vc = []
            nbr_pos = len(pos_literals)
            if 'vcp' in Config.Graphs.dnf_graphs and 'cdegrees' in Config.Sequences.dnf_sequences: vc.append(('vcp', nbr_pos, self.total_nbr_pos))
            if 'vcn' in Config.Graphs.dnf_graphs and 'cdegrees' in Config.Sequences.dnf_sequences: vc.append(('vcn', len_clause - nbr_pos, self.total_nbr_neg))
            for graph, nbr_lits, total_nbr_lits in vc:
                if total_nbr_lits != 0:
                    self.sequences[f'{graph}_cdegrees'][i_clause] = nbr_lits/total_nbr_lits
                    if is_rsf_or_lsf:
                        update_statistics('rsf', f"{graph}_cdegrees", self.dnf_features, [nbr_lits/total_nbr_lits], self.len_clauses)
            
        # VC sequences : 
        vc = []
        if 'vcp' in Config.Graphs.dnf_graphs: vc.append(('vcp', self.total_nbr_pos))
        if 'vcn' in Config.Graphs.dnf_graphs: vc.append(('vcn', self.total_nbr_neg))
        for graph, nbr_nodes in vc:
            if nbr_nodes != 0: 
                if 'cdegrees' in Config.Sequences.dnf_sequences:
                    len_zeros = self.len_clauses - (len(self.sequences[f'{graph}_cdegrees'].keys()) - 1)
                    # zeros = np.zeros(len_zeros).tolist()
                    self.sequences[f'{graph}_cdegrees']['zeros'] = len_zeros
                    if is_rsf_or_lsf:
                        update_statistics('rsf', f"{graph}_cdegrees", self.dnf_features, [0], self.len_clauses, obs_count=len_zeros)
                        wrap_up_statistics('rsf', f"{graph}_cdegrees", self.dnf_features)
                if 'vdegrees' in Config.Sequences.dnf_sequences:
                    if is_rsf_or_lsf:
                        update_statistics('rsf', f"{graph}_vdegrees", self.dnf_features, [v for k,v in self.sequences[f'{graph}_vdegrees'].items() if k != 'zeros'], nbr_nodes)
                        wrap_up_statistics('rsf', f"{graph}_vdegrees", self.dnf_features)

                if 'weights' in Config.Sequences.dnf_sequences:
                    len_zeros = self.len_clauses*nbr_nodes - self._meta[f'{graph}_edges_count']
                    self.sequences[f'{graph}_weights']['zeros'] = len_zeros
                    if is_rsf_or_lsf:
                        update_statistics('rsf', f"{graph}_weights", self.dnf_features, [0], self.len_clauses*nbr_nodes, len_zeros)
                        update_statistics('rsf', f"{graph}_weights", self.dnf_features, [v for k,v in self.sequences[f'{graph}_weights'].items() if k != 'zeros'], self.len_clauses*nbr_nodes)
                        wrap_up_statistics('rsf', f"{graph}_weights", self.dnf_features)

        # VG/CG sequences : 
        graphs = []
        if 'vgp' in Config.Graphs.dnf_graphs: graphs.append(('vgp', self.vg['vgp'], self.total_nbr_pos))
        if 'vgn' in Config.Graphs.dnf_graphs: graphs.append(('vgn', self.vg['vgn'], self.total_nbr_neg))
        if 'vgos' in Config.Graphs.dnf_graphs: graphs.append(('vgos', self.vg['vgos'], self.len_symbols))
        if 'cgp' in Config.Graphs.dnf_graphs: graphs.append(('cgp', self.cg['cgp'], self.len_clauses))
        if 'cgn' in Config.Graphs.dnf_graphs: graphs.append(('cgn', self.cg['cgn'], self.len_clauses))
        for graph_name, graph, nbr_nodes in graphs:
            self.run_stats_on_graphs('rsf', graph_name, graph, self.dnf_features, nbr_nodes)
        
        mx = lambda x,col: (f'moment{x}' in col and f'moment{x}' in Config.Stats.rsf_stats) or (f'moment{x}' not in col)
        features = pd.Series({
            self.comp_name + "_" + col: (np.round(val, decimals = 1) if ('ratio' not in col) and ('entropy' not in col) else np.round(val, decimals = 2))
            for col,val in self.dnf_features.items() if ("pmf" not in col) and mx(1, col) and mx(2, col) and mx(3, col)
        })
        # features = pd.Series({f"{self.comp_name}_{col}": np.round(val, decimals = 1) if ('ratio' not in col) and ('entropy' not in col) else val for col,val in self.dnf_features.items() if "pmf" not in col and 'moment2' not in col and 'moment3' not in col})
        graphs = {'vc':self.vc, 'vg':self.vg, 'cg':self.cg} if Config.Memory.memorize_dnf_graphs else {}
        seqs = self.sequences if Config.Memory.memorize_dnf_sequences else ({k:v for k,v in self.sequences.items() if 'vg' in k} if 'ptrns' in Config.Embeddings else {})
        return graphs, seqs, features
