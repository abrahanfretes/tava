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
import pandas as pd
import numpy as np

import operator
import random as rm
from math import factorial
import scipy.stats as st
from scipy.cluster.vq import kmeans, vq


class Shape():

    population = 0
    clusters = []
    tendencies = []
    columns_shape = 'Shape'

    def __init__(self, df_population, clus=0):
        self.population = len(df_population.values)
        self.clusters = self.generate_clusters(df_population, clus)
        pass

    def generate_clusters(self, df_population,  clus):

        # normalizar los datos

        # se obtienen los shapes de los elementos
        new_columns = df_population.columns
        new_columns.append(self.columns_shape)
        df_shapes = pd.DataFrame(columns=new_columns)

        for i, value in enumerate(df_population.values.tolist()):
            name = '_'.join([str(v) for v in np.argsort(value[:-1])])
            value.append(name)
            df_shapes.loc[i] = value

        self.tendencies = df_shapes[self.columns_shape].drop_duplicates()

        # analisis shape
        if clus < 1 or clus == len(self.tendencies):
            return self.generalized_shape(df_shapes)

        if clus < len(self.tendencies):

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
                df_shapes[self.columns_shape].replace(u_name_shape,
                                                      s_name_shape,
                                                      inplace=True)
            return self.generalized_shape(df_shapes)

        # unificar valores --- falta implementar
        return self.generalized_shape(df_shapes)

    def generalized_shape(self, df_shapes):

        current_clusters = []
        # optener las tendencias
        all_shapes = df_shapes[self.columns_shape].tolist()
        # ordenarlos de mayor a menor
        tendency, shape_counts = np.unique(all_shapes, return_counts=True)
        s_dict = dict(zip(tendency, shape_counts))
        tendency_frequency = sorted(s_dict.items(), key=operator.itemgetter(1))
        tendency_frequency.reverse()
        # tendencias ordenadas
        self.tendencies = tendency_frequency[0]
        # agregar a lista de clusters
        df_group = df_shapes.groupby(self.columns_shape)
        i_name = 1
        for shape, freq in tendency_frequency:
            df = df_group.get_group(shape)
            current_clusters.append(Cluster(str(i_name), shape, freq, df))
            i_name += 1

        return current_clusters




class Cluster():
    name = ''
    shape = []
    individuals = 0
    df_value = None

    def __init__(self, name, shape, individuals, df_value):
        name = name
        shape = shape
        individuals = individuals
        df_value = df_value


