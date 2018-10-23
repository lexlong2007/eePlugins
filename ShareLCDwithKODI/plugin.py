# -*- coding: utf-8 -*-
#######################################################################
#
#    Plugin for Enigma2
#    Coded by j00zek (c)2018
#
#    Uszanuj moja prace i nie kasuj/zmieniaj informacji kto jest autorem konwertera
#    Please respect my work and don't delete/change name of the converter author
#
#    This program is free software; you can redistribute it and/or
#    modify it under the terms of the GNU General Public License
#    as published by the Free Software Foundation; either version 2
#    of the License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#     
#######################################################################
 
from __init__ import *
_ = mygettext

from Screens.Screen import Screen
from Components.config import config, ConfigSubsection, ConfigIP, ConfigNumber
from Components.ConfigList import ConfigListScreen
from Components.ActionMap import ActionMap
from Components.Sources.StaticText import StaticText
from Components.config import config, getConfigListEntry
from Plugins.Plugin import PluginDescriptor
from Screens.Setup import SetupSummary

config.plugins.ShareLCDwithKODI = ConfigSubsection()
config.plugins.ShareLCDwithKODI.IP = ConfigIP(default = [192,168,1,8], auto_jump = True) 
config.plugins.ShareLCDwithKODI.PORT = ConfigNumber(default = 8123)
######################################################################################################
def main(session, **kwargs):
    session.open(ShareLCDwithKODIconfig)

def Plugins(**kwargs):
    return [(  PluginDescriptor(name=_("Share LCD with KODI"), description=_("To show KODI state on LCD"),
                where=PluginDescriptor.WHERE_PLUGINMENU, icon="logo.png", fnc=main))]
######################################################################################################
class ShareLCDwithKODIconfig(Screen, ConfigListScreen):

    skin = """
    <screen name="ShareLCDwithKODIconfig" position="center,center" size="640,500" title="Share LCD with KODI" backgroundColor="#20606060" >
        <widget name="config" position="10,10" size="620,100" zPosition="-1" transparent="0" scrollbarMode="showOnDemand" />
        <eLabel position="10,120" size="620,350" zPosition="-1" backgroundColor="#00222222" /> 
        <!-- STATEICON -->
        <widget position="20,130" size="64,64" source="session.CurrentService" render="j00zekPicons" path="/usr/lib/enigma2/python/Plugins/Extensions/ShareLCDwithKODI"  picontype="icons" showdefaultpic="no" zPosition="5" alphatest="blend"> 
            <convert type="j00zekLCD4KODI">stateicon</convert>
        </widget>
        <!-- FULL INFO -->
        <eLabel position="20,200" size="130,40" font="HD_Thin; 27" zPosition="5" transparent="1" foregroundColor="yellow" noWrap="1" text="Full info:"/> 
        <widget position="140,200" size="600,24" font="Regular;22" zPosition="5" transparent="1" foregroundColor="white" render="Label" source="session.CurrentService" valign="center">
            <convert type="j00zekLCD4KODI">fullInfo</convert>
        </widget>
        <!-- TITLE -->
        <eLabel position="20,240" size="90,40" font="HD_Thin; 27" zPosition="5" transparent="1" foregroundColor="yellow" text="Title:"/> 
        <widget position="140,240" size="600,24" font="Regular;22" zPosition="5" transparent="1" foregroundColor="white" render="Label" source="session.CurrentService" valign="center">
            <convert type="j00zekLCD4KODI">title</convert>
        </widget>
        <!-- Movie Length/DURATION -->
        <eLabel position="20,280" size="100,40" font="HD_Thin; 27" zPosition="5" transparent="1" foregroundColor="yellow" text="Length:"/> 
        <widget position="140,280" size="600,24" font="Regular;22" zPosition="5" transparent="1" foregroundColor="white" render="Label" source="session.CurrentService" valign="center">
            <convert type="j00zekLCD4KODI">duration</convert>
        </widget>
        <!-- PLAYED TIME -->
        <eLabel position="20,320" size="100,40" font="HD_Thin; 27" zPosition="5" transparent="1" foregroundColor="yellow" text="Played:"/> 
        <widget position="140,320" size="600,24" font="Regular;22" zPosition="5" transparent="1" foregroundColor="white" render="Label" source="session.CurrentService" valign="center">
            <convert type="j00zekLCD4KODI">playedtime</convert>
        </widget>
        <!-- LEFT TIME -->
        <eLabel position="20,360" size="100,40" font="HD_Thin; 27" zPosition="5" transparent="1" foregroundColor="yellow" text="Left:"/> 
        <widget position="140,360" size="600,24" font="Regular;22" zPosition="5" transparent="1" foregroundColor="white" render="Label" source="session.CurrentService" valign="center">
            <convert type="j00zekLCD4KODI">lefttime</convert>
        </widget>
        <!-- LEFT MINS -->
        <eLabel position="290,360" size="100,40" font="HD_Thin; 27" zPosition="5" transparent="1" foregroundColor="yellow" text="/"/> 
        <widget position="320,360" size="600,24" font="Regular;22" zPosition="5" transparent="1" foregroundColor="white" render="Label" source="session.CurrentService" valign="center">
            <convert type="j00zekLCD4KODI">leftmins</convert>
        </widget>
        <!-- Progress -->
        <eLabel position="20,400" size="120,40" font="HD_Thin; 27" zPosition="5" transparent="1" foregroundColor="yellow" text="Progress:"/> 
        <ePixmap position="140,417" size="480,6" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/ShareLCDwithKODI/icons/progress_gray.png" zPosition="1" alphatest="blend" />
        <widget position="140,417" size="480,6" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/ShareLCDwithKODI/icons/progress_infobar.png" zPosition="5" source="session.CurrentService" render="Progress" transparent="1">
            <convert type="j00zekLCD4KODI">progress</convert>
        </widget>
        <widget name="key_red" position="0,365" zPosition="12" size="200,35" valign="center" halign="center" font="Regular;22" transparent="1" foregroundColor="red" />
        <widget name="key_green" position="220,365" zPosition="12" size="200,35" valign="center" halign="center" font="Regular;22" transparent="1" foregroundColor="green" />
    </screen>"""
    
    def __init__(self, session):
        Screen.__init__(self, session)
        # Summary
        self.setup_title = _("Share LCD with KODI %s" % Info )
        self.onChangedEntry = []

        # Buttons
        self["key_red"] = StaticText("Cancel")
        self["key_green"] = StaticText("OK")

        # Define Actions
        self["actions"] = ActionMap(["SetupActions"],
            {
                "cancel": self.keyCancel,
                "save": self.keySave,
            }
        )

        ConfigListScreen.__init__(
            self,
            [
                getConfigListEntry(_("Kodi address:"), config.plugins.ShareLCDwithKODI.IP),
                getConfigListEntry(_("Kodi port:"), config.plugins.ShareLCDwithKODI.PORT)
            ],
            session = session,
            on_change = self.changed
        )

        # Trigger change
        self.changed()

        self.onLayoutFinish.append(self.layoutFinished)

    def layoutFinished(self):
        self.setTitle(self.setup_title)

    def changed(self):
        for x in self.onChangedEntry:
            x()

    def getCurrentEntry(self):
        return self["config"].getCurrent()[0]

    def getCurrentValue(self):
        return str(self["config"].getCurrent()[1].getText())

    def createSummary(self):
        return SetupSummary
 