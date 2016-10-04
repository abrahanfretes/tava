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


class FigureConfigDialog(wx.Dialog):
    '''
    Dialog de configuración de la Figura.
    '''
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, size=(600, 500),
                           title='Configuración de Gráfico')

        notebook = LB.LabelBook(self, -1, agwStyle=LB.INB_FIT_LABELTEXT |
                LB.INB_LEFT | LB.INB_DRAW_SHADOW | LB.INB_GRADIENT_BACKGROUND |
                LB.INB_SHOW_ONLY_TEXT | LB.INB_BOLD_TAB_SELECTION)
        notebook.SetFontBold(False)
        notebook.SetColour(LB.INB_TAB_AREA_BACKGROUND_COLOUR,
                           wx.Colour(132, 164, 213))

        imagelist = wx.ImageList(32, 32)
        imagelist.Add(wx.Bitmap("my_bitmap.png", wx.BITMAP_TYPE_PNG))
        notebook.AssignImageList(imagelist)

        notebook.AddPage(FigureConfigPanel(notebook, self), "Figura", 1, 0)
        notebook.AddPage(AxesConfigPanel(notebook, self), "Ejes", 0, 0)

        self.Bind(wx.EVT_CLOSE, self.on_close)

        self.CenterOnScreen()
        self.Show()

    def set_axes_parent_values(self):
        ax_conf = self.GetParent().ax_conf
        ax_conf.color_top_spine = self.clr_top_sp.GetValue().\
        GetAsString(wx.C2S_HTML_SYNTAX)
        ax_conf.color_bottom_spine = self.clr_bottom_sp.GetValue().\
        GetAsString(wx.C2S_HTML_SYNTAX)
        ax_conf.color_left_spine = self.clr_left_sp.GetValue().\
        GetAsString(wx.C2S_HTML_SYNTAX)
        ax_conf.color_right_spine = self.clr_right_sp.GetValue().\
        GetAsString(wx.C2S_HTML_SYNTAX)

    def on_close(self, e):
        self.set_axes_parent_values()
        self.Destroy()


class FigureConfigPanel(wx.Panel):
    '''
    Panel de configuracion de la figura.
    '''

    def __init__(self, parent, dialog_ref):
        '''
        Método de inicialización del Panel.
        :param parent: referencia al contenedor padre.
        '''
        wx.Panel.__init__(self, parent, style=0)

        self.SetBackgroundColour(wx.Colour(255, 255, 255))

        sboxs_sf = self.get_size_figure()

        sboxs_spf = self.get_spacing_figure()

        msizer = wx.BoxSizer(wx.VERTICAL)

        msizer.Add(sboxs_sf, 0, wx.EXPAND | wx.ALL, 10)
        msizer.Add(sboxs_spf, 0, wx.EXPAND | wx.ALL, 10)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(msizer, 0, wx.EXPAND)

        self.SetSizer(sizer)

    def get_size_figure(self):
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

    def get_spacing_figure(self):
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


class AxesConfigPanel(wx.Panel):
    """
    Panel de configuración de los ejes de la Figura.
    """

    def __init__(self, parent, dialog_ref):
        '''
        Método de inicialización de la clase.
        :param parent: referencia al contenedor padre.
        :param dialog_ref: referencia a la clase Dialog principal
        '''
        wx.Panel.__init__(self, parent, style=0)

        self.dialog_ref = dialog_ref

        sizer = wx.BoxSizer(wx.VERTICAL)

        self.SetBackgroundColour(wx.Colour(255, 255, 255))

        sboxs_spif = self.get_spines_figure()

        sizer.Add(sboxs_spif, 0, wx.EXPAND | wx.ALL, 3)

        self.SetSizer(sizer)

    def get_spines_figure(self):
        sbox_spf = wx.StaticBox(self, -1, "Bordes")
        sboxs_spf = wx.StaticBoxSizer(sbox_spf, wx.VERTICAL)

        grid = wx.FlexGridSizer(cols=5)

        top_label = wx.StaticText(self, -1, "Top:")
        clr_top_sp = csel.ColourSelect(self, -1, label="Escoja un color",
                                           colour=(255, 255, 0),
                                           size=(120, 30))
        self.dialog_ref.clr_top_sp = clr_top_sp

        bottom_label = wx.StaticText(self, -1, "Bottom:")
        clr_bottom_sp = csel.ColourSelect(self, -1, "Escoja un color",
                                              colour=(255, 0, 255),
                                              size=(120, 30))
        self.dialog_ref.clr_bottom_sp = clr_bottom_sp

        left_label = wx.StaticText(self, -1, "Left:")
        clr_left_sp = csel.ColourSelect(self, -1, "Escoja un color",
                                            colour=(127, 0, 255),
                                            size=(120, 30))
        self.dialog_ref.clr_left_sp = clr_left_sp

        right_label = wx.StaticText(self, -1, "Right:")
        clr_right_sp = csel.ColourSelect(self, -1, "Escoja un color",
                                             colour=(255, 100, 130),
                                             size=(120, 30))
        self.dialog_ref.clr_right_sp = clr_right_sp

        grid.Add(top_label, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL |
                                                                    wx.ALL, 5)
        grid.Add(clr_top_sp, 0, wx.EXPAND | wx.ALL, 5)

        grid.Add(wx.StaticText(self, -1, "                "), wx.ALL)

        grid.Add(bottom_label, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL |
                                                                    wx.ALL, 5)
        grid.Add(clr_bottom_sp, 0, wx.EXPAND | wx.ALL, 5)

        grid.Add(left_label, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL |
                                                                     wx.ALL, 5)
        grid.Add(clr_left_sp, 0, wx.EXPAND | wx.ALL, 5)

        grid.Add(wx.StaticText(self, -1, "                "), wx.ALL)

        grid.Add(right_label, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL |
                                                                    wx.ALL, 5)
        grid.Add(clr_right_sp, 0, wx.EXPAND | wx.ALL, 5)

        sboxs_spf.Add(grid, 0, wx.ALL, 3)

        return sboxs_spf


class AxesConfig():
    '''
    Clase que contendrá las configuraciones de los ejes contenidas en las
    Figuras.
    '''
    def __init__(self):
        '''
        Método de inicializacion de variables
        '''
        self.color_top_spine = (0, 0, 0)
        self.color_bottom_spine = (0, 0, 0)
        self.color_left_spine = (0, 0, 0)
        self.color_right_spine = (0, 0, 0)


class Example(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(Example, self).__init__(*args, **kwargs)

        self.InitUI()

    def InitUI(self):
        self.SetSize((300, 200))
        self.Centre()
        self.Show(True)
        self.SetPosition((0, 0))
        self.ax_conf = AxesConfig()
        FigureConfigDialog(self)


def main():

    ex = wx.App()
    Example(None)
    ex.MainLoop()


if __name__ == '__main__':
    main()
