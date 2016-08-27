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
# Creado:  26/8/2016                                         ###
#                                                            ###
# ##############################################################
'''

import wx

from main import MainFrame


class TavaiApp(wx.App):

    def OnInit(self):
        frame = MainFrame(None)
        self.SetTopWindow(frame)
        print "Print statements go to this stdout window by default."
        frame.Center(wx.BOTH)
        # frame.Maximize()
        frame.Show(True)
        return True

app = TavaiApp(redirect=False)
app.MainLoop()
