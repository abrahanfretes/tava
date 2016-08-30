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
# Creado:  30/8/2016                                         ###
#                                                            ###
# ##############################################################
'''

import wx
import os
from imgs.iproject import execute_bit, help32x32_bit, error_bit
from wx import GetTranslation as L


wildcard = "Files results |*"
FILES_FORMATS = ['Von Tava', 'Tava']


class NewProject(wx.Dialog):
    def __init__(self, parent, add_result=False):
        wx.Dialog.__init__(self, parent, size=(700, 630))

        self.error_name = True
        self.add_result = add_result
        self.parent = parent

        self.existing_names = []
        self.hidden_names = []
        self.path_files = []
        self.InitUI()
        self.create.Disable()
        if add_result:
            self.add_only_results()
        self.Centre()
        self.ShowModal()

    def InitUI(self):

        # ------ variables principales --------------------------------------
        panel = wx.Panel(self)
        sizer = wx.GridBagSizer(8, 5)

        # ------ Titulo de Proyecto Tava ------------------------------------
        font_title = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font_title.SetWeight(wx.BOLD)
        font_title.SetPointSize(14)
        title1 = wx.StaticText(panel, label=L('NEW_PROJECT_TITLE'))
        title1.SetFont(font_title)

        exec_bmp = wx.StaticBitmap(panel)

        sizer.Add(title1, pos=(0, 0), flag=wx.LEFT | wx.TOP |
                  wx.ALIGN_LEFT, border=10)
        sizer.Add(exec_bmp, pos=(0, 4), flag=wx.ALIGN_CENTER)

        # ------ Texto Descriptivo que cambia --------------------------------
        des_box = wx.BoxSizer(wx.HORIZONTAL)

        font_description = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font_description.SetPointSize(9)
        self.alert_text = wx.StaticText(panel)
        self.alert_text.SetFont(font_description)
        self.alert_text.SetLabel(L('NEW_PROJECT_ENTER_NAME'))

        self.alert_bmp = wx.StaticBitmap(panel)
        self.alert_bmp.SetBitmap(execute_bit.GetBitmap())

        des_box.Add(self.alert_bmp, flag=wx.ALIGN_LEFT | wx.RIGHT, border=5)
        des_box.Add(self.alert_text, flag=wx.ALIGN_LEFT)

        sizer.Add(des_box, pos=(1, 0), span=(1, 3), flag=wx.LEFT, border=10)

        # ------ linea estática horizontal -----------------------------------
        line = wx.StaticLine(panel)
        sizer.Add(line, pos=(2, 0), span=(1, 5), flag=wx.EXPAND |
                  wx.ALIGN_TOP | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=10)

        # ------ Texto para nombre de proyecto ------------------------------
        label = wx.StaticText(panel, label=L('NEW_PROJECT_NAME'))

        sizer.Add(label, pos=(3, 0), flag=wx.ALIGN_CENTER_HORIZONTAL |
                  wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

        self.name = wx.TextCtrl(panel)
        self.name.SetBackgroundColour((255, 255, 255))
        self.name.Bind(wx.EVT_KEY_UP, self.on_key_up)
        self.name.SetFocus()

        sizer.Add(self.name, pos=(3, 1), span=(1, 4),
                  flag=wx.EXPAND | wx.RIGHT, border=10)

        # ------ Agregacion de archivo  (x, y)-------------------------------
        sb = wx.StaticBox(panel, label=L('FILE_STATIC_LABEL'))
        boxsizer = wx.StaticBoxSizer(sb, wx.VERTICAL)

        # boton para busqueda (1)
        browse = wx.Button(panel, -1, L('FILE_BUTTON_BROWSER'))
        self.Bind(wx.EVT_BUTTON, self.OnButtonBrowse, browse)
        boxsizer.Add(browse, flag=wx.ALIGN_LEFT | wx.TOP | wx.BOTTOM, border=5)

        # grilla de archivos (2)
        import wx.dataview as dv
        self.dvlc = dv.DataViewListCtrl(panel, size=(400, 298))
        self.dvlc.AppendTextColumn(L('FILE_LABEL_COL_NAME'), width=250)
        self.dvlc.AppendTextColumn(L('FILE__COL_DIRECTORY'), width=150)
        boxsizer.Add(self.dvlc, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=2)

        # opciones de estilos (3)
        s_sizer = wx.BoxSizer()
        self.rb = wx.RadioBox(panel, -1, L('FILE_RADIO_BOX_TITLE'),
                              wx.DefaultPosition, (580, 50), FILES_FORMATS,
                              len(FILES_FORMATS), wx.RA_SPECIFY_COLS)
        # self.rb.Bind(wx.EVT_RADIOBOX, self.OnSelectStyle)

        s_sizer.Add(self.rb, 1, wx.EXPAND)
        boxsizer.Add(s_sizer, flag=wx.EXPAND | wx.TOP | wx.BOTTOM, border=10)

        sizer.Add(boxsizer, pos=(4, 0), span=(1, 5), flag=wx.RIGHT |
                  wx.LEFT | wx.ALIGN_CENTER_HORIZONTAL, border=10)

        # ------ Buttons foot -----------------------------------------------
        help_p = wx.BitmapButton(panel, bitmap=help32x32_bit.GetBitmap(),
                                 style=wx.NO_BORDER)
        sizer.Add(help_p, pos=(5, 0), span=(1, 3),
                  flag=wx.ALIGN_LEFT | wx.LEFT, border=10)
        # help_p.Bind(wx.EVT_BUTTON, self.OnHelpP)

        cancel = wx.Button(panel,
                           label=L('NEW_PROJECT_CANCEL'), size=(125, 32))
        sizer.Add(cancel, pos=(5, 3), flag=wx.ALIGN_BOTTOM
                  | wx.RIGHT, border=25)
        cancel.Bind(wx.EVT_BUTTON, self.on_cancel)

        self.create = wx.Button(panel, label=L('NEW_PROJECT_OK'),
                                size=(125, 32))
        sizer.Add(self.create, pos=(5, 4), flag=wx.ALIGN_BOTTOM |
                  wx.RIGHT | wx.LEFT, border=10)
        self.create.Bind(wx.EVT_BUTTON, self.on_create)

        # ------ configuraciones Globales -----------------------------------
        sizer.AddGrowableCol(2)
        panel.SetSizer(sizer)

        panel.Bind(wx.EVT_CHAR, self.on_key_down)

        # self.existing_names = ProjectM().names_not_hidden()
        # self.hidden_names = ProjectM().names_hidden()

    def add_only_results(self):
        self.alert_text.SetLabel(L('ADD_FILE_RESULT_HEADER'))
        self.name.SetValue(self.parent.p_project.name)
        self.name.Disable()

        self.create.SetLabel(L('ADD_FILE_RESULT'))
        self.create.Enable()
        pass

    def on_cancel(self, event):
        self.parent.p_create = False
        self.Close()

    def on_create(self, event):
        if not self.add_result:
            self.parent.p_name = self.name.GetValue()
            self.parent.p_path_files = self.path_files
            self.parent.p_formate = self.rb.GetSelection()
        else:
            if len(self.path_files) > 0:
                self.parent.p_path_files = self.path_files
                self.parent.p_formate = self.rb.GetSelection()
            else:
                self.parent.p_create = False
        self.parent.p_create = True
        self.Close()

    def on_key_down(self, e):
        key = e.GetKeyCode()
        if key == wx.WXK_ESCAPE:
            self.parent.p_create = False
            self.Close()

    def on_key_up(self, event):

        key_code = event.GetKeyCode()

        if key_code == wx.WXK_ESCAPE:
            self.parent.p_create = False
            self.Close()

        elif key_code == wx.WXK_RETURN:
            # verificar si se puede crear
            if not self.error_name:
                self.on_create(None)

        else:
            # verificar caracteres permitidos para nombre

            name = self.name.GetValue()
            self.error_name = False
            self.create.Enable()
            error_message = ''

            if len(name) == 0:
                self.alert_text.SetLabel(L('NEW_PROJECT_ENTER_NAME'))
                self.alert_bmp.SetBitmap(execute_bit.GetBitmap())
                self.name.SetBackgroundColour('#FFFFFF')
                self.error_name = True
                self.create.Disable()
                return None

            if len(name.strip(' ')) == 0:
                self.alert_text.SetLabel(L('NEW_PRO_BLANK_SPACE'))
                self.alert_bmp.SetBitmap(error_bit.GetBitmap())
                self.name.SetBackgroundColour('#F9EDED')
                self.create.Disable()
                self.error_name = True
                return None

            elif name.strip(' ')[0] == '.':
                error_message = L('NEW_PRO_CONTAINS_POINT')
                self.error_name = True
            if '/' in name:
                error_message = L('NEW_PRO_CONTAINS_SLASH')
                self.error_name = True
            if len(name.strip(' ')) > 100:
                error_message = L('NEW_PRO_MAXIMUM_LENGTH')
                self.error_name = True
            if name in self.existing_names:
                error_message = L('NEW_PRO_EXISTING_NAME')
                self.error_name = True
            if name in self.hidden_names:
                error_message = L('NEW_PRO_HIDDEN_EXISTING_NAME')
                self.error_name = True

            if self.error_name:
                self.alert_text.SetLabel(error_message)
                self.alert_bmp.SetBitmap(error_bit.GetBitmap())
                self.name.SetBackgroundColour('#F9EDED')
                self.create.Disable()
                return None

            self.alert_text.SetLabel(L('NEW_PROJECT_ENTER_NAME'))
            self.alert_bmp.SetBitmap(execute_bit.GetBitmap())
            self.name.SetBackgroundColour('#FFFFFF')
            self.create.Enable()

    # --Funciones para agregar archivos -------------------------------------
    def OnButtonBrowse(self, event):
        dlg = wx.FileDialog(self, message=L('ADD_FILE_DIALOG_TITLE'),
                            defaultDir=os.path.expanduser("~") + '/tesis',
                            wildcard=wildcard,
                            style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR)

        if dlg.ShowModal() == wx.ID_OK:
            _ps = []
            if len(self.path_files) == 0:
                self.path_files = _ps = dlg.GetPaths()
            else:
                for p in dlg.GetPaths():
                    if not (p in self.path_files):
                        self.path_files.append(p)
                        _ps.append(p)

            for address in _ps:
                path, name = os.path.split(address)
                self.dvlc.AppendItem([name, path])
        dlg.Destroy()
