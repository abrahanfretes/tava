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

        if sh and km:
            self.shape_list.DeleteAllItems()
            self.kmeans_list.DeleteAllItems()
        if km:
            self.nb_clus.SetSelection(1)
        if sh:
            self.nb_clus.SetSelection(0)

    def generate_shapes(self, df_population, clus):
        # ---- generar clusters
        self.shape = Shape(df_population, clus=clus)

    def generate_kmeans(self, df_population, clus):
        # ---- generar clusters
        self.tkmeans = Kmeans(df_population, clus=clus)

    def update_list(self, c_shape, c_kmenas):

        self._checked_all.SetValue(False)

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

    def g_elements(self):
        if self.pages[0]:
            return self.shape.clusters_count

        if self.pages[1]:
            return self.tkmeans.clusters_count

    # ---- funciones para análisis

    def more_representative(self, repre, less_rep):

        self.un_select_all()

        if self.pages[0]:
            # ---- más representativos
            for index in self.shape_row_index[:repre]:
                self.shape_list.CheckItem(index)

            # ---- menos representativos
            for index in self.shape_row_index[less_rep:]:
                self.shape_list.CheckItem(index)

        if self.pages[1]:
            # ---- más representativos
            for index in self.kmeans_row_index[:repre]:
                self.kmeans_list.CheckItem(index)

            # ---- menos representativos
            for index in self.kmeans_row_index[less_rep:]:
                self.kmeans_list.CheckItem(index)

    def max_min_objective(self, v_max, v_min):
        self.un_select_all()

        if self.pages[0]:
            for index in self.shape.g_clusters_max_min_in_var(v_max, v_min):
                self.shape_list.CheckItem(index)

        if self.pages[1]:
            for index in self.tkmeans.g_clusters_max_min_in_var(v_max, v_min):
                self.kmeans_list.CheckItem(index)

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
