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


class FilterClusterDialog(wx.Dialog):
    def __init__(self, parent, data):
        wx.Dialog.__init__(self, parent, title="Cluster Filter",
                                                            size=(400, 360))
        self.SetBackgroundColour(wx.Colour(255, 255, 255))

        self.parent = parent
        self.data = data

        sboxs_fc = self.set_filter_config()

        line = self.get_line()

        sbuttons = self.set_buttons()

        vsizer = wx.BoxSizer(wx.VERTICAL)

        vsizer.Add(sboxs_fc, 0, wx.EXPAND | wx.ALL, 7)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(vsizer, 0, wx.EXPAND)
        sizer.Add(line, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.RIGHT |
                                                                wx.TOP, 5)
        sizer.Add(sbuttons, flag=wx.ALIGN_RIGHT | wx.TOP | wx.BOTTOM,
                  border=10)

        self.SetSizer(sizer)

        self.ShowModal()

    def on_cancel(self, event):
        self.parent.data_selected.cancel = True
        self.Close()

    def on_accept(self, event):
        self.parent.data_selected.max_repre = self.more_repre.GetMax()
        selection = self.parent.data_selected.option
        if selection == 0:
            self.parent.data_selected.more_repre = self.more_repre.GetValue()
        elif selection == 1:
            self.parent.data_selected.less_repre = self.less_repre.GetValue()
        elif selection == 2:
            self.parent.data_selected.max_objetives_use = self.lb1.GetChecked()
            self.parent.data_selected.min_objetives_use = self.lb2.GetChecked()
        self.Close()

    def get_line(self):
        line = wx.StaticLine(self, -1, size=(20, -1), style=wx.LI_HORIZONTAL)
        return line

    def set_buttons(self):
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        ok_button = wx.Button(self, label='Aceptar')
        ok_button.SetDefault()

        close_button = wx.Button(self, label='Cancelar')

        ok_button.Bind(wx.EVT_BUTTON, self.on_accept)

        close_button.Bind(wx.EVT_BUTTON, self.on_cancel)

        hbox.Add(close_button)
        hbox.Add(ok_button, flag=wx.RIGHT, border=5)

        return hbox

    def set_filter_config(self):
        sbox_fc = wx.StaticBox(self, -1, "Configuración de Filtro")
        sboxs_fc = wx.StaticBoxSizer(sbox_fc, wx.HORIZONTAL)

        p = wx.Panel(self)
        nb = wx.Choicebook(p, -1)

        nb.AddPage(self.get_more_representative(nb), "Clusters más " + \
                                                            "representativos")
        nb.AddPage(self.get_less_representative(nb), "Clusters menos " + \
                                                            "representativos")
        nb.AddPage(self.get_representative_per_obj(nb), "Clusters " + \
                                    "representativos respecto a los Objetivos")

        nb.Bind(wx.EVT_CHOICEBOOK_PAGE_CHANGED, self.on_page_changed)

        sizer = wx.BoxSizer()
        sizer.Add(nb, 1, wx.EXPAND | wx.EXPAND, 5)
        p.SetSizer(sizer)

        sboxs_fc.Add(p, 1, wx.ALL | wx.EXPAND, 5)
        return sboxs_fc

    def on_page_changed(self, e):
        self.parent.data_selected.option = e.GetSelection()

        e.Skip()

    def get_more_representative(self, parent):
        panel = wx.Panel(parent)

        sizer = wx.BoxSizer(wx.VERTICAL)

        grid = wx.FlexGridSizer(cols=2)

        label = wx.StaticText(panel, -1, "Establezca la cantidad:")

        self.more_repre = wx.SpinCtrl(panel, 1, "", (30, 50))
        self.more_repre.SetRange(1, self.data.count_tendency)
        self.more_repre.SetValue(self.data.more_repre)

        grid.Add(label, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL |
                                                                    wx.ALL, 5)
        grid.Add(self.more_repre, 0, wx.ALIGN_LEFT | wx.ALL, 5)

        sizer.Add(grid, 1, wx.EXPAND | wx.ALL, 10)

        panel.SetSizer(sizer)

        return panel

    def get_less_representative(self, parent):
        panel = wx.Panel(parent)

        sizer = wx.BoxSizer(wx.VERTICAL)

        grid = wx.FlexGridSizer(cols=2)

        label = wx.StaticText(panel, -1, "Establezca la cantidad:")

        self.less_repre = wx.SpinCtrl(panel, 1, "", (30, 50))
        self.less_repre.SetRange(1, self.data.count_tendency)
        self.less_repre.SetValue(self.data.more_repre)

        grid.Add(label, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL |
                                                                    wx.ALL, 5)
        grid.Add(self.less_repre, 0, wx.ALIGN_LEFT | wx.ALL, 5)

        sizer.Add(grid, 1, wx.EXPAND | wx.ALL, 10)

        panel.SetSizer(sizer)

        return panel

    def get_representative_per_obj(self, parent):
        panel = wx.Panel(parent)

        sizer = wx.BoxSizer(wx.VERTICAL)

        grid = wx.FlexGridSizer(cols=3)

        sizer_lb1 = wx.BoxSizer(wx.VERTICAL)
        lb1_label = wx.StaticText(panel, -1, "Valores Mayores:")
        pts = lb1_label.GetFont().GetPointSize()
        lb1_label.SetFont(wx.FFont(pts, wx.SWISS, wx.FONTFLAG_BOLD))
        self.lb1 = wx.CheckListBox(panel, choices=self.data.max_objetives)
        sizer_lb1.Add(lb1_label, flag=wx.ALL, border=2)
        sizer_lb1.Add(self.lb1, flag=wx.ALL | wx.EXPAND, border=5)

        sizer_lb2 = wx.BoxSizer(wx.VERTICAL)
        lb2_label = wx.StaticText(panel, -1, "Valores Menores:")
        pts = lb2_label.GetFont().GetPointSize()
        lb2_label.SetFont(wx.FFont(pts, wx.SWISS, wx.FONTFLAG_BOLD))
        self.lb2 = wx.CheckListBox(panel, choices=self.data.max_objetives)
        sizer_lb2.Add(lb2_label, flag=wx.ALL, border=2)
        sizer_lb2.Add(self.lb2, flag=wx.ALL | wx.EXPAND, border=5)

        grid.Add(sizer_lb1, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL |
                                                                    wx.ALL, 5)
        grid.Add(wx.StaticLine(panel, wx.ID_ANY, style=wx.LI_VERTICAL), 0,
                                                        wx.ALL | wx.EXPAND, 5)
        grid.Add(sizer_lb2, 0, wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL |
                                                                    wx.ALL, 5)

        sizer.Add(grid, 1, wx.EXPAND | wx.ALL, 10)

        panel.SetSizer(sizer)

        return panel


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


class Example(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(Example, self).__init__(*args, **kwargs)

        self.InitUI()

    def InitUI(self):

        self.SetSize((300, 200))
        self.SetTitle('About dialog box')
        self.Centre()
        self.Show(True)
        self.SetPosition((0, 0))

        data = SelectedData()
        data.count_tendency = 3
        data.more_repre = 2
        data.less_repre = 2
        FilterClusterDialog(self, data)


def main():

    ex = wx.App()
    Example(None)
    ex.MainLoop()


if __name__ == '__main__':
    main()
