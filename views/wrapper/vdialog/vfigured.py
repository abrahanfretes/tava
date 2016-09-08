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
# Creado:  8/9/2016                                          ###
#                                                            ###
# ##############################################################
'''

import wx


class DataConfig(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, size=(600, 500),
                           title='Configuracion de Grafico')

        self.parent = parent

        sizer = wx.BoxSizer(wx.VERTICAL)

        _nor = wx.CheckBox(self, -1, "Datos Normalizados")
        _nor.SetValue(self.parent.normalized)
        _nor.Bind(wx.EVT_CHECKBOX, self.on_normalized)
        sizer.Add(_nor, flag=wx.ALIGN_CENTER_VERTICAL)

        _dup = wx.RadioBox(self, label='Allow Duplicates?',
                           choices=['True', 'False', 'Only'])
        _dup.SetSelection(self.parent.duplicate_true)
        _dup.Bind(wx.EVT_RADIOBOX, self.on_duplicate)
        sizer.Add(_dup, flag=wx.ALIGN_CENTER_VERTICAL)

        sl1 = wx.StaticLine(self, -1, style=wx.LI_HORIZONTAL)
        sizer.Add(sl1, flag=wx.EXPAND)

        _kplot = wx.RadioBox(self, label='Plots',
                             choices=['One', 'Block'])
        _kplot.SetSelection(self.parent.k_plot)
        _kplot.Bind(wx.EVT_RADIOBOX, self.on_k_plot)
        sizer.Add(_kplot, flag=wx.ALIGN_CENTER_VERTICAL)

        # buttons confirmar, cancelar
        sizer_button = wx.BoxSizer(wx.HORIZONTAL)
        sizer_cancel = wx.BoxSizer()
        self.cancel = wx.Button(self, -1, 'Cancelar')
        self.cancel.SetDefault()
        sizer_cancel.Add(self.cancel)
        sizer_apply = wx.BoxSizer()
        self.apply = wx.Button(self, -1, 'Aceptar')
        sizer_apply.Add(self.apply, 0, wx.ALIGN_RIGHT)

        sizer_button.Add(sizer_cancel, 0, wx.ALL, 5)
        sizer_button.Add(sizer_apply, 0, wx.ALL, 5)
        sizer.Add(sizer_button, 0, wx.EXPAND | wx.LEFT, 100)

        self.Bind(wx.EVT_BUTTON, self.on_button_apply, self.apply)
        self.Bind(wx.EVT_BUTTON, self.on_button_cancel, self.cancel)

        self.SetSizer(sizer)
        self.CenterOnScreen()
        self.ShowModal()

    def on_button_cancel(self, event):
        self.Close()

    def on_button_apply(self, event):
        self.Close()

    def on_key_escape(self, event):
        if event.GetKeyCode() == wx.WXK_ESCAPE:
            self.Close()

    def on_duplicate(self, event):
        self.parent.duplicate_true = event.GetSelection()

    def on_normalized(self, event):
        self.parent.normalized = event.IsChecked()

    def on_k_plot(self, event):
        self.parent.k_plot = event.GetSelection()
