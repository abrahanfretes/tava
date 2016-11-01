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

from pandas.tools.plotting import radviz
from views.wrapper.wraview.vgraphic.fuse import square_plot


# #######################################################################
#        GRÁFICO - RadViz
# #######################################################################
def _radviz(frame, ax, ax_conf, class_column, color_values=None):

    radviz(frame, class_column, ax=ax, color=color_values)

    # ---- configuración de leyenda
    if ax_conf.legend_show:
        _c = ax_conf.legend_edge_color
        ax.legend(prop={'size': ax_conf.legend_size},
                  loc=ax_conf.legend_loc).get_frame().set_edgecolor(_c)

    # ---- configuración de tick - visualización, labels, colors

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


def kradviz(dframes, class_column, fig, ax_conf, colors):

    s_row, s_col = square_plot(len(dframes))
    for i, df in enumerate(dframes):
        ax = fig.add_subplot(s_row, s_col, i + 1)
        _radviz(df, ax, ax_conf, class_column, colors[i])

    return fig
