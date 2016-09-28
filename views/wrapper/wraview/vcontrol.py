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
from wx.lib.agw import customtreectrl as CT
from wx.lib.mixins.listctrl import CheckListCtrlMixin

from imgs.iview import refresh_plot
import numpy as np
import pandas as pd
from views.wrapper.vdialog.vfigured import DataConfig
from views.wrapper.wraview.cluster.shape import Shape
from views.wrapper.wraview.vcontrolf import FigureManyD, FigureD, Figure1D
from views.wrapper.wraview.vcontrolm import KMSG_EMPTY_DATA_SELECTED, \
    KMessage, KMSG_EMPTY_DUPLICATE_DATA
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


class ControlPanel(wx.Panel):

    def __init__(self, parent, kfigure, ksub_blocks, mainpanel):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.mainpanel = mainpanel
        self.kfigure = kfigure
        self.SetBackgroundColour("#3B598D")

        self.normalized = True
        self.duplicate_true = K_DATE_DUPLICATE_TRUE
        self.k_plot = K_PLOT_BLOCK
        self.k_color = K_COLOR_SUB_BLOCK

#         self.nb_dates = aui.AuiNotebook(self, agwStyle=KURI_AUI_NB_STYLE)
#         self.nb_dates.SetArtProvider(aui.VC71TabArt())
# 
#         self.data_seccion = DataSeccion(
#             self.nb_dates, ksub_blocks)
# 
#         self.nb_dates.AddPage(self.data_seccion, "Datas")
#         self.clusters_seccion = ClusterSeccion(self.nb_dates)
#         self.nb_dates.AddPage(self.clusters_seccion, "Clusters")

        # ---- Lista de Datos
        self.data_seccion = DataSeccion(self, ksub_blocks)
        self.clusters_seccion = ClusterSeccion(self)

        # ---------------- controles medios -------------
        cpanel = wx.Panel(self)
        cpanel.SetBackgroundColour('#DCE5EE')
        sampleList = ['Datos', 'Clusters']
        psizer = wx.BoxSizer(wx.HORIZONTAL)
        self.rb_option = wx.RadioBox(cpanel, -1, "", wx.DefaultPosition,
                                     wx.DefaultSize, sampleList, 1,
                                     wx.RA_SPECIFY_COLS | wx.NO_BORDER)
        psizer.Add(self.rb_option, flag=wx.ALIGN_CENTER_VERTICAL)
        _refresh = wx.BitmapButton(cpanel, style=wx.NO_BORDER,
                                   bitmap=refresh_plot.GetBitmap())
        _refresh.Bind(wx.EVT_BUTTON, self.on_refresh)
        psizer.Add(_refresh, flag=wx.ALIGN_CENTER_VERTICAL)
        cpanel.SetSizer(psizer)
        # /---------------- controles medios -------------

        # ---- selección de Figuras
