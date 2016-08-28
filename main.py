#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
# ##############################################################
#                                                            ###
# Universidad Nacional de Asunción - Facultad Politécnica    ###
# Ingenieria en Informática - Proyecto Final de Grado        ###
#                                                            ###
# Autores:                                                   ###
#           - Arsenio Ferreira (arse.ferreira@gmail.com)      ###
#           - Abrahan Fretes (abrahan.fretes@gmail.com)      ###
#                                                            ###
# Creado:  26/8/2016                                          ###
#                                                            ###
# ##############################################################
'''

import wx
from wx.lib.agw import aui
from wx.lib.agw import customtreectrl as CT
from imgs.prin import shortcut, splash


class MainFrame(wx.Frame):

    def __init__(self, parent=None):
        wx.Frame.__init__(self, parent)

        self.v_setting()

        self.sizer = wx.BoxSizer()
        self.SetSizer(self.sizer)

        self.v_content()

    def v_setting(self):
        self.SetTitle("FPUNA: Tavai")
        self.SetSize(wx.Size(800, 700))
        self.SetBackgroundColour("#F5D0A9")
        self.SetMinSize((660, 480))
        self.SetIcon(shortcut.GetIcon())
        self.Center(wx.BOTH)

    def v_content(self):

        # aui que manejará los paneles principales
        self._mgr = aui.AuiManager(self, aui.AUI_MGR_ANIMATE_FRAMES)
        self.build_panels()
        pass

    def build_panels(self):

        # tree panel
        self._mgr.AddPane(TreePanel(self),
                          aui.AuiPaneInfo().Name("tree_pane").
                          Left().Layer(1).Position(1).CloseButton(False).
                          MaximizeButton(True).MinimizeButton(True).
                          Floatable(False))

        # Panel central
        self._mgr.AddPane(CentralPanel(self), aui.AuiPaneInfo().
                          Name("space_work_pane").CenterPane())
        self._mgr.Update()


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


class TreePanel(CT.CustomTreeCtrl):
    def __init__(self, parent):
        CT.CustomTreeCtrl.__init__(self, parent)

        self.v_setting()

        self.v_content()

    def v_setting(self):
        self.SetBackgroundColour("red")
        self.SetSize(wx.Size(220, -1))
        self.SetAGWWindowStyleFlag(CT.TR_HAS_BUTTONS | CT.TR_HIDE_ROOT)

    def v_content(self):
        self.root = self.AddRoot("TAVA TREE PROJECT", 0)
        pass


class SplashFrame(wx.SplashScreen):

    def __init__(self):
        wx.SplashScreen.__init__(self, splash.GetBitmap(),
                                 wx.SPLASH_CENTRE_ON_SCREEN |
                                 wx.SPLASH_TIMEOUT, 5000, None, -1)

        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.fc = wx.FutureCall(2000, self.ShowMain)

    def OnClose(self, evt):
        evt.Skip()
        self.Hide()
        if self.fc.IsRunning():
            self.fc.Stop()
            self.ShowMain()

    def ShowMain(self):
        frame = MainFrame(None)
        frame.Center(wx.BOTH)
        frame.Show()

        if self.fc.IsRunning():
            self.Raise()
