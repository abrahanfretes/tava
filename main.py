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

from imgs.itree import explorer
from imgs.prin import shortcut, splash
from wrapper.tbody import TreePanel, CentralPanel
from wrapper.tmenubar import TMenuBar


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

        # add Menu Bar
        self.SetMenuBar(TMenuBar(self))

        self.build_panels()
        pass

    def build_panels(self):

        # tree panel
        self._mgr.AddPane(TreePanel(self),
                          aui.AuiPaneInfo().Name("tree_pane").
                          Icon(explorer.GetBitmap()).
                          Caption('Explorador de Proyectos').
                          Left().Layer(1).Position(1).CloseButton(False).
                          MaximizeButton(True).MinimizeButton(True).
                          Floatable(False))

        # Panel central
        self._mgr.AddPane(CentralPanel(self), aui.AuiPaneInfo().
                          Name("space_work_pane").CenterPane())
        self._mgr.Update()

    def on_exit(self, event):
        self.Close()


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
