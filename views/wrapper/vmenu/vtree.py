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
# Creado:  31/8/2016                                         ###
#                                                            ###
# ##############################################################
'''

import wx
from wx.lib.pubsub import Publisher as pub
from languages import topic as T
from wx import GetTranslation as L


# ------ menu para paquete de vistas -------------------------------------
class MenuPackageView(wx.Menu):
    '''
    Clase Menu que estará contenida en un contextMenu de la entidad proyecto
    '''
    def __init__(self, parent, project):
        wx.Menu.__init__(self)

        # ------ definiciones iniciales ---------------------------------------
        self.project = project
        self.init_ui()
        # ---------------------------------------------------------------------

    def init_ui(self):

        # ------ items projects ----------------------------------------

        # -- add result
        self.add = wx.MenuItem(self, wx.ID_ANY, L('MENU_VIEW_CREATE'))
        self.AppendItem(self.add)
        self.Bind(wx.EVT_MENU, self.on_create, self.add)

    def on_create(self, event):
        pub().sendMessage(T.CREATE_VIEW, self.project)
        pass


# ------ menu para vistas -------------------------------------
class MenuVista(wx.Menu):
    '''
    Clase Menu que estará contenida en un contextMenu de la entidad proyecto
    '''
    def __init__(self, parent, view):
        wx.Menu.__init__(self)

        # ------ definiciones iniciales ---------------------------------------
        self.view = view
        self.parent = parent
        self.init_ui()
        # ---------------------------------------------------------------------

    def init_ui(self):

        # ------ items projects ----------------------------------------
        self.AppendSeparator()

        # -- ver View
        self.open = wx.MenuItem(self, wx.ID_ANY, L('MENU_VIEW_OPEN'))
        self.AppendItem(self.open)
        self.Bind(wx.EVT_MENU, self.on_open, self.open)

        self.AppendSeparator()

        # -- delete view
        self.delete = wx.MenuItem(self, wx.ID_ANY, L('MENU_VIEW_DELETE'))
        self.AppendItem(self.delete)
        self.Bind(wx.EVT_MENU, self.on_delete, self.delete)

        self.AppendSeparator()

    def on_open(self, event):
        pub().sendMessage(T.SHOW_SELECTED_VIEW, self.parent.c_data[0])
        pass

    def on_delete(self, event):
        # self.parent.delete_item_selected()
        # pub().sendMessage(T.DELETE_VIEW, self.view)
        pass