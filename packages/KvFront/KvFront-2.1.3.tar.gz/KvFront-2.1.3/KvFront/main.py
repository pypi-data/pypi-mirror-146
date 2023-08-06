 #   Copyright (C) 2017-2022  Gavin W
 #   This program is free software: you can redistribute it and/or modify
 #   it under the terms of the GNU General Public License as published by
 #   the Free Software Foundation, either version 3 of the License, or
 #   (at your option) any later version.

 #   This program is distributed in the hope that it will be useful,
 #   but WITHOUT ANY WARRANTY; without even the implied warranty of
 #   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 #   GNU General Public License for more details.

 #   You should have received a copy of the GNU General Public License
 #   along with this program.  If not, see <http://www.gnu.org/licenses/>.
 
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gi
gi.require_version('GtkSource', '4')
from gi.repository import Gtk,GtkSource,Gio,GdkPixbuf
from KvFront.memcached import *
from KvFront.redis_helper import *
from KvFront.connection import *
from KvFront.conninfo import *
from KvFront.redis_conninfo import *
from KvFront.config import *
from KvFront.constants import *
import json
import sys
# gi.require_version('Gtk', '3.0') 


class KvFront():
    
    def __init__(self):
        
        GObject.type_register(Conninfo)
        GObject.type_register(GtkSource.View)
        
        Gtk.Settings().set_property('gtk-dialogs-use-header', True)
        self.builder = Gtk.Builder()
        self.builderStats = Gtk.Builder()
        
        self.memip = "127.0.0.1"
        self.notebookdetail = None
        
        self.cfg = Config()
        servernames = self.cfg.getServerNames()
        
#         try:
        print(FILE_UI_MAIN)
        self.builder.add_from_file(FILE_UI_MAIN)
        self.builderStats.add_from_file(FILE_UI_DETAILPAGE)
