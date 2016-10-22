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
# Creado:  1/9/2016                                          ###
#                                                            ###
# ##############################################################
'''

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2Wx as Toolbar
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
from wx import GetTranslation as L
import wx
from wx.lib.pubsub import Publisher as pub

from imgs.ifigure import settings_fig, play_fig
from languages import topic as T
import numpy as np
from views.wrapper.vdialog.vfigured import FigureConfigDialog, AxesConfig, \
                                           FigureConfig, RadarChadConfig
from views.wrapper.wraview.vgraphic.cparallel import k_parallel_coordinates
from views.wrapper.wraview.vgraphic.fuse import g_color
from views.wrapper.wraview.vgraphic.rchart import k_radar_chart
from views.wrapper.wraview.vgraphic.rviz import k_radviz


K_PARALLEL_COORDENATE = 0
K_RADAR_CHART_POLYGON = 1
K_RADVIZ = 2
K_ANDREWS_CURVES = 3
K_RADAR_CHART_CIRCLE = 4
K_SCATTER_MATRIX = 5
K_SOM = 6
K_HITMAP = 7


class FigurePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour('#DCE5EE')

        pub().subscribe(self.update_language, T.LANGUAGE_CHANGED)

        self.control_panel = None
        self.dframes = []
        self.key_figure = 1

        self.kmeans_value = True
        self.shape_value = True
        self.figure_config_dialog_ref = None

        # ---- inicialización de figura
        self.fig = Figure()
        self.canvas = FigureCanvas(self, -1, self.fig)

        # ---- configuración de figura
        self.fig_config = FigureConfig()
        self.set_figure_config()

        # ---- configuración de axe
        self.ax_conf = AxesConfig()

        # ---- radar chard config
        self.radar_chard_con = RadarChadConfig()

        # ---- toolbar
        self.sizer_tool = wx.BoxSizer(wx.HORIZONTAL)
        _bitmap = play_fig.GetBitmap()
        self.b_play = wx.BitmapButton(self, -1, _bitmap, style=wx.NO_BORDER)
        self.sizer_tool.Add(self.b_play, flag=wx.ALIGN_CENTER_VERTICAL)
        self.b_play.Bind(wx.EVT_BUTTON, self.on_play)
        self.b_play.SetToolTipString(L('VISUALIZE_DATE_CLUSTER'))
        _bitmap = settings_fig.GetBitmap()
        self.b_setting = wx.BitmapButton(self, -1, _bitmap, style=wx.NO_BORDER)
        self.sizer_tool.Add(self.b_setting, flag=wx.ALIGN_CENTER_VERTICAL)
        self.b_setting.Bind(wx.EVT_BUTTON, self.on_config)
        self.b_setting.SetToolTipString(L('FIGURE_CONF'))

        self.toolbar = Toolbar(self.canvas)
        self.toolbar.Realize()
        self.toolbar.SetBackgroundColour('#DCE5EE')
        self.sizer_tool.Add(self.toolbar, 0, wx.ALIGN_CENTER_VERTICAL)

        choice_grafic = self.get_choice_grafic()
        self.sizer_tool.Add(choice_grafic, wx.ALIGN_LEFT)

        self.prog = wx.Gauge(self, size=(150, 15))
        self.sizer_tool.Add(self.prog, 0, wx.ALIGN_CENTER_VERTICAL)
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_pulse, self.timer)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.sizer_tool, 0, wx.EXPAND)
        self.sizer.Add(self.canvas, 1, wx.EXPAND)

        self.SetSizer(self.sizer)
#         self.Fit()
        self.prog.Hide()
        self._welcome()

    def on_pulse(self, event):
        self.prog.Pulse()

    def _welcome(self):
        Axes3D(self.fig)

    def set_figure_config(self):

        self.fig.set_figwidth(self.fig_config.width)
        self.fig.set_figheight(self.fig_config.height)
        self.fig.set_facecolor(self.fig_config.facecolor)

        left = self.fig_config.subplot_left
        bottom = self.fig_config.subplot_bottom
        right = self.fig_config.subplot_right
        top = self.fig_config.subplot_top
        wspace = self.fig_config.subplot_wspace
        hspace = self.fig_config.subplot_hspace
        self.fig.subplots_adjust(left, bottom, right, top, wspace, hspace)

        self.fig.suptitle('Tava Tool', fontsize=14, fontweight='light',
                          style='italic', family='serif', color='c',
                          horizontalalignment='center',
                          verticalalignment='center')

    def kdraw(self, dframes):

        self.dframes = dframes
        key_figure = self.g_figure()
        self.key_figure = key_figure
        # actualización de figura
        self.fig.clear()

        if key_figure == K_PARALLEL_COORDENATE:
            self.fig = k_parallel_coordinates(dframes, 'Name', self.fig,
                                              self.ax_conf, self.fig_config)
        elif key_figure == K_RADAR_CHART_POLYGON:
            self.fig = k_radar_chart(dframes, 'Name', self.fig,
                                     self.ax_conf, self.radar_chard_con)
        elif key_figure == K_RADVIZ:
            self.fig = k_radviz(dframes, 'Name', self.fig, self.ax_conf)

        self.canvas.draw()

    def kdraw_one(self, list_df, key_figure=1):
        class_column = 'Name'

        df = list_df[0]

        # actualización de figura
        self.fig.clear()
        # axe = self.fig.gca()
        df1 = df.drop(class_column, axis=1)
        _len = len(df1)
        col_names = df1.columns.tolist()
        _len_color = len(col_names)

        if key_figure == key_figure:

            ax = self.fig.add_subplot(1, 1, 1, projection='3d')

            ax.set_color_cycle(g_color(_len_color))
            y = np.linspace(0, 1, _len)
            x = [0] * _len
            ic = 0
            for n in col_names:
                d = df1[n].values.tolist()
                ax.plot(x, y, d, label=n)
                ic += 1
            if True:
                ax.legend()

            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Dtlz')

            self.canvas.draw()

    def on_show_clusters(self, event):

        self.c_shape = False
        self.c_kmenas = False
        self.c_number = 0
        k_shape_frame = []

        if k_shape_frame != []:
            self.kdraw(k_shape_frame, self.key_figure)

    def on_play(self, event):

        self.control_panel.run_fig()
        # obtener datos
        # leer configuracion
        # ver si dibujar cluster o data
        # dibujar
        pass

    def on_config(self, event):
        if self.figure_config_dialog_ref is None:
            self.figure_config_dialog_ref = FigureConfigDialog(self)
        else:
            self.figure_config_dialog_ref.nb.SetSelection(0)
            self.figure_config_dialog_ref.ShowModal()

    def g_figure(self):
        return self.ch_graph.GetSelection()

    def get_choice_grafic(self):
        grid = wx.FlexGridSizer(cols=2)
        sampleList = self.get_item_list()

        self.ch_graph = wx.Choice(self, -1, choices=sampleList)
        self.ch_graph.SetSelection(0)
        self.ch_graph.SetToolTipString(L('SELECT_A_GRAPHIC'))

        grid.Add(self.ch_graph, 0, wx.ALIGN_LEFT | wx.ALL, 5)

        return grid

    def get_item_list(self):
        return [L('PARALLEL_COORDINATES'), 'Radar Chart', 'Radvis']

    def update_language(self, msg):
        s = self.ch_graph.GetSelection()
        self.ch_graph.SetItems(self.get_item_list())
        self.ch_graph.SetSelection(s)
        self.ch_graph.SetToolTipString(L('SELECT_A_GRAPHIC'))
        self.b_setting.SetToolTipString(L('FIGURE_CONF'))
        self.b_play.SetToolTipString(L('VISUALIZE_DATE_CLUSTER'))
