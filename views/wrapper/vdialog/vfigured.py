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
from wx.lib.masked import Ctrl
from wx.lib.masked.ctrl import NUMBER

from imgs.iview import my_bitmap
import wx.lib.agw.labelbook as LB
import wx.lib.colourselect as csel
from wx import GetTranslation as L

TYPES_GRID = ['-', '--', '-.', ':']


class DataConfig(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, size=(600, 500),
                           title=L('GRAPHIC_CONFIG'))

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
        wx.Dialog.__init__(self, parent, size=(600, 600),
                           title=L('GRAPHIC_CONFIG'))

        # ---- variable de configuración de Figura
        conf = parent.fig_config
        a_conf = parent.ax_conf

        ag_st = LB.INB_FIT_LABELTEXT | LB.INB_LEFT | LB.INB_DRAW_SHADOW
        ag_st = ag_st | LB.INB_GRADIENT_BACKGROUND | LB.INB_SHOW_ONLY_TEXT
        ag_st = ag_st | LB.INB_BOLD_TAB_SELECTION
        notebook = LB.LabelBook(self, -1, agwStyle=ag_st)
        notebook.SetFontBold(False)
        notebook.SetColour(LB.INB_TAB_AREA_BACKGROUND_COLOUR,
                           wx.Colour(132, 164, 213))

        imagelist = wx.ImageList(32, 32)
        imagelist.Add(my_bitmap.GetBitmap())
        notebook.AssignImageList(imagelist)

        notebook.AddPage(FigureConfigPanel(notebook, self, conf),
                         L('FIGURE'), 1, 0)
        self.ax_panel = AxesConfigPanel(notebook, self, a_conf)
        notebook.AddPage(self.ax_panel, L('AXES'), 0, 0)
        self.nb = notebook

        self.Bind(wx.EVT_CLOSE, self.on_close)

        self.CenterOnScreen()
        self.ShowModal()

    def set_figure_parent_values(self):
        fig_config = self.GetParent().fig_config
        fig_config.width = self.figure_width.GetValue()
        fig_config.height = self.figure_height.GetValue()

        # ---- Espaciado de Subplots
        fig_config.subplot_top = self.top_spacing.GetValue()
        fig_config.subplot_bottom = self.bottom_spacing.GetValue()
        fig_config.subplot_left = self.left_spacing.GetValue()
        fig_config.subplot_right = self.right_spacing.GetValue()

    def set_axes_parent_values(self):
        ax_conf = self.GetParent().ax_conf

        # ---- Colores de Spines
        top, bottom, right, left = self.ax_panel.g_spines_colors()
        ax_conf.color_top_spine = top
        ax_conf.color_bottom_spine = bottom
        ax_conf.color_left_spine = left
        ax_conf.color_right_spine = right

        # ---- Localizacion de la leyenda
        ax_conf.legend_show = self.chk_show_lg.GetValue()
        ax_conf.legend_loc = self.ch_loc_leg.GetStringSelection()

        # ---- grilla
        v, o, w, c, ac = self.ax_panel.g_grid_conf()
        ax_conf.grid_lines = v
        ax_conf.grid_lines_style = o
        ax_conf.grid_linewidth = w
        ax_conf.grid_color = c
        ax_conf.grid_color_alpha = ac

        # ---- labels - axes
        x, y, xc, yc = self.ax_panel.g_axes_labels()
        ax_conf.x_axis_show = x
        ax_conf.y_axis_show = y
        ax_conf.x_axis_color = xc
        ax_conf.y_axis_color = yc

    def on_close(self, e):
        self.set_figure_parent_values()
        self.set_axes_parent_values()
        self.Hide()


class FigureConfigPanel(wx.Panel):
    '''
    Panel de configuracion de la figura.
    '''

    def __init__(self, parent, dialog_ref, conf):
        '''
        Método de inicialización del Panel.
        :param parent: referencia al contenedor padre.
        '''
        wx.Panel.__init__(self, parent, style=0)
        self.dialog_ref = dialog_ref
        self.SetBackgroundColour(wx.Colour(255, 255, 255))

        sboxs_sf = self.get_size_figure(conf)

        sboxs_spf = self.get_spacing_figure(conf)

        msizer = wx.BoxSizer(wx.VERTICAL)

        msizer.Add(sboxs_sf, 0, wx.EXPAND | wx.ALL, 10)
        msizer.Add(sboxs_spf, 0, wx.EXPAND | wx.ALL, 10)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(msizer, 0, wx.EXPAND)

        self.SetSizer(sizer)

        # ----       ---------------------------------------------
        # ---- FALTAN
