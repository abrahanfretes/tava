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

from bd.entity import Project
from exception.tava_exception import PreParserError, ParserError
from models.mproject import ProjectM
from models.mresult import ResultModel
from parser.preparser import VonToTavaParser
from parser.tavaparser import TavaFileToResult
from resources.tava_path import tava_dir_parsed, tava_dir_temp


FORMAT_TAVA = 0
FORMAT_OBJETIVE = 1


class MainFrameP(object):

    '''
    classdocs
    '''

    def __init__(self, iview):
        '''
        Constructor
        '''
        self.dir_parser = tava_dir_parsed(tava_dir_temp())
        self.iview = iview

    def add_project(self, name):
        project = ProjectM().add(Project(name))
        return project

    def add_results_by_project(self, project, path_files, t_format, dlg=None):

        results = []
        parse_correct = []
        parse_error = []

        if FORMAT_TAVA == t_format:

            files_von_parsed = []

            # parsear archivos
            _all = len(path_files)

            for i, p in enumerate(path_files):
                m_initial = 'Formateando archivo:' + str(i+1)+'/'+str(_all)
                m_initial = m_initial + '\narchivo:' + p[1] + '\n'
                keepGoing = dlg.UpdatePulse(m_initial)
                try:
                    keepGoing = dlg.UpdatePulse(m_initial + 'iniciando')
                    vtot = VonToTavaParser(p[0], self.dir_parser)
                    keepGoing = dlg.UpdatePulse(m_initial + 'formateando...')
                    file_parsed = vtot.make_preparsing()
                    keepGoing = dlg.UpdatePulse(m_initial + 'terminado')

                except PreParserError as preherror:
                    keepGoing = dlg.UpdatePulse("Error de formato" + '\narchivo:' + p[1])
                    parse_error.append(preherror)
                else:
                    files_von_parsed.append(file_parsed)

            keepGoing = dlg.UpdatePulse('Todos los arcivos Parseados')
            # crear resultdos a partir de archivos preparseados
            for i, tava_file in enumerate(files_von_parsed):
                try:
                    m_initial = 'Parseando archivo:' + str(i+1)+'/'+str(_all)
                    keepGoing = dlg.UpdatePulse(m_initial + '\niniciando')
                    tfr = TavaFileToResult(tava_file)
                    keepGoing = dlg.UpdatePulse(m_initial + '\nformateando...')
                    tfr.make_parsing()
                    keepGoing = dlg.UpdatePulse(m_initial + '\nterminado')
                except ParserError as parseerror:
                    keepGoing = dlg.UpdatePulse("Error de parseo" + '\narchivo:'+tava_file)
                    parse_error.append(preherror)
                else:
                    try:
                        # agrega a la base de datos
                        m_initial = 'Agregando a Base de Datos:' + str(i+1)+'/'+str(_all)
                        keepGoing = dlg.UpdatePulse(m_initial + '\niniciando')
                        tfr.result.project_id = project.id
                        keepGoing = dlg.UpdatePulse(m_initial + '\nagregando...')
                        result = ResultModel().add(tfr.result)
                        keepGoing = dlg.UpdatePulse(m_initial + '\nterminado')
                    except Exception as e:
                        keepGoing = dlg.UpdatePulse("Error al agregar en Base de Datos"+
                                                    '\narchivo:'+tava_file)
                        p_e = ParserError(tava_file,
                                          "Error Exception: {0}".format(e),
                                          None)
                        print('Error', p_e)
                        parse_error.append(p_e)
                    else:
                        results.append(result)
                        parse_correct.append(object)

        elif FORMAT_OBJETIVE == t_format:

            # crear resultdos a partir de archivos preparseados
            for tava_file in path_files:
                try:
                    tfr = TavaFileToResult(tava_file)
                    tfr.make_parsing()
                except ParserError as parseerror:
                    print('Error', parseerror)
                    parse_error[tava_file] = parseerror
                else:
                    try:
                        # agrega a la base de datos
                        tfr.result.project_id = project.id
                        result = ResultModel().add(tfr.result)
                    except Exception as e:
                        p_e = ParserError(tava_file,
                                          "Error Exception: {0}".format(e),
                                          None)
                        print('Error', p_e)
                        parse_error[tava_file] = p_e
                    else:
                        results.append(result)
                        parse_correct.append(object)

        return results
