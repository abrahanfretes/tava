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

from matplotlib.figure import Figure
from pandas.compat import lrange
from pandas.core import common as com
from pandas.tools.plotting import _get_standard_colors
from views.wrapper.vdialog.vfigured import AxesConfig, FigureConfig

import numpy as np
from views.wrapper.wraview.vgraphic.fuse import square_plot


#     Parameters
#     ----------
#     frame: DataFrame
#     class_column: str
#         Column name containing class names
#     cols: list, optional
#         A list of column names to use
#     ax: matplotlib.axis, optional
#         matplotlib axis object
#     color: list or tuple, optional
#         Colors to use for the different classes
#     use_columns: bool, optional
#         If true, columns will be used as xticks
#     xticks: list or tuple, optional
#         A list of values to use for xticks
#     colormap: str or matplotlib colormap, default None
#         Colormap to use for line colors.
#     axvlines: bool, optional
#         If true, vertical lines will be added at each xtick
#     kwds: keywords
#         Options to pass to matplotlib plotting method
# 
#     Returns
#     -------
#     ax: matplotlib axis object
# 
#     Examples
#     --------
#     >>> from pandas import read_csv
#     >>> from pandas.tools.plotting import parallel_coordinates
#     >>> from matplotlib import pyplot as plt
#     >>> df = read_csv('https://raw.github.com/
#     >>> pydata/pandas/master/pandas/tests/data/iris.csv')
#     >>> parallel_coordinates(df, 'Name',
#     >>> color=('#556270', '#4ECDC4', '#C7F464'))
#     >>> plt.show()


# #######################################################################
#        GRÁFICO - COORDENADAS PARALELAS
# #######################################################################
# def k_cp(frame, class_column, cols=None, ax=None, color=None,
#          use_columns=False, xticks=None, colormap=None, axvlines=True,
#          u_legend=True, u_grid=True, _xaxis=True, _yaxis=True, one_color=False,
#          klinewidth=1, klinecolor='black', _loc='upper right', **kwds):


def k_cp(frame, ax, ax_conf, class_column, **kwds):
    """Parallel coordinates plotting.
    """
    # import matplotlib.pyplot as plt

    # ---- varaibles globales
    n = len(frame)
    classes = frame[class_column].drop_duplicates()
    class_col = frame[class_column]

    # ---- usar columnas personalizada o predeterminada
    if ax_conf.cols is None:
        df = frame.drop(class_column, axis=1)
    else:
        df = frame[ax_conf.cols]

    # ---- cantidad de columnas de datos
    ncols = len(df.columns)

    # ---- determina valor para  xticks
    if ax_conf.xticks is not None:
        if not np.all(np.isreal(ax_conf.xticks)):
            raise ValueError('xticks specified must be numeric')
        elif len(ax_conf.xticks) != ncols:
            raise ValueError('Length of xticks must ' +
                             'match number of columns')
        x = ax_conf.xticks
    else:
        x = lrange(ncols)

    # ---- selección de colores - automático/personalizado
    color_values = g_colors(len(classes), ax_conf.color)
    colors = dict(zip(classes, color_values))

    # ---- creación de leyenda por valor
    used_legends = set([])

    for i in range(n):
        y = df.iloc[i].values
        kls = class_col.iat[i]
        label = com.pprint_thing(kls)
        if label not in used_legends:
            used_legends.add(label)
            ax.plot(x, y, color=colors[kls], label=label, **kwds)
        else:
            ax.plot(x, y, color=colors[kls], **kwds)

        # for i in y: ------------------------------------------------------
        # ax.axhline(i, linewidth=klinewidth, color=klinecolor) ------------

    if ax_conf.axvlines:
        for i in x:
            ax.axvline(i, linewidth=ax_conf.axv_line_width,
                       color=ax_conf.axv_line_color)

    # ---- configuración de tick - visualización, labels, colors
    ax.set_xticks(x)
    ax.set_xticklabels(df.columns)
    ax.set_xlim(x[0], x[-1])
    ax.get_xaxis().set_visible(ax_conf.x_axis_show)
    ax.get_yaxis().set_visible(ax_conf.y_axis_show)
    ax.tick_params(axis='x', colors=ax_conf.x_axis_color)
    ax.tick_params(axis='y', colors=ax_conf.y_axis_color)

    ax.set_xlabel(ax_conf.x_axis_label, labelpad=-1)
    ax.xaxis.label.set_color(ax_conf.x_color_label)

    ax.set_ylabel(ax_conf.y_axis_label, labelpad=-1)
    ax.yaxis.label.set_color(ax_conf.y_color_label)

    # configuración de spines

    ax.spines['top'].set_color(ax_conf.color_top_spine)
    ax.spines['bottom'].set_color(ax_conf.color_bottom_spine)
    ax.spines['left'].set_color(ax_conf.color_left_spine)
    ax.spines['right'].set_color(ax_conf.color_right_spine)

    # ---- configuración de leyenda
    if ax_conf.legend_show:
        _c = ax_conf.legend_edge_color
        ax.legend(prop={'size': ax_conf.legend_size},
                  loc=ax_conf.legend_loc).get_frame().set_edgecolor(_c)

    # ---- configuración de grid
    if ax_conf.grid_lines:
        ax.grid(color=ax_conf.grid_color, linestyle=ax_conf.grid_lines_style,
                linewidth=ax_conf.grid_linewidth,
                alpha=ax_conf.grid_color_alpha)

    return ax


