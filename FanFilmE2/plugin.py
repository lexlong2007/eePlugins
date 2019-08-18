# -*- coding: utf-8 -*-

# FanFilmE2
#
# maintainer: j00zek
# Uszanuj czyjąś pracę i NIE przywłaszczaj sobie autorstwa!

#This plugin is free software, you are allowed to use it but you are not allowed to distribute/publish disassemble/decompile

from inits import *
import mainScript

from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
from Tools.Directories import SCOPE_PLUGINS

printDEBUG('plugin.py','został załadowany' )

def Plugins(**kwargs):
    return [PluginDescriptor(name="FanFilm dla E2", description=" ", where = PluginDescriptor.WHERE_PLUGINMENU, icon="icons/FanFilmE2_100x40.png", fnc=loadMain)]

def loadMain(session, **kwargs):
    try:
        reload(mainScript)
    except Exception, e:
        printDEBUG('plugin.loadMain()','Wyjątek przy przeładowaniu main: %s' % str(e))
    try:
        session.open(mainScript.FanFilmE2)
    except Exception, e:
        printDEBUG('plugin.loadMain()','Wyjątek przy uruchamianiu mainScript.FanFilmE2: %s' % str(e))
