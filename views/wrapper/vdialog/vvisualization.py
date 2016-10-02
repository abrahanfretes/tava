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
# Creado:  01/10/2016                                        ###
#                                                            ###
# ##############################################################
'''
import wx

V_M_CLUSTER = 0
V_M_SUMMARY = 1
V_M_CLUSTER_SUMMARY = 2


class ClusterConfig(wx.Dialog):
    """
    Vista de configuración para la visualizacion de clusters.
    """

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, title="Cluster Config",
                                                    size=(400, 460))
        self.SetBackgroundColour(wx.Colour(255, 255, 255))

        sboxs_mv = self.set_visualization_mode()

        sboxs_lg = self.set_legend()

        sbuttons = self.set_buttons()

        line = self.get_line()

        msizer = wx.BoxSizer(wx.VERTICAL)

        msizer.Add(sboxs_mv, 0, wx.EXPAND | wx.ALL, 7)
        msizer.Add(sboxs_lg, 0, wx.EXPAND | wx.ALL, 7)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(msizer, 0, wx.EXPAND)
        sizer.Add(line, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.RIGHT |
                                                                wx.TOP, 5)
        sizer.Add(sbuttons, flag=wx.ALIGN_RIGHT | wx.TOP | wx.BOTTOM,
                  border=10)

        self.SetSizer(sizer)
        self.Show()

    def set_visualization_mode(self):
        sbox_mv = wx.StaticBox(self, -1, "Modo Visualización")
        sboxs_mv = wx.StaticBoxSizer(sbox_mv, wx.VERTICAL)

        self.radio1 = wx.RadioButton(self, -1, "Mostrar sólo Cluster",
                                style=wx.RB_GROUP)

        self.radio2 = wx.RadioButton(self, -1, "Mostrar sólo Resumen")
        self.radio2.SetValue(False)

        self.radio3 = wx.RadioButton(self, -1, "Mostrar Resumen y Cluster")
        self.radio3.SetValue(False)

        sboxs_mv.Add(self.radio1, 0, wx.ALL, 5)
        sboxs_mv.Add(self.radio2, 0, wx.ALL, 5)
        sboxs_mv.Add(self.radio3, 0, wx.ALL, 5)
        return sboxs_mv

    def set_legend(self):
        sbox_mv = wx.StaticBox(self, -1, "Leyenda")
        sboxs_mv = wx.StaticBoxSizer(sbox_mv, wx.VERTICAL)

        # Here we create a panel and a notebook on the panel
        p = wx.Panel(self)
        nb = wx.Notebook(p)

        # add the pages to the notebook with the label to show on the tab
        nb.AddPage(ClusterPage(nb, self), "Cluster")
        nb.AddPage(SummaryPage(nb, self), "Resumen")

        # finally, put the notebook in a sizer for the panel to manage
        # the layout
        sizer = wx.BoxSizer()
        sizer.Add(nb, 1, wx.EXPAND)
        p.SetSizer(sizer)

        sboxs_mv.Add(p, 0, wx.ALL | wx.EXPAND, 5)
        return sboxs_mv

    def set_buttons(self):
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        ok_button = wx.Button(self, label='Ok')
        ok_button.SetDefault()

        close_button = wx.Button(self, label='Close')

        ok_button.Bind(wx.EVT_BUTTON, self.on_close)

        close_button.Bind(wx.EVT_BUTTON, self.on_close)

        hbox.Add(close_button)
        hbox.Add(ok_button, flag=wx.RIGHT, border=5)

        return hbox

    def get_line(self):
        line = wx.StaticLine(self, -1, size=(20, -1), style=wx.LI_HORIZONTAL)
        return line

    def set_visualization_mode_parent_value(self):
        if self.radio1.GetValue():
            self.GetParent().visualization_mode = V_M_CLUSTER
            return
        if self.radio2.GetValue():
            self.GetParent().visualization_mode = V_M_SUMMARY
            return
        if self.radio3.GetValue():
            self.GetParent().visualization_mode = V_M_CLUSTER_SUMMARY

    def set_legends_parent_values(self):
#        Para Cluster
        self.GetParent().legends_cluster = []
        self.GetParent().legends_cluster.append(self.clus_check1.GetValue())
        self.GetParent().legends_cluster.append(self.clus_check2.GetValue())
        self.GetParent().legends_cluster.append(self.clus_check3.GetValue())
        self.GetParent().legends_cluster.append(self.clus_check4.GetValue())

#         Para Resumen
        self.GetParent().legends_summary = []
        self.GetParent().legends_summary.append(self.summ_check1.GetValue())
        self.GetParent().legends_summary.append(self.summ_check2.GetValue())
        self.GetParent().legends_summary.append(self.summ_check3.GetValue())
        self.GetParent().legends_summary.append(self.summ_check4.GetValue())

    def on_close(self, e):
        self.set_visualization_mode_parent_value()
        self.set_legends_parent_values()
        self.Close()


class ClusterPage(wx.Panel):
    def __init__(self, parent, dialog_ref):
        wx.Panel.__init__(self, parent)
        sizer = wx.BoxSizer(wx.VERTICAL)
        checkbox1 = wx.CheckBox(self, -1, "Mostrar porcentaje de " + \
                                                            "observaciones")
        dialog_ref.clus_check1 = checkbox1

        checkbox2 = wx.CheckBox(self, -1, "Mostrar cantidad de observaciones")
        checkbox2.SetValue(True)
        dialog_ref.clus_check2 = checkbox2

        checkbox3 = wx.CheckBox(self, -1, "Mostrar nombre")
        dialog_ref.clus_check3 = checkbox3

        checkbox4 = wx.CheckBox(self, -1, "Mostrar shapes")
        dialog_ref.clus_check4 = checkbox4

        sizer.Add(checkbox1, 0, wx.ALL, 5)
        sizer.Add(checkbox2, 0, wx.ALL, 5)
        sizer.Add(checkbox3, 0, wx.ALL, 5)
        sizer.Add(checkbox4, 0, wx.ALL, 5)

        self.SetSizer(sizer)


class SummaryPage(wx.Panel):
    def __init__(self, parent, dialog_ref):
        wx.Panel.__init__(self, parent)
        sizer = wx.BoxSizer(wx.VERTICAL)
        checkbox1 = wx.CheckBox(self, -1, "Mostrar porcentaje de " + \
                                                            "observaciones")
        checkbox1.SetValue(True)
        dialog_ref.summ_check1 = checkbox1

        checkbox2 = wx.CheckBox(self, -1, "Mostrar cantidad de observaciones")
        dialog_ref.summ_check2 = checkbox2

        checkbox3 = wx.CheckBox(self, -1, "Mostrar nombre")
        dialog_ref.summ_check3 = checkbox3

        checkbox4 = wx.CheckBox(self, -1, "Mostrar shapes")
        dialog_ref.summ_check4 = checkbox4

        sizer.Add(checkbox1, 0, wx.ALL, 5)
        sizer.Add(checkbox2, 0, wx.ALL, 5)
        sizer.Add(checkbox3, 0, wx.ALL, 5)
        sizer.Add(checkbox4, 0, wx.ALL, 5)

        self.SetSizer(sizer)


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

        ClusterConfig(self)


def main():

    ex = wx.App()
    Example(None)
    ex.MainLoop()


if __name__ == '__main__':
    main()
