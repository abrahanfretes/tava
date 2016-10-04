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
from wx.lib.agw import pyprogress as PP

from bd import entity
from imgs.itree import explorer
from imgs.prin import shortcut, splash
from languages import topic as T
from languages.i18n import I18nLocale
from views.wrapper.tbody import TTree, CentralPanel
from views.wrapper.tmenubar import TMenuBar
from views.wrapper.ttoolbar import TToolBar
from views.wrapper.vdialog.vproject import NewProject
from presenters.pmain import MainFrameP
from views.wrapper.vdialog.vview import ViewsTava


class MainFrame(wx.Frame):

    def __init__(self, parent=None):
        wx.Frame.__init__(self, parent)

        self.v_setting()

        # --- vistas
        pub().subscribe(self.new_view, T.CREATE_VIEW)
        pub.subscribe(self.delete_view, T.DELETE_VIEW)

        # ---- results
        pub.subscribe(self.new_results, T.NEW_RESULTS)
        pub.subscribe(self.delete_result, T.DELETE_RESULT)

        self.sizer = wx.BoxSizer()
        self.SetSizer(self.sizer)

        self.v_content()

        self.ppr = MainFrameP(self)

    def v_setting(self):
        self.SetTitle("FPUNA: Tavai")
        self.SetSize(wx.Size(1110, 700))
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
        if self.p_create:
            project = self.ppr.add_project(self.p_name)

            if self.p_path_files != []:
                style = wx.PD_APP_MODAL
                style |= wx.PD_CAN_ABORT

                dlg = PP.PyProgress(self, -1, L('MSG_PRO_HEADER_TITLE'),
                                    "                              :)",
                                    agwStyle=style)
                self.ppr.add_results_by_project(project,
                                                self.p_path_files,
                                                self.p_formate, dlg)

                dlg.Destroy()
                wx.SafeYield()
                wx.GetApp().GetTopWindow().Raise()

            pub().sendMessage(T.ADD_PROJECT_IN_TREE, project)

    def new_results(self, message):
        self.p_project = message.data
        self.p_path_files = []
        self.p_formate = 10
        self.p_create = False

        NewProject(self, True)
        if self.p_create:

            style = wx.PD_APP_MODAL
            style |= wx.PD_CAN_ABORT
            dlg = PP.PyProgress(self, -1, L('MSG_PRO_HEADER_TITLE'),
                                "                              :)",
                                agwStyle=style)

            results = self.ppr.add_results_by_project(self.p_project,
                                                      self.p_path_files,
                                                      self.p_formate, dlg)
            dlg.Destroy()
            wx.SafeYield()
            wx.GetApp().GetTopWindow().Raise()

            pub().sendMessage(T.ADD_RESULTS_IN_TREE, results)

    def delete_result(self, message):

        if self.ppr.contain_view(message.data.id):
            # ---- no se puede eliminar resultado, utilizado en vista
            dlg = wx.MessageDialog(self, L('RESULT_NOT_DELETE'),
                                   L('RESULT_NOT_DELETE_HEADER'),
                                   wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
        else:
            # --- elimina de la bd y envía mensaje de eliminación
            self.ppr.delete_result(message.data)
            pub().sendMessage(T.DELETE_RESULT_TREE)

    def new_view(self, message):
        project = message.data
        self.view_name = ''
        self.vews_results = []

        ViewsTava(self, project)
        if self.vews_results:
            view = self.ppr.add_views(self.view_name,
                                      self.vews_results, project)
            pub().sendMessage(T.ADD_VIEW_IN_TREE, view)

    def delete_view(self, message):
        self.ppr.delete_view(message.data)
        pub().sendMessage(T.DELETE_VIEW_TREE)


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
        wx.SafeYield()
        wx.GetApp().GetTopWindow().Raise()
