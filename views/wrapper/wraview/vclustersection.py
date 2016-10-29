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
import wx.lib.agw.ultimatelistctrl as ULC
import wx.lib.colourselect as csel
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
        self.nb_clus.AddPage(self.shape_list, "Shape")

        self.kmeans_list = CheckListCtrlCluster(self.nb_clus)
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
            self.shape_row_index = []
            self.populate_list(self.shape_list, self.shape_row_index,
                               self.shape.clusters)

        # ---- Sección Kmeans
        if c_kmenas:
            # ----- limpiar clusters anteriores
            self.kmeans_row_index = []
            self.populate_list(self.kmeans_list, self.kmeans_row_index,
                               self.tkmeans.clusters)

    def populate_list(self, _list_ctrl, _row_index, _clusters):
        # ----- limpiar clusters anteriores
        _list_ctrl.DeleteAllItems()
        # ---- agregar clusters a la vista
        for i, c in enumerate(_clusters):
            name = ' cluster_' + str(i + 1) + ': ' + c.g_percent_format()
            index = _list_ctrl.InsertStringItem(sys.maxint, name, it_kind=1)

            _list_ctrl.SetStringItem(index, 1, "")

            _list_ctrl.SetStringItem(index, 2, "")

            _list_ctrl.SetItemData(index, index)
            _row_index.append(index)
        _list_ctrl.SetColumnWidth(0, wx.LIST_AUTOSIZE)

        fontMask = ULC.ULC_MASK_FONTCOLOUR | ULC.ULC_MASK_FONT
        fullMask = fontMask | ULC.ULC_MASK_BACKCOLOUR

        for i, c in enumerate(_clusters):
            item = _list_ctrl.GetItem(i, 1)
            item.SetMask(fullMask)
            font = wx.SystemSettings_GetFont(wx.SYS_DEFAULT_GUI_FONT)
            font.SetWeight(wx.BOLD)
            item.SetFont(font)
            item.SetBackgroundColour(wx.NamedColour(c.clus_color[0]))
            _list_ctrl.SetItem(item)

            item = _list_ctrl.GetItem(i, 2)
            item.SetMask(fullMask)
            font = wx.SystemSettings_GetFont(wx.SYS_DEFAULT_GUI_FONT)
            font.SetWeight(wx.BOLD)
            item.SetFont(font)
            item.SetBackgroundColour(wx.NamedColour(c.resu_color[0]))
            _list_ctrl.SetItem(item)

    def change_color_cluster(self, index, colour):
        if self.nb_clus.GetSelection() == 0:
            c = self.shape.clusters[index]
            c.clus_color = [colour.GetAsString(wx.C2S_HTML_SYNTAX)]
        if self.nb_clus.GetSelection() == 1:
            c = self.tkmeans.clusters[index]
            c.clus_color = [colour.GetAsString(wx.C2S_HTML_SYNTAX)]

    def change_color_summary(self, index, colour):
        if self.nb_clus.GetSelection() == 0:
            c = self.shape.clusters[index]
            c.resu_color = [colour.GetAsString(wx.C2S_HTML_SYNTAX)]
        if self.nb_clus.GetSelection() == 1:
            c = self.tkmeans.clusters[index]
            c.resu_color = [colour.GetAsString(wx.C2S_HTML_SYNTAX)]

    def select_all(self):

        if self.pages[0]:
            for index in self.shape_row_index:
                self.check_item(self.shape_list, index, True)

        if self.pages[1]:
            for index in self.kmeans_row_index:
                self.check_item(self.kmeans_list, index, True)

    def un_select_all(self):
        if self.pages[0]:
            for index in self.shape_row_index:
                self.check_item(self.shape_list, index, False)

        if self.pages[1]:
            for index in self.kmeans_row_index:
                self.check_item(self.kmeans_list, index, False)

    def on_checked_all(self, event):
        if event.IsChecked():
            self.select_all()
        else:
            self.un_select_all()

    def pre_view(self):

        if self.pages[0]:
            position_checked = []
            position_unchecked = []
            for i, r_i in enumerate(self.shape_row_index):
                if self.shape_list.IsItemChecked(r_i):
                    position_checked.append(i)
                else:
                    position_unchecked.append(i)
            self.shape.cluster_checkeds = position_checked
            self.shape.cluster_uncheckeds = position_unchecked

        if self.pages[1]:
            position_checked = []
            position_unchecked = []

            for i, r_i in enumerate(self.kmeans_row_index):
                if self.kmeans_list.IsItemChecked(r_i):
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
                if self.shape_list.IsItemChecked(index):
                    return True
            return False

        if self.pages[1]:
            for index in self.kmeans_row_index:
                if self.kmeans_list.IsItemChecked(index):
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
                self.check_item(self.shape_list, index, True)

            # ---- menos representativos
            for index in self.shape_row_index[less_rep:]:
                self.check_item(self.shape_list, index, True)

        if self.pages[1]:
            # ---- más representativos
            for index in self.kmeans_row_index[:repre]:
                self.check_item(self.kmeans_list, index, True)

            # ---- menos representativos
            for index in self.kmeans_row_index[less_rep:]:
                self.check_item(self.kmeans_list, index, True)

    def max_min_objective(self, v_max, v_min):
        self.un_select_all()

        if self.pages[0]:
            for index in self.shape.g_clusters_max_min_in_var(v_max, v_min):
                self.check_item(self.shape_list, index, True)

        if self.pages[1]:
            for index in self.tkmeans.g_clusters_max_min_in_var(v_max, v_min):
                self.check_item(self.kmeans_list, index, True)

    def check_item(self, _list, index, value):
        item = _list.GetItem(index, 0)
        item.Check(value)
        _list.SetItem(item)

    def update_language(self, msg):
        self._checked_all.SetLabel(L('SELECT_ALL'))


