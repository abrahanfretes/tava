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

from pandas.core.frame import DataFrame
import sys
import wx
from wx.lib import platebtn
from wx.lib.agw import customtreectrl as CT
from wx.lib.mixins.listctrl import CheckListCtrlMixin

import numpy as np
import pandas as pd
from views.wrapper.vdialog.vfigured import DataConfig
from views.wrapper.vdialog.vvisualization import ClusterConfig, V_M_CLUSTER,\
    V_M_SUMMARY, V_M_CLUSTER_SUMMARY, SelectedData, FilterClusterDialog
from views.wrapper.wraview.cluster.shape import Shape
from views.wrapper.wraview.vcontrolm import KMSG_EMPTY_DATA_SELECTED, \
    KMessage, KMSG_EMPTY_DUPLICATE_DATA, KMSG_EMPTY_CLUSTER_SELECTED, \
    KMSG_EMPTY_CLUSTER_DATA, KMSG_EMPTY_DATA_GENERATE_CLUSTER, \
    KMSG_GENERATE_CLUSTER
import wx.lib.agw.aui as aui


K_MANY_PAGE = 0
K_3D_PAGE = 1
K_2D_PAGE = 2
K_1D_PAGE = 3

KURI_AUI_NB_STYLE = aui.AUI_NB_TOP | aui.AUI_NB_TAB_SPLIT | \
    aui.AUI_NB_TAB_MOVE | aui.AUI_NB_SCROLL_BUTTONS | \
    aui.AUI_NB_MIDDLE_CLICK_CLOSE | aui.AUI_NB_DRAW_DND_TAB

KURI_AUI_NB_STYLE1 = aui.AUI_NB_TOP | \
    aui.AUI_NB_TAB_MOVE | aui.AUI_NB_SCROLL_BUTTONS | \
    aui.AUI_NB_MIDDLE_CLICK_CLOSE | aui.AUI_NB_DRAW_DND_TAB

KURI_TR_STYLE = CT.TR_HIDE_ROOT | CT.TR_NO_LINES | \
    CT.TR_HAS_BUTTONS | CT.TR_AUTO_CHECK_CHILD

KURI_TR_STYLE1 = CT.TR_HIDE_ROOT | CT.TR_TWIST_BUTTONS

option_figures_3d = ['Lineas 3D', 'Scatter 3D', 'Barras vertical 3D',
                     'Poligono']


K_DATE_DUPLICATE_TRUE = 0
K_DATE_DUPLICATE_FALSE = 1
K_DATE_DUPLICATE_ONLY = 2

K_PLOT_ALL_IN_ONE = 0
K_PLOT_BLOCK = 1

K_COLOR_ONE = 0
K_COLOR_BLOCK = 1
K_COLOR_SUB_BLOCK = 2
K_COLOR_VALUE = 3

NORMA_METO = ['Normalizado', 'Natural']
DATA_SELEC = ['Cluster', 'Datos']


