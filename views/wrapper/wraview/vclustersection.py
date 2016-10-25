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
# Creado:  25/10/2016                                        ###
#                                                            ###
# ##############################################################
'''

# from wx.lib.agw.customtreectrl import A

import sys
from wx import GetTranslation as L
import wx
from wx.lib.agw import aui
from wx.lib.agw.aui.auibook import AuiNotebook
from wx.lib.mixins.listctrl import CheckListCtrlMixin
from wx.lib.pubsub import Publisher as pub

from languages import topic as T
from views.wrapper.wraview.cluster.shape import Shape
from views.wrapper.wraview.cluster.tkmeans import Kmeans


# from views.wrapper.wraview.vcontrol import CLUS_SHAPE, CLUS_KMEANS, CLUS_BOTH
class ClusterSeccionNew(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)

        pub().subscribe(self.update_language, T.LANGUAGE_CHANGED)

        self.SetBackgroundColour('#FFFFFF')

        # ---- componetes de vistas
        self._checked_all = wx.CheckBox(self, -1, L('SELECT_ALL'))
        self._checked_all.Bind(wx.EVT_CHECKBOX, self.on_checked_all)

        _agws = aui.AUI_NB_TOP | aui.AUI_NB_TAB_SPLIT | aui.AUI_NB_TAB_MOVE
        _agws = _agws | aui.AUI_NB_SCROLL_BUTTONS | aui.AUI_NB_DRAW_DND_TAB

        self.nb_clus = AuiNotebook(self, agwStyle=_agws)

        self.shape_list = CheckListCtrlCluster(self.nb_clus)
        self.shape_list.InsertColumn(0, L('NAME'))
        self.nb_clus.AddPage(self.shape_list, "Shape")

        self.kmeans_list = CheckListCtrlCluster(self.nb_clus)
        self.kmeans_list.InsertColumn(0, L('NAME'))
        self.nb_clus.AddPage(self.kmeans_list, "Kmeans")
        self.nb_clus.EnableTab(1, False)

        self.shape = None
        self.tkmeans = None
        self.shape_row_index = []
        self.kmeans_row_index = []
        self.pages = [True, False]

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self._checked_all, flag=wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(self.nb_clus, 1, wx.EXPAND | wx.ALL, 1)
        self.SetSizer(sizer)

    def update_page(self, sh, km):
        self.nb_clus.EnableTab(0, enable=sh)
        self.nb_clus.EnableTab(1, enable=km)
        self.pages = [sh, km]

    def generate_shapes(self, df_population, clus):
        # ---- generar clusters
        self.shape = Shape(df_population, clus=clus)

    def generate_kmeans(self, df_population, clus):
        # ---- generar clusters
        self.tkmeans = Kmeans(df_population, clus=clus)

    def update_list(self, c_shape, c_kmenas):

        # ---- Sección Shape

        if c_shape:
            # ----- limpiar clusters anteriores
            self.shape_row_index = []
            self.shape_list.DeleteAllItems()
            # ---- agregar clusters a la vista
            for i, c in enumerate(self.shape.clusters):
                name = 'cluster_' + str(i + 1) + ': ' + c.g_percent_format()
                index = self.shape_list.InsertStringItem(sys.maxint, name)
                self.shape_list.SetItemData(index, index)
                self.shape_row_index.append(index)
            self.shape_list.SetColumnWidth(0, wx.LIST_AUTOSIZE)

        # ---- Sección Kmeans

        if c_kmenas:
            # ----- limpiar clusters anteriores
            self.kmeans_row_index = []
            self.kmeans_list.DeleteAllItems()
            # ---- agregar clusters a la vista
            for i, c in enumerate(self.tkmeans.clusters):
                name = 'cluster_' + str(i + 1) + ': ' + c.g_percent_format()
                index = self.kmeans_list.InsertStringItem(sys.maxint, name)
                self.kmeans_list.SetItemData(index, index)
                self.kmeans_row_index.append(index)
            self.kmeans_list.SetColumnWidth(0, wx.LIST_AUTOSIZE)

    def select_all(self):

        if self.pages[0]:
            for index in self.shape_row_index:
                self.shape_list.CheckItem(index)

        if self.pages[1]:
            for index in self.kmeans_row_index:
                self.kmeans_list.CheckItem(index)

    def un_select_all(self):
        if self.pages[0]:
            for index in self.shape_row_index:
                self.shape_list.CheckItem(index, False)

        if self.pages[1]:
            for index in self.kmeans_row_index:
                self.kmeans_list.CheckItem(index, False)

    def on_checked_all(self, event):
        if event.IsChecked():
            self.select_all()
        else:
            self.un_select_all()

    def g_for_view(self):

        if self.pages[0]:
            position_checked = []
            position_unchecked = []
            for i, r_i in enumerate(self.shape_row_index):
                if self.shape_list.IsChecked(r_i):
                    position_checked.append(i)
                else:
                    position_unchecked.append(i)
            self.shape.cluster_checkeds = position_checked
            self.shape.cluster_uncheckeds = position_unchecked

        if self.pages[1]:
            position_checked = []
            position_unchecked = []

            for i, r_i in enumerate(self.kmeans_row_index):
                if self.kmeans_list.IsChecked(r_i):
                    position_checked.append(i)
                else:
                    position_unchecked.append(i)
            self.tkmeans.cluster_checkeds = position_checked
            self.tkmeans.cluster_uncheckeds = position_unchecked

    def contain_elemens(self):

        if self.pages[0]:
            return self.shape_list.GetItemCount()

        if self.pages[1]:
            return self.kmeans_list.GetItemCount()

    def checked_elemens(self):

        if self.pages[0]:
            for index in self.shape_row_index:
                if self.shape_list.IsChecked(index):
                    return True
            return False

        if self.pages[1]:
            for index in self.kmeans_row_index:
                if self.kmeans_list.IsChecked(index):
                    return True
            return False

# 
#         sel = self.nb.GetSelection()
#         if sel == CLUS_SHAPE:
#             self.shape_row_index = []
#             shape_list = self.nb.GetPage(CLUS_SHAPE).shape_list
#             self.populate_list(shape_list, self.shape.clusters,
#                                self.shape_row_index)
#         if sel == CLUS_KMEANS:
#             self.kmeans_row_index = []
#             kmeans_list = self.nb.GetPage(CLUS_KMEANS).kmeans_list
#             self.populate_list(kmeans_list, self.kmeans.clusters,
#                                self.kmeans_row_index)
#         if sel == CLUS_BOTH:
#             self.kmeans_row_index = []
#             self.shape_row_index = []
#             shape_list = self.nb.GetPage(CLUS_BOTH).nb.GetPage(0).shape_list
#             self.populate_list(shape_list, self.shape.clusters,
#                                self.shape_row_index)
#             kmeans_list = self.nb.GetPage(CLUS_BOTH).nb.GetPage(1).kmeans_list
#             self.populate_list(kmeans_list, self.kmeans.clusters,
#                                self.kmeans_row_index)

#     def populate_list(self, _list, _clusters, _row_index):
#         # ----- limpiar clusters anteriores
#         _list.DeleteAllItems()
# 
#         # ---- agregar clusters a la vista
#         for i, c in enumerate(_clusters):
#             name = 'cluster_' + str(i + 1) + ': ' + c.g_percent_format()
#             index = _list.InsertStringItem(sys.maxint, name)
#             _list.SetItemData(index, index)
#             _row_index.append(index)
# 
#         _list.SetColumnWidth(0, wx.LIST_AUTOSIZE)

    def pre_un_select_all(self):
        sel = self.nb.GetSelection()
        if sel == CLUS_SHAPE:
            shape_list = self.nb.GetPage(CLUS_SHAPE).shape_list
            self.un_select_all(shape_list, self.shape_row_index)
        if sel == CLUS_KMEANS:
            kmeans_list = self.nb.GetPage(CLUS_KMEANS).kmeans_list
            self.un_select_all(kmeans_list, self.kmeans_row_index)
        if sel == CLUS_BOTH:
            shape_list = self.nb.GetPage(CLUS_BOTH).nb.GetPage(0).shape_list
            kmeans_list = self.nb.GetPage(CLUS_BOTH).nb.GetPage(1).kmeans_list
            self.un_select_all(shape_list, self.shape_row_index)
            self.un_select_all(kmeans_list, self.kmeans_row_index)

#     def on_checked_all(self, event):
#         if event.IsChecked():
#             
#             sel = self.nb.GetSelection()
#             if sel == CLUS_SHAPE:
#                 shape_list = self.nb.GetPage(CLUS_SHAPE).shape_list
#                 self.select_all(shape_list, self.shape_row_index)
#             if sel == CLUS_KMEANS:
#                 kmeans_list = self.nb.GetPage(CLUS_KMEANS).kmeans_list
#                 self.select_all(kmeans_list, self.kmeans_row_index)
#             if sel == CLUS_BOTH:
#                 shape_list = self.nb.GetPage(CLUS_BOTH).nb.GetPage(0).shape_list
#                 kmeans_list = self.nb.GetPage(CLUS_BOTH).nb.GetPage(1).kmeans_list
#                 self.select_all(shape_list, self.shape_row_index)
#                 self.select_all(kmeans_list, self.kmeans_row_index)
#         else:
#             self.pre_un_select_all()

#     def select_all(self, _list, _row_index):
#         for index in _row_index:
#             _list.CheckItem(index)
# 
#     def un_select_all(self, _list, _row_index):
#         for index in _row_index:
#             _list.CheckItem(index, False)

#     def contain_elemens(self):
#         sel = self.nb.GetSelection()
#         if sel == CLUS_SHAPE:
#             shape_list = self.nb.GetPage(CLUS_SHAPE).shape_list
#             return shape_list.GetItemCount()
#         if sel == CLUS_KMEANS:
#             kmeans_list = self.nb.GetPage(CLUS_KMEANS).kmeans_list
#             return kmeans_list.GetItemCount()
#         if sel == CLUS_BOTH:
#             shape_list = self.nb.GetPage(CLUS_BOTH).nb.GetPage(0).shape_list
#             return shape_list.GetItemCount()
# 
#     def checked_elemens(self):
#         sel = self.nb.GetSelection()
#         if sel == CLUS_SHAPE:
#             _list = self.nb.GetPage(CLUS_SHAPE).shape_list
#             _row_index = self.shape_row_index
#         if sel == CLUS_KMEANS:
#             _list = self.nb.GetPage(CLUS_KMEANS).kmeans_list
#             _row_index = self.kmeans_row_index
#         if sel == CLUS_BOTH:
#             _list = self.nb.GetPage(CLUS_BOTH).nb.GetPage(0).shape_list
#             _row_index = self.shape_row_index
#         for index in _row_index:
#             if _list.IsChecked(index):
#                 return True
#             return False

#     # ---- funciones para análisis
# 
#     def more_representative(self, repre, less_rep):
#         self.pre_un_select_all()
# 
#         # ---- más representativos
#         for index in self.row_index[:repre]:
#             self.list_control.CheckItem(index)
# 
#         # ---- menos representativos
#         for index in self.row_index[less_rep:]:
#             self.list_control.CheckItem(index)
# 
#     def less_representative(self, repre):
#         self.pre_un_select_all()
#         for index in self.row_index[repre:]:
#             self.list_control.CheckItem(index)

    def max_min_objective(self, v_max, v_min):
        self.pre_un_select_all()
        for index in self.shape.g_clusters_max_min_in_var(v_max, v_min):
            self.list_control.CheckItem(index)

    def update_language(self, msg):
        self._checked_all.SetLabel(L('SELECT_ALL'))


class CheckListCtrlCluster(wx.ListCtrl, CheckListCtrlMixin):

    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1,
                             style=wx.LC_REPORT | wx.LC_NO_HEADER)
        CheckListCtrlMixin.__init__(self)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemActivated)

    def OnItemActivated(self, evt):
        self.ToggleItem(evt.m_itemIndex)
