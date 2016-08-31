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
# Creado:  18/2/2016                                         ###
#                                                            ###
# ##############################################################
'''
from bd.entity import Result, Iteration, Individual
from exception.tava_exception import ParserError
from resources.tava_path import tava_base_name


# cabeceras de archivo tava
RESULTNAME = '*RESULTNAME:'
ALGORITHMS = '*ALGORITHMS:'
NOTES = '*NOTES:'
RUNSSTORE = '*RUNSSTORE:'
MAXPOPULATION = '*POPULATIONMAX:'
OBJECTIVESNAMES = '*OBJECTIVESNAMES:'
VARIABLESNAMES = '*VARIABLESNAMES:'
OBJECTIVES = '*OBJECTIVES:'
VARIABLES = '*VARIABLES:'

# cabeceras de iteraciones archivo tava
IDITERATION = '*IDITERATION:'
TIMEPROCESS = '*TIMEPROCESS:'
INDIVIDUAL = '*INDIVIDUAL:'


class TavaFileToResult():
    '''

    '''

    def __init__(self, f_tava):
        self.result = Result()
        self.c_line = 0
        self.all_headers = {}
        self.f_tava = f_tava
        self.size_header = 0
        pass

    def make_parsing(self):

        try:
            self.header_processing()
            self.add_atributes()
            self.add_iterations()
        except IOError as ioerror:
            self.value_error("Error IOError: {0}".format(ioerror))
        except IndexError as indexerror:
            self.value_error("Error IndexError: {0}".format(indexerror))
        except ValueError as valueerror:
            self.value_error("Error ValueError: {0}".format(valueerror))
        except Exception as e:
            self.value_error("Error Exception: {0}".format(e))

    def add_iterations(self):

        with open(self.f_tava, 'r') as f_tava:

            # lectura de cabeceras no necesarias
            self.c_line = self.size_header-3
            [f_tava.readline() for _ in range(self.size_header-3)]

            # iteraciones
            _its = []
            for _ in range(self.result.runstore):
                i_h = []
                self.c_line += 1
                i_h.append(f_tava.readline())
                self.c_line += 1
                i_h.append(f_tava.readline())
                self.c_line += 1
                i_h.append(f_tava.readline())

                _h = [h.strip().split(':') for h in i_h]

                # atributos
                _it = Iteration()
                _it.number = int(_h[0][1])
                _it.individual = int(_h[1][1])
                _it.run_time = float(_h[2][1])

                # individuos
                _ins = []
                for i_num in range(_it.individual):
                    self.c_line += 1
                    o, v, d = self.g_individuals(f_tava.readline().strip())

                    # atributos
                    _in = Individual()
                    _in.number = i_num + 1
                    _in.objectives = o
                    _in.variables = v
                    _in.var_dtlz = d
                    _ins.append(_in)

                _it.individuals = _ins
                _its.append(_it)

            self.result.iterations = _its

    def g_individuals(self, str_indi):
        '''
        Verifica que los valores o individuos cumplen con los tipos de datos
        necesarios.

        :param str_indi:
        :type str_indi:
        '''
        str_o, str_v, str_z = str_indi.split(';')

        # prueba de objetivos
        try:
            [float(o) for o in str_o.split(',')]
        except:
            _obj = [str(float.fromhex(o)) for o in str_o.split(',')]
            str_o = ','.join(_obj)

        # prueba de variables
        try:
            [float(v) for v in str_v.split(',')]
        except:
            _var = [str(float.fromhex(v)) for v in str_v.split(',')]
            str_v = ','.join(_var)

        # prueba de dtlz
        try:
            str_z = float(str_z)
        except:
            str_z = float.fromhex(str_z)

        return str_o, str_v, str_z

    def header_processing(self):
        with open(self.f_tava, 'r') as f_tava:

            # extrayendo cabecera

            self.c_line += 1
            lineread = f_tava.readline().strip()
            while lineread[0] == '*':
                self.size_header += 1
                # ValueError: too many values to unpack
                key, value = lineread.split(':')
                self.all_headers[key+':'] = value
                self.c_line += 1
                lineread = f_tava.readline().strip()

            # comprobando minima cantidad de cabeceras
            if self.size_header < 6:
                raise ParserError(self.f_tava,
                                  'Faltan minimas obligatorias')

            # comprobando cabeceras obligatorias
            for value in [RUNSSTORE, OBJECTIVES, VARIABLES]:
                if not(value in self.all_headers.keys()):
                    raise ParserError(self.f_tava,
                                      'Faltan cabeceras obligatorias')

            # comprobando cabeceras obligatorias
            for value in [IDITERATION, INDIVIDUAL, TIMEPROCESS]:
                if not(value in self.all_headers.keys()):
                    raise ParserError(self.f_tava,
                                      'Faltan cabeceras obligatorias')

    def add_atributes(self):
        all_headers = self.all_headers
        # atributos, obligatorios
        self.result.runstore = int(all_headers[RUNSSTORE])
        self.result.objectives = int(all_headers[OBJECTIVES])
        self.result.variables = int(all_headers[VARIABLES])

        # atributos, calculados si no encontrados
        if RESULTNAME in all_headers.keys():
            self.result.name = all_headers[RESULTNAME]
            self.result.alias = all_headers[RESULTNAME]
        else:
            self.result.name = tava_base_name(self.f_tava)
            self.result.alias = tava_base_name(self.f_tava)

        if OBJECTIVESNAMES in all_headers.keys():
            self.result.name_objectives = all_headers[OBJECTIVESNAMES]
        else:
            c = self.result.objectives
            n_objs = ','.join(['O'+str(i+1) for i in range(c)])
            self.result.name_objectives = n_objs

        if VARIABLESNAMES in all_headers.keys():
            self.result.name_variables = all_headers[VARIABLESNAMES]
        else:
            c = self.result.objectives
            n_vars = ','.join(['V'+str(i+1) for i in range(c)])
            self.result.name_variables = n_vars

        # atributos, opcionales
        if NOTES in all_headers.keys():
            self.result.notes = all_headers[NOTES]
        if ALGORITHMS in all_headers.keys():
            self.result.algorithms = all_headers[ALGORITHMS]
        if MAXPOPULATION in all_headers.keys():
            self.result.populationmax = int(all_headers[MAXPOPULATION])

    def value_error(self, message):
        raise ParserError(self.f_tava, 'message', self.c_line)
