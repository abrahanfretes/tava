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
from wx.lib.agw import customtreectrl as CT

from imgs.itree import iopen, iopened, iclose, \
    iview_package_open, iview_package_close, iview_pack

from numpy import arange, sin, pi

import matplotlib
matplotlib.use('WXAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure


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
        wel = wx.StaticText(self, -1, "Your Welcome to Tavai :)")
        wel.SetForegroundColour((255, 255, 255))
        self.sizer.Add(wel, 0, wx.ALIGN_CENTRE)

        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        t = arange(0.0, 3.0, 0.01)
        s = sin(2 * pi * t)

        self.axes.plot(t, s)
        self.canvas = FigureCanvas(self, -1, self.figure)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.EXPAND)
        self.SetSizer(self.sizer)
        self.Fit()

        self.add_toolbar()  # comment this out for no toolbar

    def add_toolbar(self):
        self.toolbar = NavigationToolbar2Wx(self.canvas)
        self.toolbar.Realize()
        # By adding toolbar in sizer, we are able to put it at the bottom
        # of the frame - so appearance is closer to GTK version.
        self.sizer.Add(self.toolbar, 0, wx.LEFT | wx.EXPAND)
        # update the axes menu on the toolbar
        self.toolbar.update()


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