class ControlPanel(wx.Panel):

    def __init__(self, parent, kfigure, ksub_blocks, mainpanel):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.mainpanel = mainpanel
        self.kfigure = kfigure
        self.SetBackgroundColour("#3B598D")

        self.data_selected = None
        self.normalization = 0
        self.cluster_or_date = 0

        self.duplicate_true = K_DATE_DUPLICATE_TRUE
        self.k_plot = K_PLOT_BLOCK
        self.k_color = K_COLOR_SUB_BLOCK
        self.cluster_config = None
        self.cluster_filter = None
        self.visualization_mode = V_M_CLUSTER
        self.legends_cluster = [False, False, False, True]
        self.legends_summary = [True, False, False, False]
        self.clus_one_axe = True
        self.summ_one_axe = True
        self.clus_summ_axs = [True, False, False]

        # ---- Lista de Datos
        self.data_seccion = DataSeccion(self, ksub_blocks)

        # ---- datos - normalización de datos

        grid = wx.FlexGridSizer(cols=2)
        self.tbtn = platebtn.PlateButton(self, -1,
                                         DATA_SELEC[self.cluster_or_date],
                                         None,
                                         style=platebtn.PB_STYLE_DEFAULT |
                                         platebtn.PB_STYLE_NOBG)
        tmenu = wx.Menu()
        tmenu.Append(wx.NewId(), DATA_SELEC[0])
        tmenu.Append(wx.NewId(), DATA_SELEC[1])
        self.tbtn.SetMenu(tmenu)
        self.tbtn.Bind(wx.EVT_MENU, self.on_select_menu)
        self.tbtn0 = platebtn.PlateButton(self, -1,
                                          NORMA_METO[self.normalization], None,
                                          style=platebtn.PB_STYLE_DEFAULT |
                                          platebtn.PB_STYLE_NOBG)
        menu = wx.Menu()
        menu.Append(wx.NewId(), NORMA_METO[0])
        menu.Append(wx.NewId(), NORMA_METO[1])
        self.tbtn0.SetMenu(menu)
        self.tbtn0.Bind(wx.EVT_MENU, self.on_nor_menu)
        grid.Add(self.tbtn, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        grid.Add(self.tbtn0, 1, wx.ALIGN_LEFT | wx.ALL, 5)

        # ---- Configuración de Clusters
        c_sizer = wx.BoxSizer()
        self.sc_count_clusters = wx.SpinCtrl(self, -1, "", size=(75, 30))
        self.sc_count_clusters.SetRange(0, 1000)
        self.sc_count_clusters.SetValue(0)
        tbtn = platebtn.PlateButton(self, -1, '  Crear  ', None,
                                    style=platebtn.PB_STYLE_SQUARE |
                                    platebtn.PB_STYLE_NOBG)
        tbtn.SetPressColor(wx.Colour(245, 55, 245))
        tbtn.SetLabelColor(wx.Colour(0, 0, 255))
        tbtn.Bind(wx.EVT_BUTTON, self.on_generate)
        c_sizer.Add(self.sc_count_clusters, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 2)
        c_sizer.Add(tbtn, 0, wx.TOP | wx.RIGHT | wx.LEFT | wx.ALIGN_CENTER_HORIZONTAL, 5)

        # ---- seleccionar - analizar
        a_sizer = wx.BoxSizer()
        tbtn1 = platebtn.PlateButton(self, -1, 'Marcar', None,
                                     style=platebtn.PB_STYLE_DEFAULT |
                                     platebtn.PB_STYLE_NOBG)
        tbtn1.SetPressColor(wx.Colour(255, 165, 0))
        tbtn1.SetLabelColor(wx.Colour(127, 0, 255))
        tbtn1.Bind(wx.EVT_BUTTON, self.on_filter)
        tbtn2 = platebtn.PlateButton(self, -1, '    Ver    ', None,
                                     style=platebtn.PB_STYLE_DEFAULT |
                                     platebtn.PB_STYLE_NOBG)
        tbtn2.SetPressColor(wx.Colour(255, 165, 0))
        tbtn2.SetLabelColor(wx.Colour(127, 0, 255))
        tbtn2.Bind(wx.EVT_BUTTON, self.on_config)
        a_sizer.Add(tbtn1, 0, wx.TOP | wx.RIGHT | wx.LEFT | wx.ALIGN_CENTER_HORIZONTAL, 5)
        a_sizer.Add(tbtn2, 0, wx.TOP | wx.RIGHT | wx.LEFT | wx.ALIGN_CENTER_HORIZONTAL, 5)

        # ---- Lista de Clusters
        self.clusters_seccion = ClusterSeccion(self)

        # ---- marco visualización
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.data_seccion, 1, wx.EXPAND | wx.ALL |
                       wx.ALIGN_CENTER_HORIZONTAL, 2)

        self.sizer.Add(grid, 0, wx.TOP | wx.RIGHT | wx.LEFT |
                       wx.ALIGN_CENTER_HORIZONTAL, 2)
        self.sizer.Add(c_sizer, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 2)
        self.sizer.Add(a_sizer, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 2)
        self.sizer.Add(self.clusters_seccion, 1, wx.EXPAND | wx.ALL, 1)

        self.SetSizer(self.sizer)
        self.Fit()

    def run_fig(self):

        # ---- Se desea visualizar Clusters
        if self.cluster_or_date == 0:
            self.v_clusters()

        # ---- Se desea visualizar Datos
        if self.cluster_or_date == 1:
            self.v_datas()

    def v_datas(self):
        blocks = []
        # se obtine la lista de bloques marcados
        if self.kfigure.g_type() == 0:
            blocks = self.data_seccion.get_checkeds()

            if blocks == []:
                KMessage(self.mainpanel, KMSG_EMPTY_DATA_SELECTED).kshow()
                return

            # se verifica datos duplicados
            blocks_1 = []
            if self.duplicate_true == K_DATE_DUPLICATE_TRUE:
                blocks_1 = blocks
            elif self.duplicate_true == K_DATE_DUPLICATE_FALSE:
                blocks_1 = self.delete_duplicate(blocks)
            else:
                # self.duplicate_true == K_DATE_DUPLICATE_ONLY
                blocks_1 = self.only_duplicate(blocks)
                if blocks_1 == []:
                    KMessage(self.mainpanel, KMSG_EMPTY_DUPLICATE_DATA).kshow()
                    return

            # se debería verificar la cantidad de plot y de acuerdo a eso
            # crear los dataframe

            blocks_2 = []
            if self.k_plot == K_PLOT_ALL_IN_ONE:
                blocks_2 = [pd.concat(blocks_1)]
            elif self.k_plot == K_PLOT_BLOCK:
                blocks_2 = blocks_1

            # update figure
            self.kfigure.kdraw(blocks_2)

    def v_clusters(self):

        # ---- verificar valores en clusters
        if not self.clusters_seccion.contain_elemens():
            KMessage(self.mainpanel, KMSG_EMPTY_CLUSTER_DATA).kshow()
            return

        if not self.clusters_seccion.checked_elemens():
            KMessage(self.mainpanel, KMSG_EMPTY_CLUSTER_SELECTED).kshow()
            return
        # ---- selección de clusters checked
        shape = self.clusters_seccion.g_for_view()
        s_clusters = shape.g_checkeds()

        # Se establece el modo de visualizacion para los clusters.
        _v = []
        if self.visualization_mode == V_M_CLUSTER:
            dd = shape.g_data_for_fig(s_clusters, self.legends_cluster,
                                      self.clus_one_axe)
            _v = dd
        if self.visualization_mode == V_M_SUMMARY:
            dr = shape.g_resume_for_fig(s_clusters, self.legends_summary,
                                        self.summ_one_axe)
            _v = dr
        if self.visualization_mode == V_M_CLUSTER_SUMMARY:
            dcr = shape.g_data_and_resume_for_fig(s_clusters,
                                                  self.legends_cluster,
                                                  self.legends_summary,
                                                  self.clus_summ_axs)
            _v = dcr

        # ---- update figure
        self.kfigure.kdraw(_v)

    def on_refresh(self, event):
        DataConfig(self)

    def delete_duplicate(self, blocks):
        _blocks = []
        for df in blocks:
            _blocks.append(df.drop_duplicates())
        return _blocks

    def only_duplicate(self, blocks):
        _blocks = []
        for df in blocks:
            col_aux = df.duplicated().tolist()
            if True in col_aux:
                c_d = 'duplicate_true'
                df[c_d] = col_aux
                _blocks.append(df[df[c_d] == True].drop(c_d, axis=1))
        return _blocks

    def on_generate(self, event):
        self.data_selected = None
        # ---- controlar valores consistentes para clusters
        if not self.data_seccion.contain_elemens():
            KMessage(self.mainpanel, KMSG_EMPTY_DATA_GENERATE_CLUSTER).kshow()
            return

        if not self.data_seccion.checked_elemens():
            KMessage(self.mainpanel, KMSG_GENERATE_CLUSTER).kshow()
            return
        self.clusters_seccion.generate(self.sc_count_clusters.GetValue(),
                                       self.normalization)

    def on_filter(self, event):

        # ---- controlar valores consistentes para clusters
        if not self.clusters_seccion.contain_elemens():
            KMessage(self.mainpanel, KMSG_EMPTY_CLUSTER_DATA).kshow()
            return

        if self.data_selected is None:
            self.data_selected = SelectedData()
            _data = self.data_selected
            _shape = self.clusters_seccion.shape

            # --- opción de selección
            _data.option = 0

            # ---- cantidad de tendencias
            _data.count_tendency = _shape.clusters_count

            # ---- clusters más representativos - en número de individuos
            _data.more_repre = 1

            # ---- clusters menos representativos - en número de individuos
            _data.less_repre = 1

            # ---- clusters por valor de objetivos mayores
            _shape.name_objectives
            _data.max_objetives = list(_shape.name_objectives)

        if not self.cluster_filter:
            self.cluster_filter = FilterClusterDialog(self, self.data_selected)
        else:
            self.cluster_filter.ShowModal()

        # ---- se cancela - retorna sin seleccionar
        if self.data_selected.cancel:
            return

        _data = self.clusters_seccion
        # ---- seleccionar clusters automáticamente
        if self.data_selected.option == 0:
            # ---- seleccionar los mas representativos
            _max = self.data_selected.more_repre
            self.clusters_seccion.more_representative(_max)
        if self.data_selected.option == 1:
            # seleccionar los menos representativos
            _ten = self.data_selected.count_tendency
            _min = self.data_selected.less_repre
            self.clusters_seccion.less_representative(_ten - _min)
        if self.data_selected.option == 2:
            # seleccionar los menos representativos
            _o_max = self.data_selected.max_objetives_use
            _o_min = self.data_selected.min_objetives_use
            self.clusters_seccion.max_min_objective(_o_max, _o_min)

    def on_config(self, event):
        # ---- controlar valores consistentes para clusters
        if not self.data_seccion.contain_elemens():
            KMessage(self.mainpanel, KMSG_EMPTY_DATA_GENERATE_CLUSTER).kshow()
            return

        if not self.data_seccion.checked_elemens():
            KMessage(self.mainpanel, KMSG_GENERATE_CLUSTER).kshow()
            return

        if not self.cluster_config:
            self.cluster_config = ClusterConfig(self)
        self.cluster_config.ShowModal()

    def on_select_menu(self, evt):
        """Events from button menus"""

        e_obj = evt.GetEventObject()
        mitem = e_obj.FindItemById(evt.GetId())
        if mitem != wx.NOT_FOUND:
            label = mitem.GetItemLabel()
            self.tbtn.SetLabel(label)
            self.cluster_or_date = DATA_SELEC.index(label)

    def on_nor_menu(self, evt):
        """Events from button menus"""

        e_obj = evt.GetEventObject()
        mitem = e_obj.FindItemById(evt.GetId())
        if mitem != wx.NOT_FOUND:
            label = mitem.GetItemLabel()
            self.tbtn0.SetLabel(label)
            self.normalization = NORMA_METO.index(label)


