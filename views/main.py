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

from wx import GetTranslation as L
import wx
from wx.lib.agw import aui
from wx.lib.pubsub import Publisher as pub

from bd import entity
from imgs.itree import explorer
from imgs.prin import shortcut, splash
from languages import topic as T
from languages.i18n import I18nLocale
from views.wrapper.tbody import TTree, CentralPanel
from views.wrapper.tmenubar import TMenuBar
from views.wrapper.ttoolbar import TToolBar
from views.wrapper.vproject.new import NewProject
from presenters.pmain import MainFrameP


class MainFrame(wx.Frame):

    def __init__(self, parent=None):
        wx.Frame.__init__(self, parent)

        self.v_setting()

        self.sizer = wx.BoxSizer()
        self.SetSizer(self.sizer)

        self.v_content()

        self.ppr = MainFrameP(self)

    def v_setting(self):
        self.SetTitle("FPUNA: Tavai")
        self.SetSize(wx.Size(800, 700))
        self.SetBackgroundColour("#F5D0A9")
        self.SetMinSize((660, 480))
        self.SetIcon(shortcut.GetIcon())
        self.Center(wx.BOTH)

    def v_content(self):

        # configuración de lenguajes
        self.i18n = I18nLocale()

        # aui que manejará los paneles principales
        self._mgr = aui.AuiManager(self, aui.AUI_MGR_ANIMATE_FRAMES)

        # add Menu Bar
        self.menu_bar = TMenuBar(self)
        self.SetMenuBar(self.menu_bar)

        self.build_panels()
        pass

    def build_panels(self):

        # Agrega los Toolbar
        self.ttoolbar = TToolBar(self)
        self._mgr.AddPane(self.ttoolbar, aui.AuiPaneInfo().Name("tb1").
                          Caption("Big Toolbar").ToolbarPane().Top())

        # tree panel
        self._mgr.AddPane(TTree(self),
                          aui.AuiPaneInfo().Name("tree_pane").
                          Icon(explorer.GetBitmap()).
                          Caption(L('PROJECT_EXPLORER')).
                          Left().Layer(1).Position(1).CloseButton(False).
                          MaximizeButton(True).MinimizeButton(True).
                          Floatable(False))

        # Panel central
        self._mgr.AddPane(CentralPanel(self), aui.AuiPaneInfo().
                          Name("space_work_pane").CenterPane())
        self._mgr.Update()

    def on_exit(self, event):
        self.Close()

    def change_language(self, language):
        if not self.i18n.isEnUsLanguage() and language == 'en':
            self.i18n.OnEnUs()
            self.update_language()
            pub().sendMessage(T.LANGUAGE_CHANGED)

        if not self.i18n.isEsPyLanguage() and language == 'es':
            self.i18n.OnEsPy()
            self.update_language()
            pub().sendMessage(T.LANGUAGE_CHANGED)

    def update_language(self):
        self._mgr.GetPaneByName("tree_pane").Caption(L('PROJECT_EXPLORER'))
        self._mgr.RefreshCaptions()
        self.menu_bar.SetLabelsLanguges()
        self.ttoolbar.SetLabelsLanguges()

    # ------------- funciones logicas ---------------------

    def new_project(self):
        self.p_name = ''
        self.p_path_files = []
        self.p_formate = 10
        self.p_create = False

        NewProject(self)
        project = self.ppr.add_project(self.p_name, self.p_path_files,
                                       self.p_formate)

        print 'Se agregó un nuevo proyecto'
        print project.id
        print project.name


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
        entity.createDB()
        frame = MainFrame(None)
        frame.Center(wx.BOTH)
        frame.Show()

        if self.fc.IsRunning():
            self.Raise()
