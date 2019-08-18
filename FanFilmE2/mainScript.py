# -*- coding: utf-8 -*-

from inits import *
from e2navigator import *

from Components.Sources.List import List
from Screens.ChoiceBox import ChoiceBox
from Screens.MessageBox import MessageBox

from Screens.Screen import Screen
from enigma import getDesktop, gFont, eListboxPythonMultiContent, RT_HALIGN_LEFT, RT_HALIGN_RIGHT, \
                    RT_HALIGN_CENTER, RT_VALIGN_CENTER, RT_VALIGN_TOP, RT_VALIGN_BOTTOM, \
                      eLabel
from Tools.LoadPixmap import LoadPixmap
from Tools.Directories import fileExists, resolveFilename, SCOPE_SKIN, SCOPE_FONTS
from Plugins.Plugin import PluginDescriptor
from Components.Label import Label
from Components.ActionMap import ActionMap, HelpableActionMap
from Components.AVSwitch import AVSwitch
from Components.Sources.StaticText import StaticText
from Components.Pixmap import Pixmap, MovingPixmap
from Components.Slider import Slider
from Components.MenuList import MenuList
from Components.Pixmap import Pixmap

import glob, re, os, random, time

class FanFilmE2(Screen):
    def __init__(self, session):
              
        self.skin = """
        <screen name="FanFilmE2" title="FanFilmE2" position="center,center" size="1200,600">
          <!-- Widgets list on right -->
            <widget name="InfoLine" position="5,5" size="410,30" zPosition="5" transparent="0" halign="left" valign="top" font="Regular;28" foregroundColor="yellow" />
            <widget source="walkingList" render="Listbox" position="5,40" size="470,525" scrollbarMode="showOnDemand" zPosition="10" backgroundColor="#20a0a0a0">
                <convert type="TemplatedMultiContent">
                    {"template": [
                        MultiContentEntryPixmapAlphaTest(pos = (12, 2), size = (40, 40), png = 0),
                        MultiContentEntryText(pos = ( 8, 0), size = ( 40, 40), font=2, flags = RT_HALIGN_CENTER|RT_VALIGN_CENTER, text = 1, color=0xff0000, color_sel=0xff0000),
                        MultiContentEntryText(pos = (58, 2), size = (410, 40), font=0, flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 2, color=0x000000, color_sel=0xf0f0f0),
                        MultiContentEntryText(pos = (58, 2), size = (410, 40), font=1, flags = RT_HALIGN_RIGHT|RT_VALIGN_BOTTOM, text = 3, color=0xff0000, color_sel=0x880000),
                        ],
                        "fonts": [gFont("Regular", 21), gFont("Regular", 16), gFont("Regular", 32)],
                        "itemHeight": 44
                    }
                </convert>
            </widget>
          <!-- WIDGETS -->
          <!-- Bottom MENU -->
            <eLabel position="5,570" size="5,25" zPosition="-10" backgroundColor="#20b81c46" />
            <widget name="red" position="15,570" size="485,25" zPosition="10" font="Regular;21" noWrap="1" halign="left" valign="center" transparent="1"/>
            <eLabel position="305,570" size="5,25" zPosition="-10" backgroundColor="#20009f3c" />
            <widget name="green" position="315,570" size="485,25" zPosition="10" font="Regular;21" noWrap="1" halign="left" valign="center"  transparent="1"/>
            <eLabel position="605,570" size="5,25" zPosition="-10" backgroundColor="#209ca81b" />
            <widget name="yellow" position="615,570" size="485,25" zPosition="10" font="Regular;21" noWrap="1" halign="left" valign="center"  transparent="1"/>
            <eLabel position="905,570" size="5,25" zPosition="-10" backgroundColor="#202673ec" />
            <widget name="blue" position="915,570" size="485,25" zPosition="10" font="Regular;21" noWrap="1" halign="left" valign="center"  transparent="1"/>
</screen>"""
          
        self.session = session
        Screen.__init__(self, session)

        self["actions"]  = ActionMap(["OkCancelActions", "ColorActions"], {
            "keyCancel": self.KeyCancel,
            "keyOK": self.KeyOK,
            "red" : self.KeyRed,
            "green": self.KeyGreen,
            "yellow": self.KeyYellow,
            "blue" : self.KeyBlue,
        }, -1)

        self["walkingList"] = List()
        self["walkingList"].list = []

        self.chooseMenuList3 = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
        self.chooseMenuList3.l.setFont(0, gFont('Regular', 23))
        self.chooseMenuList3.l.setItemHeight(50)

        self['InfoLine'] = Label("Poziom główny")
        self['red'] = Label("Wyjście")
        self['green'] = Label("?")
        self['yellow'] = Label("??")
        self['blue'] = Label("Konfiguracja")
        
        self.onLayoutFinish.append(self.start)

    def start(self):
        self.setTitle(PluginName + pluginInfo)
          
        self.selectionChanged()

    def selectionChanged(self):
        self.currIndex=self["walkingList"].getIndex()
        
    def KeyOK(self):
        pass
        
    def KeyGreen(self):
        pass
        
    def KeyYellow(self):
        pass
        
    def KeyBlue(self):
        pass
        
    def KeyCancel(self):
        self.KeyRed()
        
    def KeyRed(self):
        self.close()
