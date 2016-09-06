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

from imgs.iview import refresh_plot, run_plot
import numpy as np
import pandas as pd
from views.wrapper.wraview.vcontrolf import FigureManyD, FigureD, Figure1D
from views.wrapper.wraview.vcontrolm import KMSG_EMPTY_DATA_SELECTED, \
    KMessage, KMSG_EMPTY_DUPLICATE_DATA
from views.wrapper.wraview.vcontrolp import KMenuBlocks, BlockSorted, \
    K_MENU_ITEM_DATA_BLOCK, K_MENU_ITEM_DATA_SUBBLOCK, SubBlockSorted
import wx.lib.agw.aui as aui
from views.wrapper.wraview.cluster.shape import TShape


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

    def __init__(self, parent, kfigure, kdata, ksub_blocks, mainpanel):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.mainpanel = mainpanel
        self.kfigure = kfigure
        self.kdata = kdata
        # self.SetBackgroundColour('#ADADAD')
        self.SetBackgroundColour('#DCDCDC')

        self.normalized = True
        self.duplicate_true = K_DATE_DUPLICATE_TRUE
        self.k_plot = K_PLOT_BLOCK
        self.k_color = K_COLOR_SUB_BLOCK

        self.nb_dates = aui.AuiNotebook(self, agwStyle=KURI_AUI_NB_STYLE)
        self.nb_dates.SetArtProvider(aui.VC71TabArt())

        self.data_seccion = DataSeccion(
            self.nb_dates, ksub_blocks)

        self.nb_dates.AddPage(self.data_seccion, "Datas")
        self.clusters_seccion = ClusterSeccion(self.nb_dates)
        self.nb_dates.AddPage(self.clusters_seccion, "Clusters")

        sizer_center = wx.BoxSizer(wx.VERTICAL)

        sampleList = ['Datos', 'Clusters']
        sizer_p0 = wx.BoxSizer(wx.HORIZONTAL)
        self.rb_option = wx.RadioBox(self, -1, "", wx.DefaultPosition,
                                     wx.DefaultSize, sampleList, 3,
                                     wx.RA_SPECIFY_COLS | wx.NO_BORDER)
        sizer_p0.Add(self.rb_option, flag=wx.ALIGN_CENTER_VERTICAL)
        sizer_center.Add(sizer_p0, flag=wx.ALIGN_LEFT)

        sizer_p1 = wx.BoxSizer(wx.HORIZONTAL)
        _run = wx.BitmapButton(self, style=wx.NO_BORDER,
                               bitmap=run_plot.GetBitmap())
        sizer_p1.Add(_run, flag=wx.ALIGN_CENTER_VERTICAL)
        _run.Bind(wx.EVT_BUTTON, self.on_run)
        _refresh = wx.BitmapButton(self, style=wx.NO_BORDER,
                                   bitmap=refresh_plot.GetBitmap())
        sizer_p1.Add(_refresh, flag=wx.ALIGN_CENTER_VERTICAL)
        _refresh.Bind(wx.EVT_BUTTON, self.on_refresh)
        _normalized = wx.CheckBox(self, -1, "nor")
        _normalized.SetValue(self.normalized)
        _normalized.Bind(wx.EVT_CHECKBOX, self.on_normalized)
        sizer_p1.Add(_normalized, flag=wx.ALIGN_CENTER_VERTICAL)
        sizer_center.Add(sizer_p1, flag=wx.ALIGN_LEFT)

        sline1 = wx.StaticLine(self, -1, style=wx.LI_HORIZONTAL)
        sizer_center.Add(sline1, flag=wx.EXPAND)

        # sizer_p2 = wx.BoxSizer(wx.HORIZONTAL) --------------------------------
        # _normalized = wx.CheckBox(self, -1, "nor") ---------------------------
        # _normalized.SetValue(self.normalized) --------------------------------
        # _normalized.Bind(wx.EVT_CHECKBOX, self.on_normalized) ----------------
        # sizer_p2.Add(_normalized, flag=wx.ALIGN_CENTER_VERTICAL) -------------
        # sizer_center.Add(sizer_p2, flag=wx.ALIGN_LEFT) -----------------------

        sline2 = wx.StaticLine(self, -1, style=wx.LI_HORIZONTAL)
        sizer_center.Add(sline2, flag=wx.EXPAND)

        sizer_p3 = wx.BoxSizer(wx.HORIZONTAL)
        _duplicate = wx.RadioBox(self, label='Allow Duplicates?',
                                 choices=['True', 'False', 'Only'])
        _duplicate.SetSelection(self.duplicate_true)
        _duplicate.Bind(wx.EVT_RADIOBOX, self.on_duplicate)
        sizer_p3.Add(_duplicate, flag=wx.ALIGN_CENTER_VERTICAL)
        sizer_center.Add(sizer_p3, flag=wx.ALIGN_LEFT)

        sline3 = wx.StaticLine(self, -1, style=wx.LI_HORIZONTAL)
        sizer_center.Add(sline3, flag=wx.EXPAND)

        sizer_p4 = wx.BoxSizer(wx.HORIZONTAL)
        _k_plot = wx.RadioBox(self, label='Plots',
                              choices=['One', 'Block'])
        _k_plot.SetSelection(self.k_plot)
        _k_plot.Bind(wx.EVT_RADIOBOX, self.on_k_plot)
        sizer_p4.Add(_k_plot, flag=wx.ALIGN_CENTER_VERTICAL)
        sizer_center.Add(sizer_p4, flag=wx.ALIGN_LEFT)

        # sizer_p5 = wx.BoxSizer(wx.HORIZONTAL) --------------------------------
        # _k_color = wx.RadioBox(self, label='Colors', -------------------------
                               # choices=['One', 'Block', 'SubBlock', 'value']) 
        # _k_color.SetSelection(self.k_color) ----------------------------------
        # _k_color.Bind(wx.EVT_RADIOBOX, self.on_k_color) ----------------------
        # sizer_p5.Add(_k_color, flag=wx.ALIGN_CENTER_VERTICAL) ----------------
        # sizer_center.Add(sizer_p5, flag=wx.ALIGN_LEFT) -----------------------

        self.nb_figure = aui.AuiNotebook(self, agwStyle=KURI_AUI_NB_STYLE1)
        self.nb_figure.SetArtProvider(aui.VC71TabArt())
        self.many_dimension = FigureManyD(self.nb_figure)
        self.nb_figure.InsertPage(K_MANY_PAGE, self.many_dimension,
                                  "> 3D", True)
        page = FigureD(self.nb_figure, [])
        self.nb_figure.InsertPage(K_3D_PAGE, page, " 3D")
        self.nb_figure.EnableTab(K_3D_PAGE, False)
        page = FigureD(self.nb_figure, [])
        self.nb_figure.InsertPage(K_2D_PAGE, page, " 2D")
        self.nb_figure.EnableTab(K_2D_PAGE, False)
        self.one_dimension = Figure1D(self.nb_figure)
        self.nb_figure.InsertPage(K_1D_PAGE, self.one_dimension, " 1D")

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.nb_dates, 1, wx.EXPAND)
        self.sizer.Add(sizer_center, 0.5, wx.EXPAND)
        self.sizer.Add(self.nb_figure, 1, wx.EXPAND)

        self.SetSizer(self.sizer)
        self.Fit()

    def on_run(self, event):
        self.run_fig()

    def run_fig(self):

        blocks = []
        # se obtine la lista de bloques marcados
        if self.rb_option.GetSelection() == 0:
            blocks = self.data_seccion.get_checkeds(self.normalized)
        else:
            blocks = self.clusters_seccion.get_checkeds()

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
        if self.nb_figure.GetSelection() == K_MANY_PAGE:
            key_figure = self.many_dimension.g_key_figure()
            self.kfigure.kdraw(blocks_2, key_figure)
        elif self.nb_figure.GetSelection() == K_1D_PAGE:
            self.kfigure.kdraw_one(blocks_2)

        # update data list
        self.kdata.kadd(pd.concat(blocks_2))

    def on_refresh(self, event):
        print 'on click refres'

        self.kmeans_value = True
        self.shape_value = True

        self.c_shape = False
        self.c_kmenas = False
        self.c_number = 0
        k_shape_frame = []

        GenerateCluster(self)

    def on_normalized(self, event):
        self.normalized = event.IsChecked()

    def on_duplicate(self, event):
        self.duplicate_true = event.GetSelection()

    def on_k_plot(self, event):
        self.k_plot = event.GetSelection()

    def on_k_color(self, event):
        self.k_color = event.GetSelection()

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

        self.parent = parent
        self.row_index = []
        self.kcluters = {}
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.list = CheckListCtrl(self)
        self.list.InsertColumn(0, "Nombre")
        sizer.Add(self.list, 1, wx.EXPAND)

        sizer_t = wx.BoxSizer(wx.HORIZONTAL)
        b_create = wx.BitmapButton(self, style=wx.NO_BORDER,
                                   bitmap=refresh_plot.GetBitmap())
        sizer_t.Add(b_create, flag=wx.ALIGN_CENTER_VERTICAL)

        self.sc_clusters = wx.SpinCtrl(self, -1, "", (30, 50))
        self.sc_clusters.SetRange(-1, 100)
        self.sc_clusters.SetValue(-1)
        sizer_t.Add(self.sc_clusters, flag=wx.ALIGN_CENTER_VERTICAL)

        sizer_m = wx.BoxSizer(wx.HORIZONTAL)
        self.merge_block = wx.CheckBox(self, -1, "Merge Bloks")
        self.merge_block.SetValue(False)
        sizer_m.Add(self.merge_block, flag=wx.ALIGN_CENTER_VERTICAL)

        sizer.Add(sizer_t, 0)
        sizer.Add(sizer_m, 0)
        self.SetSizer(sizer)

        b_create.Bind(wx.EVT_BUTTON, self.on_create)
        # refresh.Bind(wx.EVT_BUTTON, self.on_refresh)

    def get_checkeds(self):
        blocks_checked = []

        for index in self.row_index:
            if self.list.IsChecked(index):
                print  index
                key = self.list.GetItemData(index)
                df = self.kcluters[key][2]
                blocks_checked.append(df)
        return blocks_checked

    def on_create(self, event):
        _tit = '- '
        # limpiar filas
        self.list.DeleteAllItems()

        # optengo los datos checkeados de DataSeccion
        gp = self.parent.GetParent()
        kblocks = gp.data_seccion.get_checkeds_for_cluster()
        self.row_index = []

        # si son seleccionados mas de una iteracion
        # y mezclar esta activo, se concatenan los datos
        kblocks_two = {}
        if self.merge_block.IsChecked() and len(kblocks) > 1:
            kblocks_merge = []
            for _key, data in kblocks.iteritems():
                kblocks_merge.append(data[1].dframe_nor)
            df = pd.concat(kblocks_merge)
            kblocks_two[0] = ('', KBlock('0', df))
            _tit = ''
        else:
            kblocks_two = kblocks

        # generamos clusters
        vclus = 1
        for _key, data in kblocks_two.iteritems():
            df = data[1].dframe_nor
            tshape = TShape(df)

            for shape, freq, df in tshape.get_for_view():
                name = data[0] + _tit + 'c' + str(vclus)
                index = self.list.InsertStringItem(sys.maxint, name)
                self.list.SetItemData(index, index)
                self.kcluters[index] = (shape, freq, df)
                self.row_index.append(index)
                vclus += 1

        self.list.SetColumnWidth(0, wx.LIST_AUTOSIZE)


