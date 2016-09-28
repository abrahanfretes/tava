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
# Creado:  1/9/2016                                        ###
#                                                            ###
# ##############################################################
'''

import operator
from pandas.core.frame import DataFrame

import numpy as np
import pandas as pd
import random as rm
import scipy.stats as st
from views.wrapper.wraview.vgraphic.cparallel import k_cp


class Shape():

    population = 0

    clusters = []
    clusters_count = 0

    tendencies = []
    tendency_count = 0

    column_shape = 'Shape'
    column_name = 'Name'

    def __init__(self, df_population, clus=0, nor=0):
        self.population = len(df_population.values.tolist())
        self.clusters = self.generate_clusters(df_population, clus, nor)
        self.clusters_count = len(self.clusters)

    def generate_clusters(self, df_population,  clus, nor):

        # ---- normalizar los datos
        if nor == 1:
            df_population = self.frobenius_nor(df_population)
        elif nor == 2:
            df_population = self.rangecero_nor(df_population)

        # ---- calculo de shape para cada elemento
        new_columns = df_population.columns.tolist()
        new_columns.append(self.column_shape)
        df_shapes = pd.DataFrame(columns=new_columns)
        for i, value in enumerate(df_population.values.tolist()):
            name = '_'.join([str(v) for v in np.argsort(value[:-1])])
            value.append(name)
            df_shapes.loc[i] = value

        # ---- se obtienen las tendencias del conjunto de datos
        self.tendencies = df_shapes[self.column_shape].drop_duplicates().tolist()
        self.tendency_count = len(self.tendencies)

        # ---- misma cantidad de tendencias que clusters(análisis shapes)
        if clus < 1 or clus == self.tendency_count:
            return self.generalized_shape(df_shapes)

        # ---- cantidad de cluster menor a tendencias
        if clus < self.tendency_count:

            # selección aleatoria de shape
            i_distinct = range(len(self.tendencies))
            rm.shuffle(i_distinct)
            s_selected = [self.tendencies[s] for s in i_distinct[:clus]]
            r_selected = [self.tendencies[s] for s in i_distinct[clus:]]

            # caso especial
            if clus == 1:
                reemplaze = s_selected * self.population
                df_shapes[self.column_shape] = reemplaze
                return self.generalized_shape(df_shapes)

            # unificamos los clusters mas cercanos
            for i, r_shape in enumerate(r_selected):
                l_rho = 2
                a_shape = ''

                for s_shape in s_selected:
                    _s = [int(_i) for _i in s_shape.split('_')]
                    _r = [int(_i) for _i in r_shape.split('_')]
                    rho, _pva = st.spearmanr(_s, _r)
                    if abs(rho) < l_rho:
                        l_rho = abs(rho)
                        a_shape = s_shape
                df_shapes[self.column_shape].replace(r_shape, a_shape,
                                                     inplace=True)

            return self.generalized_shape(df_shapes)

        # ---- número de clusters mayor a tendencias
        # esta parte falta completar
        missing = self.tendency_count - clus
        c_shape = list(self.tendencies)
        c_repeat = np.random.randint(0, missing, missing)
        c_shape = [c_shape.append(c_shape[cs]) for cs in c_repeat]
        df_group = df_shapes.groupby(self.column_shape)

        for tend in self.tendencies:
            df = df_group.get_group(tend)

        return self.generalized_shape(df_shapes)

    def generalized_shape(self, df_shapes):

        current_clusters = []
        # optener las tendencias
        all_shapes = df_shapes[self.column_shape].tolist()
        # ordenarlos de mayor a menor
        _clusters, _clusters_counts = np.unique(all_shapes, return_counts=True)
        s_dt = dict(zip(_clusters, _clusters_counts))
        _clusters_frequency = sorted(s_dt.items(), key=operator.itemgetter(1))
        _clusters_frequency.reverse()

        # agregar a lista de clusters
        df_group = df_shapes.groupby(self.column_shape)
        i_name = 1
        for shape, freq in _clusters_frequency:
            _df = df_group.get_group(shape)
            current_clusters.append(Cluster(str(i_name), shape, freq, _df,
                                            self.population))
            i_name += 1
        return current_clusters

    def frobenius_nor(self, df):
        df1 = df.drop(self.column_name, axis=1)
        nor = (lambda x: x / np.linalg.norm(x))
        dframe_nor = DataFrame(nor(df1.values.tolist()),
                               columns=df1.columns.tolist())
        dframe_nor[self.column_name] = df[self.column_name].tolist()
        return dframe_nor

    def rangecero_nor(self, df):
        for cols in df.columns[:-1]:
            vals = df[cols]
            _min = vals.min()
            _max = vals.max()
            _vnor = [(x-_min)/(_max-_min) for x in vals]
            df[cols] = _vnor
        return df

    # ------------------ METODOS PARA ANALISIS SHAPES -----------
    # -----------------------------------------------------------

    def g_all_clusters(self):
        _clusters = []
        for c in self.clusters:
            _df = c.df_value.drop(self.column_name, axis=1)
            _clusters.append(_df)
        return pd.concat(_clusters)

    def g_all_resumes(self):
        df_resumes = pd.DataFrame()
        for c in self.clusters:
            _df = c.df_value.drop(self.column_name, axis=1)
            serie_mean = _df[_df.columns[:-1]].mean()
            df_mean = serie_mean.to_frame()
            df_mean = df_mean.transpose()
            df_mean[self.column_shape] = c.shape
            df_resumes = df_resumes.append(df_mean)
        return df_resumes

    def g_percent_up(self, percent):
        _per = 0.0
        _clusters = []
        for c in self.clusters:
            _per = _per + c.g_percent(self.population)
            _clusters.append(c)
            if percent <= _per:
                return _clusters
        return _clusters

    def g_percent_up_resumes(self, percent):
        _per = 0.0
        df_resumes = pd.DataFrame()
        for c in self.clusters:
            _df = c.df_value.drop(self.column_name, axis=1)
            serie_mean = _df[_df.columns[:-1]].mean()
            df_mean = serie_mean.to_frame()
            df_mean = df_mean.transpose()
            df_mean[self.column_shape] = c.shape
            df_resumes = df_resumes.append(df_mean)
            _per = _per + c.g_percent(self.population)
            if percent <= _per:
                return df_resumes
        return df_resumes

    def g_data_for_fig(self, s_clusters):
        if s_clusters == []:
            return pd.DataFrame()
        _clusters = []
        _legends = []

        for c in s_clusters:
            _df = c.df_value.drop(self.column_name, axis=1)
            _leg = c.g_legend(_legends)
            _legends.append(_leg)
            _df[self.column_shape] = [_leg] * c.count
            _clusters.append(_df)
        return pd.concat(_clusters)

    def g_resume_for_fig(self, s_clusters):
        if s_clusters == []:
            return pd.DataFrame()

        _clusters = []
        _legends = []
        for c in s_clusters:
            _df = c.df_resume.drop(self.column_name, axis=1)
            _leg = c.g_legend(_legends, por=1, sh=0)
            _legends.append(_leg)
            _df[self.column_shape] = [_leg]
            _clusters.append(_df)
        return pd.concat(_clusters)

    def g_data_and_resume_for_fig(self, s_clusters):
        if s_clusters == []:
            return pd.DataFrame()
        _clusters = []
        _legends = []

        for c in s_clusters:
            # data
            _df = c.df_value.drop(self.column_name, axis=1)
            _leg = c.g_legend(_legends)
            _legends.append(_leg)
            _df[self.column_shape] = [_leg] * c.count
            _clusters.append(_df)
            # resume
            _df = c.df_resume.drop(self.column_name, axis=1)
            _leg = c.g_legend(_legends, por=1, sh=0)
            _legends.append(_leg)
            _df[self.column_shape] = [_leg]
            _clusters.append(_df)
        return pd.concat(_clusters)


class Cluster():
    name = ''
    shape = []
    individuals = 0
    df_value = None
    column_shape = 'Shape'
    column_name = 'Name'

    def __init__(self, name, shape, count, df_value, all_count):
        self.name = name
        self.shape = shape
        self.count = count
        self.df_value = df_value
        self.all_count = all_count
        self.df_resume = self.g_resume(df_value, shape, name)

    def g_percent(self, total=None):
        if total is None:
            total = self.all_count
        return (self.count*100.0)/total

    def g_resume(self, df, shape, name):

        serie_mean = df[df.columns[:-2]].mean()
        df_mean = serie_mean.to_frame()
        df_mean = df_mean.transpose()
        df_mean[self.column_name] = name
        df_mean[self.column_shape] = shape
        return df_mean

    def g_legend(self, legends, repeat=False, sh=1, por=0, ind=0, name=0):
        _legend = ""

        if por == 1:
            if _legend != "":
                _legend = _legend + ' - '
            _legend = _legend + str(self.g_percent()) + '%'

        if ind == 1:
            if _legend != "":
                _legend = _legend + ' - '
            _legend = _legend + str(self.count)

        if name == 1:
            if _legend != "":
                _legend = _legend + ' - '
            _legend = _legend + self.name

        if sh == 1:
            if _legend != "":
                _legend = _legend + ' - '
            _legend = _legend + self.shape

        if not repeat:
            while _legend in legends:
                _legend = _legend + "."
        return _legend


def axe_con(ax, label=None):
    ax.spines['bottom'].set_color('w')
    ax.spines['top'].set_color('w')
    ax.spines['right'].set_color('#DDDDDD')
    ax.spines['left'].set_color('#DDDDDD')
    if label is not None:
        ax.set_xlabel(label, labelpad=-1)
        ax.xaxis.label.set_color('#606060')
        ax.tick_params(axis='x', colors='w')
    return ax


def grafic_r1(f_path=None, _sep=' '):
    import matplotlib
    from matplotlib import pyplot as plt
    matplotlib.rcParams['text.latex.unicode'] = True

    fig = plt.figure(facecolor='w', figsize=(6.75, 5.75), dpi=80)
    fig.subplots_adjust(top=0.98, bottom=0.07,
                        left=0.02,  right=0.98,
                        wspace=0.05, hspace=0.10)

    # ---------------------------------------------------------

    df = pd.read_csv(f_path,  sep=_sep)
    shape = Shape(df.copy(), clus=0, nor=2)

    # ver clusters
    s_clusters = shape.g_percent_up(15.0)
    dv = shape.g_data_and_resume_for_fig(s_clusters)

    ax = fig.add_subplot(2, 1, 1)
    k_cp(dv, 'Shape', ax=ax, u_legend=True, u_grid=False,
         _xaxis=False, one_color=False, _loc='upper left',
         _yaxis=True, klinewidth=0.3, klinecolor='#DDDDDD')
    ax = axe_con(ax)
    ax.legend(prop={'size': 9},
              loc='upper left').get_frame().set_edgecolor('#DDDDDD')

    # resumenes de clusters
    dv = shape.g_resume_for_fig(s_clusters)
    # print len(dv.values)
    ax = fig.add_subplot(2, 1, 2)
    k_cp(dv, 'Shape', ax=ax, u_legend=True, u_grid=False,
         _xaxis=False, one_color=False, _loc='upper left',
         _yaxis=True, klinewidth=0.3, klinecolor='#DDDDDD')
    ax = axe_con(ax)
    ax.legend(prop={'size': 9},
              loc='upper left').get_frame().set_edgecolor('#DDDDDD')
    plt.show()


if __name__ == '__main__':

    f_path = '/home/abrahan/tesis/proyectos/kuri/datas/objetivos_8.csv'
    grafic_r1(f_path, ',')
