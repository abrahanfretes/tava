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

V_M_CLUSTER = 1
V_M_SUMMARY = 2
V_M_CLUSTER_SUMMARY = 0


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
        nb.AddPage(ClusterSummaryPage(nb, self), "clusters y Resúmenes")
        nb.AddPage(ClusterPage(nb, self), "Clusters")
        nb.AddPage(SummaryPage(nb, self), "Resumenes")

        nb.Bind(wx.EVT_CHOICEBOOK_PAGE_CHANGED, self.on_page_changed)

        # finally, put the notebook in a sizer for the panel to manage
        # the layout
        sizer = wx.BoxSizer()
        sizer.Add(nb, 1, wx.EXPAND | wx.EXPAND, 5)
        p.SetSizer(sizer)

        sboxs_mv.Add(p, 1, wx.ALL | wx.EXPAND, 5)
        return sboxs_mv

    def on_page_changed(self, e):
        print e.GetSelection()
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
        self.GetParent().clus_summ_axs.append(self.clus_summ_ax_rd4.GetValue())

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
        sbox_ax = wx.StaticBox(self, -1, "Visualizar Seleccionados")
        sboxs_ax = wx.StaticBoxSizer(sbox_ax, wx.VERTICAL)

        radio1 = wx.RadioButton(self, -1, "En una Figura",
                                style=wx.RB_GROUP)
        radio1.SetValue(False)
        dialog_ref.clus_ax_rd1 = radio1

        radio2 = wx.RadioButton(self, -1, "En diferentes Figuras")
        dialog_ref.clus_ax_rd2 = radio2

        sboxs_ax.Add(radio1, 0, wx.ALL, 5)
        sboxs_ax.Add(radio2, 0, wx.ALL, 5)

        return sboxs_ax

    def get_legends(self, dialog_ref):
        sbox_lg = wx.StaticBox(self, -1, "Visualizar como Leyenda")
        sboxs_lg = wx.StaticBoxSizer(sbox_lg, wx.VERTICAL)

        checkbox1 = wx.CheckBox(self, -1, "Porcentaje de Observaciones")
        dialog_ref.clus_lg_check1 = checkbox1

        checkbox2 = wx.CheckBox(self, -1, "Cantidad de Observaciones")
        dialog_ref.clus_lg_check2 = checkbox2

        checkbox3 = wx.CheckBox(self, -1, "Nombre")
        dialog_ref.clus_lg_check3 = checkbox3

        checkbox4 = wx.CheckBox(self, -1, "Shapes")
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

        sbox_ax = wx.StaticBox(self, -1, "Visualizar Seleccionados")
        sboxs_ax = wx.StaticBoxSizer(sbox_ax, wx.VERTICAL)

        radio1 = wx.RadioButton(self, -1, "En una Figura",
                                style=wx.RB_GROUP)
        radio1.SetValue(False)
        dialog_ref.summ_ax_rd1 = radio1

        radio2 = wx.RadioButton(self, -1, "En diferentes Figuras")
        dialog_ref.summ_ax_rd2 = radio2

        sboxs_ax.Add(radio1, 0, wx.ALL, 5)
        sboxs_ax.Add(radio2, 0, wx.ALL, 5)

        return sboxs_ax

    def get_legends(self, dialog_ref):
        sbox_lg = wx.StaticBox(self, -1, "Visualizar como Leyenda")
        sboxs_lg = wx.StaticBoxSizer(sbox_lg, wx.VERTICAL)

        checkbox1 = wx.CheckBox(self, -1, "Porcentaje de Observaciones")
        checkbox1.SetValue(True)
        dialog_ref.summ_lg_check1 = checkbox1

        checkbox2 = wx.CheckBox(self, -1, "Cantidad de Observaciones")
        dialog_ref.summ_lg_check2 = checkbox2

        checkbox3 = wx.CheckBox(self, -1, "Nombre")
        dialog_ref.summ_lg_check3 = checkbox3

        checkbox4 = wx.CheckBox(self, -1, "Shapes")
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
        sbox_ax = wx.StaticBox(self, -1, "Visualizar Seleccionados")
        sboxs_ax = wx.StaticBoxSizer(sbox_ax, wx.VERTICAL)

        radio1 = wx.RadioButton(self, -1, "Todos en misma Figura",
                                style=wx.RB_GROUP)
        radio1.SetValue(False)
        dialog_ref.clus_summ_ax_rd1 = radio1

        radio2 = wx.RadioButton(self, -1, "Todos en diferentes Figuras")
        dialog_ref.clus_summ_ax_rd2 = radio2

        radio3 = wx.RadioButton(self, -1, "Una Figura por cada Cluster y Resumen")
        dialog_ref.clus_summ_ax_rd3 = radio3

        radio4 = wx.RadioButton(self, -1, "Clusters en una Figura y Resumenes en otra")
        dialog_ref.clus_summ_ax_rd4 = radio4

        sboxs_ax.Add(radio1, 0, wx.ALL, 5)
        sboxs_ax.Add(radio2, 0, wx.ALL, 5)
        sboxs_ax.Add(radio3, 0, wx.ALL, 5)
        sboxs_ax.Add(radio4, 0, wx.ALL, 5)

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