#         self.facecolor = 'w'    # figure facecolor; 0.75 is scalar gray
#         # the amount of width reserved for blank space between subplots
#         self.subplot_wspace = 0.05
#         # the amount of height reserved for white space between subplots
#         self.subplot_hspace = 0.10

    def get_size_figure(self, conf):

        sbox_sf = wx.StaticBox(self, -1, L('SIZE'))
        sboxs_sf = wx.StaticBoxSizer(sbox_sf, wx.VERTICAL)
        grid = wx.FlexGridSizer(cols=4)

        width_label = wx.StaticText(self, -1, L('FIGURE_WIDTH'))
        figure_width = Ctrl(self, value=conf.width, integerWidth=5,
                            fractionWidth=2, controlType=NUMBER)

        self.dialog_ref.figure_width = figure_width

        height_label = wx.StaticText(self, -1, L('FIGURE_HEIGHT'))
        figure_height = Ctrl(self, value=conf.height, integerWidth=5,
                             fractionWidth=2, controlType=NUMBER)

        self.dialog_ref.figure_height = figure_height

        st_grip = wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL | wx.ALL
        grid.Add(width_label, 0, st_grip, 5)
        grid.Add(figure_width, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        grid.Add(height_label, 0, st_grip, 5)
        grid.Add(figure_height, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        sboxs_sf.Add(grid, 1, wx.EXPAND | wx.ALL, 10)

        return sboxs_sf

    def get_spacing_figure(self, conf):
        sbox_spf = wx.StaticBox(self, -1, L('SPACING'))
        sboxs_spf = wx.StaticBoxSizer(sbox_spf, wx.VERTICAL)
        grid = wx.FlexGridSizer(cols=4)

        top_label = wx.StaticText(self, -1, L('TOP'))
        top_spacing = Ctrl(self, value=conf.subplot_top, integerWidth=5,
                           fractionWidth=2, controlType=NUMBER)
        self.dialog_ref.top_spacing = top_spacing

        bottom_label = wx.StaticText(self, -1, L('BOTTOM'))
        bottom_spacing = Ctrl(self, value=conf.subplot_bottom, integerWidth=5,
                              fractionWidth=2, controlType=NUMBER)
        self.dialog_ref.bottom_spacing = bottom_spacing

        left_label = wx.StaticText(self, -1, L('LEFT'))
        left_spacing = Ctrl(self, value=conf.subplot_left, integerWidth=5,
                            fractionWidth=2, controlType=NUMBER)
        self.dialog_ref.left_spacing = left_spacing

        right_label = wx.StaticText(self, -1, L('RIGHT'))
        right_spacing = Ctrl(self, value=conf.subplot_right, integerWidth=5,
                             fractionWidth=2, controlType=NUMBER)
        self.dialog_ref.right_spacing = right_spacing

        _style = wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL | wx.ALL
        grid.Add(top_label, 0, _style, 5)
        grid.Add(top_spacing, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        grid.Add(bottom_label, 0, _style, 5)
        grid.Add(bottom_spacing, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        grid.Add(left_label, 0, _style, 5)
        grid.Add(left_spacing, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        grid.Add(right_label, 0, _style, 5)
        grid.Add(right_spacing, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        sboxs_spf.Add(grid, 1, wx.EXPAND | wx.ALL, 10)

        return sboxs_spf


class AxesConfigPanel(wx.Panel):
    """
    Panel de configuración de los ejes de la Figura.
    """

    def __init__(self, parent, dialog_ref, a_conf):
        '''
        Método de inicialización de la clase.
        :param parent: referencia al contenedor padre.
        :param dialog_ref: referencia a la clase Dialog principal
        '''
        wx.Panel.__init__(self, parent, style=0)
        self.dialog_ref = dialog_ref
        self.SetBackgroundColour(wx.Colour(255, 255, 255))

        sboxs_spif = self.get_spines_figure(a_conf)
        sboxs_lglc = self.get_legend_location(a_conf)
        sboxs_grid = self.get_grid(a_conf)
        sboxs_axes_labels = self.get_xy_label(a_conf)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(sboxs_spif, 0, wx.EXPAND | wx.ALL, 3)
        sizer.Add(sboxs_lglc, 0, wx.EXPAND | wx.ALL, 3)
        sizer.Add(sboxs_grid, 0, wx.EXPAND | wx.ALL, 3)
        sizer.Add(sboxs_axes_labels, 0, wx.EXPAND | wx.ALL, 3)

        self.SetSizer(sizer)

    def get_spines_figure(self, a_conf):
        sbox_spf = wx.StaticBox(self, -1, L('EDGES'))
        sboxs_spf = wx.StaticBoxSizer(sbox_spf, wx.VERTICAL)

        grid = wx.FlexGridSizer(cols=5)

        # ---- color de bordes
        top_label = wx.StaticText(self, -1, L('TOP'))
        _c = wx.NamedColour(a_conf.color_top_spine)
        self.clr_top_sp = csel.ColourSelect(self, -1, L('CHOOSE_A_COLOR'),
                                            _c, size=(120, 30))

        bottom_label = wx.StaticText(self, -1, L('BOTTOM'))
        _c = wx.NamedColour(a_conf.color_bottom_spine)
        self.clr_bottom_sp = csel.ColourSelect(self, -1, L('CHOOSE_A_COLOR'),
                                               _c, size=(120, 30))

        left_label = wx.StaticText(self, -1, L('LEFT'))
        _c = wx.NamedColour(a_conf.color_left_spine)
        self.clr_left_sp = csel.ColourSelect(self, -1, L('CHOOSE_A_COLOR'),
                                             _c, size=(120, 30))

        right_label = wx.StaticText(self, -1, L('RIGHT'))
        _c = wx.NamedColour(a_conf.color_right_spine)
        _l = L('CHOOSE_A_COLOR')
        self.clr_right_sp = csel.ColourSelect(self, -1, _l, _c, size=(120, 30))

        _style = wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL | wx.ALL
        grid.Add(top_label, 0, _style, 5)
        grid.Add(self.clr_top_sp, 0, wx.EXPAND | wx.ALL, 5)
        grid.Add(wx.StaticText(self, -1, "                "), wx.ALL)
        grid.Add(bottom_label, 0, _style, 5)
        grid.Add(self.clr_bottom_sp, 0, wx.EXPAND | wx.ALL, 5)
        grid.Add(left_label, 0, _style, 5)
        grid.Add(self.clr_left_sp, 0, wx.EXPAND | wx.ALL, 5)
        grid.Add(wx.StaticText(self, -1, "                "), wx.ALL)
        grid.Add(right_label, 0, _style, 5)
        grid.Add(self.clr_right_sp, 0, wx.EXPAND | wx.ALL, 5)

        sboxs_spf.Add(grid, 0, wx.ALL, 3)

        return sboxs_spf

    def get_legend_location(self, a_conf):
        sbox_lglc = wx.StaticBox(self, -1, L('LEGEND'))
        sboxs_lglc = wx.StaticBoxSizer(sbox_lglc, wx.VERTICAL)

        chk_show_lg = wx.CheckBox(self, -1, L('SHOW_LEGEND'),
                                  style=wx.ALIGN_RIGHT)
        chk_show_lg.SetValue(True)
        self.dialog_ref.chk_show_lg = chk_show_lg

        loc_label = wx.StaticText(self, -1, L('LOCATION'))

        locations = ['upper left', 'center', 'upper center', 'lower left',
                     'lower right', 'center left', 'upper right', 'right',
                     'lower center', 'best', 'center right']

        ch_loc_leg = wx.Choice(self, -1, choices=locations)
        ch_loc_leg.SetSelection(0)
        ch_loc_leg.SetToolTipString(L('SELECT_A_LOCATION'))
        self.dialog_ref.ch_loc_leg = ch_loc_leg

        grid = wx.FlexGridSizer(cols=2)
        grid.Add(chk_show_lg, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        grid.Add(wx.StaticText(self, -1, ""), 0, wx.ALIGN_LEFT | wx.ALL, 5)
        _style = wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL | wx.ALL
        grid.Add(loc_label, 0, _style, 5)
        grid.Add(ch_loc_leg, 0, wx.ALIGN_LEFT | wx.ALL, 5)

        sboxs_lglc.Add(grid, 1, wx.EXPAND | wx.ALL, 10)

        return sboxs_lglc

    def get_grid(self, conf):

        sbox_grid = wx.StaticBox(self, -1, L('GRID'))
        sboxs_grid = wx.StaticBoxSizer(sbox_grid, wx.VERTICAL)

        _label = L('SHOW_GRID')
        self.ch = wx.CheckBox(self, -1, _label, style=wx.ALIGN_RIGHT)
        self.ch.SetValue(conf.grid_lines)
        self.ch.Bind(wx.EVT_CHECKBOX, self.on_checked_grid)

        cho_label = wx.StaticText(self, -1, L('TYPE'))
        self.cho = wx.Choice(self, -1, choices=TYPES_GRID)
        self.cho.SetSelection(TYPES_GRID.index(conf.grid_lines_style))
        self.cho.SetToolTipString(L('SELECT_TYPE_OF_GRID'))

        g_linewidth_label = wx.StaticText(self, -1, L('WIDTH'))
        self.g_linewidth = wx.SpinCtrlDouble(self, -1, "")
        self.g_linewidth.SetDigits(1)
        self.g_linewidth.SetRange(0.1, 1.0)
        self.g_linewidth.SetValue(conf.grid_linewidth)

        g_color_label = wx.StaticText(self, -1, L('COLOR'))
        _c = wx.NamedColour(conf.grid_color)
        self.g_color = csel.ColourSelect(self, colour=_c)

        g_color_alpha_label = wx.StaticText(self, -1, L('COLOR_ALPHA'))
        self.g_color_alpha = wx.SpinCtrlDouble(self, -1, "")
        self.g_color_alpha.SetDigits(1)
        self.g_color_alpha.SetRange(0.1, 1.0)
        self.g_color_alpha.SetValue(conf.grid_color_alpha)

        grid = wx.FlexGridSizer(cols=4)

        _style = wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL | wx.ALL
        grid.Add(cho_label, 0, _style, 5)
        grid.Add(self.cho, 0, wx.ALIGN_LEFT | wx.ALL, 5)

        grid.Add(g_linewidth_label, 0, _style, 5)
        grid.Add(self.g_linewidth, 0, wx.ALIGN_LEFT | wx.ALL, 5)

        grid.Add(g_color_label, 0, _style, 5)
        grid.Add(self.g_color, 0, wx.ALIGN_LEFT | wx.ALL, 5)

        grid.Add(g_color_alpha_label, 0, _style, 5)
        grid.Add(self.g_color_alpha, 0, wx.ALIGN_LEFT | wx.ALL, 5)

        sboxs_grid.Add(self.ch, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        sboxs_grid.Add(grid, 1, wx.EXPAND | wx.ALL, 10)

        self.checked_grid(conf.grid_lines)

        return sboxs_grid

    def get_xy_label(self, conf):

        sbox_grid = wx.StaticBox(self, -1, L('AXES_VALUES'))
        sboxs_grid = wx.StaticBoxSizer(sbox_grid, wx.VERTICAL)

        _label = L('IN_X')
        self.x_ch = wx.CheckBox(self, -1, _label, style=wx.ALIGN_RIGHT)
        self.x_ch.SetValue(conf.x_axis_show)
        self.x_ch.Bind(wx.EVT_CHECKBOX, self.on_checked_x_axes_label)

        x_label_color = wx.StaticText(self, -1, L('COLOR_X'))
        _c = wx.NamedColour(conf.x_axis_color)
        self.x_label_color_cs = csel.ColourSelect(self, colour=_c)
        self.x_label_color_cs.Enable(conf.x_axis_show)

        _label = L('IN_Y')
        self.y_ch = wx.CheckBox(self, -1, _label, style=wx.ALIGN_RIGHT)
        self.y_ch.SetValue(conf.y_axis_show)
        self.y_ch.Bind(wx.EVT_CHECKBOX, self.on_checked_y_axes_label)

        y_label_color = wx.StaticText(self, -1, L('COLOR_Y'))
        _c = wx.NamedColour(conf.y_axis_color)
        self.y_label_color_cs = csel.ColourSelect(self, colour=_c)
        self.y_label_color_cs.Enable(conf.y_axis_show)

        grid = wx.FlexGridSizer(cols=2)

        grid.Add(self.x_ch, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        grid.Add(wx.StaticText(self, -1, ""), 0, wx.ALIGN_LEFT | wx.ALL, 5)

        _style = wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL | wx.ALL
        grid.Add(x_label_color, 0, _style, 5)
        grid.Add(self.x_label_color_cs, 0, wx.ALIGN_LEFT | wx.ALL, 5)

        grid.Add(self.y_ch, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        grid.Add(wx.StaticText(self, -1, ""), 0, wx.ALIGN_LEFT | wx.ALL, 5)

        grid.Add(y_label_color, 0, _style, 5)
        grid.Add(self.y_label_color_cs, 0, wx.ALIGN_LEFT | wx.ALL, 5)

        sboxs_grid.Add(grid, 1, wx.EXPAND | wx.ALL, 10)

        return sboxs_grid

    def on_checked_grid(self, event):
        cb = event.GetEventObject()
        self.checked_grid(cb.Get3StateValue())

    def checked_grid(self, value):
        self.cho.Enable(value)
        self.g_linewidth.Enable(value)
        self.g_color.Enable(value)
        self.g_color_alpha.Enable(value)

    def on_checked_x_axes_label(self, event):
        cb = event.GetEventObject()
        self.x_label_color_cs.Enable(cb.Get3StateValue())

    def on_checked_y_axes_label(self, event):
        cb = event.GetEventObject()
        self.y_label_color_cs.Enable(cb.Get3StateValue())

    def g_spines_colors(self):
        top = c_color(self.clr_top_sp.GetValue())
        bottom = c_color(self.clr_bottom_sp.GetValue())
        left = c_color(self.clr_left_sp.GetValue())
        right = c_color(self.clr_right_sp.GetValue())
        return top, bottom, right, left

    def g_grid_conf(self):
        v = self.ch.GetValue()
        o = TYPES_GRID[self.cho.GetSelection()]
        w = self.g_linewidth.GetValue()
        c = c_color(self.g_color.GetValue())
        ac = self.g_color_alpha.GetValue()
        return v, o, w, c, ac

    def g_axes_labels(self):
        x = self.x_ch.GetValue()
        xc = c_color(self.x_label_color_cs.GetValue())
        y = self.y_ch.GetValue()
        yc = c_color(self.y_label_color_cs.GetValue())
        return x, y, xc, yc


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
        # figure facecolor; 0.75 is scalar gray
        self.facecolor = c_color(wx.Colour(255, 255, 255))

        # the left side of the subplots of the figure
        self.subplot_left = 0.08
        # the right side of the subplots of the figure
        self.subplot_right = 0.92
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

        # ---- colores border o spines
        self.color_top_spine = c_color(wx.Colour(221, 221, 221))
        self.color_bottom_spine = c_color(wx.Colour(221, 221, 221))
        self.color_left_spine = c_color(wx.Colour(221, 221, 221))
        self.color_right_spine = c_color(wx.Colour(221, 221, 221))

        # ---- axis value and label
        self.x_axis_show = True
        self.y_axis_show = True
        self.x_axis_color = c_color(wx.Colour(0, 0, 0))
        self.y_axis_color = c_color(wx.Colour(0, 0, 0))

        self.x_axis_label = ''
        self.y_axis_label = ''
        self.x_color_label = c_color(wx.Colour(96, 96, 96))
        self.y_color_label = c_color(wx.Colour(96, 96, 96))

        # ---- legends
        self.legend_show = True
        self.legend_loc = 'upper left'
        self.legend_size = 9
        self.legend_edge_color = c_color(wx.Colour(221, 221, 221))

        # ---- ticks
        self.xticks = None
        self.yticks = None

        # ---- lines
        self.axvlines = True
        self.axv_line_width = 1
        self.axv_line_color = c_color(wx.Colour(221, 221, 221))

        # ---- grilla
        self.grid_lines = False
        self.grid_lines_style = ':'
        self.grid_linewidth = 0.5
        self.grid_color = c_color(wx.Colour(0, 0, 0))
        self.grid_color_alpha = 1.0     # transparency, between 0.0 and 1.0

        # ---- lista de columnas - nombres de variables
        self.cols = None
        self.color = None


def c_color(wx_color):
    return wx_color.GetAsString(wx.C2S_HTML_SYNTAX)


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
