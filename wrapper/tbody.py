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
# Creado:  27/8/2016                                         ###
#                                                            ###
# ##############################################################
'''


import wx
from wx.lib.agw import customtreectrl as CT, aui

from imgs.itree import iopen, iopened, iclose, \
    iview_package_open, iview_package_close, iview_pack
from wrapper.view import TView, TViewWelCome


KURI_AUI_NB_STYLE = aui.AUI_NB_TOP | aui.AUI_NB_TAB_SPLIT | \
    aui.AUI_NB_TAB_MOVE | aui.AUI_NB_SCROLL_BUTTONS |\
    aui.AUI_NB_CLOSE_BUTTON | aui.AUI_NB_DRAW_DND_TAB


class CentralPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.v_setting()

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)

        self.v_content()

    def v_setting(self):
        self.SetBackgroundColour("#3B598D")

    def v_content(self):

        self.nb_main = aui.AuiNotebook(self)
        self.nb_main.SetArtProvider(aui.ChromeTabArt())
        # self.nb_main.SetAGWWindowStyleFlag(KURI_AUI_NB_STYLE)

        self.nb_main.AddPage(TViewWelCome(self.nb_main), "Welcome to Tava")
        self.nb_main.AddPage(TView(self.nb_main), "Prueba Matplotlib")

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.nb_main, 1,
                       wx.LEFT | wx.TOP | wx.EXPAND | wx.ALL, 1)
        self.SetSizer(self.sizer)
        self.Fit()


class TTree(CT.CustomTreeCtrl):

    def __init__(self, parent):
        CT.CustomTreeCtrl.__init__(self, parent)

        self.v_setting()

        self.v_content()

    def v_setting(self):
        # self.SetBackgroundColour("red")
        self.SetSize(wx.Size(220, -1))
        self.SetAGWWindowStyleFlag(CT.TR_HAS_BUTTONS | CT.TR_HIDE_ROOT)

    def v_content(self):

        img_list = wx.ImageList(16, 16)
        img_list.Add(iopen.GetBitmap())
        img_list.Add(iopened.GetBitmap())
        img_list.Add(iclose.GetBitmap())

        img_list.Add(iview_package_close.GetBitmap())
        img_list.Add(iview_package_open.GetBitmap())

        img_list.Add(iview_pack.GetBitmap())

        self.AssignImageList(img_list)

        self.root = self.AddRoot("TAVA TREE PROJECT", 0)
        self.add_projects()

        pass

    def add_projects(self):
        for _ in range(1):
            project_item = self.AppendItem(self.root, 'Proyecto 1')
            self.SetItemImage(project_item, 0, wx.TreeItemIcon_Normal)
            self.SetItemImage(project_item, 1, wx.TreeItemIcon_Expanded)
            self.SetItemTextColour(project_item, '#000000')
            self._expanded(project_item, True)

            packege_file = self.AppendItem(project_item, 'Archivos')
            self.SetItemImage(packege_file, 3, wx.TreeItemIcon_Normal)
            self.SetItemImage(packege_file, 4, wx.TreeItemIcon_Expanded)
            self._expanded(packege_file, True)

            self.AppendItem(packege_file, 'name File o')
            self.AppendItem(packege_file, 'name File 1')

            packege_view = self.AppendItem(project_item, 'Vistas')
            self.SetItemImage(packege_view, 5, wx.TreeItemIcon_Normal)
            self._expanded(packege_view, True)

            self.AppendItem(packege_view, 'vista 1')
            self.AppendItem(packege_view, 'vista 2')

    def _expanded(self, item, expand=True):
        if expand:
            item.Expand()
        else:
            item.Collapse()