class FilterClusterDialog(wx.Dialog):
    def __init__(self, parent, data):
        wx.Dialog.__init__(self, parent, title="Cluster Filter",
                                                            size=(400, 390))
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
        self.parent.data_selected.cancel = False
        self.Close()

    def get_line(self):
        line = wx.StaticLine(self, -1, size=(20, -1), style=wx.LI_HORIZONTAL)
        return line

    def set_buttons(self):
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.ok_button = wx.Button(self, label='Aceptar')
        self.ok_button.Bind(wx.EVT_BUTTON, self.on_accept)

        self.close_button = wx.Button(self, label='Cancelar')
        self.close_button.SetDefault()
        self.close_button.Bind(wx.EVT_BUTTON, self.on_cancel)

        hbox.Add(self.close_button)
        hbox.Add(self.ok_button, flag=wx.RIGHT, border=5)

        return hbox

    def update_button(self):
        page = self.parent.data_selected.option
        self.ok_button.Disable()

        if page == 0:
            _v = self.more_repre.GetValue()+self.less_repre.GetValue()
            if _v != 0:
                self.ok_button.Enable()
                self.ok_button.SetDefault()
        elif page == 1:
            _v = len(self.lb1.GetChecked()) + len(self.lb2.GetChecked())
            if _v != 0:
                self.ok_button.Enable()
                self.ok_button.SetDefault()

    def set_filter_config(self):
        sbox_fc = wx.StaticBox(self, -1, "Configuración de Filtro")
        sboxs_fc = wx.StaticBoxSizer(sbox_fc, wx.HORIZONTAL)

        p = wx.Panel(self)
        nb = wx.Choicebook(p, -1)

        _label = "Representatividad en Cantidad"
        nb.AddPage(self.get_more_representative(nb), _label)
#         _label = "Menor - representatividad respecto a la cantidad"
#         nb.AddPage(self.get_less_representative(nb), _label)
        _label = "Representatividad en Valores Objetivos"
        nb.AddPage(self.get_representative_per_obj(nb), _label)

        nb.Bind(wx.EVT_CHOICEBOOK_PAGE_CHANGED, self.on_page_changed)

        sizer = wx.BoxSizer()
        sizer.Add(nb, 1, wx.EXPAND | wx.EXPAND, 5)
        p.SetSizer(sizer)

        sboxs_fc.Add(p, 1, wx.ALL | wx.EXPAND, 5)
        return sboxs_fc

    def on_page_changed(self, e):
        selection = e.GetSelection()
        self.GetParent().visualization_mode = selection

        self.parent.data_selected.max_repre = self.more_repre.GetMax()

        if selection == 0:
            self.parent.data_selected.option = 0
            self.parent.data_selected.more_repre = self.more_repre.GetValue()
            self.parent.data_selected.less_repre = self.less_repre.GetValue()
            self.update_button()

        elif selection == 1:
            self.parent.data_selected.option = 1
            self.parent.data_selected.max_objetives_use = self.lb1.GetChecked()
            self.parent.data_selected.min_objetives_use = self.lb2.GetChecked()
            self.update_button()

