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

from imgs.itree import iopen, iopened, iclose, ipackage_open, ipackage_opened,\
    imoduleg, iview_package_open, iview_package_close


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


class TTree(CT.CustomTreeCtrl):

    def __init__(self, parent):
        CT.CustomTreeCtrl.__init__(self, parent)

        self.v_setting()

        self.v_content()

    def v_setting(self):
        self.SetBackgroundColour("red")
        self.SetSize(wx.Size(220, -1))
        self.SetAGWWindowStyleFlag(CT.TR_HAS_BUTTONS | CT.TR_HIDE_ROOT)

    def v_content(self):

        img_list = wx.ImageList(16, 16)
        img_list.Add(iopen.GetBitmap())
        img_list.Add(iopened.GetBitmap())
        img_list.Add(iclose.GetBitmap())
        img_list.Add(ipackage_open.GetBitmap())
        img_list.Add(ipackage_opened.GetBitmap())
        img_list.Add(imoduleg.GetBitmap())
        img_list.Add(iview_package_open.GetBitmap())
        img_list.Add(iview_package_close.GetBitmap())

        self.AssignImageList(img_list)

        self.root = self.AddRoot("TAVA TREE PROJECT", 0)
        pass
