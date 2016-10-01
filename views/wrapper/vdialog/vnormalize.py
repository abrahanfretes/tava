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


class FilterClustersDialog(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, size=(700, 630))

        self.parent = parent

        # ---- titulo de cabecera
        title_sizer = wx.BoxSizer(wx.VERTICAL)
        title = wx.StaticText(self, label='Filtro de Datos')
        title_line = wx.StaticLine(self)
        title_sizer.Add(title, 0, wx.CENTER | wx.TOP, 10)
        title_sizer.Add(title_line, 0, wx.EXPAND | wx.RIGHT | wx.LEFT, 5)

        # ---- panel de datos
        b_panel = wx.Panel(self, -1)
        self.radio1 = wx.RadioButton(b_panel, -1, " Todos los clusters.",
                                style=wx.RB_GROUP)
        self.radio2 = wx.RadioButton(b_panel, -1, "Clusters más representativos.")

        # ---- Configuración de Clusters
        _count_clus = 10
        self.first_repre = wx.SpinCtrl(b_panel, 1, "", (30, 50))
        self.first_repre.SetRange(1, _count_clus)
        self.first_repre.SetValue(1)

        # Layout controls on panel:
        vs = wx.BoxSizer(wx.VERTICAL)
        vs.Add(self.radio1)
        vs.Add(self.radio2)
        vs.Add(self.first_repre)
        b_panel.SetSizer(vs)
        vs.Fit(b_panel)

        # ---- button para controls
        b_sizer = wx.BoxSizer(wx.HORIZONTAL)
        cancel = wx.Button(self, label='Cancelar', size=(125, 32))
        cancel.Bind(wx.EVT_BUTTON, self.on_cancel)
        self.accept = wx.Button(self, label='Aceptar', size=(125, 32))
        self.accept.Bind(wx.EVT_BUTTON, self.on_accept)
        b_sizer.Add(cancel)
        b_sizer.Add(self.accept)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(title_sizer, 0, wx.EXPAND | wx.BOTTOM, 10)
        sizer.Add(b_panel)
        sizer.Add(b_sizer)
        self.SetSizer(sizer)

        self.Centre()
        self.ShowModal()

    def on_cancel(self, event):
        self.Close()

    def on_accept(self, event):
        a = SelectedData()
        if self.radio1.GetValue():
            a.option = 0
        else:
            a.option = 1
            a.more_repre = self.first_repre.GetValue()

        self.parent.data_selected = a
        self.Close()


class SelectedData():
    def __init__(self):
        self.option = None
        self.more_repre = None
