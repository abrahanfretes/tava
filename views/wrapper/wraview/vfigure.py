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
import wx

import numpy as np
from views.wrapper.wraview.vgraphic.acurves import k_andrews_curves
from views.wrapper.wraview.vgraphic.cparallel import k_parallel_coordinates
from views.wrapper.wraview.vgraphic.fuse import g_color
from views.wrapper.wraview.vgraphic.rchart import k_radar_chart
from views.wrapper.wraview.vgraphic.rviz import k_radviz
from imgs.ifigure import settings_fig, play_fig
from views.wrapper.vdialog.vfigured import DialogConfig


K_PARALLEL_COORDENATE = 0
K_ANDREWS_CURVES = 1
K_RADVIZ = 2
K_RADAR_CHART_POLYGON = 3
K_RADAR_CHART_CIRCLE = 4
K_SCATTER_MATRIX = 5
K_SOM = 6
K_HITMAP = 7


class FigurePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour('#DCE5EE')

        self.control_panel = None
        self.dframes = []
        self.key_figure = 1

        self.kmeans_value = True
        self.shape_value = True

        self.fig = Figure()
        self.fig.suptitle('Tava Tool', fontsize=14, fontweight='light',
                          style='italic', family='serif', color='c',
                          horizontalalignment='center',
                          verticalalignment='center')
        self.canvas = FigureCanvas(self, -1, self.fig)

        # toolbar
        sizer_tool = wx.BoxSizer(wx.HORIZONTAL)

        b_play = wx.BitmapButton(self, style=wx.NO_BORDER,
                                 bitmap=play_fig.GetBitmap())
        sizer_tool.Add(b_play, flag=wx.ALIGN_CENTER_VERTICAL)
        b_play.Bind(wx.EVT_BUTTON, self.on_play)

#       Boton de configuracion
        b_setting = wx.BitmapButton(self, style=wx.NO_BORDER,
                                    bitmap=settings_fig.GetBitmap())
        sizer_tool.Add(b_setting, flag=wx.ALIGN_CENTER_VERTICAL)
        b_setting.Bind(wx.EVT_BUTTON, self.on_config)

        self.toolbar = Toolbar(self.canvas)
        self.toolbar.Realize()
        self.toolbar.SetBackgroundColour('#DCE5EE')
        sizer_tool.Add(self.toolbar, 0, wx.ALIGN_CENTER_VERTICAL)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(sizer_tool, 0, wx.EXPAND)
        self.sizer.Add(self.canvas, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
        self.Fit()
        self._welcome()

    def _welcome(self):
        Axes3D(self.fig)

    def kdraw(self, dframes, key_figure):

        self.dframes = dframes
        self.key_figure = key_figure
        # actualización de figura
        self.fig.clear()

        if key_figure == K_PARALLEL_COORDENATE:
            self.fig = k_parallel_coordinates(dframes, 'Name', self.fig,
                                              legend=True)
        elif key_figure == K_ANDREWS_CURVES:
            self.fig = k_andrews_curves(dframes, 'Name', self.fig)
        elif key_figure == K_RADVIZ:
            self.fig = k_radviz(dframes, 'Name', self.fig)
        elif key_figure == K_RADAR_CHART_CIRCLE:
            self.fig = k_radar_chart(dframes, 'Name', fig=self.fig)
        elif key_figure == K_RADAR_CHART_POLYGON:
            self.fig = k_radar_chart(dframes, 'Name', fig=self.fig,
                                     frame='polygon')
        elif key_figure == K_SCATTER_MATRIX:
            print 'scatter_matrix selected'
            # scatter_matrix(dframes.drop('Name', 1), ax=axe, diagonal='kde')
        elif key_figure == K_SOM:
            print 'SOM selected'
        elif key_figure == K_HITMAP:
            print 'HITMAT selected'
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
            x = [0]*_len
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
        DialogConfig(self)
