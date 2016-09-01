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
from wx.lib.pubsub import Publisher as pub
from languages import topic as T

from models.mproject import ProjectM as pm


class TTreeP(object):
    '''
    classdocs
    '''

    def __init__(self, iview):
        '''
        Constructor
        '''
        pub().subscribe(self.add_project_in_tree, T.ADD_PROJECT_IN_TREE)
        pub().subscribe(self.add_view_in_tree, T.ADD_VIEW_IN_TREE)

        self.iview = iview
        self.init_tree()

    def init_tree(self):

        # proyectos abiertos
        for project in pm().state_open():
            item_p = self.iview.add_open_project(project)
            self.add_packages_item(item_p, project)

        # proyectos cerrados
        for project in pm().state_close():
            self.iview.add_closed_project(project)

    def add_packages_item(self, item_project, project):

        # Agregar los archivos resultados del proyecto
        pfile = PackageFile(project.pack_file, project)
        pack_file = self.iview.add_package_files(item_project, pfile)

        for r in project.results:
            self.iview.add_results(pack_file, r)

        # Agregar vistas del proyecto
        pview = PackageView(project.pack_view, project)
        pack_view = self.iview.add_package_views(item_project, pview)

        for v in project.views:
            self.iview.add_views(pack_view, v)

        return pack_file, pack_view

    # --- add new project in tree ------------------------------------
    def add_project_in_tree(self, message):
        project = message.data
        # self.init_vars()
        # pub.sendMessage(T.TYPE_CHANGED_SELECTED_PROJECT, 4)

        item_p = self.iview.add_open_project(project)
        self.add_packages_item(item_p, project)
        self.iview.ExpandAllChildren(item_p)

    def add_view_in_tree(self, message):
        new_view = message.data
        self.iview.add_views(self.iview.c_item, new_view)
        self.iview.Expand(self.iview.c_item)


class PackageFile():
    def __init__(self, state, project):
        self.state = state
        self.project = project
    pass


class PackageView():
    def __init__(self, state, project):
        self.state = state
        self.project = project
    pass
