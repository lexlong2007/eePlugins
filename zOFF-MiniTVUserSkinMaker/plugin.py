# -*- coding: utf-8 -*-

# MiniTVUserSkinMaker
#
# maintainer: j00zek
# Uszanuj czyjąś pracę i NIE przywłaszczaj sobie autorstwa!

#This plugin is free software, you are allowed to
#modify it (if you keep the license),
#but you are not allowed to distribute/publish
#it without source code (this version and your modifications).
#This means you also have to distribute
#source code of your modifications.

from inits import *

from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
from Tools.Directories import fileExists, resolveFilename, SCOPE_PLUGINS

def Plugins(**kwargs):
    return [PluginDescriptor(name=_("miniTV User skin maker"), description="NA", where = PluginDescriptor.WHERE_MENU, fnc=menu)]

def menu(menuid, **kwargs):
    runPlugin = False
    if menuid == 'display': #display always on LCD submenu
        runPlugin = True
    elif menuid in ('vtimain', 'system') and not fileExists(resolveFilename(SCOPE_PLUGINS, 'Extensions/UserSkin')):
        runPlugin = True
    if runPlugin == True:
        from miniTVskinner import miniTVskinnerInitiator        
        return [(_("miniTV user skin maker"), miniTVskinnerInitiator, "miniTVUserSkinMeaker", 40)]
    return []