class TShape():

    def __init__(self, dataframe, class_column='Name'):

        self.porcent_column = 'porcent'
        self.class_column = class_column

        # cantidad de elementos
        self.elements = len(dataframe.values)

        self.df_shapes = pd.DataFrame(columns=dataframe.columns)
        self.generate_shape(dataframe)

        # tuple de shapes unicos y ordenados de mayor a menor elemntos
        self.shape_val = self.shapes_sort_freq(self.df_shapes)

        # nombres unicos y ordenados
        self.unique_shapes = list()
        self.all_unique_shapes()

        # shapes u resumenes
        self.dict_shapes = {}
        self.dict_resumes = {}
        # self.generate_group()

    def generate_shape(self, dataframe):

        # creación de los shapes
        self.df_shapes = pd.DataFrame(columns=dataframe.columns)
        for i, value in enumerate(dataframe.values.tolist()):
            _value = value[:-1]
            name = '_'.join([str(v) for v in np.argsort(_value)])
            _value.append(name)
            self.df_shapes.loc[i] = _value

    def shapes_sort_freq(self, df_shapes, sort=True, class_column='Name'):
        shapes = df_shapes[class_column].tolist()
        s_unique, s_counts = np.unique(shapes, return_counts=True)
        s_dict = dict(zip(s_unique, s_counts))
        shape_val = sorted(s_dict.items(), key=operator.itemgetter(1))
        if sort:
            shape_val.reverse()
        return shape_val

    def all_unique_shapes(self):
        for shape, _ in self.shape_val:
            self.unique_shapes.append([int(ii) for ii in shape.split('_')])

    def order_and_resumens(self, df_clusters, resumes=True, all_elements=0,
                           class_column='Name', u_color_res=False):

        # agrupaciones por shape
        df_group = df_clusters.groupby(class_column)
        sh_result = self.shapes_sort_freq(df_clusters)

        if all_elements == 0:
            for _, freq in sh_result:
                all_elements += freq

        df_result = pd.DataFrame(columns=df_clusters.columns)
        df_resumes = pd.DataFrame(columns=df_clusters.columns)

        for shape, freq in sh_result:
            df_aux = df_group.get_group(shape)
            df_result = df_result.append(df_aux)

            serie_mean = df_aux[df_aux.columns[:-1]].mean()
            df_mean = serie_mean.to_frame()
            df_mean = df_mean.transpose()
            porcent = round((freq*100.0)/all_elements, 3)
            df_mean[class_column] = str(porcent)+' %'
            df_resumes = df_resumes.append(df_mean)

        if u_color_res:
            _len_shapes = len(df_resumes[class_column])
            _total = factorial(len(df_resumes.columns) - 1)
            _lavel = str(_len_shapes) + '/' + str(_total)
            new_name = [_lavel]*_len_shapes
            df_resumes[class_column] = new_name

        return df_result, df_resumes

    def generate_group_old(self):

        # agrupaciones por shape
        df_group = self.df_shapes.groupby(self.class_column)

        # agrupaciones - resúmenes - porcentajes
        _aux = []
        for shape, freq in self.shape_val:
            df_aux = df_group.get_group(shape)
            self.dict_shapes[shape] = df_aux.copy()

            serie_mean = df_aux[df_aux.columns[:-1]].mean()
            df_mean = serie_mean.to_frame()
            df_mean = df_mean.transpose()
            df_mean[self.class_column] = shape
            porcent = str((freq*100)/self.elements)
            df_mean[self.porcent_column] = porcent
            self.dict_resumes[shape] = df_mean
            _aux.append(df_aux)

        self.df_shapes = pd.concat(_aux)

    def get_by_group(self):

        # agrupaciones por shape
        ret_to = []
        df_group = self.df_shapes.groupby(self.class_column)
        for _, df in df_group:
            ret_to.append(df)
        return ret_to

    def get_for_view(self):

        to_ret = []
        list_frequency_order = self.shapes_sort_freq(self.df_shapes)
        df_group = self.df_shapes.groupby(self.class_column)
        for shape, freq in list_frequency_order:
            df = df_group.get_group(shape)
            to_ret.append((shape, freq, df))
        return to_ret

    def shape(self, n_cluster=None, u_color_res=False):

        df_clusters = self.df_shapes.copy()

        if n_cluster is None:
            df_clusters = df_clusters

        # unir los clusters
        elif n_cluster <= len(self.unique_shapes):

            # selección aleatoria de shape
            i_select = range(len(self.unique_shapes))
            rm.shuffle(i_select)
            s_selected = [self.unique_shapes[s] for s in i_select[:n_cluster]]
            r_selected = [self.unique_shapes[s] for s in i_select[n_cluster:]]

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
                df_clusters[self.class_column].replace(u_name_shape,
                                                       s_name_shape,
                                                       inplace=True)

        elif n_cluster > len(self.unique_shapes):
            print 'Falta'

        # ordenar y generar resúmenes
        df_clus, df_resu = self.order_and_resumens(df_clusters,
                                                   u_color_res=u_color_res)

        return df_clus, df_resu

    def kmeans(self, cluster_number, class_column='Name'):

        df = self.df_shapes.drop(class_column, axis=1)
        # whitened = whiten(df.values)
        whitened = df.values
        centroids, _ = kmeans(whitened, cluster_number)
        indexes, _ = vq(whitened, centroids)

        df_clusters = pd.DataFrame(whitened, columns=df.columns)
        df_clusters['Name'] = indexes

        df_clusters, df_resumes = self.order_and_resumens(df_clusters)

        return df_clusters, df_resumes

    def g_clus_max_and_min(self, df_clusters, class_column='Name'):

        # agrupaciones por shape
        df_group = df_clusters.groupby(class_column)
        sh_result = self.shapes_sort_freq(df_clusters)

        all_elements = 0
        for _, freq in sh_result:
            all_elements += freq

        df_clus_max_min = pd.DataFrame(columns=df_clusters.columns)
        df_resu_max_min = pd.DataFrame(columns=df_clusters.columns)

        sh_max_min = [sh_result[0], sh_result[-1]]

        for shape, freq in sh_max_min:
            df_aux = df_group.get_group(shape)
            df_clus_max_min = df_clus_max_min.append(df_aux)

            serie_mean = df_aux[df_aux.columns[:-1]].mean()
            df_mean = serie_mean.to_frame()
            df_mean = df_mean.transpose()
            porcent = (freq*100)/all_elements
            df_mean[class_column] = str(porcent)+' % ' + str(shape)
            df_resu_max_min = df_resu_max_min.append(df_mean)

        return df_clus_max_min, df_resu_max_min

    def g_clusters_un_select(self, df_select, df_clusters=None,
                             class_column='Name',
                             only_clus=True):

        if df_clusters is None:
            df_clusters = self.df_shapes.copy()

        shapes_s = df_select[class_column].drop_duplicates()
        for shape in shapes_s:
            df_clusters = df_clusters[df_clusters[class_column] != shape]

        return df_clusters

    def backgrunp_resume(self, df_select, df_un_select, class_column='Name',
                         all_elements=0):

        freq_un_select = len(df_un_select[class_column])
        if all_elements == 0:
            all_elements = freq_un_select + len(df_select[class_column])

        porcent = round((freq_un_select*100.0)/all_elements, 3)
        lavel = str(porcent)+' %'
        new_name = [lavel]*freq_un_select
        df_un_select[class_column] = new_name

        return df_un_select.append(df_select)

    def g_max_by_value_column(self, pos, df_clusters=None,
                              class_column='Name'):

        if df_clusters is None:
            df_clusters = self.df_shapes

        column = df_clusters.columns.tolist()[pos]

        max_value = df_clusters[column].max()
        df_max_in = df_clusters[df_clusters[column] == max_value]
        shapes_max = df_max_in[class_column].drop_duplicates()
        list_max = []
        for shape in shapes_max:
            list_max.append(df_clusters[df_clusters[class_column] == shape])
        df_max = pd.concat(list_max)

        return df_max

    def g_min_by_value_column(self, pos, df_clusters=None,
                              class_column='Name'):

        if df_clusters is None:
            df_clusters = self.df_shapes

        column = df_clusters.columns.tolist()[pos]

        min_value = df_clusters[column].min()
        df_min_in = df_clusters[df_clusters[column] == min_value]
        shapes_min = df_min_in[class_column].drop_duplicates()
        list_min = []
        for shape in shapes_min:
            list_min.append(df_clusters[df_clusters[class_column] == shape])
        df_min = pd.concat(list_min)

        return df_min

    def g_max_by_value_shapes(self, df_clusters=None, class_column='Name'):

        if df_clusters is None:
            df_clusters = self.df_shapes

        sh_result = self.shapes_sort_freq(df_clusters)
        obs_all = 0
        for _, freq in sh_result:
            obs_all += freq

        list_shape_max = []
        max_value = sh_result[0][1]
        for shape, value in sh_result:
            if value == max_value:
                list_shape_max.append(shape)

        df_group = df_clusters.groupby(class_column)

        df_max_in = []
        for shape in list_shape_max:
            df_max_in.append(df_group.get_group(shape))
        df_max = pd.concat(df_max_in)

        return df_max

    def g_min_by_value_shapes(self, df_clusters=None, class_column='Name'):

        if df_clusters is None:
            df_clusters = self.df_shapes

        sh_result = self.shapes_sort_freq(df_clusters)
        obs_all = 0
        for _, freq in sh_result:
            obs_all += freq

        list_shape_min = []
        min_value = sh_result[-1][1]
        for shape, value in sh_result:
            if value == min_value:
                list_shape_min.append(shape)

        df_group = df_clusters.groupby(class_column)

        df_min_in = []
        for shape in list_shape_min:
            df_min_in.append(df_group.get_group(shape))
        df_min = pd.concat(df_min_in)

        return df_min

    def unifique_classcolumns(self, df_frame, class_column='Name'):
        freq = len(df_frame[class_column])
        new_name = ['unificate']*freq
        df_frame[class_column] = new_name
        return df_frame

    def generate_labels(self, df_partial, df_total=None, class_column='Name',
                        label_shape=False):

        if df_total is None:
            df_total = self.df_shapes

        total_e = len(df_total[class_column])
        shapes_freq = self.shapes_sort_freq(df_partial)
        df_group = df_partial.groupby(class_column)
        list_with_label = []

        for shape, freq in shapes_freq:
            df_aux = df_group.get_group(shape).copy()

            # --------------------------------------------
            # distintos label  a tener en cuenta luego
            porcent = round((freq*100.0)/total_e, 3)
            new_name = str(porcent)+' %'
            if label_shape:
                new_name = shape + ' - ' + new_name
            list_new_name = [new_name]*freq
            # --------------------------------------------

            df_aux[class_column] = list_new_name
            list_with_label.append(df_aux)

        df_with_label = pd.concat(list_with_label)

        return df_with_label

    def generate_labels_resumes(self, df_resumes, df_total=None,
                                class_column='Name'):

        if df_total is None:
            df_total = self.df_shapes

        total_e = len(df_total[class_column])

        list_label = []
        for shape in df_resumes[class_column].values:
            df_aux = df_total[df_total[class_column] == shape]
            freq = len(df_aux[class_column].values)

            # --------------------------------------------
            # distintos label  a tener en cuenta luego
            porcent = round((freq*100.0)/total_e, 3)
            new_name = str(porcent)+' %'
            # --------------------------------------------

            list_label.append(new_name)

        df_resumes[class_column] = list_label

        return df_resumes

    def generate_resumes(self, df_partial=None, class_column='Name'):

        if df_partial is None:
            df_partial = self.df_shapes

        sh_result = self.shapes_sort_freq(df_partial)
        df_group = df_partial.groupby(class_column)
        df_resumes = pd.DataFrame(columns=df_partial.columns)

        for shape, _ in sh_result:
            df_aux = df_group.get_group(shape)
            serie_mean = df_aux[df_aux.columns[:-1]].mean()
            df_mean = serie_mean.to_frame()
            df_mean = df_mean.transpose()
            df_mean[class_column] = shape
            df_resumes = df_resumes.append(df_mean)

        return df_resumes
