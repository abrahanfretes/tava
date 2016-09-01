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
import wx
from wx.lib.agw import customtreectrl as CT

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
            self.nb_dates, ksub_blocks, self.mainpanel)
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
        blocks = self.data_seccion.g_selecteds(self.normalized)
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
            for block in blocks_1:
                for df in block:
                    blocks_2.append(df)
            blocks_2 = [pd.concat(blocks_2)]
        elif self.k_plot == K_PLOT_BLOCK:
            for block in blocks_1:
                blocks_2.append(pd.concat(block))
        else:
            for block in blocks_1:
                for df in block:
                    blocks_2.append(df)

        # update figure

        if self.nb_figure.GetSelection() == K_MANY_PAGE:
            key_figure = self.many_dimension.g_key_figure()
            self.kfigure.kdraw(blocks_2, key_figure)
        elif self.nb_figure.GetSelection() == K_1D_PAGE:
            self.kfigure.kdraw_one(df)

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
        for s_blocks in blocks:
            _sub_blocks = []
            for df in s_blocks:
                _sub_blocks.append(df.drop_duplicates())
            _blocks.append(_sub_blocks)
        return _blocks

    def only_duplicate(self, blocks):
        _blocks = []
        for s_blocks in blocks:
            _sub_blocks = []
            for df in s_blocks:
                col_aux = df.duplicated().tolist()
                if True in col_aux:
                    c_d = 'duplicate_true'
                    df[c_d] = col_aux
                    _sub_blocks.append(df[df[c_d] == True].drop(c_d, axis=1))
            if _sub_blocks != []:
                _blocks.append(_sub_blocks)
        return _blocks


# -------------------                                  ------------------------
class DataSeccion(CT.CustomTreeCtrl):

    def __init__(self, parent, ksub_blocks, mainpanel):
        CT.CustomTreeCtrl.__init__(self, parent, -1, wx.Point(0, 0),
                                   wx.Size(220, 250))

        self.mainpanel = mainpanel
        self.SetAGWWindowStyleFlag(KURI_TR_STYLE)
        self.root = self.AddRoot('ROOT-DATE')
        self.ksub_blocks = ksub_blocks

        self.init_ui()

        self.Bind(wx.EVT_RIGHT_UP, self.on_contex)

    def init_ui(self):

        b_ord = 0
        for kb in self.ksub_blocks:
            kb.order = b_ord
            rr_item = self.AppendItem(self.root, kb.name, ct_type=1)
            self.SetItemBold(rr_item)
            self.SetItemPyData(rr_item, kb)

            sb_ord = 0
            for skb in kb.ksub_blocks:
                skb.order = sb_ord
                r_item = self.AppendItem(rr_item, skb.name,
                                         ct_type=1)
                self.SetItemPyData(r_item, skb)

                for col in skb.columns:
                    item_col = self.AppendItem(r_item, col)
                    self.SetItemItalic(item_col)
                sb_ord += 1
            b_ord += 1

        for item in self.root.GetChildren():
            self.Expand(item)

    # ordenador de datos
    def OnCompareItems(self, item1, item2):
        return cmp(item1.GetData().order, item2.GetData().order)

    def g_selecteds(self, nor):

        _blocks = []

        if nor:
            for i_block in self.root.GetChildren():
                _block = []
                for i_sub_block in i_block.GetChildren():
                    if i_sub_block.IsChecked():
                        _block.append(i_sub_block.GetData().dframe_nor)
                if _block != []:
                    _blocks.append(_block)
            return _blocks

        for i_block in self.root.GetChildren():
            _block = []
            for i_sub_block in i_block.GetChildren():
                if i_sub_block.IsChecked():
                    _block.append(i_sub_block.GetData().dframe)
                if _block != []:
                    _blocks.append(_block)

        return _blocks

    # ####################################################################
    # menu del contexto
    # ####################################################################

    def on_contex(self, event):

        c_item = self.GetSelection()
        if c_item is None:
            return

        c_data = c_item.GetData()
        self.menu_block = -10

        if isinstance(c_data, KSubBlock):
            print 'instancia de subbloque'
        elif isinstance(c_data, KBlock):
            menu_block = KMenuBlocks(self)
            self.PopupMenu(menu_block)

            if self.menu_block == K_MENU_ITEM_DATA_BLOCK:
                BlockSorted(self, self.g_block_labels())

            elif self.menu_block == K_MENU_ITEM_DATA_SUBBLOCK:
                SubBlockSorted(self, self.g_subblock_labels(c_item), c_item)

    # ####################################################################
    # ordenaciones de datos, bloques, subbloque e item
    # ####################################################################

    def g_block_labels(self):
        block_labels = []
        for i_block in self.root.GetChildren():
            block_labels.append(i_block.GetText())
        return block_labels

    def sort_blocks(self, order_list):
        i = 0
        for i_block in self.root.GetChildren():
            i_block.GetData().order = order_list[i]
            i += 1
        self.SortChildren(self.root)

    def g_subblock_labels(self, c_item):
        subblock_labels = []
        for sub_block in c_item.GetChildren():
            subblock_labels.append(sub_block.GetText())
        return subblock_labels

    def sort_subblocks(self, order_list, c_item):
        i = 0
        for i_subblock in c_item.GetChildren():
            i_subblock.GetData().order = order_list[i]
            i += 1
        self.SortChildren(c_item)

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
class KBlock():

    def __init__(self, name, columns, ksub_blocks):
        self.name = name
        self.columns = columns
        self.ksub_blocks = ksub_blocks
        self.order = 0


# -------------------                                  ------------------------
class KSubBlock():

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
