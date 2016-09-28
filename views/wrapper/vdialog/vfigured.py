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
from wx.lib import masked
import wx.lib.colourselect as  csel
import wx.lib.agw.labelbook as LB


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


class DialogConfig(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, size=(600, 500),
                           title='Configuración de Gráfico')

#         Possible values for Tab placement are INB_TOP, INB_BOTTOM,
#         INB_RIGHT, INB_LEFT

        notebook = LB.LabelBook(self, -1, agwStyle=LB.INB_FIT_LABELTEXT |
                LB.INB_LEFT | LB.INB_DRAW_SHADOW | LB.INB_GRADIENT_BACKGROUND |
                LB.INB_SHOW_ONLY_TEXT)
        notebook.SetFontBold(False)
        notebook.SetColour(LB.INB_TAB_AREA_BACKGROUND_COLOUR, wx.Colour(132, 164, 213))

        imagelist = wx.ImageList(32, 32)
        imagelist.Add(wx.Bitmap("my_bitmap.png", wx.BITMAP_TYPE_PNG))
        notebook.AssignImageList(imagelist)

        pane1 = FigureConfig(notebook)
        pane2 = ClusterConfig(notebook)

        notebook.AddPage(pane1, "Figura", 1, 0)
        notebook.AddPage(pane2, "Análisis", 0, 0)
#         self.CenterOnScreen()
        self.Show()

        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def OnClose(self, event):
        self.GetParent().Close()
        event.Skip()


# ver ButtonPanel
class FigureConfig(wx.Panel):
    """
    Just a simple test window to put into the LabelBook.
    """

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, style=0)
        self.SetBackgroundColour(wx.Colour(255, 255, 255))

        sboxs_sf = self.set_size_figure()

        sboxs_spf = self.set_spacing_figure()

        sboxs_spif = self.set_spines_figure()

        msizer = wx.BoxSizer(wx.VERTICAL)

        msizer.Add(sboxs_sf, 0, wx.EXPAND | wx.ALL, 10)
        msizer.Add(sboxs_spf, 0, wx.EXPAND | wx.ALL, 10)
        msizer.Add(sboxs_spif, 0, wx.EXPAND | wx.ALL, 10)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(msizer, 0, wx.EXPAND)

        self.SetSizer(sizer)

    def set_size_figure(self):
        sbox_sf = wx.StaticBox(self, -1, "Tamaño")
        sboxs_sf = wx.StaticBoxSizer(sbox_sf, wx.VERTICAL)

        grid = wx.FlexGridSizer(cols=4)

        width_label = wx.StaticText(self, -1, "Figure width:")
        self.figure_width = masked.NumCtrl(self, value=0, integerWidth=4,
                                           allowNegative=False)

        height_label = wx.StaticText(self, -1, "Figure height:")
        self.figure_height = masked.NumCtrl(self, value=0, integerWidth=4,
                                           allowNegative=False)

        grid.Add(width_label, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL |
                                                                    wx.ALL, 5)
        grid.Add(self.figure_width, 0, wx.ALIGN_LEFT | wx.ALL, 5)

        grid.Add(height_label, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL |
                                                                    wx.ALL, 5)
        grid.Add(self.figure_height, 0, wx.ALIGN_LEFT | wx.ALL, 5)

        sboxs_sf.Add(grid, 1, wx.EXPAND | wx.ALL, 10)

        return sboxs_sf

    def set_spacing_figure(self):
        sbox_spf = wx.StaticBox(self, -1, "Espaciado")
        sboxs_spf = wx.StaticBoxSizer(sbox_spf, wx.VERTICAL)

        grid = wx.FlexGridSizer(cols=4)

        top_label = wx.StaticText(self, -1, "Top:")
        self.top_spacing = masked.Ctrl(self, integerWidth=5, fractionWidth=2,
                                    controlType=masked.controlTypes.NUMBER)

        bottom_label = wx.StaticText(self, -1, "Bottom:")
        self.bottom_spacing = masked.Ctrl(self, integerWidth=5,
                    fractionWidth=2, controlType=masked.controlTypes.NUMBER)

        left_label = wx.StaticText(self, -1, "Left:")
        self.left_spacing = masked.Ctrl(self, integerWidth=5, fractionWidth=2,
                                    controlType=masked.controlTypes.NUMBER)

        right_label = wx.StaticText(self, -1, "Right:")
        self.right_spacing = masked.Ctrl(self, integerWidth=5, fractionWidth=2,
                                    controlType=masked.controlTypes.NUMBER)

        grid.Add(top_label, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL |
                                                                    wx.ALL, 5)
        grid.Add(self.top_spacing, 0, wx.ALIGN_LEFT | wx.ALL, 5)

        grid.Add(bottom_label, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL |
                                                                    wx.ALL, 5)
        grid.Add(self.bottom_spacing, 0, wx.ALIGN_LEFT | wx.ALL, 5)

        grid.Add(left_label, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL |
                                                                    wx.ALL, 5)
        grid.Add(self.left_spacing, 0, wx.ALIGN_LEFT | wx.ALL, 5)

        grid.Add(right_label, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL |
                                                                    wx.ALL, 5)
        grid.Add(self.right_spacing, 0, wx.ALIGN_LEFT | wx.ALL, 5)

        sboxs_spf.Add(grid, 1, wx.EXPAND | wx.ALL, 10)

        return sboxs_spf

    def set_spines_figure(self):
        sbox_spf = wx.StaticBox(self, -1, "Bordes")
        sboxs_spf = wx.StaticBoxSizer(sbox_spf, wx.VERTICAL)

        grid = wx.FlexGridSizer(cols=4)

        top_label = wx.StaticText(self, -1, "Top:")

        self.top_color = csel.ColourSelect(self, -1, "", (255, 255, 0), (60, 20))

        bottom_label = wx.StaticText(self, -1, "Bottom:")

        self.bottom_color = csel.ColourSelect(self, -1, "", (255, 0, 255), (60, 20))

        left_label = wx.StaticText(self, -1, "Left:")
        self.left_color = csel.ColourSelect(self, -1, "", (127, 0, 255), (60, 20))

        right_label = wx.StaticText(self, -1, "Right:")
        self.right_color = csel.ColourSelect(self, -1, "", (255, 100, 130), (60, 20))

        grid.Add(top_label, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL |
                                                                    wx.ALL, 5)
        grid.Add(self.top_color, 0, wx.EXPAND | wx.ALL, 5)

        grid.Add(bottom_label, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL |
                                                                    wx.ALL, 5)
        grid.Add(self.bottom_color, 0, wx.EXPAND | wx.ALL, 5)

        grid.Add(left_label, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL |
                                                                     wx.ALL, 5)
        grid.Add(self.left_color, 0, wx.EXPAND | wx.ALL, 5)

        grid.Add(right_label, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL |
                                                                    wx.ALL, 5)
        grid.Add(self.right_color, 0, wx.EXPAND | wx.ALL, 5)

        sboxs_spf.Add(grid, 1, wx.EXPAND | wx.ALL, 10)

        return sboxs_spf