class CheckListCtrlCluster(ULC.UltimateListCtrl):

    def __init__(self, parent):
        ULC.UltimateListCtrl.__init__(self, parent, wx.ID_ANY,
                                      agwStyle=wx.LC_REPORT | wx.LC_VRULES |
                                      wx.LC_HRULES | wx.LC_SINGLE_SEL |
                                      ULC.ULC_HAS_VARIABLE_ROW_HEIGHT |
                                      ULC.ULC_AUTO_CHECK_CHILD)

        self.currentItem = 0

        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemActivated)
        self.Bind(wx.EVT_RIGHT_UP, self.OnRightClick)
        self.Bind(ULC.EVT_LIST_ITEM_SELECTED, self.OnItemSelected)

        self.InsertColumn(0, L('NAME'))
        self.InsertColumn(1, L('COLOR_CLUSTER'))
        self.InsertColumn(2, L('COLOR_SUMMARY'))

    def OnItemSelected(self, event):
        self.currentItem = event.m_itemIndex

    def OnItemActivated(self, evt):
        self.ToggleItem(evt.m_itemIndex)

    def OnRightClick(self, event):

        # only do this part the first time so the events are only bound once
        if not hasattr(self, "popupID1"):
            self.popupID1 = wx.NewId()
            self.popupID2 = wx.NewId()
            self.Bind(wx.EVT_MENU, self.on_change_color_clus, id=self.popupID1)
            self.Bind(wx.EVT_MENU, self.on_change_color_summ, id=self.popupID2)

        # make a menu
        menu = wx.Menu()
        # add some items
        menu.Append(self.popupID1, L('CHANGE_COLOR_CLUSTER'))
        menu.Append(self.popupID2, L('CHANGE_COLOR_SUMMARY'))

        # Popup the menu.  If an item is selected then its handler
        # will be called before PopupMenu returns.
        self.PopupMenu(menu)
        menu.Destroy()

    def on_change_color_clus(self, evt):
        item = self.GetItem(self.currentItem, 1)
        colour = item.GetBackgroundColour()
        c = wx.ColourData()
        c.SetColour(colour)
        dlg = wx.ColourDialog(self, c)

        dlg.GetColourData().SetChooseFull(True)

        if dlg.ShowModal() == wx.ID_OK:
            fontMask = ULC.ULC_MASK_FONTCOLOUR | ULC.ULC_MASK_FONT
            fullMask = fontMask | ULC.ULC_MASK_BACKCOLOUR
            data = dlg.GetColourData()
            item.SetMask(fullMask)
            font = wx.SystemSettings_GetFont(wx.SYS_DEFAULT_GUI_FONT)
            font.SetWeight(wx.BOLD)
            item.SetFont(font)
            item.SetBackgroundColour(data.GetColour())
            self.SetItem(item)
            self.GetParent().GetParent().change_color_cluster(self.currentItem,
                                                              data.GetColour())

        dlg.Destroy()

    def on_change_color_summ(self, evt):
        item = self.GetItem(self.currentItem, 2)
        colour = item.GetBackgroundColour()
        c = wx.ColourData()
        c.SetColour(colour)
        dlg = wx.ColourDialog(self, c)

        dlg.GetColourData().SetChooseFull(True)

        if dlg.ShowModal() == wx.ID_OK:
            fontMask = ULC.ULC_MASK_FONTCOLOUR | ULC.ULC_MASK_FONT
            fullMask = fontMask | ULC.ULC_MASK_BACKCOLOUR
            data = dlg.GetColourData()
            item.SetMask(fullMask)
            font = wx.SystemSettings_GetFont(wx.SYS_DEFAULT_GUI_FONT)
            font.SetWeight(wx.BOLD)
            item.SetFont(font)
            item.SetBackgroundColour(data.GetColour())
            self.SetItem(item)
            self.GetParent().GetParent().change_color_summary(self.currentItem,
                                                              data.GetColour())

        dlg.Destroy()
