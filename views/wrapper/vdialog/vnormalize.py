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
        self.parent.normalization = self.rb_nor.GetSelection()
        label = self.parent.nor_label.GetLabel().split(':')[0]
        new_label = label + ': ' + self.rb_nor.GetStringSelection()
        self.parent.nor_label.SetLabel(new_label)
        self.Close()

    def on_change(self, event):
        self.accept.Disable()
        if self.current != event.GetSelection():
            self.accept.Enable()


class FilterClustersDialog(wx.Dialog):
    def __init__(self, parent, data):
        wx.Dialog.__init__(self, parent, size=(700, 630))

        self.parent = parent
        self.data = data

        # ---- titulo de cabecera
        title_sizer = wx.BoxSizer(wx.VERTICAL)
        title = wx.StaticText(self, label='Filtro de Datos')
        title_line = wx.StaticLine(self)
        title_sizer.Add(title, 0, wx.CENTER | wx.TOP, 10)
        title_sizer.Add(title_line, 0, wx.EXPAND | wx.RIGHT | wx.LEFT, 5)

        # ---- panel de datos
        b_panel = wx.Panel(self, -1)

        # ---- selección de todos los clusters
        label = "Todos los clusters."
        self.radio1 = wx.RadioButton(b_panel, -1, label, style=wx.RB_GROUP)

        # ---- selección de todos clusters más representativos
        label = "Clusters más representativos."
        self.radio2 = wx.RadioButton(b_panel, -1, label)
        self.first_repre = wx.SpinCtrl(b_panel, 1, "", (30, 50))
        self.first_repre.SetRange(1, data.count_tendency)
        self.first_repre.SetValue(data.more_repre)

        # ---- selección de todos clusters menos representativos
        label = "Clusters menos representativos."
        self.radio3 = wx.RadioButton(b_panel, -1, label)
        self.less_repre = wx.SpinCtrl(b_panel, 1, "", (30, 50))
        self.less_repre.SetRange(1, data.count_tendency)
        self.less_repre.SetValue(data.less_repre)

        # ---- selección de clusters respecto a objetivos
        label = "Clusters representativos respecto a los Objetivos."
        self.radio4 = wx.RadioButton(b_panel, -1, label)
        sizer_lb = wx.BoxSizer(wx.HORIZONTAL)

        sizer_lb1 = wx.BoxSizer(wx.VERTICAL)
        lb1_label = wx.StaticText(b_panel, -1, "Valores Mayores:")
        lb1_label.SetFont(wx.FFont(15, wx.SWISS, wx.FONTFLAG_BOLD))
        self.lb1 = wx.CheckListBox(b_panel, choices=data.max_objetives)
        sizer_lb1.Add(lb1_label, flag=wx.ALL, border=2)
        sizer_lb1.Add(self.lb1, flag=wx.ALL, border=2)

        sizer_lb2 = wx.BoxSizer(wx.VERTICAL)
        lb2_label = wx.StaticText(b_panel, -1, "Valores Mayores:")
        lb2_label.SetFont(wx.FFont(15, wx.SWISS, wx.FONTFLAG_BOLD))
        # self.Bind(wx.EVT_LISTBOX, self.EvtListBox, lb1)
        self.lb2 = wx.CheckListBox(b_panel, choices=data.max_objetives)
        # self.Bind(wx.EVT_LISTBOX, self.EvtListBox, lb2)
        sizer_lb2.Add(lb2_label, flag=wx.ALL, border=2)
        sizer_lb2.Add(self.lb2, flag=wx.ALL, border=2)

        sizer_lb.Add(sizer_lb1)
        sizer_lb.Add(sizer_lb2)

        # Layout controls on panel:
        vs = wx.BoxSizer(wx.VERTICAL)
        vs.Add(self.radio1)
        vs.Add(self.radio2)
        vs.Add(self.first_repre)
        vs.Add(self.radio3)
        vs.Add(self.less_repre)
        vs.Add(self.radio4)
        vs.Add(sizer_lb, flag=wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, border=5)
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

        self._init_value(data)
        self.Centre()
        self.ShowModal()

    def _init_value(self, data):
        if data.option == 0:
            self.radio1.SetValue(True)
        elif data.option == 1:
            self.radio2.SetValue(True)
            self.first_repre.SetValue(data.more_repre)
        elif data.option == 2:
            self.radio3.SetValue(True)
            self.less_repre.SetValue(data.less_repre)
        elif data.option == 3:
            self.radio4.SetValue(True)
            self.lb1.SetChecked(data.max_objetives_use)
            self.lb2.SetChecked(data.min_objetives_use)

    def on_cancel(self, event):
        self.parent.data_selected.cancel = True
        self.Close()

    def on_accept(self, event):
        # a = SelectedData()
        self.parent.data_selected.max_repre = self.first_repre.GetMax()

        if self.radio1.GetValue():
            self.parent.data_selected.option = 0
        elif self.radio2.GetValue():
            self.parent.data_selected.option = 1
            self.parent.data_selected.more_repre = self.first_repre.GetValue()
        elif self.radio3.GetValue():
            self.parent.data_selected.option = 2
            self.parent.data_selected.less_repre = self.less_repre.GetValue()
        elif self.radio4.GetValue():
            self.parent.data_selected.option = 3
            self.parent.data_selected.max_objetives_use = self.lb1.GetChecked()
            self.parent.data_selected.min_objetives_use = self.lb2.GetChecked()

        self.Close()


class SelectedData():
    def __init__(self):

        # ---- opción seleccionado
        self.option = None

        # ---- cantidad de tendencias existentes
        self.count_tendency = None

        # ---- más representivos
        self.more_repre = None

        # ---- menos representativos
        self.less_repre = None

        # ----  cancelar la selección
        self.cancel = False

        # ---- valores de objetivos mayores
        self.max_objetives = []
        self.max_objetives_use = []
        self.min_objetives_use = []