#         except:
#             print("add from file failed")
#             sys.exit()
            
        self.window = self.builder.get_object("window1")
        self.btnrefreshstats = self.builder.get_object("btnRefreshStats")
        self.btnFlush = self.builder.get_object("btnFlush")
        self.btnExport = self.builder.get_object("btnExport")
        self.btnrefreshstats.set_sensitive(False)
        self.btnFlush.set_sensitive(False)
        self.btnExport.set_sensitive(False)
    
        self.builder.connect_signals(self)

        self.store = Gtk.TreeStore(GObject.Object)
        for sn in servernames:
            serverinfo = self.cfg.getServerInfo(sn)
            #print(serverinfo)
            #print(serverinfo[0][1])
            p = Conninfo()
            p.name = sn + "(" + serverinfo[1][1]+ ")"
            p.hosts = serverinfo[0][1]
            p.category = serverinfo[1][1]
            p.password = serverinfo[2][1]
            tp = self.store.append(None, (p,))
            if serverinfo[1][1] == "Redis Standalone":
                for db_sn in range(0,16):
                    rp = RedisConninfo()
                    rp.name = "db" + str(db_sn)
                    rp.db_sn = db_sn
                    rp.hosts = serverinfo[0][1]
                    rp.category = serverinfo[1][1]
                    rp.password = serverinfo[2][1]
                    self.store.append(tp,(rp,))
            if serverinfo[1][1] == "Redis Cluster":
                for db_sn in range(0,1):
                    rp = RedisConninfo()
                    rp.name = "db" + str(db_sn)
                    rp.db_sn = db_sn
                    rp.hosts = serverinfo[0][1]
                    rp.category = serverinfo[1][1]
                    rp.password = serverinfo[2][1]
                    self.store.append(tp,(rp,))

        view = self.builder.get_object("treeview2")
        view.set_model(self.store)
        
        renderer_connections = Gtk.CellRendererText()
        column_connections = Gtk.TreeViewColumn("Connections", renderer_connections, text=0)
        column_connections.set_cell_data_func(renderer_connections, self.get_connection_name)
        view.append_column(column_connections)
        column_connections.set_sort_column_id(0)
        
        self.window.connect("destroy", Gtk.main_quit)
        self.window.show_all()
        
        self.memHelper = MemcachedHelper()
        self.redisHelper = RedisHelper()
        Gtk.main()
        
    def get_connection_name(self, column, cell, model, iter, data):
        cell.set_property('text', self.store.get_value(iter, 0).name)
    
    def init_detail_page_redis(self, builder):
        print("init detail page 4 redis")

        # image_status = builder.get_object("image_status")
        # image_status.set_from_pixbuf(GdkPixbuf.Pixbuf.new_from_file_at_size(os.path.join(DIR_ICON,"status.svg"), 32, 32))
        
        store = Gtk.ListStore(str, str)
        for i, column_title in enumerate(["key", "value"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            column.set_sizing(Gtk.TreeViewColumnSizing.GROW_ONLY)
            column.set_resizable(True)
            column.set_min_width(400)
            builder.get_object("TreeViewStats").append_column(column)
        builder.get_object("TreeViewStats").set_model(store)
        
        store1 = Gtk.ListStore(str, str, str, str)
        for i, column_title in enumerate(["key", "field", "value", "type"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            column.set_sizing(Gtk.TreeViewColumnSizing.GROW_ONLY)
            column.set_resizable(True)
            column.set_min_width(200)
#             column.set_max_width(300)
            builder.get_object("TreeViewResults").append_column(column)
        builder.get_object("TreeViewResults").set_model(store1)

        store2 = Gtk.ListStore(str, str)
        for i, column_title in enumerate(["key", "type"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            column.set_sizing(Gtk.TreeViewColumnSizing.GROW_ONLY)
            column.set_resizable(True)
            column.set_min_width(200)
#             column.set_max_width(300)
            builder.get_object("TreeViewResults1").append_column(column)
        builder.get_object("TreeViewResults1").set_model(store2)
        
        builder.get_object("btnRun").connect("clicked", self.btnRun_clicked_cb)
        builder.get_object("btnRun1").connect("clicked", self.btnRun1_clicked_cb)
        
        cbcmd = builder.get_object("cbcmd")
        storeCmd = builder.get_object("storecmd")
        storeCmd.append([1, "set"])
        storeCmd.append([2, "mget"])
        #storeCmd.append([3, "mset"])
        #storeCmd.append([4, "mget"])
        storeCmd.append([5, "hmset"])
        storeCmd.append([6, "hgetall"])
        storeCmd.append([7, "lrange"])
        storeCmd.append([8, "lpush"])
        # storeCmd.append([10, "xadd"])
        storeCmd.append([11, "xrange"])
        storeCmd.append([9, "delete"])
        cbcmd.set_active(0)

        sbcount = builder.get_object("sbcount")
        sbcount.set_range(1, 10000)
        sbcount.set_increments (1, 10)
        sbcount.set_value(500)

        sbfrom = builder.get_object("sbfrom")
        sbfrom.set_range(0, 20000000000)
        sbfrom.set_increments (1, 10)
        # sbfrom.set_value(0)
        
    def init_detail_page(self, builder):
        print("init detail page")
        store = Gtk.ListStore(str, str)
        for i, column_title in enumerate(["key", "value"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            column.set_sizing(Gtk.TreeViewColumnSizing.GROW_ONLY)
            column.set_resizable(True)
            column.set_min_width(400)
            builder.get_object("TreeViewStats").append_column(column)
        builder.get_object("TreeViewStats").set_model(store)
        
        store1 = Gtk.ListStore(str, str)
        for i, column_title in enumerate(["key", "value"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            column.set_sizing(Gtk.TreeViewColumnSizing.GROW_ONLY)
            column.set_resizable(True)
            column.set_min_width(200)
#             column.set_max_width(300)
            builder.get_object("TreeViewResults").append_column(column)
        builder.get_object("TreeViewResults").set_model(store1)
        
        builder.get_object("btnRun").connect("clicked", self.btnRun_clicked_cb)
        
        cbcmd = builder.get_object("cbcmd")
        storeCmd = builder.get_object("storecmd")
        storeCmd.append([1, "set"])
        storeCmd.append([2, "get"])
        storeCmd.append([3, "delete"])
        cbcmd.set_active(0)
        
    def treeview2_row_activated_cb(self, treeview, path, column):
        # model, treeiter = selection.get_selected()
        model = treeview.get_model()
        iter = model.get_iter(path)
        self.category = model[iter][0].category
        self.password = model[iter][0].password
        if iter != None:
            if self.category == "Memcached":
                print("You selected memcached", model[iter][0].hosts)
                self.memHelper.close()
                self.memip = model[iter][0].hosts
                memiplist = self.memip.split(",")
                self.memHelper.connect(memiplist)

                self.btnrefreshstats.set_sensitive(True)
                self.btnFlush.set_sensitive(True)
                self.btnExport.set_sensitive(False)
                # paned1 = self.builder.get_object("paned1")
                builderStats = Gtk.Builder()
                builderStats.add_from_file(FILE_UI_DETAILPAGE)
                notebookdetail = builderStats.get_object("notebookdetail")
                boxCmd = self.builder.get_object("BoxCmd")

                if not self.notebookdetail is None:
                    Gtk.Container.remove(boxCmd, self.notebookdetail)
                    print("add notbook widget")
                else:
                    print("notebookdetail is null")
                boxCmd.add(notebookdetail)
                notebookdetail.set_property ("expand", True)
                self.notebookdetail = notebookdetail
                self.builderStats = builderStats
                self.init_detail_page(builderStats)
                ret = self.memHelper.stats()
                print(ret[0][1])
                dictd = ret[0][1]
                store = Gtk.ListStore(str, str)
                for r in dictd:
                    store.append((r, dictd[r]))
                self.builderStats.get_object("TreeViewStats").set_model(store)
                self.builderStats.get_object("TreeViewResults").connect("row-activated", self.treeview_result_row_activated_cb);
            elif self.category == "Redis Standalone":
                if len(path) == 2:
                    print("You selected redis", model[iter][0].hosts)
                    self.redisHelper.close()
                    self.btnrefreshstats.set_sensitive(True)
                    self.btnFlush.set_sensitive(True)
                    self.btnExport.set_sensitive(True)
                    builderStats = Gtk.Builder()
                    builderStats.add_from_file(FILE_UI_DETAILPAGE4REDIS)
                    notebookdetail = builderStats.get_object("notebookdetail")
                    boxCmd = self.builder.get_object("BoxCmd")

                    if not self.notebookdetail is None:
                        Gtk.Container.remove(boxCmd, self.notebookdetail)
                        print("add notbook widget")
                    else:
                        print("notebookdetail is null")
                    boxCmd.add(notebookdetail)
                    notebookdetail.set_property ("expand", True)
                    self.notebookdetail = notebookdetail
                    self.builderStats = builderStats
                    self.init_detail_page_redis(builderStats)

                    self.redisIpPort = model[iter][0].hosts
                    self.db_sn = model[iter][0].db_sn
                    connRet = self.redisHelper.connect(self.redisIpPort, self.password, self.db_sn)
                    if connRet == 0:
                        dictd = self.redisHelper.stats()
                        #print(dictd)
                        store = Gtk.ListStore(str, str)
                        for r in dictd:
                            store.append((r, str(dictd[r])))
                        self.builderStats.get_object("TreeViewStats").set_model(store)
                        self.builderStats.get_object("TreeViewResults").connect("row-activated", self.treeview_result_row_activated_cb)
                        self.builderStats.get_object("TreeViewResults1").connect("row-activated", self.treeview_result1_row_activated_cb)
                    else:
                        msgdlg = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.WARNING,
                                                    Gtk.ButtonsType.CLOSE, connRet)
                        msgdlg.run()
                        msgdlg.destroy()
            elif self.category == "Redis Cluster":
                if len(path) == 2:
                    print("You selected redis", model[iter][0].hosts)
                    self.redisHelper.close()
                    self.btnrefreshstats.set_sensitive(True)
                    self.btnFlush.set_sensitive(True)
                    self.btnExport.set_sensitive(True)
                    builderStats = Gtk.Builder()
                    builderStats.add_from_file(FILE_UI_DETAILPAGE4REDIS)
                    notebookdetail = builderStats.get_object("notebookdetail")
                    boxCmd = self.builder.get_object("BoxCmd")

                    if not self.notebookdetail is None:
                        Gtk.Container.remove(boxCmd, self.notebookdetail)
                        print("add notbook widget")
                    else:
                        print("notebookdetail is null")
                    boxCmd.add(notebookdetail)
                    notebookdetail.set_property ("expand", True)
                    self.notebookdetail = notebookdetail
                    self.builderStats = builderStats
                    self.init_detail_page_redis(builderStats)

                    self.redisIpPort = model[iter][0].hosts
                    self.db_sn = model[iter][0].db_sn
                    connRet = self.redisHelper.connect_cluster(self.redisIpPort, self.password, self.db_sn)
                    if connRet == 0:
                        dictd = self.redisHelper.stats()
                        store = Gtk.ListStore(str, str)
                        for r in dictd:
                            store.append((r, str(dictd[r])))
                        self.builderStats.get_object("TreeViewStats").set_model(store)
                        self.builderStats.get_object("TreeViewResults").connect("row-activated", self.treeview_result_row_activated_cb)
                        self.builderStats.get_object("TreeViewResults1").connect("row-activated", self.treeview_result1_row_activated_cb)
                    else:
                        msgdlg = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.WARNING,
                                                    Gtk.ButtonsType.CLOSE, connRet)
                        msgdlg.run()
                        msgdlg.destroy()

    def treeview_result1_row_activated_cb(self, treeview, path, column):
        model = treeview.get_model()
        iter = model.get_iter(path)
        if iter != None:
            svalue = ""
            if model[iter][1] == "string":
                value=self.redisHelper.get(model[iter][0])
                svalue = str(value)
               
            elif model[iter][1] == "hash":
                value=self.redisHelper.hgetall(model[iter][0])
                svalue = str(value)
            
            elif model[iter][1] == "list":
                value=self.redisHelper.lrange(model[iter][0],0,-1)
                svalue = str(value)

            elif model[iter][1] == "set":
                value=self.redisHelper.smembers(model[iter][0])
                svalue = str(value)

            elif model[iter][1] == "zset":
                value=self.redisHelper.zrange(model[iter][0],0,-1)
                svalue = str(value)
            
            elif model[iter][1] == "stream":
                value=self.redisHelper.xrange(model[iter][0])
                svalue = str(value)
                
            txtviewdetail = self.builderStats.get_object("txt_view_value_detail1")
            valuebuffer = txtviewdetail.get_buffer()
            lmanager = GtkSource.LanguageManager.get_default()
            language = lmanager.get_language("json")      
            valuebuffer.set_language(language)
            
            try:
                print("---"+svalue)
                obj_val = json.loads(svalue, encoding='utf-8')
                valuebuffer.set_highlight_syntax(True)
                formated_json_val = json.dumps(obj_val, sort_keys=True, indent=2)
                valuebuffer.set_text(formated_json_val)
            except ValueError:
                print("not json format")
                valuebuffer.set_highlight_syntax(False) 
                valuebuffer.set_text(svalue)
            
    def treeview_result_row_activated_cb(self, treeview, path, column):
        model = treeview.get_model()
        iter = model.get_iter(path)
        if iter != None:
            if self.category == "Memcached":
                value = model[iter][1]
            elif self.category == "Redis Standalone" or self.category == "Redis Cluster":
                if model[iter][0] == "string":
                    vindex = 2
                elif model[iter][0] == "hash":
                    vindex = 3
                elif model[iter][0] == "list":
                    vindex = 2
                # elif model[iter][1] == "set":
                #     
                #     
                # elif model[iter][1] == "zset":
                #     
                #     
                elif model[iter][0] == "stream":
                    vindex = 4
            value = model[iter][vindex]
            txtviewdetail = self.builderStats.get_object("txt_view_value_detail")
            valuebuffer = txtviewdetail.get_buffer()
            lmanager = GtkSource.LanguageManager.get_default()
            language = lmanager.get_language("json")
            valuebuffer.set_language(language)
            
            try:
                obj_val = json.loads(value, encoding='utf-8')
                valuebuffer.set_highlight_syntax(True)
                formated_json_val = json.dumps(obj_val, sort_keys=True, indent=2)
                valuebuffer.set_text(formated_json_val)
            except ValueError:
                print("not json format")
                valuebuffer.set_highlight_syntax(False) 
                valuebuffer.set_text(value)
            
    
    def removeConnection(self):
        print("remove a connection")
        treeselection = self.builder.get_object("treeview-selection2")
        treeview = self.builder.get_object("treeview2")
        selserver = treeselection.get_selected()

        model = selserver[0]
        iter = selserver[1]
    
        if iter != None:
            print("selected", model[iter][0].name)
            tmp = model[iter][0].name
            serverdescription =tmp.split("(",1)
            model.remove(iter)
#             treeview.set_model(model)
            self.cfg.removeServer(serverdescription[0])
        else:
            msgdlg = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.INFO,
                                               Gtk.ButtonsType.OK, "please select a connection to remove")
            msgdlg.run()
            msgdlg.destroy()
            
            
    def btnRemoveConnection_clicked(self, button):
        msgdlg = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.INFO,
                                               Gtk.ButtonsType.OK_CANCEL, "Are you sure you want to remove the connection?")
        response = msgdlg.run()
        msgdlg.destroy()
        if response == Gtk.ResponseType.OK:
            self.removeConnection()
            
    def btnFlush_clicked_cb(self,button):
        msgdlg = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.INFO,
                                               Gtk.ButtonsType.OK_CANCEL, "Are you sure you want to flush all data?")
        response = msgdlg.run()
        msgdlg.destroy()
        if response == Gtk.ResponseType.OK:
            if self.category == "Memcached":
                self.memHelper.flush()
            elif self.category == "Redis Standalone" or self.category == "Redis Cluster":
                self.redisHelper.flush()
            msgdlg2 = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.INFO,
                                               Gtk.ButtonsType.CLOSE, "flush data successed!")
            msgdlg2.run()
            msgdlg2.destroy()
            return False
        return True

    def mi_about_clicked_cb(self,button):
        dialog = Gtk.AboutDialog()
        dialog.set_title("About")
        dialog.set_name("KvFront")
        dialog.set_version("2.1.3")
        dialog.set_comments("A GUI Tool for Redis and Memcached")
        dialog.set_authors(["Gavin W <qmongofront@live.com>"])
        dialog.set_logo(GdkPixbuf.Pixbuf.new_from_file_at_size(os.path.join(os.path.expanduser('~'),".local/share/icons/kvfront.png"), 64, 64))
        dialog.connect('response', lambda dialog, data: dialog.destroy())
        dialog.show_all()

    def btnExport_clicked_cb(self,button):
        # filedlg = Gtk.FileChooserDialog("Please choose a file", self.window,
        #                                     Gtk.FileChooserAction.SAVE,
        #                                     (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
        #                                     Gtk.STOCK_SAVE, Gtk.ResponseType.OK))
        # response = filedlg.run()
        # if response == Gtk.ResponseType.OK:
        #     file_path = filedlg.get_filename()
        #     print("Save clicked")
        #     print("File selected: " + file_path)
        #     # export data to file
        #     data_keys = self.redisHelper.get_all_keys()
        #     all_data = {}
        #     for i in data_keys:
        #         all_data[i] = json.loads(self.redisHelper.get(i))
        #     file_object = open(file_path, 'w', encoding="utf8")
        #     json.dump(all_data, file_object, ensure_ascii=False)
 
        #     file_object.close()

        # elif response == Gtk.ResponseType.CANCEL:
        #     print("Cancel clicked")

        # filedlg.destroy()
        # return True
        msgdlg = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.INFO,
                                                Gtk.ButtonsType.CLOSE, "Sorry, the backup module is under development")
        msgdlg.run()
        msgdlg.destroy()
        return

    def btnRefreshStats_clicked_cb(self, button):
        if self.category == "Memcached":
            print("refresh memcached stats")
            ret = self.memHelper.stats()
            print(ret[0][1])
            dictd = ret[0][1]
            store = Gtk.ListStore(str, str)
            for r in dictd:
                store.append((r, dictd[r]))
            self.builderStats.get_object("TreeViewStats").set_model(store)
        elif self.category == "Redis Standalone" or self.category == "Redis Cluster":
            print("refresh redis stats")
            dictd = self.redisHelper.stats()
                #print(dictd)
            store = Gtk.ListStore(str, str)
            for r in dictd:
                store.append((r, str(dictd[r])))
            self.builderStats.get_object("TreeViewStats").set_model(store)
     
    def btnAddServer_clicked_cb(self, button):
        Connection(self.window, self)

    def btnRun1_clicked_cb(self, button):

        key = self.builderStats.get_object("entrykey1")
        keypattern = "*"
        sbfrom = self.builderStats.get_object("sbfrom")
        sbcount = self.builderStats.get_object("sbcount")
        pfrom = int(sbfrom.get_value())
        count = int(sbcount.get_value())

        if key.get_text().strip() != "":
            keypattern = "*" + str(key.get_text().strip()) +"*"
        ret = self.redisHelper.scan(pfrom, "*" + str(key.get_text().strip()) +"*", count)
        store1 = Gtk.ListStore(str, str)
        print(ret[1])
        i = 0
        for v in ret[1]:
            if v == None:
                break
            store1.append([v, self.redisHelper.type(v)])
            i += 1
            print(i)
        self.builderStats.get_object("TreeViewResults1").set_model(store1)
 
    def btnRun_clicked_cb(self, button):
        print("category:" + self.category)

        if self.category == "Memcached":
            cbcmd = self.builderStats.get_object("cbcmd")
            tree_iter = cbcmd.get_active_iter()
            if tree_iter != None:
                model = cbcmd.get_model()
                cmdcode = model[tree_iter][0]
                print("Selected: =%s" % cmdcode)
                if cmdcode == 1:
                    key = self.builderStats.get_object("entrykey").get_text().strip()
                    time = self.builderStats.get_object("entrykeytimeout").get_text().strip()
                    if time == "":
                        time = "0"
                    if key == "":
                        msgdlg = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.INFO,
                                                Gtk.ButtonsType.CLOSE, "please input key name")
                        msgdlg.run()
                        msgdlg.destroy()
                        return
                    txtview = self.builderStats.get_object("txt_view_input")
                    valuebuffer = txtview.get_buffer()
                    value = valuebuffer.get_text(valuebuffer.get_start_iter(), valuebuffer.get_end_iter(), False)
                    print(value)
                    ret = self.memHelper.set(key, value, int(time))
                    if ret is True:
                        msgdlg = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.INFO,
                                                Gtk.ButtonsType.CLOSE, "set successed")
                        msgdlg.run()
                        msgdlg.destroy()
                    else:
                        msgdlg = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.INFO,
                                                Gtk.ButtonsType.CLOSE, "set failed")
                        msgdlg.run()
                        msgdlg.destroy()
                        
                elif cmdcode == 2:
                
                    store1 = Gtk.ListStore(str, str)
                    key = self.builderStats.get_object("entrykey").get_text()
                    keylist = key.split(",")
                    print(keylist)
                    values = self.memHelper.get_multi(keylist)
                    print(values)
                    for key in values:
                        store1.append([key, values[key]])
                    self.builderStats.get_object("TreeViewResults").set_model(store1)
                
                elif cmdcode == 3:
                
                    key = self.builderStats.get_object("entrykey").get_text()
                    keylist = key.split(",")
                    print(keylist)
                    ret = self.memHelper.delete_multi(keylist)
                    if ret == 1:
    #                     print("set successed")
                        msgdlg = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.INFO,
                                                Gtk.ButtonsType.CLOSE, "delete successed")
                        msgdlg.run()
                        msgdlg.destroy()
                    else:
    #                     print("set failed")
                        msgdlg = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.WARNING,
                                                Gtk.ButtonsType.CLOSE, ret)
                        msgdlg.run()
                        msgdlg.destroy()
        elif self.category == "Redis Standalone" or self.category == "Redis Cluster":
            cbcmd = self.builderStats.get_object("cbcmd")
            tree_iter = cbcmd.get_active_iter()
            if tree_iter != None:
                model = cbcmd.get_model()
                cmdcode = model[tree_iter][0]
                print("Selected: =%s" % cmdcode)
                if cmdcode == 1:
                    key = self.builderStats.get_object("entrykey").get_text().strip()
                    time = self.builderStats.get_object("entrykeytimeout").get_text().strip()
                    if time == "":
                        time = "0"
                    if key == "":
                        msgdlg = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.INFO,
                                                Gtk.ButtonsType.CLOSE, "please input key name")
                        msgdlg.run()
                        msgdlg.destroy()
                        return
    #                 print(key)
                    txtview = self.builderStats.get_object("txt_view_input")
                    valuebuffer = txtview.get_buffer()
                    value = valuebuffer.get_text(valuebuffer.get_start_iter(), valuebuffer.get_end_iter(), False)
                    ret = self.redisHelper.set(key, value, int(time))
                    if ret is True:
    #                     print("set successed")
                        msgdlg = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.INFO,
                                                Gtk.ButtonsType.CLOSE, "set successed")
                        msgdlg.run()
                        msgdlg.destroy()
                    else:
    #                     print("set failed")
                        msgdlg = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.WARNING,
                                                Gtk.ButtonsType.CLOSE, ret)
                        msgdlg.run()
                        msgdlg.destroy()

                elif cmdcode == 2:
                
                    columns = self.builderStats.get_object("TreeViewResults").get_columns()
                    for c in columns:
                        self.builderStats.get_object("TreeViewResults").remove_column(c)
                    store1 = Gtk.ListStore(str, str, str)
                    for i, column_title in enumerate(["type","key", "value"]):
                        renderer = Gtk.CellRendererText()
                        column = Gtk.TreeViewColumn(column_title, renderer, text=i)
                        column.set_sizing(Gtk.TreeViewColumnSizing.GROW_ONLY)
                        column.set_resizable(True)
                        column.set_min_width(200)
                        self.builderStats.get_object("TreeViewResults").append_column(column)

                    key = self.builderStats.get_object("entrykey").get_text()
                    keylist = key.split(",")
                    #print(keylist)
                    values = self.redisHelper.get_multi(keylist)
                    i = 0
                    for v in values:
                        #print(v)
                        #print(values[v])
                        if v == None:
                            break
                        store1.append(["string",keylist[i], v])
                        i += 1
                    self.builderStats.get_object("TreeViewResults").set_model(store1)

                elif cmdcode == 5:
                
                    key = self.builderStats.get_object("entrykey").get_text().strip()
                    if key == "":
                        msgdlg = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.INFO,
                                                Gtk.ButtonsType.CLOSE, "please input key name")
                        msgdlg.run()
                        msgdlg.destroy()
                        return
                    txtview = self.builderStats.get_object("txt_view_input")
                    valuebuffer = txtview.get_buffer()
                    value = valuebuffer.get_text(valuebuffer.get_start_iter(), valuebuffer.get_end_iter(), False)
                    field_line = value.split("\n")
                    mapping = {}
                    for fl in field_line:
                        kv = fl.split(":",1)
                        mapping[kv[0]]=kv[1]
                    ret = self.redisHelper.hmset(key, mapping)
                    if ret == 0 or ret == 1:
    #                     print("set successed")
                        msgdlg = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.INFO,
                                                Gtk.ButtonsType.CLOSE, "set successed")
                        msgdlg.run()
                        msgdlg.destroy()
                    else:
    #                     print("set failed")
                        msgdlg = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.WARNING,
                                                Gtk.ButtonsType.CLOSE, ret)
                        msgdlg.run()
                        msgdlg.destroy()

                elif cmdcode == 6:
                
                    columns = self.builderStats.get_object("TreeViewResults").get_columns()
                    for c in columns:
                        self.builderStats.get_object("TreeViewResults").remove_column(c)
                    store1 = Gtk.ListStore(str, str, str, str)
                    for i, column_title in enumerate(["type", "key", "field", "value"]):
                        renderer = Gtk.CellRendererText()
                        column = Gtk.TreeViewColumn(column_title, renderer, text=i)
                        column.set_sizing(Gtk.TreeViewColumnSizing.GROW_ONLY)
                        column.set_resizable(True)
                        column.set_min_width(200)
                        self.builderStats.get_object("TreeViewResults").append_column(column)

                    key = self.builderStats.get_object("entrykey").get_text()
                    #print(keylist)
                    values = self.redisHelper.hgetall(key)
                    print(values)
                    for v in values:
                        #print(v)
                        #print(values[v])
                        if v == None:
                            break
                        store1.append(["hash", key, v, values[v]])
                    self.builderStats.get_object("TreeViewResults").set_model(store1)

                elif cmdcode == 7:
                    columns = self.builderStats.get_object("TreeViewResults").get_columns()
                    for c in columns:
                        self.builderStats.get_object("TreeViewResults").remove_column(c)
                    store1 = Gtk.ListStore(str, str, str)
                    for i, column_title in enumerate(["type", "key", "value"]):
                        renderer = Gtk.CellRendererText()
                        column = Gtk.TreeViewColumn(column_title, renderer, text=i)
                        column.set_sizing(Gtk.TreeViewColumnSizing.GROW_ONLY)
                        column.set_resizable(True)
                        column.set_min_width(200)
                        self.builderStats.get_object("TreeViewResults").append_column(column)

                    key = self.builderStats.get_object("entrykey").get_text()
                    values = self.redisHelper.lrange(key,0,-1)
                    print(values)
                    for v in values:
                        print(v)
                        if v == None:
                            break
                        store1.append(["list", key, v])
                    self.builderStats.get_object("TreeViewResults").set_model(store1)
                
                elif cmdcode == 8:
                
                    key = self.builderStats.get_object("entrykey").get_text().strip()
                    if key == "":
                        msgdlg = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.INFO,
                                                Gtk.ButtonsType.CLOSE, "please input key name")
                        msgdlg.run()
                        msgdlg.destroy()
                        return
                    txtview = self.builderStats.get_object("txt_view_input")
                    valuebuffer = txtview.get_buffer()
                    value = valuebuffer.get_text(valuebuffer.get_start_iter(), valuebuffer.get_end_iter(), False)
                    field_line = value.split(",")
                    # mapping = {}
                    # for fl in field_line:
                    #     kv = fl.split(":",1)
                    #     mapping[kv[0]]=kv[1]
                    ret = self.redisHelper.lpush(key, value)
                    if ret == 0 or ret == 1:
    #                     print("set successed")
                        msgdlg = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.INFO,
                                                Gtk.ButtonsType.CLOSE, "set successed")
                        msgdlg.run()
                        msgdlg.destroy()
                    else:
    #                     print("set failed")
                        msgdlg = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.WARNING,
                                                Gtk.ButtonsType.CLOSE, ret)
                        msgdlg.run()
                        msgdlg.destroy()
                
                elif cmdcode == 9:
                    key = self.builderStats.get_object("entrykey").get_text()
                    keylist = key.split(",")
                    ret = self.redisHelper.delete_multi(keylist)
                    if ret == 1:
                        msgdlg = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.INFO,
                                                Gtk.ButtonsType.CLOSE, "delete successed")
                        msgdlg.run()
                        msgdlg.destroy()
                    else:
                        msgdlg = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.INFO,
                                                Gtk.ButtonsType.CLOSE, "delete failed")
                        msgdlg.run()
                        msgdlg.destroy()
                
                elif cmdcode == 11:
                
                    columns = self.builderStats.get_object("TreeViewResults").get_columns()
                    for c in columns:
                        self.builderStats.get_object("TreeViewResults").remove_column(c)
                    store1 = Gtk.ListStore(str, str, str, str, str)
                    for i, column_title in enumerate(["type", "key", "ID", "field", "value"]):
                        renderer = Gtk.CellRendererText()
                        column = Gtk.TreeViewColumn(column_title, renderer, text=i)
                        column.set_sizing(Gtk.TreeViewColumnSizing.GROW_ONLY)
                        column.set_resizable(True)
                        column.set_min_width(200)
                        self.builderStats.get_object("TreeViewResults").append_column(column)

                    key = self.builderStats.get_object("entrykey").get_text()
                    values = self.redisHelper.xrange(key)
                    # print(values)
                    for v in values:
                        if v == None:
                            break
                        for v1 in v[1]:
                            store1.append(["stream", key, v[0], v1, v[1][v1]])
                    self.builderStats.get_object("TreeViewResults").set_model(store1)
            

