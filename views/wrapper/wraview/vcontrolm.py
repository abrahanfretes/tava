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
# Creado:  1/9/2016                                        ###
#                                                            ###
# ##############################################################
'''

import wx
from wx.lib.agw.genericmessagedialog import GenericMessageDialog
from wx.lib.agw.genericmessagedialog import GMD_USE_GRADIENTBUTTONS


H_EMPTY_DATA_SELECTED = 'Selección Vacío de Datos'
EMPTY_DATA_SELECTED = "Selección de datos para Visualizar.\n\n" + \
    "No has seleccionado ninguna opción de \n" + \
    "Datos para Visualizar, checkee algunas de\n" + \
    "las casillas disponibles en la parte\n" + \
    'superior derecha "Datas" o "Clusters".\n\n' + \
    "            TAVA-TOOL  "

H_EMPTY_DUPLICATE_DATA = 'Datos duplicados'
EMPTY_DUPLICATE_DATA = "Los Datos no están duplicados.\n\n" + \
    "Los items seleccionados no contienes datos\n" + \
    "duplicados, seleccione otros items o cambie el\n" + \
    'modo de visualización a "True" o "False"\n' + \
    'en la opción "Allow Duplicates?".\n\n' + \
    "            TAVA-TOOL  "


KMSG_EMPTY_DATA_SELECTED = 0
KMSG_EMPTY_DUPLICATE_DATA = 1


K_ICON_INFORMATION = wx.ICON_INFORMATION
K_ICON_QUESTION = wx.ICON_QUESTION
K_ICON_ERROR = wx.ICON_ERROR
K_ICON_HAND = wx.ICON_HAND
K_ICON_EXCLAMATION = wx.ICON_EXCLAMATION

K_OK = wx.OK
K_CANCEL = wx.CANCEL
K_YES_NO = wx.YES_NO
K_YES_DEFAULT = wx.YES_DEFAULT
K_NO_DEFAULT = wx.NO_DEFAULT


class KMessage():

    def __init__(self, parent, key_message, key_ico=K_ICON_INFORMATION,
                 key_button=K_OK):

        self.parent = parent

        if key_message == KMSG_EMPTY_DATA_SELECTED:
            self.h_msg = H_EMPTY_DATA_SELECTED
            self.m_msg = EMPTY_DATA_SELECTED
            self.k_ico = key_ico
            self.k_but = key_button
        elif key_message == KMSG_EMPTY_DUPLICATE_DATA:
            self.h_msg = H_EMPTY_DUPLICATE_DATA
            self.m_msg = EMPTY_DUPLICATE_DATA
            self.k_ico = key_ico
            self.k_but = key_button
        else:
            self.h_msg = 'Defaul'
            self.m_msg = 'Defaul'
            self.k_ico = key_ico
            self.k_but = key_button

    def kshow(self):
        dlg = GenericMessageDialog(self.parent, self.m_msg,
                                   self.h_msg,
                                   self.k_ico | self.k_but |
                                   GMD_USE_GRADIENTBUTTONS)
        dlg.ShowModal()
        dlg.Destroy()
