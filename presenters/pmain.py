#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
# ##############################################################
#                                                            ###
# Universidad Nacional de Asunción - Facultad Politécnica    ###
# Ingenieria en Informática - Proyecto Final de Grado        ###
#                                                            ###
# Autores:                                                   ###
#           - Arsenio Ferreira (arse.ferreira@gmail.com)      ###
#           - Abrahan Fretes (abrahan.fretes@gmail.com)      ###
#                                                            ###
# Creado:  30/8/2016                                          ###
#                                                            ###
# ##############################################################
'''
from bd.entity import Project
from models.mproject import ProjectM


class MainFrameP(object):

    '''
    classdocs
    '''

    def __init__(self, iview):
        '''
        Constructor
        '''

    def add_project(self, name, path_files, t_format):
        project = ProjectM().add(Project(name))
        return project
