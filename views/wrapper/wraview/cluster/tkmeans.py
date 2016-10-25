#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
# ##############################################################
#                                                            ###
# Universidad Nacional de Asunción - Facultad Politécnica    ###
# Ingenieria en Informática - Proyecto Final de Grado        ###
#                                                            ###
# Autores:                                                   ###
#           - Arsenio Ferreira (arse.ferreira@gmail.com)     ###
#           - Abrahan Fretes (abrahan.fretes@gmail.com)      ###
#                                                            ###
# Creado:  23/10/2016                                        ###
#                                                            ###
# ##############################################################
'''

import operator
from scipy.cluster.vq import kmeans, vq

import numpy as np
import pandas as pd
from views.wrapper.wraview.cluster.shape import Cluster


class Kmeans():

    population = 0
    clusters = []
    clusters_count = 0
    tendencies = []
    tendency_count = 0
    column_name = 'Name'
    cluster_checkeds = []
    cluster_uncheckeds = []
    name_objectives = []

    def __init__(self, df_population, clus=0, nor=0):
        self.population = len(df_population.values.tolist())
        self.clusters = self.generate_clusters(df_population, clus, nor)
        self.clusters_count = len(self.clusters)
        self.name_objectives = df_population.columns.tolist()[:-1]
        self.full_normalization()

    def full_normalization(self):
        cs = []
        for c in self.clusters:
            cs.append(c.df_value)

        # ---- normalizar completo
        df = pd.concat(cs)
        df = self._nor(df)
        df_group = df.groupby(self.column_name)

        for c in self.clusters:
            c.full_nor = df_group.get_group(c.shape)
            c.df_resume_nor = c.g_resume(c.full_nor, c.shape)

    def _nor(self, df):
        def normalize(series):
            a = min(series)
            b = max(series)
            return (series - a) / (b - a)
        class_column = df.columns[-1]
        class_col = df[class_column]
        df = df.drop(class_column, axis=1).apply(normalize)
        df[class_column] = class_col
        return df

    def generate_clusters(self, df_population,  clus, nor):
        df = df_population.drop(self.column_name, axis=1)
        # ---- forma de normalizar
        # whitened = whiten(df.values)

        whitened = df.values
        centroids, _ = kmeans(whitened, clus)
        indexes, _ = vq(whitened, centroids)

        # ---- resumenes o centroides
        resumes = {}
        for i, rs in enumerate(centroids):
            resumes[i] = np.concatenate((rs, [i]))

        # ---- se crea un dataframe de toda la población
        df_clusters = pd.DataFrame(whitened, columns=df.columns)
        df_clusters['Name'] = indexes

        # ---- se crean grupos
        return self.generalized_shape(df_clusters, resumes)

    def generalized_shape(self, df_shapes, resumes):

        current_clusters = []

        # ---- optener las tendencias
        all_shapes = df_shapes[self.column_name].tolist()

        # ---- ordenarlos de mayor a menor
        _clusters, _clusters_counts = np.unique(all_shapes, return_counts=True)
        s_dt = dict(zip(_clusters, _clusters_counts))
        _clusters_frequency = sorted(s_dt.items(), key=operator.itemgetter(1))
        _clusters_frequency.reverse()

        # ---- agregar a lista de clusters
        df_group = df_shapes.groupby(self.column_name)
        i_name = 1
        for shape, freq in _clusters_frequency:
            _df = df_group.get_group(shape)
            _c = Cluster(str(i_name), shape, freq, _df, self.population,
                         resumes[shape])
            current_clusters.append(_c)
            i_name += 1

        return current_clusters

    def g_checkeds(self):
        return [self.clusters[cl] for cl in self.cluster_checkeds]

    def g_data_by_dr(self, s_clusters, legends_cluster,
                     legends_summary, crude=True):

        if s_clusters == []:
            return pd.DataFrame()

        _clusters = []
        _resumes = []
        _legends = []

        for c in s_clusters:
            # data
            _df = c.df_value.copy() if crude else c.full_nor.copy()
            _leg = c.g_legend(_legends, legends_cluster)
            _legends.append(_leg)
            _df[self.column_name] = [_leg] * c.count
            _clusters.append(_df)

            # resume
            _dfr = c.df_resume.copy() if crude else c.df_resume_nor.copy()
            _leg = c.g_legend(_legends, legends_summary)
            _legends.append(_leg)
            _dfr[self.column_name] = [_leg]
            _resumes.append(_dfr)

        return _clusters, _resumes

    def g_legend(self, legends, legends_condition, repeat=False):
        _legend = ""

        if legends_condition[0]:
            if _legend != "":
                _legend = _legend + ' - '
            _legend = _legend + self.g_percent_format()

        if legends_condition[1]:
            if _legend != "":
                _legend = _legend + ' - '
            _legend = _legend + str(self.count)

        if legends_condition[2]:
            if _legend != "":
                _legend = _legend + ' - '
            _legend = _legend + self.name

        if legends_condition[3]:
            if _legend != "":
                _legend = _legend + ' - '
            _legend = _legend + self.shape

        if not repeat:
            while _legend in legends:
                _legend = _legend + "."
        return _legend

    def g_data_for_fig(self, s_clusters, legends_cluster, crude=True):

        # ---- si no contiene clusters
        if s_clusters == []:
            return pd.DataFrame()

        _clusters = []
        _legends = []

        # ---- clsuters seleccionados y creción de legendas
        for c in s_clusters:
            _df = c.df_value.copy() if crude else c.full_nor.copy()
            _leg = c.g_legend(_legends, legends_cluster)
            _legends.append(_leg)
            _df[self.column_name] = [_leg] * c.count
            _clusters.append(_df)

        return _clusters

    def g_resume_for_fig(self, s_clusters, legends_summary, crude=True):
        if s_clusters == []:
            return pd.DataFrame()

        _clusters = []
        _legends = []
        for c in s_clusters:
            _df = c.df_resume.copy() if crude else c.df_resume_nor.copy()
            _leg = c.g_legend(_legends, legends_summary)
            _legends.append(_leg)
            _df[self.column_name] = [_leg]
            _clusters.append(_df)

        return _clusters