#         self.nb_figure = aui.AuiNotebook(self, agwStyle=KURI_AUI_NB_STYLE1)
#         self.nb_figure.SetArtProvider(aui.VC71TabArt())
#         self.many_dimension = FigureManyD(self.nb_figure)
#         self.nb_figure.InsertPage(K_MANY_PAGE, self.many_dimension,
#                                   "> 3D", True)
#         page = FigureD(self.nb_figure, [])
#         self.nb_figure.InsertPage(K_3D_PAGE, page, " 3D")
#         self.nb_figure.EnableTab(K_3D_PAGE, False)
#         page = FigureD(self.nb_figure, [])
#         self.nb_figure.InsertPage(K_2D_PAGE, page, " 2D")
#         self.nb_figure.EnableTab(K_2D_PAGE, False)
#         self.one_dimension = Figure1D(self.nb_figure)
#         self.nb_figure.InsertPage(K_1D_PAGE, self.one_dimension, " 1D")

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(cpanel, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 1)
        self.sizer.Add(self.data_seccion, 1, wx.EXPAND | wx.ALL, 1)
        self.sizer.Add(self.clusters_seccion, 1, wx.EXPAND | wx.ALL, 1)
        self.SetSizer(self.sizer)
        self.Fit()

    def run_fig(self):

        blocks = []
        # se obtine la lista de bloques marcados
        if self.rb_option.GetSelection() == 0:
            blocks = self.data_seccion.get_checkeds(self.normalized)

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
            self.kfigure.kdraw(blocks_2, self.kfigure.graphics.g_selected())

        else:
            shape = self.clusters_seccion.g_for_view()

            # porcentajes requeridos
            s_clusters = shape.g_percent_up(3.0)

            dd = shape.g_data_for_fig(s_clusters)
            dr = shape.g_resume_for_fig(s_clusters)
            _v = [dd, dr]

            # datos seleccionados
            # dd = shape.g_data_checkeds_for_fig()
            # dr = shape.g_resume_checkeds_for_fig()

            # update figure
            self.kfigure.kdraw(_v, self.kfigure.graphics.g_selected())

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
                _blocks.append(df[df[c_d]==True].drop(c_d, axis=1))
        return _blocks


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

        sizer_t = wx.BoxSizer(wx.HORIZONTAL)
        b_create = wx.BitmapButton(self, style=wx.NO_BORDER,
                                   bitmap=refresh_plot.GetBitmap())
        sizer_t.Add(b_create, flag=wx.ALIGN_CENTER_VERTICAL)

        self.sc_count_clusters = wx.SpinCtrl(self, 0, "", (30, 50))
        self.sc_count_clusters.SetRange(0, 1000)
        self.sc_count_clusters.SetValue(0)
        sizer_t.Add(self.sc_count_clusters, flag=wx.ALIGN_CENTER_VERTICAL)

        _checked_all = wx.CheckBox(self, -1, "Seleccionar Todo")
        _checked_all.Bind(wx.EVT_CHECKBOX, self.on_checked_all)

        sizer.Add(sizer_t, 0)
        sizer.Add(_checked_all, flag=wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(self.list_control, 1, wx.EXPAND)

        self.SetSizer(sizer)

        b_create.Bind(wx.EVT_BUTTON, self.on_generate)
        # refresh.Bind(wx.EVT_BUTTON, self.on_refresh)

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

    def on_generate(self, event):
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
        _clus = self.sc_count_clusters.GetValue()
        self.shape = Shape(df_population, clus=_clus, nor=2)

        # ---- agregar clusters a la vista
        for i, c in enumerate(self.shape.clusters):
            # name = data[0] + _tit + 'c' + str(vclus)
            name = 'cluster_' + str(i+1) + ': ' + c.g_percent_format()
            index = self.list_control.InsertStringItem(sys.maxint, name)
            self.list_control.SetItemData(index, index)
            self.row_index.append(index)

        self.list_control.SetColumnWidth(0, wx.LIST_AUTOSIZE)

    def on_checked_all(self, event):
        if event.IsChecked():
            for index in self.row_index:
                self.list_control.CheckItem(index)
        else:
            for index in self.row_index:
                self.list_control.CheckItem(index, False)


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

    def get_checkeds(self, nor):
        _subblocks_checked = []

        if nor:
            for index in self.row_index:
                if self.list_control.IsChecked(index):
                    key = self.list_control.GetItemData(index)
                    kblock = self.kblocks[key][1]
                    _subblocks_checked.append(kblock.dframe_nor)
            return _subblocks_checked

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
                # _subblocks_checked.append(kblock.dframe)
                block_checked[key] = self.kblocks[key]
        return block_checked

    def on_checked_all(self, event):
        if event.IsChecked():
            for index in self.row_index:
                self.list_control.CheckItem(index)
        else:
            for index in self.row_index:
                self.list_control.CheckItem(index, False)


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
        self.dframe_nor = self.normalized()
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


# -------------------                                  ------------------------
# -------------------                                  ------------------------
class GenerateCluster(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, size=(400, 300),
                           title='Generar Clusters')
        self.parent = parent
        self.init_ui()

        # ------ Definiciones iniciales -----

        self.Centre(wx.BOTH)
        self.CenterOnScreen()
        self.ShowModal()

    def init_ui(self):

        sizer = wx.BoxSizer(wx.VERTICAL)

        self.cb_shape = wx.CheckBox(self, -1, "Shape")
        self.cb_shape.SetValue(self.parent.shape_value)

        self.cb_kmeans = wx.CheckBox(self, -1, "K-means")
        self.cb_kmeans.SetValue(self.parent.kmeans_value)

        self.sc_count_clusters = wx.SpinCtrl(self, -1, "", (30, 50))
        self.sc_count_clusters.SetRange(2, 100)
        self.sc_count_clusters.SetValue(2)

        self.cb_shape.Bind(wx.EVT_CHECKBOX, self.on_cluster_ckeck)
        self.cb_kmeans.Bind(wx.EVT_CHECKBOX, self.on_cluster_ckeck)

        # buttons confirmar, cancelar
        sizer_button = wx.BoxSizer(wx.HORIZONTAL)
        sizer_cancel = wx.BoxSizer()
        self.cancel = wx.Button(self, -1, 'Cancelar')
        self.cancel.SetDefault()
        sizer_cancel.Add(self.cancel)
        sizer_apply = wx.BoxSizer()
        self.apply = wx.Button(self, -1, 'Aplicar')
        sizer_apply.Add(self.apply, 0, wx.ALIGN_RIGHT)

        sizer_button.Add(sizer_cancel, 0, wx.ALL, 5)
        sizer_button.Add(sizer_apply, 0, wx.ALL, 5)

        sizer.Add(self.cb_shape, 0, wx.ALL, 5)
        sizer.Add(self.cb_kmeans, 0, wx.ALL, 5)
        sizer.Add(self.sc_count_clusters, 0, wx.ALL, 5)
        sizer.Add(sizer_button, 0, wx.EXPAND | wx.LEFT, 100)

        self.SetSizer(sizer)

        self.Bind(wx.EVT_BUTTON, self.on_button_apply, self.apply)
        self.Bind(wx.EVT_BUTTON, self.on_button_cancel, self.cancel)

    def on_button_cancel(self, event):
        self.parent.c_shape = False
        self.parent.c_kmenas = False
        self.Close()

    def on_button_apply(self, event):
        self.parent.c_shape = self.cb_shape.IsChecked()
        self.parent.c_kmenas = self.cb_kmeans.IsChecked()
        self.parent.c_number = self.sc_count_clusters.GetValue()

        self.Close()

    def on_key_escape(self, event):
        if event.GetKeyCode() == wx.WXK_ESCAPE:
            self.parent.c_shape = False
            self.parent.c_kmenas = False
            self.Close()

    def on_cluster_ckeck(self, event):
        self.apply.Disable()
        self.cancel.SetDefault()

        if self.cb_shape.IsChecked():
            self.parent.shape_value = True
            self.apply.Enable()
            self.apply.SetDefault()

        if self.cb_kmeans.IsChecked():
            self.parent.kmeans_value = True
            self.apply.Enable()
            self.apply.SetDefault()

        if not self.cb_shape.IsChecked():
            self.parent.shape_value = False

        if not self.cb_kmeans.IsChecked():
            self.parent.kmeans_value = False