class ClusterConfig(wx.Panel):
    """
    Just a simple test window to put into the LabelBook.
    """

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, style=0)
        self.SetBackgroundColour(wx.Colour(255, 255, 255))

        sboxs_mv = self.set_visualization_mode()

        sboxs_sm = self.set_summary()

        sboxs_lg = self.set_legend()

        msizer = wx.BoxSizer(wx.VERTICAL)

        msizer.Add(sboxs_mv, 0, wx.EXPAND | wx.ALL, 7)
        msizer.Add(sboxs_sm, 0, wx.EXPAND | wx.ALL, 7)
        msizer.Add(sboxs_lg, 0, wx.EXPAND | wx.ALL, 7)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(msizer, 0, wx.EXPAND)

        self.SetSizer(sizer)

    def set_visualization_mode(self):
        sbox_mv = wx.StaticBox(self, -1, "Modo Visualización")
        sboxs_mv = wx.StaticBoxSizer(sbox_mv, wx.VERTICAL)

        radio1 = wx.RadioButton(self, -1, "Mostrar en un solo eje",
                                style=wx.RB_GROUP)

        radio2 = wx.RadioButton(self, -1, "Mostrar en varios ejes")
        radio2.SetValue(False)

        sboxs_mv.Add(radio1, 0, wx.ALL, 5)
        sboxs_mv.Add(radio2, 0, wx.ALL, 5)
        return sboxs_mv

    def set_summary(self):
        sbox_sm = wx.StaticBox(self, -1, "Resumen")
        sboxs_sm = wx.StaticBoxSizer(sbox_sm, wx.VERTICAL)

        radio1 = wx.RadioButton(self, -1, "Mostrar en un solo eje",
                                style=wx.RB_GROUP)
        radio1.SetValue(False)

        radio2 = wx.RadioButton(self, -1, "Mostrar en varios ejes")
        radio2.SetValue(False)

        checkbox1 = wx.CheckBox(self, -1, "Mostrar cluster de fondo")

        sboxs_sm.Add(radio1, 0, wx.ALL, 5)
        sboxs_sm.Add(radio2, 0, wx.ALL, 5)
        sboxs_sm.Add(checkbox1, 0, wx.ALL, 5)
        return sboxs_sm

    def set_legend(self):
        sbox_mv = wx.StaticBox(self, -1, "Leyenda")
        sboxs_mv = wx.StaticBoxSizer(sbox_mv, wx.VERTICAL)

        checkbox1 = wx.CheckBox(self, -1, "Mostrar cantidad de observaciones por cluster")

        checkbox2 = wx.CheckBox(self, -1, "Mostrar porcentaje de observaciones por cluster")

        sboxs_mv.Add(checkbox1, 0, wx.ALL, 5)
        sboxs_mv.Add(checkbox2, 0, wx.ALL, 5)
        return sboxs_mv


class SamplePane(wx.Panel):
    """
    Just a simple test window to put into the LabelBook.
    """
    def __init__(self, parent, label):

        wx.Panel.__init__(self, parent, style=0)  # wx.BORDER_SUNKEN)
        self.SetBackgroundColour(wx.Colour(255, 255, 255))

        label = label + "\nEnjoy the LabelBook && FlatImageBook demo!"
        wx.StaticText(self, -1, label, pos=(10, 10))


class Example(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(Example, self).__init__(*args, **kwargs) 

        self.InitUI()

    def InitUI(self):

        menubar = wx.MenuBar()
        help_ = wx.Menu()
        help_.Append(100, '&About')
        self.Bind(wx.EVT_MENU, self.OnAboutBox, id=100)
        menubar.Append(help_, '&Help')
        self.SetMenuBar(menubar)
        self.SetSize((300, 200))
        self.SetTitle('About dialog box')
        self.Centre()
        self.Show(True)
        self.SetPosition((0, 0))
#         self.Centre()

        DialogConfig(self)

    def OnAboutBox(self, e):
        DialogConfig(self)


def main():

    ex = wx.App()
    Example(None)
    ex.MainLoop()


if __name__ == '__main__':
    main()
