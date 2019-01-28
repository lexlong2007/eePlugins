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
import time

config.plugins.dynamicLCD = ConfigSubsection()
if eDBoxLCD.getInstance().detected():
    config.plugins.dynamicLCD.enabled = ConfigEnableDisable(default = False)
    config.plugins.dynamicLCD.debug = ConfigEnableDisable(default = False)
    val = int(config.lcd.standby.value * 255 / 10)
    if val > 255:
        val = 255
    config.plugins.dynamicLCD.NightStandbyBrightness = ConfigSlider(default= val, limits=(0, 255))
    config.plugins.dynamicLCD.NightStandbyBrightness23 = ConfigSlider(default=config.lcd.standby.value, limits=(0, 255))
    config.plugins.dynamicLCD.NightStandbyBrightness00 = ConfigSlider(default=config.lcd.standby.value, limits=(0, 255))
    config.plugins.dynamicLCD.NightStandbyBrightness01 = ConfigSlider(default=config.lcd.standby.value, limits=(0, 255))
    config.plugins.dynamicLCD.NightStandbyBrightness02 = ConfigSlider(default=config.lcd.standby.value, limits=(0, 255))
    config.plugins.dynamicLCD.NightStandbyBrightness03 = ConfigSlider(default=config.lcd.standby.value, limits=(0, 255))
    config.plugins.dynamicLCD.NightStandbyBrightness04 = ConfigSlider(default=config.lcd.standby.value, limits=(0, 255))
    config.plugins.dynamicLCD.NightStandbyBrightness05 = ConfigSlider(default=config.lcd.standby.value, limits=(0, 255))
    config.plugins.dynamicLCD.NightStandbyBrightness06 = ConfigSlider(default=config.lcd.standby.value, limits=(0, 255))
    config.plugins.dynamicLCD.NightStandbyBrightness07 = ConfigSlider(default=config.lcd.standby.value, limits=(0, 255))
else:
    config.plugins.dynamicLCD.enabled = NoSave(ConfigSelection(default = "0",choices = [("0", _("no LCD"))]))
    config.plugins.dynamicLCD.debug = ConfigNothing()
    config.plugins.dynamicLCD.NightStandbyBrightness = ConfigNothing()
    config.plugins.dynamicLCD.NightStandbyBrightness23 = ConfigNothing()
    config.plugins.dynamicLCD.NightStandbyBrightness00 = ConfigNothing()
    config.plugins.dynamicLCD.NightStandbyBrightness01 = ConfigNothing()
    config.plugins.dynamicLCD.NightStandbyBrightness02 = ConfigNothing()
    config.plugins.dynamicLCD.NightStandbyBrightness03 = ConfigNothing()
    config.plugins.dynamicLCD.NightStandbyBrightness04 = ConfigNothing()
    config.plugins.dynamicLCD.NightStandbyBrightness05 = ConfigNothing()
    config.plugins.dynamicLCD.NightStandbyBrightness06 = ConfigNothing()
    config.plugins.dynamicLCD.NightStandbyBrightness07 = ConfigNothing()

#DEBUG
if config.plugins.dynamicLCD.debug.value:
    DBG=True
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
    global MyTimer
    MyTimer.stop()

def standbyCounterChanged(configElement):
    if DBG: printDEBUG('standbyCounterChanged')
    global MyTimer
    try:
        if leaveStandby not in Screens.Standby.inStandby.onClose:
            Screens.Standby.inStandby.onClose.append(leaveStandby)
            MyTimer.start(1000,True)
    except Exception as e:
        if DBG: printDEBUG('standbyCounterChanged %s' % str(e))

def main(session, **kwargs):
    if DBG: printDEBUG("Open Config Screen")
    session.open(DynamicLCDbrightnessInStandbyConfiguration)

def delayedStandbyActions():
    global MyTimer
    MyTimer.stop()
    #tutaj logika ktore wlaczyc
    if eDBoxLCD.getInstance().detected():
        try:
            currTime = time.localtime()
            hour = int(currTime[3])
            Minutes = int(currTime[4])
            hourAndMinutes = time.strftime('%H:%M', currTime)
            if hour == 23:  val = config.plugins.dynamicLCD.NightStandbyBrightness23.value
            elif hour == 0: val = config.plugins.dynamicLCD.NightStandbyBrightness00.value
            elif hour == 1: val = config.plugins.dynamicLCD.NightStandbyBrightness01.value
            elif hour == 2: val = config.plugins.dynamicLCD.NightStandbyBrightness02.value
            elif hour == 3: val = config.plugins.dynamicLCD.NightStandbyBrightness03.value
            elif hour == 4: val = config.plugins.dynamicLCD.NightStandbyBrightness04.value
            elif hour == 5: val = config.plugins.dynamicLCD.NightStandbyBrightness05.value
            elif hour == 6: val = config.plugins.dynamicLCD.NightStandbyBrightness06.value
            elif hour == 7: val = config.plugins.dynamicLCD.NightStandbyBrightness07.value
            else: val = config.plugins.dynamicLCD.NightStandbyBrightness.value
            eDBoxLCD.getInstance().setLCDBrightness(int(val))
            if DBG: printDEBUG("delayedStandbyActions() at %s has set LCD brightess to %s and waits %s minutes for next invoke" % (hourAndMinutes, val,(60 - Minutes)) )
        except Exception as e:
            if DBG: printDEBUG("delayedStandbyActions() Exception: %s" % str(e))
        MyTimer.start((60 - Minutes) * 60 * 1000,True)
        
MyTimer = eTimer()
MyTimer.callback.append(delayedStandbyActions)