#             self.parent.data_selected.option = 1
#             self.parent.data_selected.less_repre = self.less_repre.GetValue()
#         elif selection == 2:
#             self.parent.data_selected.option = 2
#             self.parent.data_selected.max_objetives_use = self.lb1.GetChecked()
#             self.parent.data_selected.min_objetives_use = self.lb2.GetChecked()

        e.Skip()

    def get_more_representative(self, parent):
        panel = wx.Panel(parent)

        sbox_sf = wx.StaticBox(panel, -1, "Clusters más representativo")
        sboxs_sf = wx.StaticBoxSizer(sbox_sf, wx.VERTICAL)

        grid = wx.FlexGridSizer(cols=2)
        label = wx.StaticText(panel, -1, "Establezca la cantidad:")
        self.more_repre = wx.SpinCtrl(panel, 0, "", (30, 50))
        self.more_repre.SetRange(0, self.data.count_tendency)
        self.more_repre.SetValue(self.data.more_repre)
        self.more_repre.Bind(wx.EVT_SPINCTRL, self.on_more_repre)
        grid.Add(label, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        grid.Add(self.more_repre, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        sboxs_sf.Add(grid, 1, wx.EXPAND | wx.ALL, 10)

        sbox_sf1 = wx.StaticBox(panel, -1, "Clusters menos representativo")
        sboxs_sf1 = wx.StaticBoxSizer(sbox_sf1, wx.VERTICAL)
        grid1 = wx.FlexGridSizer(cols=2)
        label = wx.StaticText(panel, -1, "Establezca la cantidad:")
        self.less_repre = wx.SpinCtrl(panel, 0, "", (30, 50))
        self.less_repre.SetRange(0, self.data.count_tendency)
        self.less_repre.SetValue(self.data.more_repre)
        self.less_repre.Bind(wx.EVT_SPINCTRL, self.on_less_repre)
        grid1.Add(label, 1, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        grid1.Add(self.less_repre, 1, wx.ALIGN_LEFT | wx.ALL, 5)
        sboxs_sf1.Add(grid1, 1, wx.EXPAND | wx.ALL, 10)

        sizer = wx.BoxSizer(wx.VERTICAL)
#         sizer.Add(grid, 1, wx.EXPAND | wx.ALL, 10)
        sizer.Add(sboxs_sf, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(sboxs_sf1, 1, wx.EXPAND | wx.ALL, 5)

        panel.SetSizer(sizer)

        return panel

    def on_more_repre(self, event):
        self.parent.data_selected.more_repre = self.more_repre.GetValue()
        self.update_button()

#     def get_less_representative(self, parent):
#         panel = wx.Panel(parent)
# 
#         sizer = wx.BoxSizer(wx.VERTICAL)
# 
#         grid = wx.FlexGridSizer(cols=2)
# 
#         label = wx.StaticText(panel, -1, "Establezca la cantidad:")
# 
#         self.less_repre = wx.SpinCtrl(panel, 1, "", (30, 50))
#         self.less_repre.SetRange(1, self.data.count_tendency)
#         self.less_repre.SetValue(self.data.more_repre)
#         self.less_repre.Bind(wx.EVT_SPINCTRL, self.on_less_repre)
# 
#         grid.Add(label, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL |
#                                                                     wx.ALL, 5)
#         grid.Add(self.less_repre, 0, wx.ALIGN_LEFT | wx.ALL, 5)
# 
#         sizer.Add(grid, 1, wx.EXPAND | wx.ALL, 10)
# 
#         panel.SetSizer(sizer)
# 
#         return panel

    def on_less_repre(self, event):
        self.parent.data_selected.less_repre = self.less_repre.GetValue()
        self.update_button()

    def get_representative_per_obj(self, parent):
        panel = wx.Panel(parent)

        sizer = wx.BoxSizer(wx.VERTICAL)

        grid = wx.FlexGridSizer(cols=3)

        sizer_lb1 = wx.BoxSizer(wx.VERTICAL)
        lb1_label = wx.StaticText(panel, -1, "Valores Mayores:")
        pts = lb1_label.GetFont().GetPointSize()
        lb1_label.SetFont(wx.FFont(pts, wx.SWISS, wx.FONTFLAG_BOLD))
        self.lb1 = wx.CheckListBox(panel, choices=self.data.max_objetives,
                                   size=(100, 160))
        self.lb1.Bind(wx.EVT_CHECKLISTBOX, self.on_lb1)

        sizer_lb1.Add(lb1_label, flag=wx.ALL, border=2)
        sizer_lb1.Add(self.lb1, flag=wx.ALL | wx.EXPAND, border=5)

        sizer_lb2 = wx.BoxSizer(wx.VERTICAL)
        lb2_label = wx.StaticText(panel, -1, "Valores Menores:")
        pts = lb2_label.GetFont().GetPointSize()
        lb2_label.SetFont(wx.FFont(pts, wx.SWISS, wx.FONTFLAG_BOLD))
        self.lb2 = wx.CheckListBox(panel, choices=self.data.max_objetives,
                                   size=(100, 160))
        self.lb2.Bind(wx.EVT_CHECKLISTBOX, self.on_lb2)
        sizer_lb2.Add(lb2_label, flag=wx.ALL, border=2)
        sizer_lb2.Add(self.lb2, flag=wx.ALL | wx.EXPAND, border=5)

        _style = wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL | wx.ALL
        grid.Add(sizer_lb1, 0, _style, 5)
        grid.Add(wx.StaticLine(panel, wx.ID_ANY, style=wx.LI_VERTICAL), 0,
                 wx.ALL | wx.EXPAND, 5)
        _style = wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL | wx.ALL
        grid.Add(sizer_lb2, 0, _style, 5)

        sizer.Add(grid, 1, wx.EXPAND | wx.ALL, 10)

        panel.SetSizer(sizer)

        return panel

    def on_lb1(self, event):
        self.parent.data_selected.max_objetives_use = self.lb1.GetChecked()
        self.update_button()

    def on_lb2(self, event):
        self.parent.data_selected.min_objetives_use = self.lb2.GetChecked()
        self.update_button()


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
        self.cancel = True

        # ---- valores de objetivos mayores
        self.max_objetives = []
        self.max_objetives_use = []
        self.min_objetives_use = []


def main():

    ex = wx.App()
    Example(None)
    ex.MainLoop()


if __name__ == '__main__':
    main()
