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
K_PLOT_SUB_BLOCK = 2

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

        sizer_p1 = wx.BoxSizer(wx.HORIZONTAL)
        _run = wx.BitmapButton(self, style=wx.NO_BORDER,
                               bitmap=run_plot.GetBitmap())
        sizer_p1.Add(_run, flag=wx.ALIGN_CENTER_VERTICAL)
        _run.Bind(wx.EVT_BUTTON, self.on_run)
        _refresh = wx.BitmapButton(self, style=wx.NO_BORDER,
                                   bitmap=refresh_plot.GetBitmap())
        sizer_p1.Add(_refresh, flag=wx.ALIGN_CENTER_VERTICAL)
        _refresh.Bind(wx.EVT_BUTTON, self.on_refresh)
        sizer_center.Add(sizer_p1, flag=wx.ALIGN_LEFT)

        sline1 = wx.StaticLine(self, -1, style=wx.LI_HORIZONTAL)
        sizer_center.Add(sline1, flag=wx.EXPAND)

        sizer_p2 = wx.BoxSizer(wx.HORIZONTAL)
        _normalized = wx.CheckBox(self, -1, "nor")
        _normalized.SetValue(self.normalized)
        _normalized.Bind(wx.EVT_CHECKBOX, self.on_normalized)
        sizer_p2.Add(_normalized, flag=wx.ALIGN_CENTER_VERTICAL)
        sizer_center.Add(sizer_p2, flag=wx.ALIGN_LEFT)

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
                              choices=['One', 'Block', 'SubBlock'])
        _k_plot.SetSelection(self.k_plot)
        _k_plot.Bind(wx.EVT_RADIOBOX, self.on_k_plot)
        sizer_p4.Add(_k_plot, flag=wx.ALIGN_CENTER_VERTICAL)
        sizer_center.Add(sizer_p4, flag=wx.ALIGN_LEFT)

        sizer_p5 = wx.BoxSizer(wx.HORIZONTAL)
        _k_color = wx.RadioBox(self, label='Colors',
                               choices=['One', 'Block', 'SubBlock', 'value'])
        _k_color.SetSelection(self.k_color)
        _k_color.Bind(wx.EVT_RADIOBOX, self.on_k_color)
        sizer_p5.Add(_k_color, flag=wx.ALIGN_CENTER_VERTICAL)
        sizer_center.Add(sizer_p5, flag=wx.ALIGN_LEFT)

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

        # se obtine la lista de bloques marcados
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
        if self.nb_figure.GetSelection() == K_MANY_PAGE:
            key_figure = self.many_dimension.g_key_figure()
            self.kfigure.kdraw(blocks_2, key_figure)
        elif self.nb_figure.GetSelection() == K_1D_PAGE:
            self.kfigure.kdraw_one(blocks_2)

        # update data list
        self.kdata.kadd(pd.concat(blocks_2))

    def on_refresh(self, event):
        print 'on click refres'

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


class ClusterSeccion(CT.CustomTreeCtrl):

    def __init__(self, parent):
        CT.CustomTreeCtrl.__init__(self, parent, -1, wx.Point(0, 0),
                                   wx.Size(220, 250))

        self.SetAGWWindowStyleFlag(KURI_TR_STYLE1)
        self.root = self.AddRoot('ROOT-CLUTERS')
        self.init_ui()

    def init_ui(self):

        # self.init_tree()
        # ordenamos el arbol
        self.SortChildren(self.root)
        self.ExpandAllChildren(self.root)

        # por resultado
        for r in range(2):
            r_item = self.AppendItem(self.root, str(r), ct_type=1)
            self.SetItemPyData(r_item, 'Algo')

        self.ExpandAllChildren(self.root)


# -------------------                                  ------------------------
# -------------------                                  ------------------------
class DataSeccion(wx.Panel):
    def __init__(self, parent, ksub_blocks):
        wx.Panel.__init__(self, parent, -1)
        self.ksub_blocks = ksub_blocks
        self.row_index = []

        self.list = CheckListCtrl(self)
        sizer = wx.BoxSizer()
        sizer.Add(self.list, 1, wx.EXPAND)
        self.SetSizer(sizer)

        self.list.InsertColumn(0, "Bloque")

        for key, data in ksub_blocks.iteritems():
            index = self.list.InsertStringItem(sys.maxint, data[0])
            self.list.SetItemData(index, key)
            self.row_index.append(index)

    def get_checkeds(self, nor):
        _subblocks_checked = []

        if nor:
            for index in self.row_index:
                if self.list.IsChecked(index):
                    key = self.list.GetItemData(index)
                    kblock = self.ksub_blocks[key][1]
                    _subblocks_checked.append(kblock.dframe_nor)
            return _subblocks_checked

        for index in self.row_index:
            if self.list.IsChecked(index):
                key = self.list.GetItemData(index)
                kblock = self.ksub_blocks[key][1]
                _subblocks_checked.append(kblock.dframe)
        return _subblocks_checked


class CheckListCtrl(wx.ListCtrl, CheckListCtrlMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT)
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
