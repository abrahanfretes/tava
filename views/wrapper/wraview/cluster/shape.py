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


class Shape():

    population = 0

    clusters = []
    clusters_count = 0

    tendencies = []
    tendency_count = 0

    column_shape = 'Shape'
    column_name = 'Name'

    def __init__(self, df_population, clus=0, nor=0):
        self.population = len(df_population.values)
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

            # unificamos los clusters mas cercanos
            for i, r_shape in enumerate(r_selected):
                l_rho = 2
                a_shape = []

                for s_shape in s_selected:
                    rho, _pva = st.spearmanr(s_shape, r_shape)
                    if abs(rho) < l_rho:
                        l_rho = abs(rho)
                        a_shape = s_shape

                s_name_shape = '_'.join([str(i) for i in a_shape])
                u_name_shape = '_'.join([str(i) for i in r_shape])
                df_shapes[self.column_shape].replace(u_name_shape,
                                                     s_name_shape,
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
            df = df_group.get_group(shape)
            current_clusters.append(Cluster(str(i_name), shape, freq, df))
            i_name += 1

        return current_clusters

    def frobenius_nor(self, df):
        df1 = df.drop(self.column_name, axis=1)
        df1 = df1.drop(self.column_shape, axis=1)
        nor = (lambda x: x / np.linalg.norm(x))
        dframe_nor = DataFrame(nor(df1.values), columns=df1.columns.tolist())
        dframe_nor[self.column_name] = df[self.column_name].tolist()
        dframe_nor[self.column_shape] = df[self.column_shape].tolist()
        return dframe_nor

    def rangecero_nor(self, df):
        for cols in df.columns[:-2]:
            vals = df[cols]
            _min = vals.min()
            _max = vals.max()
            _vnor = [(x-_min)/(_max-_min) for x in vals]
            df[cols] = _vnor
        return df


class Cluster():
    name = ''
    shape = []
    individuals = 0
    df_value = None

    def __init__(self, name, shape, count, df_value):
        name = name
        shape = shape
        count = count
        df_value = df_value


def grafic_r1(f_path=None, _sep=' '):
#     import matplotlib
#     from matplotlib import pyplot as plt
#     matplotlib.rcParams['text.latex.unicode'] = True
# 
#     fig = plt.figure(facecolor='w', figsize=(6.75, 5.75), dpi=80)
#     fig.subplots_adjust(top=0.98, bottom=0.07,
#                         left=0.02,  right=0.98,
#                         wspace=0.05, hspace=0.10)

    # ---------------------------------------------------------

    df = pd.read_csv(f_path,  sep=_sep)
    shape = Shape(df, clus=0, nor=2)
    print shape.tendencies
    print shape.tendency_count
    print shape.clusters_count


if __name__ == '__main__':

    f_path = '/home/afretes/tesis/proyectos/kuri/datas/objetivos_8.csv'
    grafic_r1(f_path, ',')
