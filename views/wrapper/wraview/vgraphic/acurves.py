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
from pandas.tools.plotting import andrews_curves

from views.wrapper.wraview.vgraphic.fuse import square_plot


# #######################################################################
#        GRÁFICO - CURVA DE ANDREWS
# #######################################################################
def k_andrews_curves(dframes, class_column='Name', fig=None,
                     subplot=False, grayscale=False, fill=False,
                     alpha=0.15, legend=True, one_d=False):

    # figures
    if fig is None:
        fig = Figure()

    s_row, s_col = square_plot(len(dframes))

    for i in range(len(dframes)):
        ax = fig.add_subplot(s_row, s_col, i + 1)
        andrews_curves(dframes[i], class_column, ax=ax)

    return fig
