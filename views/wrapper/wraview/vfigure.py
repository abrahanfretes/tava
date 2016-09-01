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
# Creado:  1/9/2016                                        ###
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

        sizer_tool = wx.BoxSizer(wx.HORIZONTAL)
        self.toolbar = Toolbar(self.canvas)
        self.toolbar.Realize()
        self.generate_cluster = wx.Button(self, -1, 'Clusterizar Datos')
        self.generate_cluster.Disable()
        self.generate_cluster.Bind(wx.EVT_BUTTON, self.on_show_clusters)
        sizer_tool.Add(self.toolbar, 0)
        sizer_tool.Add(self.generate_cluster, 0)

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
            self.fig = k_parallel_coordinates(dframes, 'Name', self.fig, legend=True)
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

        self.key_figure = key_figure
        self.generate_cluster.Disable()
        if self.dframes != []:
            self.generate_cluster.Enable()

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

        GenerateCluster(self.GrandParent, self)

        #------------------------------------------------------ if self.c_shape:
            #----- k_shape_frame.append(K_shape(self.dframes[0], self.c_number))
#------------------------------------------------------------------------------ 
        #----------------------------------------------------- if self.c_kmenas:
            #---- k_shape_frame.append(k_kmeans(self.dframes[0], self.c_number))

        if k_shape_frame != []:
            self.kdraw(k_shape_frame, self.key_figure)


class GenerateCluster(wx.Dialog):

    def __init__(self, gran_parent, parent):
        wx.Dialog.__init__(self, gran_parent, size=(400, 300),
                           title='Generar Clusters')
        self.parent = parent
        self.init_ui()

        # ------ Definiciones iniciales -----

        self.Centre(wx.BOTH)
        self.CenterOnScreen()
        self.ShowModal()

    def init_ui(self):

        sizer = wx.BoxSizer(wx.VERTICAL)

        self.cb_shape = wx.CheckBox(self, -1, "Shape")
        self.cb_shape.SetValue(self.parent.shape_value)

        self.cb_kmeans = wx.CheckBox(self, -1, "K-means")
        self.cb_kmeans.SetValue(self.parent.kmeans_value)

        self.sc_clusters = wx.SpinCtrl(self, -1, "", (30, 50))
        self.sc_clusters.SetRange(2, 100)
        self.sc_clusters.SetValue(2)

        self.cb_shape.Bind(wx.EVT_CHECKBOX, self.on_cluster_ckeck)
        self.cb_kmeans.Bind(wx.EVT_CHECKBOX, self.on_cluster_ckeck)

        # buttons confirmar, cancelar
        sizer_button = wx.BoxSizer(wx.HORIZONTAL)
        sizer_cancel = wx.BoxSizer()
        self.cancel = wx.Button(self, -1, 'Cancelar')
        self.cancel.SetDefault()
        sizer_cancel.Add(self.cancel)
        sizer_apply = wx.BoxSizer()
        self.apply = wx.Button(self, -1, 'Aplicar')
        sizer_apply.Add(self.apply, 0, wx.ALIGN_RIGHT)

        sizer_button.Add(sizer_cancel, 0, wx.ALL, 5)
        sizer_button.Add(sizer_apply, 0, wx.ALL, 5)

        sizer.Add(self.cb_shape, 0, wx.ALL, 5)
        sizer.Add(self.cb_kmeans, 0, wx.ALL, 5)
        sizer.Add(self.sc_clusters, 0, wx.ALL, 5)
        sizer.Add(sizer_button, 0, wx.EXPAND | wx.LEFT, 100)

        self.SetSizer(sizer)

        self.Bind(wx.EVT_BUTTON, self.on_button_apply, self.apply)
        self.Bind(wx.EVT_BUTTON, self.on_button_cancel, self.cancel)

    def on_button_cancel(self, event):
        self.parent.c_shape = False
        self.parent.c_kmenas = False
        self.Close()

    def on_button_apply(self, event):
        self.parent.c_shape = self.cb_shape.IsChecked()
        self.parent.c_kmenas = self.cb_kmeans.IsChecked()
        self.parent.c_number = self.sc_clusters.GetValue()

        self.Close()

    def on_key_escape(self, event):
        if event.GetKeyCode() == wx.WXK_ESCAPE:
            self.parent.c_shape = False
            self.parent.c_kmenas = False
            self.Close()

    def on_cluster_ckeck(self, event):
        self.apply.Disable()
        self.cancel.SetDefault()

        if self.cb_shape.IsChecked():
            self.parent.shape_value = True
            self.apply.Enable()
            self.apply.SetDefault()

        if self.cb_kmeans.IsChecked():
            self.parent.kmeans_value = True
            self.apply.Enable()
            self.apply.SetDefault()

        if not self.cb_shape.IsChecked():
            self.parent.shape_value = False

        if not self.cb_kmeans.IsChecked():
            self.parent.kmeans_value = False
