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
from wx import GetTranslation as L


class TToolBar(aui.AuiToolBar):

    def __init__(self, parent):
        aui.AuiToolBar.__init__(self, parent, -1, wx.DefaultPosition,
                                wx.DefaultSize,
                                agwStyle=aui.AUI_TB_DEFAULT_STYLE |
                                aui.AUI_TB_OVERFLOW)
        self.parent = parent
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

        self.Bind(wx.EVT_TOOL, self.on_new_project, id=self.ID_NEW_PRO)

        # Establecemos los labels
        self.SetLabelsLanguges()

    def SetIdReferences(self):
        self.ID_NEW_PRO = wx.NewId()
        self.ID_OPEN_PRO = wx.NewId()
        self.ID_CLOSE_PRO = wx.NewId()
        self.ID_DEL_PRO = wx.NewId()
        self.ID_HIDE_PRO = wx.NewId()
        self.ID_UNHIDE_PRO = wx.NewId()

    def SetLabelsLanguges(self):
        self.SetToolShortHelp(self.ID_NEW_PRO, L('NEW_PROJECT'))
        self.SetToolShortHelp(self.ID_OPEN_PRO, L('OPEN_PROJECT'))
        self.SetToolShortHelp(self.ID_CLOSE_PRO, L('CLOSE_PROJECT'))
        self.SetToolShortHelp(self.ID_DEL_PRO, L('DELETE_PROJECT'))
        self.SetToolShortHelp(self.ID_HIDE_PRO, L('HIDE_PROJECT'))
        self.SetToolShortHelp(self.ID_UNHIDE_PRO, L('UNHIDE_PROJECT'))

    def on_new_project(self, event):
        self.parent.new_project()
