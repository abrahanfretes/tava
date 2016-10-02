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
                                                    size=(400, 530))
        self.SetBackgroundColour(wx.Colour(255, 255, 255))

        sboxs_vm = self.set_visualization_mode()

        sbuttons = self.set_buttons()

        line = self.get_line()

        msizer = wx.BoxSizer(wx.VERTICAL)

        msizer.Add(sboxs_vm, 0, wx.EXPAND | wx.ALL, 7)

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
        sboxs_mv = wx.StaticBoxSizer(sbox_mv, wx.HORIZONTAL)

        # Here we create a panel and a notebook on the panel
        p = wx.Panel(self)
        nb = wx.Choicebook(p, -1)

        # add the pages to the notebook with the label to show on the tab
        nb.AddPage(ClusterPage(nb, self), "Cluster")
        nb.AddPage(SummaryPage(nb, self), "Resumen")
        nb.AddPage(ClusterSummaryPage(nb, self), "Ambos")

        nb.Bind(wx.EVT_CHOICEBOOK_PAGE_CHANGED, self.on_page_changed)

        # finally, put the notebook in a sizer for the panel to manage
        # the layout
        sizer = wx.BoxSizer()
        sizer.Add(nb, 1, wx.EXPAND | wx.EXPAND, 5)
        p.SetSizer(sizer)

        sboxs_mv.Add(p, 1, wx.ALL | wx.EXPAND, 5)
        return sboxs_mv

    def on_page_changed(self, e):
        selection = e.GetSelection()
        self.GetParent().visualization_mode = selection
        e.Skip()

    def set_buttons(self):
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        ok_button = wx.Button(self, label='Aceptar')
        ok_button.SetDefault()

        close_button = wx.Button(self, label='Cancelar')

        ok_button.Bind(wx.EVT_BUTTON, self.on_close)

        close_button.Bind(wx.EVT_BUTTON, self.on_close)

        hbox.Add(close_button)
        hbox.Add(ok_button, flag=wx.RIGHT, border=5)

        return hbox

    def get_line(self):
        line = wx.StaticLine(self, -1, size=(20, -1), style=wx.LI_HORIZONTAL)
        return line

    def set_legends_parent_values(self):
#        Para Cluster
        self.GetParent().legends_cluster = []
        self.GetParent().legends_cluster.append(self.clus_lg_check1.GetValue())
        self.GetParent().legends_cluster.append(self.clus_lg_check2.GetValue())
        self.GetParent().legends_cluster.append(self.clus_lg_check3.GetValue())
        self.GetParent().legends_cluster.append(self.clus_lg_check4.GetValue())

#         Para Resumen
        self.GetParent().legends_summary = []
        self.GetParent().legends_summary.append(self.summ_lg_check1.GetValue())
        self.GetParent().legends_summary.append(self.summ_lg_check2.GetValue())
        self.GetParent().legends_summary.append(self.summ_lg_check3.GetValue())
        self.GetParent().legends_summary.append(self.summ_lg_check4.GetValue())

    def set_axes_parent_values(self):
#         Para Cluster
        self.GetParent().clus_one_axe = self.clus_ax_rd1.GetValue()

#         Para Resumen
        self.GetParent().summ_one_axe = self.summ_ax_rd1.GetValue()

#         Para Ambos
        self.GetParent().clus_summ_axs = []
        self.GetParent().clus_summ_axs.append(self.clus_summ_ax_rd1.GetValue())
        self.GetParent().clus_summ_axs.append(self.clus_summ_ax_rd2.GetValue())
        self.GetParent().clus_summ_axs.append(self.clus_summ_ax_rd3.GetValue())

    def on_close(self, e):
        self.set_axes_parent_values()
        self.set_legends_parent_values()
        self.Close()