################################################################################################################################################################      
class FanFilmE2rLCDScreen(Screen):
    def __init__(self, session, parent):
        Screen.__init__(self, session, parent = parent)
        return
        
################################################################################################################################################################
from Components.Button import Button
from Components.config import *
from Components.ConfigList import ConfigListScreen
from Screens.VirtualKeyBoard import VirtualKeyBoard
from Tools.BoundFunction import boundFunction

################################################################################################################################################################
class FanFilmE2Config(Screen, ConfigListScreen):
    skin = """
    <screen name="FanFilmE2Config" position="center,center" size="640,500" title="FanFilmE2Config" backgroundColor="#20606060" >

            <widget name="config" position="10,10" size="620,450" zPosition="1" transparent="0" scrollbarMode="showOnDemand" />
            <widget name="key_red" position="0,465" zPosition="2" size="200,35" valign="center" halign="center" font="Regular;22" transparent="1" foregroundColor="red" />
            <widget name="key_green" position="220,465" zPosition="2" size="200,35" valign="center" halign="center" font="Regular;22" transparent="1" foregroundColor="green" />
            <widget name="key_blue" position="440,465" zPosition="2" size="200,35" valign="center" halign="center" font="Regular;22" transparent="1" foregroundColor="#202673ec" />
    </screen>"""
    
    def __init__(self, session ):
        Screen.__init__(self, session)

        ConfigListScreen.__init__(self, [], session)
        self["actions"] = ActionMap(["SetupActions", "ColorActions"],
            {
                "cancel": self.keyCancel,
                "red": self.keyRed,
                "green": self.keyGreen,
                "blue": self.keyBlue,
                "ok": self.keyOK,
            }, -2)

        self["key_green"] = Label("Zapisz")
        self["key_red"] = Label("Anuluj")
        self["key_blue"] = Label("Pokaż klawiaturę")

        self.list=[]
        
        self.onLayoutFinish.append(self.layoutFinished)

    def layoutFinished(self):
        self.setTitle('Konfiguracja ' + PluginName + pluginInfo)
        self.list.append(getConfigListEntry("--- Ogólne ---", myConfig.separator))
        self.list.append(getConfigListEntry("Zapisuj log do pliku %s:" % myDEBUGfile , myConfig.PrintDEBUG))

        self["config"].list = self.list        
        
    def keyOK(self):
        pass

    def keyGreen(self):
        for x in self["config"].list:
            x[1].save()
        configfile.save()
        self.close()

    def keyCancel(self):
        self.keyRed()
        
    def keyRed(self):
        for x in self["config"].list:
            x[1].cancel()
        self.close()
        
    def keyBlue(self):
        sel = self['config'].getCurrent()
        if sel:
            self.session.openWithCallback(self.VirtualKeyBoardCallback, VirtualKeyBoard, title=self['config'].getCurrent()[0], text=self['config'].getCurrent()[1].value)
        return

    def VirtualKeyBoardCallback(self, callback = None):
        if callback is not None and len(callback):
            self['config'].getCurrent()[1].setValue(callback)
            self['config'].invalidate(self['config'].getCurrent())
        return