def g_colors(count, color):
    color_values = _get_standard_colors(count, None, 'random', color)
    return color_values


def g_colors_old(classes, colormap, color, one_color):

    if one_color:
        color_values = _get_standard_colors(num_colors=1,
                                            colormap=colormap,
                                            color_type='random', color=color)
        color_values = color_values * len(classes)
    else:
        color_values = _get_standard_colors(num_colors=len(classes),
                                            colormap=colormap,
                                            color_type='random', color=color)
    return color_values


def set_axes_config(ax, ax_conf, label=None):
    ax.spines['top'].set_color(ax_conf.color_top_spine)
    ax.spines['bottom'].set_color(ax_conf.color_bottom_spine)
    ax.spines['left'].set_color(ax_conf.color_left_spine)
    ax.spines['right'].set_color(ax_conf.color_right_spine)
    if label is not None:
        ax.set_xlabel(label, labelpad=-1)
        ax.xaxis.label.set_color('#606060')
        ax.tick_params(axis='x', colors='w')
    return ax


def set_figure_config(fig, fig_config):
    fig.set_figwidth(fig_config.width)
    fig.set_figheight(fig_config.height)

    fig.subplots_adjust(top=fig_config.subplot_top,
                        bottom=fig_config.subplot_bottom,
                        left=fig_config.subplot_left,
                        right=fig_config.subplot_right,
                        wspace=fig_config.subplot_wspace,
                        hspace=fig_config.subplot_hspace)


# def k_parallel_coordinates(dframes, class_column='Name', fig=None,
#                            ax_conf=None, fig_config=None, subplot=False,
#                            grayscale=False, fill=False, axvlines=True,
#                            legend=True, one_d=False, u_grid=True, alpha=0.15,
#                            _xaxis=True, _yaxis=True):


def k_parallel_coordinates(dframes, class_column, fig, ax_conf, fg_conf):

    # set_figure_config(fig, fig_config)

#     legend = ax_conf.legend_show

    # ---- cantidad de subplot necesarias - filas y columnas.
    # ---- busca el cuadrado de los dos
    s_row, s_col = square_plot(len(dframes), False)

    for i, df in enumerate(dframes):
        ax = fig.add_subplot(s_row, s_col, i + 1)
        k_cp(df, ax, ax_conf, class_column)

#         k_cp(dframes[i], class_column, ax=ax, axvlines=False,
#              u_legend=legend, u_grid=u_grid, _xaxis=_xaxis, _yaxis=_yaxis)
# 
#         k_cp(dframes[i], class_column, ax=ax, u_legend=legend, u_grid=False,
#              _xaxis=False, one_color=False, _loc='upper left',
#              _yaxis=True, klinewidth=0.3, klinecolor='#DDDDDD')
# 
#         ax = set_axes_config(ax, ax_conf)
#         if legend:
#             ax.legend(prop={'size': 9}, loc=ax_conf.legend_loc).get_frame() \
#                                     .set_edgecolor('#DDDDDD')

    return fig