# sessionstart
def sessionstart(reason, session = None):
    if DBG: printDEBUG("autostart")
    from Screens.Standby import inStandby
    if reason == 0 and eDBoxLCD.getInstance().detected() and config.plugins.dynamicLCD.enabled.value:
        if DBG: printDEBUG('reason == 0 and dynamicLCD.enabled')
        config.misc.standbyCounter.addNotifier(standbyCounterChanged, initial_call=False)
        #MyTimer.start(10000,True)

def Plugins(path, **kwargs):
    return [PluginDescriptor(name=_("Dynamic LCD brightness"), where = PluginDescriptor.WHERE_PLUGINMENU, fnc = main, needsRestart = False),
            PluginDescriptor(name="DynamicLCDbrightness", where = PluginDescriptor.WHERE_SESSIONSTART, fnc = sessionstart, needsRestart = False, weight = -1)]

class DynamicLCDbrightnessInStandbyConfiguration(Screen, ConfigListScreen):
    def __init__(self, session):
        Screen.__init__(self, session)
        self.skinName = [ "Setup", ]

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

        ConfigList = self.buildConfigList()
        
        ConfigListScreen.__init__(self, ConfigList, session = session, on_change = self.changed)

        # Trigger change
        #self.changed()

        self.onLayoutFinish.append(self.__layoutFinished)
        self.onClose.append(self.__onClose)

    def buildConfigList(self):
        ConfigList = [getConfigListEntry(_("Control LCD brightness in Standby:"), config.plugins.dynamicLCD.enabled)]
        if eDBoxLCD.getInstance().detected():
            ConfigList.append(getConfigListEntry(_("Log to file"), config.plugins.dynamicLCD.debug))
            ConfigList.append(getConfigListEntry(_("08:00-23:00 (%s)") % config.plugins.dynamicLCD.NightStandbyBrightness.value, config.plugins.dynamicLCD.NightStandbyBrightness))
            ConfigList.append(getConfigListEntry(_("from %s (%s)") % ('23:00',config.plugins.dynamicLCD.NightStandbyBrightness23.value), config.plugins.dynamicLCD.NightStandbyBrightness23))
            ConfigList.append(getConfigListEntry(_("from %s (%s)") % ('00:00',config.plugins.dynamicLCD.NightStandbyBrightness00.value), config.plugins.dynamicLCD.NightStandbyBrightness00))
            ConfigList.append(getConfigListEntry(_("from %s (%s)") % ('01:00',config.plugins.dynamicLCD.NightStandbyBrightness01.value), config.plugins.dynamicLCD.NightStandbyBrightness01))
            ConfigList.append(getConfigListEntry(_("from %s (%s)") % ('02:00',config.plugins.dynamicLCD.NightStandbyBrightness02.value), config.plugins.dynamicLCD.NightStandbyBrightness02))
            ConfigList.append(getConfigListEntry(_("from %s (%s)") % ('03:00',config.plugins.dynamicLCD.NightStandbyBrightness03.value), config.plugins.dynamicLCD.NightStandbyBrightness03))
            ConfigList.append(getConfigListEntry(_("from %s (%s)") % ('04:00',config.plugins.dynamicLCD.NightStandbyBrightness04.value), config.plugins.dynamicLCD.NightStandbyBrightness04))
            ConfigList.append(getConfigListEntry(_("from %s (%s)") % ('05:00',config.plugins.dynamicLCD.NightStandbyBrightness05.value), config.plugins.dynamicLCD.NightStandbyBrightness05))
            ConfigList.append(getConfigListEntry(_("from %s (%s)") % ('06:00',config.plugins.dynamicLCD.NightStandbyBrightness06.value), config.plugins.dynamicLCD.NightStandbyBrightness06))
            ConfigList.append(getConfigListEntry(_("from %s (%s)") % ('07:00',config.plugins.dynamicLCD.NightStandbyBrightness07.value), config.plugins.dynamicLCD.NightStandbyBrightness07))
        return ConfigList
        
    def __layoutFinished(self):
        self.setTitle(self.setup_title)
        try:
            self["title"]=StaticText(self.setup_title)
        except:
            pass

    def __onClose(self):
        try:
            val = int(config.lcd.bright.value * 255 / 10)
            if val > 255:
                val = 255
            eDBoxLCD.getInstance().setLCDBrightness(val)
        except Exception:
            pass
    
    def changed(self):
        for x in self.onChangedEntry:
            x()
        if self.getCurrentEntryConfig() != config.plugins.dynamicLCD.enabled:
            currValue = self.getCurrentValue()
            try:
                currValue = int(currValue.split('/')[0].strip())
                eDBoxLCD.getInstance().setLCDBrightness(currValue)
            except Exception as e:
                if DBG: printDEBUG("Exception: %s" % str(e), True)
            if DBG: printDEBUG("%s > %s" % (self.getCurrentEntry(), currValue), True)
            self["config"].list = self.buildConfigList()

    def getCurrentEntry(self):
        return self["config"].getCurrent()[0]

    def getCurrentEntryConfig(self):
        return self["config"].getCurrent()[1]

    def getCurrentValue(self):
        return str(self["config"].getCurrent()[1].getText())

    def createSummary(self):
        return dynamicLCDsummary

##################################################################### LCD Screen <<<<<<<<<<<<<<<<<<<<<<<<<<<<<
class dynamicLCDsummary(Screen):
    def __init__(self, session, parent):
        Screen.__init__(self, session)
        self.skinName = [ "StandbySummary", ]
##################################################################### CLASS ENDS <<<<<<<<<<<<<<<<<<<<<<<<<<<<<         
if DBG: printDEBUG("Loaded", False)