class ClusterPage(wx.Panel):
    def __init__(self, parent, dialog_ref):
        wx.Panel.__init__(self, parent)

        sizer = wx.BoxSizer(wx.VERTICAL)

        sboxs_ax = self.get_axes(dialog_ref)
        sboxs_lg = self.get_legends(dialog_ref)

        sizer.Add(sboxs_ax, 0, wx.EXPAND | wx.ALL, 7)
        sizer.Add(sboxs_lg, 0, wx.EXPAND | wx.ALL, 7)

        self.SetSizer(sizer)

    def get_axes(self, dialog_ref):
        sbox_ax = wx.StaticBox(self, -1, "Ejes")
        sboxs_ax = wx.StaticBoxSizer(sbox_ax, wx.VERTICAL)

        radio1 = wx.RadioButton(self, -1, "Mostrar en un solo eje",
                                style=wx.RB_GROUP)
        radio1.SetValue(False)
        dialog_ref.clus_ax_rd1 = radio1

        radio2 = wx.RadioButton(self, -1, "Mostrar en varios ejes")
        dialog_ref.clus_ax_rd2 = radio2

        sboxs_ax.Add(radio1, 0, wx.ALL, 5)
        sboxs_ax.Add(radio2, 0, wx.ALL, 5)

        return sboxs_ax

    def get_legends(self, dialog_ref):
        sbox_lg = wx.StaticBox(self, -1, "Leyenda")
        sboxs_lg = wx.StaticBoxSizer(sbox_lg, wx.VERTICAL)

        checkbox1 = wx.CheckBox(self, -1, "Mostrar porcentaje de " + \
                                                            "observaciones")
        dialog_ref.clus_lg_check1 = checkbox1

        checkbox2 = wx.CheckBox(self, -1, "Mostrar cantidad de observaciones")
        dialog_ref.clus_lg_check2 = checkbox2

        checkbox3 = wx.CheckBox(self, -1, "Mostrar nombre")
        dialog_ref.clus_lg_check3 = checkbox3

        checkbox4 = wx.CheckBox(self, -1, "Mostrar shapes")
        checkbox4.SetValue(True)
        dialog_ref.clus_lg_check4 = checkbox4

        sboxs_lg.Add(checkbox1, 0, wx.ALL, 5)
        sboxs_lg.Add(checkbox2, 0, wx.ALL, 5)
        sboxs_lg.Add(checkbox3, 0, wx.ALL, 5)
        sboxs_lg.Add(checkbox4, 0, wx.ALL, 5)

        return sboxs_lg


class SummaryPage(wx.Panel):
    def __init__(self, parent, dialog_ref):
        wx.Panel.__init__(self, parent)

        sizer = wx.BoxSizer(wx.VERTICAL)

        sboxs_ax = self.get_axes(dialog_ref)
        sboxs_lg = self.get_legends(dialog_ref)

        sizer.Add(sboxs_ax, 0, wx.EXPAND | wx.ALL, 7)
        sizer.Add(sboxs_lg, 0, wx.EXPAND | wx.ALL, 7)

        self.SetSizer(sizer)

    def get_axes(self, dialog_ref):

        sbox_ax = wx.StaticBox(self, -1, "Ejes")
        sboxs_ax = wx.StaticBoxSizer(sbox_ax, wx.VERTICAL)

        radio1 = wx.RadioButton(self, -1, "Mostrar en un solo eje",
                                style=wx.RB_GROUP)
        radio1.SetValue(False)
        dialog_ref.summ_ax_rd1 = radio1

        radio2 = wx.RadioButton(self, -1, "Mostrar en varios ejes")
        dialog_ref.summ_ax_rd2 = radio2

        sboxs_ax.Add(radio1, 0, wx.ALL, 5)
        sboxs_ax.Add(radio2, 0, wx.ALL, 5)

        return sboxs_ax

    def get_legends(self, dialog_ref):
        sbox_lg = wx.StaticBox(self, -1, "Leyenda")
        sboxs_lg = wx.StaticBoxSizer(sbox_lg, wx.VERTICAL)

        checkbox1 = wx.CheckBox(self, -1, "Mostrar porcentaje de " + \
                                                            "observaciones")
        checkbox1.SetValue(True)
        dialog_ref.summ_lg_check1 = checkbox1

        checkbox2 = wx.CheckBox(self, -1, "Mostrar cantidad de observaciones")
        dialog_ref.summ_lg_check2 = checkbox2

        checkbox3 = wx.CheckBox(self, -1, "Mostrar nombre")
        dialog_ref.summ_lg_check3 = checkbox3

        checkbox4 = wx.CheckBox(self, -1, "Mostrar shapes")
        dialog_ref.summ_lg_check4 = checkbox4

        sboxs_lg.Add(checkbox1, 0, wx.ALL, 5)
        sboxs_lg.Add(checkbox2, 0, wx.ALL, 5)
        sboxs_lg.Add(checkbox3, 0, wx.ALL, 5)
        sboxs_lg.Add(checkbox4, 0, wx.ALL, 5)

        return sboxs_lg


