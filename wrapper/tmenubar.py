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


class TMenuBar(wx.MenuBar):

    def __init__(self, parent):
        wx.MenuBar.__init__(self)

        # ---- Menu File ---------------------
        file_menu = wx.Menu()
        self.Append(file_menu, 'File')

        # menu items - menu file
        self.exit = wx.MenuItem(file_menu, wx.ID_EXIT)

        # add menu to item
        file_menu.AppendItem(self.exit)

        # add labels to menu
        self.exit.SetText('&' + 'Salir' + '\tCtrl+Q')

        # add events
        file_menu.Bind(wx.EVT_MENU, parent.on_exit, id=wx.ID_EXIT)
