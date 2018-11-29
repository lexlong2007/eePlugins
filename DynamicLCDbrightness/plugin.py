# -*- coding: iso-8859-2 -*-
from __init__ import mygettext as _
from version import Version

from enigma import eTimer, eDBoxLCD
from Components.ActionMap import ActionMap
from Components.config import config, ConfigSubsection, ConfigEnableDisable, ConfigSlider, ConfigSelection, ConfigNothing, getConfigListEntry, NoSave
from Components.ConfigList import ConfigListScreen
from Components.Sources.StaticText import StaticText
from datetime import datetime
from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
from Screens.Setup import SetupSummary
from Tools import Notifications

import Screens.Standby

config.plugins.dynamicLCD = ConfigSubsection()
if eDBoxLCD.getInstance().detected():
    config.plugins.dynamicLCD.enabled = ConfigEnableDisable(default = False)
    #config.plugins.dynamicLCD.brightnessStandby = config.lcd.standby.value
    config.plugins.dynamicLCD.NightStandbyBrightness = ConfigSlider(default=config.lcd.standby.value, limits=(0, 255))
    config.plugins.dynamicLCD.NightStandbyPeriod = ConfigSelection(default = "23:30-4:30",
                                                                    choices = [("23:30-4:30", _("between 23:30-4:30")),
                                                                               ("sunset+30-4:30", _("30min after sunset-30min before sunrise"))
                                                                              ])
else:
    config.plugins.dynamicLCD.enabled = NoSave(ConfigSelection(default = "0",choices = [("0", _("LCD not detected"))]))
    config.plugins.dynamicLCD.DeepStandbyBrightness = ConfigNothing()
    config.plugins.dynamicLCD.DeepStandbyPeriod = ConfigNothing()

#DEBUG
DBG=True
if DBG:
    def printDEBUG(myText, append2file=True):
        try:
            if append2file == False:
                f = open('/tmp/dynamicLCDbrightness.log', 'w')
            else:
                f = open('/tmp/dynamicLCDbrightness.log', 'a')
            f.write('%s %s\n' %(str(datetime.now()), myText))
            f.close
        except: pass

def leaveStandby():
    if DBG: printDEBUG('leaveStandby, stop timer')
    MyTimer.stop()

def standbyCounterChanged(configElement):
    if DBG: printDEBUG('standbyCounterChanged')
    try:
        if leaveStandby not in Screens.Standby.inStandby.onClose:
            Screens.Standby.inStandby.onClose.append(leaveStandby)
            MyTimer.start(1000,True)
    except Exception as e:
        if DBG: printDEBUG('standbyCounterChanged %s' % str(e))

def main(session, **kwargs):
    if DBG: printDEBUG("Open Config Screen")
    session.open(DynamicLCDbrightnessConfiguration)

def delayedStandbyActions():
    if DBG: printDEBUG("delayedStandbyActions")
    global MyTimer
    MyTimer.stop()
    #tutaj logika ktore wlaczyc
    if eDBoxLCD.getInstance().detected() and 1 == 0 :
        eDBoxLCD.getInstance().setLCDBrightness(config.plugins.dynamicLCD.NightStandbyBrightness.value)
        
MyTimer = eTimer()
MyTimer.callback.append(delayedStandbyActions)

# sessionstart
def sessionstart(reason, session = None):
    if DBG: printDEBUG("autostart")
    from Screens.Standby import inStandby
    if reason == 0 and eDBoxLCD.getInstance().detected() and config.plugins.dynamicLCD.enabled.value:
        if DBG: printDEBUG('reason == 0 and dynamicLCD.enabled')
        config.misc.standbyCounter.addNotifier(standbyCounterChanged, initial_call=False)
        MyTimer.start(10000,True)

def Plugins(path, **kwargs):
    return [PluginDescriptor(name=_("Dynamic LCD brightness"), where = PluginDescriptor.WHERE_PLUGINMENU, fnc = main, needsRestart = False),
            PluginDescriptor(name="DynamicLCDbrightness", where = PluginDescriptor.WHERE_SESSIONSTART, fnc = sessionstart, needsRestart = False, weight = -1)]

class DynamicLCDbrightnessConfiguration(Screen, ConfigListScreen):
    """Configuration of Startup To Standby"""

    def __init__(self, session):
        Screen.__init__(self, session)
        self.skinName = [ "DynamicLCDbrightnessConfiguration", "Setup" ]

        # Summary
        self.setup_title = _("DynamicLCDbrightness v %s Configuration") % Version
        self.onChangedEntry = []

        # Buttons
        self["key_red"] = StaticText(_("Cancel"))
        self["key_green"] = StaticText(_("OK"))

        # Define Actions
        self["actions"] = ActionMap(["SetupActions"],
            {
                "cancel": self.keyCancel,
                "save": self.keySave,
            }
        )

        ConfigList = [getConfigListEntry(_("State:"), config.plugins.dynamicLCD.enabled)]
        if eDBoxLCD.getInstance().detected():
            ConfigList.append(getConfigListEntry(_("Brightness in standby:"), config.lcd.standby))
            ConfigList.append(getConfigListEntry(_("Brightness in night standby:"), config.plugins.dynamicLCD.NightStandbyBrightness))
            ConfigList.append(getConfigListEntry(_("Night standby period:"), config.plugins.dynamicLCD.NightStandbyPeriod))
        
        ConfigListScreen.__init__(self, ConfigList, session = session, on_change = self.changed)

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
        
if DBG: printDEBUG("Loaded", False)