class ClusterSummaryPage(wx.Panel):
    def __init__(self, parent, dialog_ref):
        wx.Panel.__init__(self, parent)

        sizer = wx.BoxSizer(wx.VERTICAL)

        sboxs_ax = self.get_axes(dialog_ref)
        sboxs_lg = self.get_legends(dialog_ref)

        sizer.Add(sboxs_ax, 0, wx.EXPAND | wx.ALL, 7)
        sizer.Add(sboxs_lg, 0, wx.EXPAND | wx.ALL, 7)

        self.SetSizer(sizer)

    def get_axes(self, dialog_ref):
        sbox_ax = wx.StaticBox(self, -1, "Ejes")
        sboxs_ax = wx.StaticBoxSizer(sbox_ax, wx.VERTICAL)

        radio1 = wx.RadioButton(self, -1, "Mostrar todos en un eje",
                                style=wx.RB_GROUP)
        radio1.SetValue(False)
        dialog_ref.clus_summ_ax_rd1 = radio1

        radio2 = wx.RadioButton(self, -1, "Mostrar cada uno en un eje")
        dialog_ref.clus_summ_ax_rd2 = radio2

        radio3 = wx.RadioButton(self, -1, "Mostrar ambos en un eje")
        dialog_ref.clus_summ_ax_rd3 = radio3

        sboxs_ax.Add(radio1, 0, wx.ALL, 5)
        sboxs_ax.Add(radio2, 0, wx.ALL, 5)
        sboxs_ax.Add(radio3, 0, wx.ALL, 5)

        return sboxs_ax

    def get_legends(self, dialog_ref):
        sbox_lg = wx.StaticBox(self, -1, "Leyenda")
        sboxs_lg = wx.StaticBoxSizer(sbox_lg, wx.VERTICAL)

        p = wx.Panel(self)
        nb = wx.Notebook(p)

        # add the pages to the notebook with the label to show on the tab
        nb.AddPage(self.get_cluster_legend(nb, dialog_ref), "Cluster")
        nb.AddPage(self.get_summary_legend(nb, dialog_ref), "Resumen")

        # finally, put the notebook in a sizer for the panel to manage
        # the layout
        sizer = wx.BoxSizer()
        sizer.Add(nb, 1, wx.EXPAND)
        p.SetSizer(sizer)

        sboxs_lg.Add(p, 0, wx.ALL | wx.EXPAND, 5)
        return sboxs_lg

    def get_cluster_legend(self, parent, dialog_ref):

        panel = wx.Panel(parent)

        sizer = wx.BoxSizer(wx.VERTICAL)
        checkbox1 = wx.CheckBox(panel, -1, "Mostrar porcentaje de " + \
                                                            "observaciones")
        dialog_ref.clus_lg_check1 = checkbox1

        checkbox2 = wx.CheckBox(panel, -1, "Mostrar cantidad de observaciones")
        dialog_ref.clus_lg_check2 = checkbox2

        checkbox3 = wx.CheckBox(panel, -1, "Mostrar nombre")
        dialog_ref.clus_lg_check3 = checkbox3

        checkbox4 = wx.CheckBox(panel, -1, "Mostrar shapes")
        checkbox4.SetValue(True)
        dialog_ref.clus_lg_check4 = checkbox4

        sizer.Add(checkbox1, 0, wx.ALL, 5)
        sizer.Add(checkbox2, 0, wx.ALL, 5)
        sizer.Add(checkbox3, 0, wx.ALL, 5)
        sizer.Add(checkbox4, 0, wx.ALL, 5)

        panel.SetSizer(sizer)

        return panel

    def get_summary_legend(self, parent, dialog_ref):

        panel = wx.Panel(parent)

        sizer = wx.BoxSizer(wx.VERTICAL)
        checkbox1 = wx.CheckBox(panel, -1, "Mostrar porcentaje de " + \
                                                            "observaciones")
        checkbox1.SetValue(True)
        dialog_ref.summ_lg_check1 = checkbox1

        checkbox2 = wx.CheckBox(panel, -1, "Mostrar cantidad de observaciones")
        dialog_ref.summ_lg_check2 = checkbox2

        checkbox3 = wx.CheckBox(panel, -1, "Mostrar nombre")
        dialog_ref.summ_lg_check3 = checkbox3

        checkbox4 = wx.CheckBox(panel, -1, "Mostrar shapes")
        dialog_ref.summ_lg_check4 = checkbox4

        sizer.Add(checkbox1, 0, wx.ALL, 5)
        sizer.Add(checkbox2, 0, wx.ALL, 5)
        sizer.Add(checkbox3, 0, wx.ALL, 5)
        sizer.Add(checkbox4, 0, wx.ALL, 5)

        panel.SetSizer(sizer)

        return panel


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