# -------------------                                  ------------------------
# -------------------                                  ------------------------
class DataSeccion(wx.Panel):
    def __init__(self, parent, kblocks):
        wx.Panel.__init__(self, parent, -1)
        self.kblocks = kblocks
        self.row_index = []

        self.list = CheckListCtrl(self)
        sizer = wx.BoxSizer()
        sizer.Add(self.list, 1, wx.EXPAND)
        self.SetSizer(sizer)

        self.list.InsertColumn(0, "Bloque")

        for key, data in kblocks.iteritems():
            index = self.list.InsertStringItem(sys.maxint, data[0])
            self.list.SetItemData(index, key)
            self.row_index.append(index)

        self.list.SetColumnWidth(0, wx.LIST_AUTOSIZE)

    def get_checkeds(self, nor):
        _subblocks_checked = []

        if nor:
            for index in self.row_index:
                if self.list.IsChecked(index):
                    key = self.list.GetItemData(index)
                    kblock = self.kblocks[key][1]
                    _subblocks_checked.append(kblock.dframe_nor)
            return _subblocks_checked

        for index in self.row_index:
            if self.list.IsChecked(index):
                key = self.list.GetItemData(index)
                kblock = self.kblocks[key][1]
                _subblocks_checked.append(kblock.dframe)
        return _subblocks_checked

    def get_checkeds_for_cluster(self):
        block_checked = {}

        for index in self.row_index:
            if self.list.IsChecked(index):
                key = self.list.GetItemData(index)
                # _subblocks_checked.append(kblock.dframe)
                block_checked[key] = self.kblocks[key]
        return block_checked


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

        self.sc_clusters = wx.SpinCtrl(self, -1, "", (30, 50))
        self.sc_clusters.SetRange(2, 100)
        self.sc_clusters.SetValue(2)

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
        sizer.Add(self.sc_clusters, 0, wx.ALL, 5)
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
        self.parent.c_number = self.sc_clusters.GetValue()

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
