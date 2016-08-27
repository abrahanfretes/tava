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

    def v_content(self):
        self.panel = MainPanel(self)
        self.sizer.Add(self.panel, 1, wx.EXPAND | wx.ALL, 3)


class MainPanel(wx.Panel):
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
