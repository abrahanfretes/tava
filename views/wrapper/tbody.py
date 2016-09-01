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
# Creado:  27/8/2016                                         ###
#                                                            ###
# ##############################################################
'''


from wx import GetTranslation as L
import wx
from wx.lib.agw import customtreectrl as CT, aui
from wx.lib.pubsub import Publisher as pub

from languages import topic as T

from imgs.itree import iopen, iopened, iclose, \
    iview_package_open, iview_package_close, iview_pack
from presenters.ptree import TTreeP, PackageFile, PackageView
from views.wrapper.view import TViewWelCome, TView
from bd.entity import Project, Result, View
from views.wrapper.vmenu.vtree import MenuVista, MenuPackageView


KURI_AUI_NB_STYLE = aui.AUI_NB_TOP | aui.AUI_NB_TAB_SPLIT | \
    aui.AUI_NB_TAB_MOVE | aui.AUI_NB_SCROLL_BUTTONS |\
    aui.AUI_NB_CLOSE_BUTTON | aui.AUI_NB_DRAW_DND_TAB


class CentralPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.v_setting()

        pub().subscribe(self.show_view, T.SHOW_SELECTED_VIEW)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)

        self.v_content()

    def v_setting(self):
        self.SetBackgroundColour("#3B598D")

    def v_content(self):

        self.instancias = {}
        self.instancias_d = {}

        self.nb_main = aui.AuiNotebook(self)
        self.nb_main.SetArtProvider(aui.ChromeTabArt())
        # self.nb_main.SetAGWWindowStyleFlag(KURI_AUI_NB_STYLE)
        self.nb_main.Bind(aui.EVT_AUINOTEBOOK_PAGE_CLOSE, self.on_close)
        self.nb_main.Bind(aui.EVT_AUINOTEBOOK_PAGE_CHANGED, self.on_change)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.nb_main, 1,
                       wx.LEFT | wx.TOP | wx.EXPAND | wx.ALL, 1)
        self.SetSizer(self.sizer)
        self.Fit()

    def show_view(self, message):
        view = message.data

        # self.nb_main.AddPage(TView(self.nb_main), "Prueba Matplotlib")
        # self.nb_main.InsertPage(idx, TViewWelCome(self.nb_main),
        # "Welcome to Tava")

        if view.id in self.instancias.keys():
            idx = self.instancias[view.id]
            self.nb_main.SetSelection(idx)
        else:
            idx = self.nb_main.GetPageCount()
            self.nb_main.AddPage(TView(self.nb_main), "Prueba Matplotlib")
            self.instancias[view.id] = idx
            self.instancias_d[idx] = view.id
            self.nb_main.SetSelection(idx)

    def on_close(self, event):
        page = self.nb_main.GetCurrentPage()
        if page is not None:
            idx = self.nb_main.GetPageIndex(page)
            _id = self.instancias_d[idx]
            del self.instancias[_id]
            del self.instancias_d[idx]

    def on_change(self, event):
        print 'Change tab'


class TTree(CT.CustomTreeCtrl):

    def __init__(self, parent):
        CT.CustomTreeCtrl.__init__(self, parent)

        self.v_setting()
        self.v_content()

        self.ppr = TTreeP(self)
        self.c_item = None
        self.c_data = None

        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.on_selected)
        self.Bind(wx.EVT_RIGHT_UP, self.on_contex)

    def v_setting(self):
        # self.SetBackgroundColour("red")
        self.SetSize(wx.Size(220, -1))
        self.SetAGWWindowStyleFlag(CT.TR_HAS_BUTTONS | CT.TR_HIDE_ROOT)

    def v_content(self):

        img_list = wx.ImageList(16, 16)
        img_list.Add(iopen.GetBitmap())
        img_list.Add(iopened.GetBitmap())
        img_list.Add(iclose.GetBitmap())

        img_list.Add(iview_package_close.GetBitmap())
        img_list.Add(iview_package_open.GetBitmap())

        img_list.Add(iview_pack.GetBitmap())

        self.AssignImageList(img_list)

        self.root = self.AddRoot("TAVA TREE PROJECT", 0)

    # --- node open project
    def add_open_project(self, project):
        project_item = self.AppendItem(self.root, project.name)
        return self.update_open_project(project_item, project)

    def update_open_project(self, project_item, project):
        self.SetItemPyData(project_item, [project, project.proj_open])
        self.SetItemImage(project_item, 0, wx.TreeItemIcon_Normal)
        self.SetItemImage(project_item, 1, wx.TreeItemIcon_Expanded)
        self.SetItemTextColour(project_item, '#000000')
        self._expanded(project_item, project.proj_open)
        return project_item

    # --- node closed project
    def add_closed_project(self, project):
        project_item = self.AppendItem(self.root, project.name)
        return self.update_close_project(project_item, project)

    def update_close_project(self, project_item, project):
        self.SetItemPyData(project_item, [project, False])
        self.SetItemImage(project_item, 2, wx.TreeItemIcon_Normal)
        self.SetItemImage(project_item, 2, wx.TreeItemIcon_Expanded)
        self.SetItemTextColour(project_item, '#AABBCC')
        return project_item

    # --- node files package
    def add_package_files(self, item_p, pack_file):
        item_file_package = self.AppendItem(item_p, self._package_file_name())
        self.SetItemPyData(item_file_package, [pack_file, pack_file.state])
        self.SetItemImage(item_file_package, 3, wx.TreeItemIcon_Normal)
        self.SetItemImage(item_file_package, 4, wx.TreeItemIcon_Expanded)
        self._expanded(item_file_package, pack_file.state)
        return item_file_package

    # --- node views package
    def add_package_views(self, item_p, pack_view):
        item_views_package = self.AppendItem(item_p, self._package_view_name())
        self.SetItemPyData(item_views_package, [pack_view, pack_view.state])
        self.SetItemImage(item_views_package, 5, wx.TreeItemIcon_Normal)
        self._expanded(item_views_package, pack_view.state)
        return item_views_package

    # --- node results
    def add_results(self, item_pack, result):
        item_result = self.AppendItem(item_pack, result.name)
        self.SetItemPyData(item_result, [result, True])
        return item_result

    # --- node views
    def add_views(self, item_pack, view):
        item_view = self.AppendItem(item_pack, view.name)
        self.SetItemPyData(item_view, [view, True])
        return item_view

    # ------------------------------------------------------------------
    # --------------- metodos privados ---------------------------------
    # ------------------------------------------------------------------

    # -- selected item
    def on_selected(self, event):
        self.c_item = event.GetItem()
        self.c_data = self.c_item.GetData()
        if self.c_data is not None:
            # self.ppr.do_selected(self.c_data[0], self.c_item)
            pass

    # --- selected contex menu
    def on_contex(self, event):
        data = self.c_data[0]
        if isinstance(data, Project):
            print 'Click derecho en Proyecto'
            # menu_p = MenuP(self, data)
            # self.PopupMenu(menu_p)
        elif isinstance(data, PackageFile):
            print 'Click derecho en Paquete Resultado'
            # menu_p = MenuPR(self, data.project)
            # self.PopupMenu(menu_p)
        elif isinstance(data, PackageView):
            print 'Click derecho en Paquete de Vista'
            menu_p = MenuPackageView(self, data.project)
            self.PopupMenu(menu_p)
        elif isinstance(data, Result):
            print 'Click derecho en Result'
            # menu_p = MenuAR(self, data)
            # self.PopupMenu(menu_p)
        elif isinstance(data, View):
            menu_p = MenuVista(self, data)
            self.PopupMenu(menu_p)
            print 'Click derecho en Vista'
        else:
            print 'ninguno de los anteriores'

    def _expanded(self, item, expand=True):
        if expand:
            item.Expand()
        else:
            item.Collapse()

    def _package_file_name(self):
        return L('PACKAGE_FILES_NAME')

    def _package_view_name(self):
        return L('PACKAGE_VIEWS_NAME')
