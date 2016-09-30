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
    def __init__(self, parent, current):
        wx.Dialog.__init__(self, parent, size=(700, 630))
        self.current = current
        self.parent = parent

        # titulo
        title_sizer = wx.BoxSizer(wx.VERTICAL)
        title = wx.StaticText(self, label='Filtro de Datos')
        title_line = wx.StaticLine(self)
        title_sizer.Add(title, 0, wx.CENTER | wx.TOP, 10)
        title_sizer.Add(title_line, 0, wx.EXPAND | wx.RIGHT | wx.LEFT, 5)
        
        self.rb_nor = wx.RadioBox(self, -1, "",
                                  choices=self.g_normal(),
                                  majorDimension=1,
                                  style=wx.RA_SPECIFY_COLS | wx.RA_HORIZONTAL
                                  | wx.NO_BORDER)
        self.rb_nor.SetSelection(current)
        self.rb_nor.Bind(wx.EVT_RADIOBOX, self.on_change)

        cancel = wx.Button(self,
                           label='Cancelar', size=(125, 32))

        self.accept = wx.Button(self,
                                label='Aceptar', size=(125, 32))
        self.accept.Disable()

        cancel.Bind(wx.EVT_BUTTON, self.on_cancel)
        self.accept.Bind(wx.EVT_BUTTON, self.on_accept)


        # pruebas -------------------------------
        panel = wx.Panel( self, -1 )

        # 1st group of controls:
        self.group1_ctrls = []
        radio1 = wx.RadioButton( panel, -1, " all clusters ", style = wx.RB_GROUP )
        radio2 = wx.RadioButton( panel, -1, "representativos " )
        radio3 = wx.RadioButton( panel, -1, " Radio3 " )
        text1 = wx.TextCtrl( panel, -1, "" )
        text2 = wx.TextCtrl( panel, -1, "" )
        text3 = wx.TextCtrl( panel, -1, "" )
        self.group1_ctrls.append((radio1, text1))
        self.group1_ctrls.append((radio2, text2))
        self.group1_ctrls.append((radio3, text3))

        # Layout controls on panel:
        vs = wx.BoxSizer( wx.VERTICAL )

        box1_title = wx.StaticBox( panel, -1, "Group 1" )
        box1 = wx.StaticBoxSizer( box1_title, wx.VERTICAL )
        grid1 = wx.FlexGridSizer( cols=2 )

        for radio, text in self.group1_ctrls:
            grid1.Add( radio, 0, wx.ALIGN_CENTRE|wx.LEFT|wx.RIGHT|wx.TOP, 5 )
            grid1.Add( text, 0, wx.ALIGN_CENTRE|wx.LEFT|wx.RIGHT|wx.TOP, 5 )

        box1.Add( grid1, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )
        vs.Add( box1, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )

        panel.SetSizer( vs )
        vs.Fit( panel )
        panel.Move( (50,50) )
        # self.panel = panel

        for radio, text in self.group1_ctrls:
            radio.SetValue(0)
            text.Enable(False)

        # Setup event handling and initial state for controls:
        for radio, text in self.group1_ctrls:
            self.Bind(wx.EVT_RADIOBUTTON, self.OnGroup1Select, radio )

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(title_sizer, 0, wx.EXPAND | wx.BOTTOM, 10)
        sizer.Add(self.rb_nor)
        sizer.Add(cancel)
        sizer.Add(self.accept)
        sizer.Add(panel)

        self.SetSizer(sizer)

        self.Centre()
        self.ShowModal()

    def OnGroup1Select( self, event ):
        radio_selected = event.GetEventObject()

        for radio, text in self.group1_ctrls:
            if radio is radio_selected:
                text.Enable(True)
            else:
                text.Enable(False)

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
