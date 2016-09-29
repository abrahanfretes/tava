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
# Creado:  28/9/2016                                         ###
#                                                            ###
# ##############################################################
'''
import wx


class NormalizeDialog(wx.Dialog):
    def __init__(self, parent, current):
        wx.Dialog.__init__(self, parent, size=(700, 630))
        self.current = current
        self.parent = parent

        self.rb_nor = wx.RadioBox(self, -1, "Normalizadores disponibles",
                                  choices=self.g_normal(),
                                  majorDimension=2,
                                  style=wx.RA_SPECIFY_COLS | wx.RA_HORIZONTAL
                                  )
        self.rb_nor.SetSelection(current)
        self.rb_nor.Bind(wx.EVT_RADIOBOX, self.on_change)

        cancel = wx.Button(self,
                           label='Cancelar', size=(125, 32))

        self.accept = wx.Button(self,
                                label='Aceptar', size=(125, 32))
        self.accept.Disable()

        cancel.Bind(wx.EVT_BUTTON, self.on_cancel)
        self.accept.Bind(wx.EVT_BUTTON, self.on_accept)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.rb_nor)
        sizer.Add(cancel)
        sizer.Add(self.accept)

        self.SetSizer(sizer)

        self.Centre()
        self.ShowModal()

    def g_normal(self):
        return ['Observación', 'Ninguno', 'Objetivo']

    def on_cancel(self, event):
        self.Close()

    def on_accept(self, event):
        self.parent.current_nor = self.rb_nor.GetSelection()
        label = self.parent.nor_label.GetLabel().split(':')[0]
        new_label = label + ': ' + self.rb_nor.GetStringSelection()
        self.parent.nor_label.SetLabel(new_label)
        self.Close()

    def on_change(self, event):
        self.accept.Disable()
        if self.current != event.GetSelection():
            self.accept.Enable()