# -------------------                                  ------------------------
# -------------------                                  ------------------------
class ClusterSeccion(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)

        self.SetBackgroundColour('#FFFFFF')
        self.parent = parent
        self.shape = None
        self.row_index = []
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.list_control = CheckListCtrl(self)
        self.list_control.InsertColumn(0, "Nombre")

        _checked_all = wx.CheckBox(self, -1, "Seleccionar Todo")
        _checked_all.Bind(wx.EVT_CHECKBOX, self.on_checked_all)

        sizer.Add(_checked_all, flag=wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(self.list_control, 1, wx.EXPAND)
        self.SetSizer(sizer)

    def g_for_view(self):
        position_checked = []
        position_unchecked = []
        for i, r_i in enumerate(self.row_index):
            if self.list_control.IsChecked(r_i):
                position_checked.append(i)
            else:
                position_unchecked.append(i)
        self.shape.cluster_checkeds = position_checked
        self.shape.cluster_uncheckeds = position_unchecked
        return self.shape

    def generate(self, clus, nor):
        _tit = '- '

        # ----- limpiar clusters anteriores
        self.list_control.DeleteAllItems()

        # ----- bloques marcados para generar clusters
        blocks_checkeds = self.parent.data_seccion.get_checkeds_for_cluster()
        self.row_index = []

        # ----- mezclar bloques marcados para crear un solo bloques
        blocks_checkeds_merge = []
        for _key, data in blocks_checkeds.iteritems():
            blocks_checkeds_merge.append(data[1].dframe)
        df_population = pd.concat(blocks_checkeds_merge)
        # kblocks_two[0] = ('', KBlock('0', df_merge))
        _tit = ''

        # ---- generar clusters
        self.shape = Shape(df_population, clus=clus, nor=nor)

        # ---- agregar clusters a la vista
        for i, c in enumerate(self.shape.clusters):
            # name = data[0] + _tit + 'c' + str(vclus)
            name = 'cluster_' + str(i + 1) + ': ' + c.g_percent_format()
            index = self.list_control.InsertStringItem(sys.maxint, name)
            self.list_control.SetItemData(index, index)
            self.row_index.append(index)

        self.list_control.SetColumnWidth(0, wx.LIST_AUTOSIZE)

    def on_checked_all(self, event):
        if event.IsChecked():
            for index in self.row_index:
                self.list_control.CheckItem(index)
        else:
            self.un_select_all()

    def select_all(self):
        for index in self.row_index:
            self.list_control.CheckItem(index)

    def un_select_all(self):
        for index in self.row_index:
            self.list_control.CheckItem(index, False)

    def contain_elemens(self):
        return self.list_control.GetItemCount()

    def checked_elemens(self):
        for index in self.row_index:
            if self.list_control.IsChecked(index):
                return True
        return False

    # ---- funciones para análisis

    def more_representative(self, repre):
        self.un_select_all()
        for index in self.row_index[:repre]:
            self.list_control.CheckItem(index)

    def less_representative(self, repre):
        self.un_select_all()
        for index in self.row_index[repre:]:
            self.list_control.CheckItem(index)

    def max_min_objective(self, v_max, v_min):
        self.un_select_all()
        for index in self.shape.g_clusters_max_min_in_var(v_max, v_min):
            self.list_control.CheckItem(index)


# -------------------                                  ------------------------
# -------------------                                  ------------------------
class DataSeccion(wx.Panel):

    def __init__(self, parent, kblocks):
        wx.Panel.__init__(self, parent, -1)
        self.SetBackgroundColour('#FFFFFF')
        self.kblocks = kblocks
        self.row_index = []

        self.list_control = CheckListCtrl(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        _checked_all = wx.CheckBox(self, -1, "Seleccionar Todo")
        _checked_all.Bind(wx.EVT_CHECKBOX, self.on_checked_all)

        sizer.Add(_checked_all, flag=wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(self.list_control, 1, wx.EXPAND)

        self.SetSizer(sizer)
        self.init()

    def init(self):
        self.list_control.InsertColumn(0, "Bloque")

        for key, data in self.kblocks.iteritems():
            index = self.list_control.InsertStringItem(sys.maxint, data[0])
            self.list_control.SetItemData(index, key)
            self.row_index.append(index)

        self.list_control.SetColumnWidth(0, wx.LIST_AUTOSIZE)

    def get_checkeds(self):
        _subblocks_checked = []

        for index in self.row_index:
            if self.list_control.IsChecked(index):
                key = self.list_control.GetItemData(index)
                kblock = self.kblocks[key][1]
                _subblocks_checked.append(kblock.dframe)
        return _subblocks_checked

    def get_checkeds_for_cluster(self):
        block_checked = {}

        for index in self.row_index:
            if self.list_control.IsChecked(index):
                key = self.list_control.GetItemData(index)
                block_checked[key] = self.kblocks[key]
        return block_checked

    def on_checked_all(self, event):
        if event.IsChecked():
            for index in self.row_index:
                self.list_control.CheckItem(index)
        else:
            for index in self.row_index:
                self.list_control.CheckItem(index, False)

    def contain_elemens(self):
        return self.list_control.GetItemCount()

    def checked_elemens(self):
        for index in self.row_index:
            if self.list_control.IsChecked(index):
                return True
        return False


class CheckListCtrl(wx.ListCtrl, CheckListCtrlMixin):

    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1,
                             style=wx.LC_REPORT | wx.LC_NO_HEADER)
        CheckListCtrlMixin.__init__(self)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemActivated)

    def OnItemActivated(self, evt):
        self.ToggleItem(evt.m_itemIndex)


# -------------------                                  ------------------------
# -------------------                                  ------------------------
class KBlock():

    def __init__(self, name, dframe):
        self.name = name
        self.dframe = dframe
#         self.dframe_nor = self.normalized()
        self.columns = self.g_columns(dframe)
        self.order = 0

    def normalized(self):
        class_column = 'Name'

        df = self.dframe.drop(class_column, axis=1)
        nor = (lambda x: x / np.linalg.norm(x))
        dframe_nor = DataFrame(nor(df.values), columns=df.columns.tolist())
        dframe_nor[class_column] = self.dframe[class_column].tolist()

        return dframe_nor

    def g_columns(self, df):
        cols = df.columns.tolist()
        return cols[:-1]


# -------------------                                  ------------------------
# -------------------                                  ------------------------
class KCluster():

    def __init__(self, name, dframe):
        self.name = name
        self.dframe = dframe
        # self.dframe_nor = self.normalized()
        self.columns = self.g_columns(dframe)
        self.order = 0

    def normalized(self):
        class_column = 'Name'

        df = self.dframe.drop(class_column, axis=1)
        nor = (lambda x: x / np.linalg.norm(x))
        dframe_nor = DataFrame(nor(df.values), columns=df.columns.tolist())
        dframe_nor[class_column] = self.dframe[class_column].tolist()

        return dframe_nor

    def g_columns(self, df):
        cols = df.columns.tolist()
        return cols[:-1]
