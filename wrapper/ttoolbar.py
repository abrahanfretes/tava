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
from wx.lib.agw import aui
from imgs.itollbar import inew, iopen, iclose, idelete, iunhide, ihide


class TToolBar(aui.AuiToolBar):

    def __init__(self, parent):
        aui.AuiToolBar.__init__(self, parent, -1, wx.DefaultPosition,
                                wx.DefaultSize,
                                agwStyle=aui.AUI_TB_DEFAULT_STYLE |
                                aui.AUI_TB_OVERFLOW)

        self.SetToolBitmapSize(wx.Size(48, 48))
        self.SetIdReferences()

        # --- item de proyecto
        self.AddSimpleTool(self.ID_NEW_PRO, '', inew.GetBitmap())
        self.AddSimpleTool(self.ID_OPEN_PRO, '', iopen.GetBitmap())
        self.AddSimpleTool(self.ID_CLOSE_PRO, '', iclose.GetBitmap())
        self.AddSimpleTool(self.ID_DEL_PRO, '', idelete.GetBitmap())
        self.AddSeparator()
        self.AddSimpleTool(self.ID_HIDE_PRO, '', iunhide.GetBitmap())
        self.AddSimpleTool(self.ID_UNHIDE_PRO, '', ihide.GetBitmap())

    def SetIdReferences(self):
        self.ID_NEW_PRO = wx.NewId()
        self.ID_OPEN_PRO = wx.NewId()
        self.ID_CLOSE_PRO = wx.NewId()
        self.ID_DEL_PRO = wx.NewId()
        self.ID_BLOG_PRO = wx.NewId()
        self.ID_EXIT_PRO = wx.NewId()
        self.ID_HIDE_PRO = wx.NewId()
        self.ID_UNHIDE_PRO = wx.NewId()
        self.ID_EXIT_PRO = wx.NewId()
