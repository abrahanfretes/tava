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

from pandas.tools.plotting import _get_standard_colors
import numpy as np


def square_plot(plots, cc=True):
    s_col = 1
    s_row = 1
    while (s_col*s_row) < plots:
        if cc:
            s_col += 1
            cc = False
        else:
            s_row += 1
            cc = True
    return s_row, s_col


def g_color(count, grayscale=False):
    if not grayscale:
        return _get_standard_colors(num_colors=count, color_type='random')
    else:
        return [str(i) for i in np.linspace(0.55555, 0.999999999999, count)]
