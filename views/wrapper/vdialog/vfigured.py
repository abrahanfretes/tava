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
        self.ShowModal()

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

    def set_figure_parent_values(self):
        fig_config = self.GetParent().fig_config
        fig_config.width = self.figure_width.GetValue()
        fig_config.height = self.figure_height.GetValue()

#         Espaciado de Subplots
        fig_config.subplot_top = self.top_spacing.GetValue()
        fig_config.subplot_bottom = self.bottom_spacing.GetValue()
        fig_config.subplot_left = self.left_spacing.GetValue()
        fig_config.subplot_right = self.right_spacing.GetValue()

    def on_close(self, e):
        self.set_figure_parent_values()
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

        self.dialog_ref = dialog_ref

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
        figure_width = masked.Ctrl(self, value=6.75, integerWidth=5,
                                   fractionWidth=2,
                                   controlType=masked.controlTypes.NUMBER)
        self.dialog_ref.figure_width = figure_width

        height_label = wx.StaticText(self, -1, "Figure height:")
        figure_height = masked.Ctrl(self, value=5.75, integerWidth=5,
                                   fractionWidth=2,
                                   controlType=masked.controlTypes.NUMBER)
        self.dialog_ref.figure_height = figure_height

        grid.Add(width_label, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL |
                                                                    wx.ALL, 5)
        grid.Add(figure_width, 0, wx.ALIGN_LEFT | wx.ALL, 5)

        grid.Add(height_label, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL |
                                                                    wx.ALL, 5)
        grid.Add(figure_height, 0, wx.ALIGN_LEFT | wx.ALL, 5)

        sboxs_sf.Add(grid, 1, wx.EXPAND | wx.ALL, 10)

        return sboxs_sf

    def get_spacing_figure(self):
        sbox_spf = wx.StaticBox(self, -1, "Espaciado")
        sboxs_spf = wx.StaticBoxSizer(sbox_spf, wx.VERTICAL)

        grid = wx.FlexGridSizer(cols=4)

        top_label = wx.StaticText(self, -1, "Top:")
        top_spacing = masked.Ctrl(self, value=0.98, integerWidth=5,
                                       fractionWidth=2,
                                       controlType=masked.controlTypes.NUMBER)
        self.dialog_ref.top_spacing = top_spacing

        bottom_label = wx.StaticText(self, -1, "Bottom:")
        bottom_spacing = masked.Ctrl(self, value=0.07, integerWidth=5,
                                          fractionWidth=2,
                                        controlType=masked.controlTypes.NUMBER)
        self.dialog_ref.bottom_spacing = bottom_spacing

        left_label = wx.StaticText(self, -1, "Left:")
        left_spacing = masked.Ctrl(self, value=0.02, integerWidth=5,
                                        fractionWidth=2,
                                        controlType=masked.controlTypes.NUMBER)
        self.dialog_ref.left_spacing = left_spacing

        right_label = wx.StaticText(self, -1, "Right:")
        right_spacing = masked.Ctrl(self, value=0.98, integerWidth=5,
                                         fractionWidth=2,
                                        controlType=masked.controlTypes.NUMBER)
        self.dialog_ref.right_spacing = right_spacing

        grid.Add(top_label, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL |
                                                                    wx.ALL, 5)
        grid.Add(top_spacing, 0, wx.ALIGN_LEFT | wx.ALL, 5)

        grid.Add(bottom_label, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL |
                                                                    wx.ALL, 5)
        grid.Add(bottom_spacing, 0, wx.ALIGN_LEFT | wx.ALL, 5)

        grid.Add(left_label, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL |
                                                                    wx.ALL, 5)
        grid.Add(left_spacing, 0, wx.ALIGN_LEFT | wx.ALL, 5)

        grid.Add(right_label, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL |
                                                                    wx.ALL, 5)
        grid.Add(right_spacing, 0, wx.ALIGN_LEFT | wx.ALL, 5)

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
                                           colour=(255, 255, 255),
                                           size=(120, 30))
        self.dialog_ref.clr_top_sp = clr_top_sp

        bottom_label = wx.StaticText(self, -1, "Bottom:")
        clr_bottom_sp = csel.ColourSelect(self, -1, "Escoja un color",
                                              colour=(0, 0, 0),
                                              size=(120, 30))
        self.dialog_ref.clr_bottom_sp = clr_bottom_sp

        left_label = wx.StaticText(self, -1, "Left:")
        clr_left_sp = csel.ColourSelect(self, -1, "Escoja un color",
                                            colour=(0, 0, 0),
                                            size=(120, 30))
        self.dialog_ref.clr_left_sp = clr_left_sp

        right_label = wx.StaticText(self, -1, "Right:")
        clr_right_sp = csel.ColourSelect(self, -1, "Escoja un color",
                                             colour=(255, 255, 255),
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


class FigureConfig():
    '''
    Clase que contendrá las configuraciones de la Figura o contenedor
    principal.
    '''
    def __init__(self):
        '''
        Método de inicializacion de variables
        '''
        self.width = 6.75       # figure size in inches
        self.height = 5.75
        self.dpi = 80           # figure dots per inch
        self.facecolor = 'w'    # figure facecolor; 0.75 is scalar gray

        # the left side of the subplots of the figure
        self.subplot_left = 0.02
        # the right side of the subplots of the figure
        self.subplot_right = 0.98
        # the bottom of the subplots of the figure
        self.subplot_bottom = 0.07
        # the top of the subplots of the figure
        self.subplot_top = 0.98
        # the amount of width reserved for blank space between subplots
        self.subplot_wspace = 0.05
        # the amount of height reserved for white space between subplots
        self.subplot_hspace = 0.10


class AxesConfig():
    '''
    Clase que contendrá las configuraciones de los ejes contenidas en las
    Figuras.
    '''
    def __init__(self):
        '''
        Método de inicializacion de variables
        '''
        self.color_top_spine = "#FFFFFF"
        self.color_bottom_spine = "#000000"
        self.color_left_spine = "#000000"
        self.color_right_spine = "#FFFFFF"


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
        self.fig_config = FigureConfig()
        FigureConfigDialog(self)


def main():

    ex = wx.App()
    Example(None)
    ex.MainLoop()


if __name__ == '__main__':
    main()
