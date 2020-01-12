# -*- coding: utf-8 -*-
#
# maintainer: j00zek 2020
#

#This plugin is free software, you are allowed to
#modify it (if you keep the license),
#but you are not allowed to distribute/publish
#it without source code (this version and your modifications).
#This means you also have to distribute
#source code of your modifications.

from __init__ import *
from __init__ import translate as _ 

from Components.ActionMap import ActionMap

from Components.config import *
from enigma import eTimer
from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
        
def Plugins(**kwargs):
    return [PluginDescriptor(name=_(PluginName), description=PluginInfo, where = PluginDescriptor.WHERE_PLUGINMENU, fnc=main,icon="logo.png")]

def main(session, **kwargs):
    from myComponents import j00zekIPTVmgr
    session.open(j00zekIPTVmgr, MenuFolder = '%s/scripts' % PluginPath, MenuFile = '%s/_Menu' % PluginPath, MenuTitle = "%s %s" % ( _(PluginName), PluginInfo))
