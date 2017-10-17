# -*- coding: utf-8 -*-

# UserSkin, based on AtileHD concept by schomi & plnick
#
# maintainer: j00zek
#
# extension for openpli, all skins, descriptions, bar selections and other @j00zek 2014/2015
# Uszanuj czyj¹œ pracê i NIE przyw³aszczaj sobie autorstwa!

#This plugin is free software, you are allowed to
#modify it (if you keep the license),
#but you are not allowed to distribute/publish
#it without source code (this version and your modifications).
#This means you also have to distribute
#source code of your modifications.

from debug import printDEBUG
from inits import *
from myComponents import UserSkinToolSet

from Components.ActionMap import ActionMap
from Components.config import *
from Components.ConfigList import ConfigListScreen
from Components.Label import Label
from Components.Pixmap import Pixmap
from Components.Sources.List import List
from Components.Sources.StaticText import StaticText
from enigma import ePicLoad, eTimer
from Plugins.Plugin import PluginDescriptor
from Screens.ChoiceBox import ChoiceBox
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Screens.Standby import TryQuitMainloop
from Tools.Directories import *
from Tools.LoadPixmap import LoadPixmap
from Tools import Notifications
#system imports
from os import listdir, remove, rename, system, path, symlink, chdir, rmdir, mkdir
import shutil
import re

from translate import _

#UserSkin permanent configs, we use AtileHD for compatibility reasons
config.plugins.AtileHD = ConfigSubsection()
config.plugins.AtileHD.refreshInterval = ConfigNumber(default=30) #in minutes
config.plugins.AtileHD.woeid = ConfigNumber(default=523920) #Location Warsaw (visit weather.yahoo.com)
config.plugins.AtileHD.tempUnit = ConfigSelection(default="Celsius", choices = [
                ("Celsius", _("Celsius")),
                ("Fahrenheit", _("Fahrenheit"))
                ])
config.plugins.UserSkin = ConfigSubsection()
config.plugins.UserSkin.refreshInterval = ConfigNumber(default=30) #in minutes
config.plugins.UserSkin.woeid = ConfigNumber(default=523920) #Location Warsaw (visit weather.yahoo.com)
config.plugins.UserSkin.tempUnit = ConfigSelection(default="Celsius", choices = [
                ("Celsius", _("Celsius")),
                ("Fahrenheit", _("Fahrenheit"))
                ])
       
def isSlowCPU():
    fc=''
    ret=False
    with open('/proc/cpuinfo', 'r') as f:
        for fc in f:
            if fc.startswith('bogomips') and fc.find(':') > 0 :
                if int(float(fc.split(':')[1].strip())) < 400:
                    ret = True
                break
        f.close()
    return ret

if isSlowCPU() == False:
    config.plugins.UserSkin.jpgPreview = ConfigYesNo(default = True)
else:
    config.plugins.UserSkin.jpgPreview = ConfigYesNo(default = False)

config.plugins.UserSkin.AdvancedMode = ConfigSelection(default="copyScreens", choices = [
                ("copyScreens", _("Generic")),
                ("mergeScreens", _("Advanced (merge screens)"))
                ])

class UserSkin_Config(Screen, ConfigListScreen):
    skin = """
  <screen name="UserSkin_Config" position="82,124" size="1101,376" title="UserSkin Setup" backgroundColor="transparent" flags="wfNoBorder">
    <eLabel position="7,2" size="1091,372" zPosition="-15" backgroundColor="#20000000" />
    <eLabel position="4,51" size="664,238" zPosition="-10" backgroundColor="#20606060" />
    <eLabel position="672,51" size="410,237" zPosition="-10" backgroundColor="#20606060" />
    <eLabel position="6,302" size="240,55" zPosition="-10" backgroundColor="#20b81c46" />
    <eLabel position="284,302" size="240,55" zPosition="-10" backgroundColor="#20009f3c" />
    <eLabel position="564,302" size="240,56" zPosition="-10" backgroundColor="#209ca81b" />
    <eLabel position="843,302" size="240,55" zPosition="-10" backgroundColor="#202673ec" />
    <widget source="Title" render="Label" position="2,4" size="889,43" font="Regular;35" foregroundColor="#00ffffff" backgroundColor="#004e4e4e" transparent="1" />
    <widget name="config" position="6,55" size="657,226" scrollbarMode="showOnDemand" transparent="1" />
    <widget name="Picture" position="676,56" size="400,225" alphatest="blend" />
    <widget name="key_red" position="18,316" size="210,25" zPosition="1" font="Regular;20" halign="left" foregroundColor="#00ffffff" backgroundColor="#20b81c46" transparent="1" />
    <widget name="key_green" position="299,317" size="210,25" zPosition="1" font="Regular;20" halign="left" foregroundColor="#00ffffff" backgroundColor="#20009f3c" transparent="1" />
    <widget name="key_yellow" position="578,317" size="210,25" zPosition="1" font="Regular;20" halign="left" foregroundColor="#00ffffff" backgroundColor="#209ca81b" transparent="1" />
    <widget name="key_blue" position="854,318" size="210,25" zPosition="1" font="Regular;20" halign="left" foregroundColor="#00ffffff" backgroundColor="#202673ec" transparent="1" />
  </screen>
"""

    skin_lines = []
    changed_screens = False
        
    def __init__(self, session, args = 0):
        self.session = session
        Screen.__init__(self, session)
        self.UserSkinToolSet = UserSkinToolSet()
        
        myTitle=_("UserSkin Setup %s") % UserSkinInfo
        self.setTitle(myTitle)
        try:
            self["title"]=StaticText(myTitle)
        except:
            pass
            
        self.currentSkin = CurrentSkinName
        printDEBUG("SkinPath=%s, skin=%s, currentSkin=%s" % (SkinPath, config.skin.primary_skin.value, self.currentSkin))
        if self.currentSkin != '':
                self.currentSkin = '_' + self.currentSkin # default_skin = '', others '_skinname', used later
                
        if path.exists(resolveFilename(SCOPE_PLUGINS, 'SystemPlugins/VTIPanel/')):
            self.isVTI = True
        else:
            self.isVTI = False
            
        self.defaultOption = "default"
        self.defaults = (self.defaultOption, _("Default"))
        self.OnlyDefault = (self.defaultOption, _("Nothing to select"))
        self.color_file = "skin_user_colors.xml"
        self.windowstyle_file = "skin_user_window.xml"
        self.user_font_file = "skin_user_header.xml"
        self.user_bar_link = 'skin_user_bar'
        
        if path.exists(SkinPath):
            #FONTS
            if path.exists(SkinPath + self.user_font_file):
                self.default_font_file = path.basename(path.realpath(SkinPath + self.user_font_file))
                printDEBUG("self.default_font_file = " + self.default_font_file )
            else:
                self.default_font_file = self.defaultOption
            if not path.exists(SkinPath + "allFonts/"):
                mkdir(SkinPath + "allFonts/")
            #COLORS
            if path.exists(SkinPath + self.color_file):
                self.default_color_file = path.basename(path.realpath(SkinPath + self.color_file))
                printDEBUG("self.default_color_file = " + self.default_color_file )
            else:
                self.default_color_file = self.defaultOption
                
            if not path.exists(SkinPath + "allColors/"):
                mkdir(SkinPath + "allColors/")
            #WINDOWS
            if path.exists(SkinPath + self.color_file):
                self.default_windowstyle_file = path.basename(path.realpath(SkinPath + self.windowstyle_file))
                printDEBUG("self.default_windowstyle_file = " + self.default_windowstyle_file )
            else:
                self.default_windowstyle_file = self.defaultOption
                
            if not path.exists(SkinPath + "allWindows/"):
                mkdir(SkinPath + "allWindows/")
            #PREVIEW
            if not path.exists(SkinPath + "allPreviews"):
                mkdir(SkinPath + "allPreviews/")
            if path.exists(SkinPath + "preview"):
                if self.isVTI == False and path.isdir(SkinPath + "preview"):
                    try: rmdir(SkinPath + "preview")
                    except: pass
            else:
                if self.isVTI == True:
                    symlink(SkinPath + "allPreviews", SkinPath + "preview")
            #SELECTOR
            if not path.exists(SkinPath + "allBars"):
                mkdir(SkinPath + "allBars/")
            if path.exists(SkinPath + self.user_bar_link):
                self.default_user_bar_link = path.basename(path.realpath(SkinPath + self.user_bar_link))
                printDEBUG("self.user_bar_link = " + self.default_user_bar_link )
            else:
                self.default_user_bar_link = self.defaultOption
            #DESCRIPTIONS
            if not path.exists(SkinPath + "allInfos"):
                mkdir(SkinPath + "allInfos/")
            #configurable screens
            if not path.exists(SkinPath + "allScreens"):
                mkdir(SkinPath + "allScreens/")
            #SELECTED Skins folder - We use different folder name (more meaningfull) for selections
            if path.exists(SkinPath + "mySkin_off"):
                if not path.exists(SkinPath + "UserSkin_Selections"):
                    chdir(SkinPath)
                    try:
                        rename("mySkin_off", "UserSkin_Selections")
                    except:
                        pass

        current_color = self.getCurrentColor()[0]
        current_windowstyle = self.getCurrentWindowstyle()[0]
        current_font = self.getCurrentFont()[0]
        current_bar = self.getCurrentBar()[0]
        myUserSkin_active = self.getmySkinState()
        self.myUserSkin_active = NoSave(ConfigYesNo(default=myUserSkin_active))
        self.myUserSkin_font = NoSave(ConfigSelection(default=current_font, choices = self.getPossibleFont()))
        self.myUserSkin_style = NoSave(ConfigSelection(default=current_color, choices = self.getPossibleColor()))
        self.myUserSkin_windowstyle = NoSave(ConfigSelection(default=current_windowstyle, choices = self.getPossibleWindowstyle()))
        self.myUserSkin_bar = NoSave(ConfigSelection(default=current_bar, choices = self.getPossibleBars()))
        
        self.myUserSkin_fake_entry = NoSave(ConfigNothing())
        self.LackOfFile = ''
        
        self.list = []
        ConfigListScreen.__init__(self, self.list, session = self.session, on_change = self.changedEntry)

        self["key_red"] = Label(_("Cancel"))
        self["key_green"] = Label(_("OK"))
        self["key_yellow"] = Label()
        self["key_blue"] = Label()
        self["setupActions"] = ActionMap(["SetupActions", "ColorActions"],
            {
                "green": self.keyOk,
                "red": self.cancel,
                "yellow": self.keyYellow,
                "blue": self.keyBlue,
                "cancel": self.cancel,
                "ok": self.keyOk,
            }, -2)
            
        self["Picture"] = Pixmap()
        
        if not self.selectionChanged in self["config"].onSelectionChanged:
            self["config"].onSelectionChanged.append(self.selectionChanged)
        
        self.createConfigList()
        self.updateEntries = False
        
    def createConfigList(self):
        self.set_bar = getConfigListEntry(_("Selector bar style:"), self.myUserSkin_bar)
        self.set_color = getConfigListEntry(_("Colors:"), self.myUserSkin_style)
        self.set_windowstyle = getConfigListEntry(_("Window style:"), self.myUserSkin_windowstyle)
        self.set_font = getConfigListEntry(_("Font:"), self.myUserSkin_font)
        self.set_myatile = getConfigListEntry(_("Enable skin personalization:"), self.myUserSkin_active)
        self.list = []
        self.list.append(self.set_myatile)
        self.list.append(getConfigListEntry(_("Personalization mode:"), config.plugins.UserSkin.AdvancedMode ))
        self.list.append(self.set_color)
        self.list.append(self.set_windowstyle)
        self.list.append(self.set_font)
        self.list.append(self.set_bar)
        if 0:
            if path.exists(resolveFilename(SCOPE_PLUGINS, '../Components/Renderer/VWeatherUpdater.py')) or \
                path.exists(resolveFilename(SCOPE_PLUGINS, '../Components/Renderer/VWeatherUpdater.pyo')) or \
                path.exists(resolveFilename(SCOPE_PLUGINS, '../Components/Converter/inHDGOSVWeather2.pyo')) or \
                path.exists(resolveFilename(SCOPE_PLUGINS, '../Components/Renderer/MetrixHDWeatherUpdaterStandalone.pyo')) or \
                path.exists(resolveFilename(SCOPE_PLUGINS, '../Components/Renderer/VWeatherUpdater.pyc')):
                self.list.append(getConfigListEntry(_("---Yahoo Weather---"), self.myUserSkin_fake_entry))
                self.list.append(getConfigListEntry(_("Refresh interval in minutes:"), config.plugins.AtileHD.refreshInterval))
                self.list.append(getConfigListEntry(_("Location # (http://weather.yahoo.com/):"), config.plugins.AtileHD.woeid))
                self.list.append(getConfigListEntry(_("Temperature unit:"), config.plugins.AtileHD.tempUnit))
        if isSlowCPU() == True:
            self.list.append(getConfigListEntry(_("No JPG previews:"), config.plugins.UserSkin.jpgPreview))
        self["config"].list = self.list
        self["config"].l.setList(self.list)
        if self.myUserSkin_active.value:
            self["key_yellow"].setText(_("User skins"))
            self["key_blue"].setText(_("Extract from skin.xml"))
        else:
            self["key_yellow"].setText("")
            self["key_blue"].setText("")

    def changedEntry(self):
        self.updateEntries = True
        printDEBUG("[UserSkin:changedEntry]")
        if self["config"].getCurrent() == self.set_color:
            self.setPicture(self.myUserSkin_style.value)
        elif self["config"].getCurrent() == self.set_windowstyle:
            self.setPicture(self.myUserSkin_windowstyle.value)
        elif self["config"].getCurrent() == self.set_font:
            self.setPicture(self.myUserSkin_font.value)
        elif self["config"].getCurrent() == self.set_bar:
            self.setPicture(self.myUserSkin_bar.value)
        elif self["config"].getCurrent() == self.set_myatile:
            if self.myUserSkin_active.value:
                self["key_yellow"].setText(_("User skins"))
            else:
                self["key_yellow"].setText("")

    def selectionChanged(self):
        if self["config"].getCurrent() == self.set_color:
            self.setPicture(self.myUserSkin_style.value)
        elif self["config"].getCurrent() == self.set_windowstyle:
            self.setPicture(self.myUserSkin_windowstyle.value)
        elif self["config"].getCurrent() == self.set_font:
            self.setPicture(self.myUserSkin_font.value)
        elif self["config"].getCurrent() == self.set_bar:
            self.setPicture(self.myUserSkin_bar.value)
        else:
            self["Picture"].hide()

    def cancel(self):
        if self["config"].isChanged():
            self.session.openWithCallback(self.cancelConfirm, MessageBox, _("Save settings?"), MessageBox.TYPE_YESNO, default = False)
        else:
            for x in self["config"].list:
                x[1].cancel()
            if self.changed_screens:
                self.restartGUI()
            else:
                self.close()

    def cancelConfirm(self, result):
        if result is None or result is False:
            printDEBUG("Cancel confirmed.")
        else:
            printDEBUG("Cancel confirmed. Config changes will be lost.")
            for x in self["config"].list:
                x[1].cancel()
            self.close()
                
    def getPossibleColor(self):
        mylist = []
        
        if path.exists(SkinPath + "allColors/"):
            for f in sorted(listdir(SkinPath + "allColors/"), key=str.lower):
                if f.endswith('.xml') and f.startswith('colors_'):
                    friendly_name = f.replace("colors_atile_", "").replace("colors_", "")
                    friendly_name = friendly_name.replace(".xml", "")
                    friendly_name = friendly_name.replace("_", " ")
                    mylist.append((f, friendly_name))
        
            for f in sorted(listdir(SkinPath), key=str.lower):
                if f.endswith('.xml') and f.startswith('colors_'):
                    friendly_name = f.replace("colors_atile_", "").replace("colors_", "")
                    friendly_name = friendly_name.replace(".xml", "")
                    friendly_name = friendly_name.replace("_", " ")
                    mylist.append((f, friendly_name))
        if len(mylist) == 0:
            mylist.insert(0, self.OnlyDefault)
        else:
            mylist.insert(0, self.defaults)
          
        return mylist

    def getPossibleWindowstyle(self):
        mylist = []
        
        if path.exists(SkinPath + "allWindows/"):
            for f in sorted(listdir(SkinPath + "allWindows/"), key=str.lower):
                if f.endswith('.xml') and f.startswith('window_'):
                    friendly_name = f.replace("window_atile_", "").replace("window_", "")
                    friendly_name = friendly_name.replace(".xml", "")
                    friendly_name = friendly_name.replace("_", " ")
                    mylist.append((f, friendly_name))
        
            for f in sorted(listdir(SkinPath), key=str.lower):
                if f.endswith('.xml') and f.startswith('window_'):
                    friendly_name = f.replace("window_atile_", "").replace("window_", "")
                    friendly_name = friendly_name.replace(".xml", "")
                    friendly_name = friendly_name.replace("_", " ")
                    mylist.append((f, friendly_name))

        if len(mylist) == 0:
            mylist.insert(0, self.OnlyDefault)
        else:
            mylist.insert(0, self.defaults)
          
        return mylist		

    def getPossibleFont(self):
        mylist = []
        
        if path.exists(SkinPath + "allFonts/"):
            for f in sorted(listdir(SkinPath + "allFonts/"), key=str.lower):
                if f.endswith('.xml') and f.startswith('font_'):
                    friendly_name = f.replace("font_atile_", "").replace("font_", "")
                    friendly_name = friendly_name.replace(".xml", "")
                    friendly_name = friendly_name.replace("_", " ")
                    mylist.append((f, friendly_name))

            for f in sorted(listdir(SkinPath), key=str.lower):
                if f.endswith('.xml') and f.startswith('font_'):
                    friendly_name = f.replace("font_atile_", "").replace("font_", "")
                    friendly_name = friendly_name.replace(".xml", "")
                    friendly_name = friendly_name.replace("_", " ")
                    mylist.append((f, friendly_name))

        if len(mylist) == 0:
            mylist.insert(0, self.OnlyDefault)
        else:
            mylist.insert(0, self.defaults)
          
        return mylist

    def getmySkinState(self):
        chdir(SkinPath)
        if path.exists("mySkin"):
            return True
        else:
            return False

    def getCurrentColor(self):
        myfile = SkinPath + self.color_file
        if not path.exists(myfile):
            if path.exists(SkinPath + "allColors/" + self.default_color_file):
                if path.islink(myfile):
                    remove(myfile)
                chdir(SkinPath)
                symlink("allColors/" + self.default_color_file, self.color_file)
            else:
                return (self.default_color_file, self.default_color_file)
        filename = path.realpath(myfile)
        filename = path.basename(filename)
        friendly_name = filename.replace("colors_atile_", "").replace("colors_", "")
        friendly_name = friendly_name.replace(".xml", "")
        friendly_name = friendly_name.replace("_", " ")
        return (filename, friendly_name)

    def getCurrentWindowstyle(self):
        myfile = SkinPath + self.windowstyle_file
        if not path.exists(myfile):
            if path.exists(SkinPath + "allWindows/" + self.default_windowstyle_file):
                if path.islink(myfile):
                    remove(myfile)
                chdir(SkinPath)
                symlink("allWindows/" + self.default_windowstyle_file, self.windowstyle_file)
            else:
                return (self.default_windowstyle_file, self.default_windowstyle_file)
        filename = path.realpath(myfile)
        filename = path.basename(filename)
        friendly_name = filename.replace("window_atile_", "").replace("window_", "")
        friendly_name = friendly_name.replace(".xml", "")
        friendly_name = friendly_name.replace("_", " ")
        return (filename, friendly_name)
		
    def getCurrentFont(self):
        myfile = SkinPath + self.user_font_file
        if not path.exists(myfile):
            if path.exists(SkinPath + "allFonts/" + self.default_font_file):
                if path.islink(myfile):
                    remove(myfile)
                chdir(SkinPath)
                symlink("allFonts/" + self.default_font_file, self.user_font_file)
            else:
                return (self.default_font_file, self.default_font_file)
        filename = path.realpath(myfile)
        filename = path.basename(filename)
        friendly_name = filename.replace("font_atile_", "").replace("font_", "")
        friendly_name = friendly_name.replace(".xml", "")
        friendly_name = friendly_name.replace("_", " ")
        return (filename, friendly_name)

    def setPictureOLD(self, f):
        preview = SkinPath + "allPreviews/"
        if not path.exists(preview):
            mkdir(preview)
        pic = f[:-4]
        if f.startswith("bar_"):
            pic = f + ".png"
        printDEBUG("[UserSkin:setPicture] pic =" + pic + '[jpg|png]')
        previewJPG = preview + "preview_" + picJPG
        if path.exists(preview + "preview_" + pic + '.jpg'):
            self.UpdatePreviewPicture(preview + "preview_" + pic + '.jpg')
        if path.exists(preview + "preview_" + pic + '.png'):
            self.UpdatePreviewPicture(preview + "preview_" + pic + '.png')
        else:
            self["Picture"].hide()

    def setPicture(self, f):
        if f[-4:] == '.xml':
            pic = f[:-4]
        else:
            pic = f
        #check for jpg
        if path.exists(SkinPath + "allPreviews/" + pic + '.jpg'):
            self.UpdatePreviewPicture(SkinPath + "allPreviews/" + pic + '.jpg')
        elif path.exists(SkinPath + "allPreviews/preview_" + pic + '.jpg'):
            self.UpdatePreviewPicture(SkinPath + "allPreviews/preview_" + pic + '.jpg')
        #check for png
        elif path.exists(SkinPath + "allPreviews/" + pic + '.png'):
            self.UpdatePreviewPicture(SkinPath + "allPreviews/" + pic + '.png')
        elif path.exists(SkinPath + "allPreviews/preview_" + pic + '.png'):
            self.UpdatePreviewPicture(SkinPath + "allPreviews/preview_" + pic + '.png')
        else:
            printDEBUG("[UserSkin:setPicture] pic for '%s' not found" % pic )
            self["Picture"].hide()
    
    def UpdatePreviewPicture(self, PreviewFileName):
            printDEBUG("[UserSkin:UpdatePreviewPicture] pic =" + PreviewFileName)
            self["Picture"].instance.setScale(1)
            self["Picture"].instance.setPixmap(LoadPixmap(path=PreviewFileName))
            self["Picture"].show()
            
    def keyYellow(self):
        if self.myUserSkin_active.value:
            if not path.exists(SkinPath + "UserSkin_Selections"):
                mkdir(SkinPath + "UserSkin_Selections")
            if not path.exists(SkinPath + "allPreviews"):
                mkdir(SkinPath + "allPreviews")
            self.session.openWithCallback(self.UserSkinScreesnCB, TreeUserSkinScreens)
        else:
            self["config"].setCurrentIndex(0)

    def keyOk(self):
        if self["config"].isChanged() or self.updateEntries == True:
            printDEBUG("[UserSkin:keyOk] self.myUserSkin_font.value=" + self.myUserSkin_font.value)
            printDEBUG("[UserSkin:keyOk] self.myUserSkin_style.value=" + self.myUserSkin_style.value)
            printDEBUG("[UserSkin:keyOk] self.myUserSkin_windowstyle.value=" + self.myUserSkin_windowstyle.value)
            printDEBUG("[UserSkin:keyOk] self.myUserSkin_bar.value=" + self.myUserSkin_bar.value)
            config.plugins.UserSkin.refreshInterval.value = config.plugins.AtileHD.refreshInterval.value
            config.plugins.UserSkin.woeid.value = config.plugins.AtileHD.woeid.value
            config.plugins.UserSkin.tempUnit.value = config.plugins.AtileHD.tempUnit.value
            for x in self["config"].list:
                x[1].save()
            configfile.save()
            #we change current folder to active skin folder
            chdir(SkinPath)
            #FONTS
            if path.exists(self.user_font_file):
                remove(self.user_font_file)
            elif path.islink(self.user_font_file):
                remove(self.user_font_file)
            if path.exists('allFonts/' + self.myUserSkin_font.value):
                symlink('allFonts/' + self.myUserSkin_font.value, self.user_font_file)
            #COLORS
            if path.exists(self.color_file):
                remove(self.color_file)
            elif path.islink(self.color_file):
                remove(self.color_file)
            if path.exists("allColors/" + self.myUserSkin_style.value):
                symlink("allColors/" + self.myUserSkin_style.value, self.color_file)
            #WINDOWS
            if path.exists(self.windowstyle_file):
                remove(self.windowstyle_file)
            elif path.islink(self.windowstyle_file):
                remove(self.windowstyle_file)
            if path.exists("allWindows/" + self.myUserSkin_windowstyle.value):
                symlink("allWindows/" + self.myUserSkin_windowstyle.value, self.windowstyle_file)
            #SELECTOR
            if path.exists(self.user_bar_link):
                remove(self.user_bar_link)
            elif path.islink(self.user_bar_link):
                remove(self.user_bar_link)
            if path.exists("allBars/" + self.myUserSkin_bar.value):
                symlink("allBars/" + self.myUserSkin_bar.value , self.user_bar_link)
                sourcePath = path.join(SkinPath , self.user_bar_link)
                destFolder = self.myUserSkin_bar.value.split(".", 1)[1]
                destPath = path.join(SkinPath , destFolder)
                printDEBUG("[UserSkin:keyOk]cp -fr %s %s" % (sourcePath,destPath))
                self.UserSkinToolSet.ClearMemory()

                printDEBUG("[UserSkin:keyOk]cp -fr %s/* %s/" % (sourcePath,destPath))
                system("cp -fr %s/* %s/" %(sourcePath,destPath)) #for safety, nicely manage overwrite ;)
            #SCREENS
            if self.myUserSkin_active.value:
                if not path.exists("mySkin") and path.exists("UserSkin_Selections"):
                    try:
                        mkdir("mySkin")
                    except:
                        printDEBUG("[UserSkin:keyOK]symlinking myskin exception")
                        self.UserSkinToolSet.ClearMemory()
                        destPath = path.join(SkinPath , "mySkin")
                        system("mkdir -p %s" % destPath )
            else:
                if path.exists("mySkin"):
                    if path.exists("UserSkin_Selections"):
                        if path.islink("mySkin"):
                            remove("mySkin")
                        else:
                            shutil.rmtree("mySkin")
                    else:
                        rename("mySkin", "UserSkin_Selections")
  
            self.update_user_skin()
            self.restartGUI()
        else:
            if self.changed_screens:
                self.update_user_skin()
                self.restartGUI()
            else:
                self.close()

    def UserSkinScreesnCB(self):
        self.changed_screens = True
        self["config"].setCurrentIndex(0)

    def restartGUI(self):
      
        def restartGUIcb(answer):
            if answer is True:
                self.session.open(TryQuitMainloop, 3)
            else:
                self.close()

        def restartNotOKcb(answer):
            if answer is True:
                self.session.open(TryQuitMainloop, 3)
            else:
                user_skin_file=resolveFilename(SCOPE_CONFIG, 'skin_user' + self.currentSkin + '.xml')
                if path.exists(user_skin_file):
                    remove(user_skin_file)
                self.close()

        myMessage = ''
        if self.LackOfFile != '':
            printDEBUG("missing components: %s" % self.LackOfFile)
            myMessage += _("Missing components found: %s\n\n") % self.LackOfFile
            myMessage += _("Skin will NOT work properly and GS expected!!!\n\n")
            myMessage += _("Are you sure you want to use it?")
            restartbox = self.session.openWithCallback(restartNotOKcb,MessageBox, myMessage, MessageBox.TYPE_YESNO, default = False)
        else:
            myMessage += _("Restart GUI now?")
            restartbox = self.session.openWithCallback(restartGUIcb,MessageBox, myMessage, MessageBox.TYPE_YESNO, default = False)
        restartbox.setTitle(_("Message"))

    def keyBlue(self):
        import xml.etree.cElementTree as ET
        from Screens.VirtualKeyBoard import VirtualKeyBoard
        
        def SaveScreen(ScreenFileName = None):
            if ScreenFileName is not None:
                if not path.exists(SkinPath + "allScreens/"):
                    mkdir(SkinPath + "allScreens/")
                if not ScreenFileName.endswith('.xml'):
                    ScreenFileName += '.xml'
                if not ScreenFileName.startswith('skin_'):
                    ScreenFileName = 'skin_' + ScreenFileName
                printDEBUG("Writing %s%s/%s" % (SkinPath, 'allScreens',ScreenFileName))
                
                for skinScreen in root.findall('screen'):
                    if 'name' in skinScreen.attrib:
                        if skinScreen.attrib['name'] == self.ScreenSelectedToExport:
                            SkinContent = ET.tostring(skinScreen)
                            break
                with open("%s%s/%s" % (SkinPath, 'allScreens', ScreenFileName), "w") as f:
                    f.write('<skin>\n')
                    f.write(SkinContent)
                    f.write('</skin>\n')

        def ScreenSelected(ret):
            if ret:
                self.ScreenSelectedToExport = ret[0]
                printDEBUG('Selected: %s' % self.ScreenSelectedToExport)
                self.session.openWithCallback(SaveScreen, VirtualKeyBoard, title=(_("Enter filename")), text = self.ScreenSelectedToExport + '_new')
        
        ScreensList= []
        root = ET.parse(SkinPath + 'skin.xml').getroot()
        for skinScreen in root.findall('screen'):
            if 'name' in skinScreen.attrib:
                printDEBUG('Found in skin.xml: %s' % skinScreen.attrib['name'])
                ScreensList.append((skinScreen.attrib['name'],skinScreen.attrib['name']))
        if len(ScreensList) > 0:
            ScreensList.sort()
            self.session.openWithCallback(ScreenSelected, ChoiceBox, title = _("Select skin to export:"), list = ScreensList)
                
    def update_user_skin(self):
        def getScreenNames(XMLfilename):
            myPath=path.realpath(XMLfilename)
            if not path.exists(myPath):
                remove(XMLfilename)
                return []
            filecontent = ''
            screenNames = []
            with open (XMLfilename, "r") as myFile:
                for line in myFile:
                    filecontent = filecontent + line
                    if line.find('<screen') >= 0:
                        screenNames.append(line.strip())
                        printDEBUG("getScreenNames found %s" % line.strip())
                myFile.close()
            return screenNames
            
        def readScreenContent(XMLfilename, screenSection):
            myPath=path.realpath(XMLfilename)
            if not path.exists(myPath):
                remove(XMLfilename)
                return ''
            screencontent = ''
            sectionmarker = False
            with open (XMLfilename, "r") as myFile:
                for line in myFile:
                    if line.find('<skin>') >= 0 or line.find('</skin>') >= 0:
                        continue
                    if line.find('name="%s"' %screenSection) >= 0 and sectionmarker == False:
                        sectionmarker = True
                        continue
                    elif line.find('</screen>') >= 0 and sectionmarker == True:
                        sectionmarker = False
                        break
                    if sectionmarker == True:
                        screencontent = screencontent + line
                myFile.close()
            return screencontent
        
        def readParametersContent(XMLfilename):
            myPath=path.realpath(XMLfilename)
            if not path.exists(myPath):
                remove(XMLfilename)
                return ''
            ParametersContent = ''
            sectionmarker = False
            with open (XMLfilename, "r") as myFile:
                for line in myFile:
                    if line.find('<skin>') >= 0 or line.find('</skin>') >= 0:
                        continue
                    if line.find('<parameters>') >= 0 and sectionmarker == False:
                        sectionmarker = True
                        continue
                    elif line.find('</parameters>') >= 0 and sectionmarker == True:
                        sectionmarker = False
                        break
                    if sectionmarker == True:
                        ParametersContent = ParametersContent + line
                myFile.close()
            return ParametersContent
        
        #print "[UserSkin} update_user_skin"
        if path.islink(SkinPath + 'mySkin'):
            remove(SkinPath + 'mySkin')
            mkdir(SkinPath + 'mySkin')       

        if self.isVTI == True: #jesli mamy VTI, to nie musimy robic pliku
            user_skin_file = SkinPath + 'mySkin/skin_user' + self.currentSkin + '.xml'
        else:
            user_skin_file = resolveFilename(SCOPE_CONFIG, 'skin_user' + self.currentSkin + '.xml')
        if path.exists(user_skin_file):
            remove(user_skin_file)
            
        if self.myUserSkin_active.value:
            printDEBUG("update_user_skin.self.myUserSkin_active.value")
            user_skin = ""
            user_parameters = ""
            if self.isVTI == False:
                if path.exists(SkinPath + 'skin_user_header.xml'):
                    user_skin = user_skin + self.readXMLfile(SkinPath + 'skin_user_header.xml' , 'fonts')
                if path.exists(SkinPath + 'skin_user_colors.xml'):
                    user_skin = user_skin + self.readXMLfile(SkinPath + 'skin_user_colors.xml' , 'ALLSECTIONS')
                if path.exists(SkinPath + 'skin_user_window.xml'):
                    user_skin = user_skin + self.readXMLfile(SkinPath + 'skin_user_window.xml' , 'ALLSECTIONS')
                    
            if path.exists(SkinPath + 'UserSkin_Selections'):
                if config.plugins.UserSkin.AdvancedMode.value == "mergeScreens":
                    # get list of screens in file
                    user_screens = []
                    for f in listdir(SkinPath + "UserSkin_Selections/"):
                        printDEBUG("reading file %smySkin/%s" % (SkinPath,f))
                        user_parameters += readParametersContent(SkinPath + "UserSkin_Selections/" + f)
                        for screen in getScreenNames(SkinPath + "UserSkin_Selections/" + f):
                            if screen != [] and screen.find('name="') > 0 :
                                screenName = re.findall(' name="([^\s]*)"', screen, re.S)[0]
                                user_screens.append([screenName, screen, f])
                    # get screens content
                    screen_name = ""
                    for screen in sorted(user_screens):
                        if screen[0] != screen_name:
                            if screen_name != "":
                                user_skin = user_skin + "</screen>\n"
                            user_skin = user_skin + screen[1] + "\n"
                            screen_name = screen[0]
                        user_skin = user_skin + readScreenContent(SkinPath + "UserSkin_Selections/" + screen[2], screen[0])
                    user_skin = user_skin + "</screen>\n"
                else:
                    for f in listdir(SkinPath + "UserSkin_Selections/"):
                        user_skin = user_skin + "<!--" + f + "-->\n" + self.readXMLfile(SkinPath + "UserSkin_Selections/" + f, 'screen')
            if user_skin != '':
                if user_parameters != '':
                     user_parameters = "  <parameters>\n" + user_parameters + "\n  </parameters>\n"
                user_skin = "<skin>\n" + user_parameters + user_skin + "</skin>\n"
                with open (user_skin_file, "w") as myFile:
                    printDEBUG("update_user_skin.self.myUserSkin_active.value write myFile")
                    myFile.write(user_skin)
                    myFile.flush()
                    myFile.close()
                    if path.exists('(/usr/lib/enigma2/python/Blackhole'):
                        system('ln -sf %s /etc/enigma2/user_skin.xml' % user_skin_file)
            #checking if all renderers are in the system
            self.checkComponent(user_skin, 'render' , resolveFilename(SCOPE_PLUGINS, '../Components/Renderer/') )
            self.checkComponent(user_skin, 'pixmap' , resolveFilename(SCOPE_SKIN, '') )
            self.checkFontColor(user_skin)

    def checkFontColor(self, myContent):
        def updateLackOfColor(name, mySeparator =', '):
            printDEBUG("Missing color definitions found:%s\n" % name)
            if self.LackOfFile == '':
                self.LackOfFile = name
            else:
                self.LackOfFile += mySeparator + name
        #preparing list of available colors
        DefinedColors=[]
        with open(SkinPath + 'skin.xml', 'r') as f:
            for line in f:
                if re.search('.*<color name="([\S]*)"',line) is not None:
                    DefinedColors.append(re.search('.*<color name="([\S]*)"',line).group(1))
            f.close()
        if len(DefinedColors) < 1:
            return
        #checking, if all colors defined
        r=re.findall(r'.*[Cc]olor="([^\W#]*)"',myContent)
        r=list(set(r)) #remove duplicates, no need to check for the same component several times
        print r
        
        if r:
            print "Found %d definitions" % len(r)
            for myColor in set(r):
                if myColor not in DefinedColors:
                    updateLackOfColor(myColor)

    def checkComponent(self, myContent, look4Component , myPath): #look4Component=render|
        def updateLackOfFile(name, mySeparator =', '):
            printDEBUG("Missing component found:%s\n" % name)
            if self.LackOfFile == '':
                self.LackOfFile = name
            else:
                self.LackOfFile += mySeparator + name
            
        r=re.findall( r' %s="([a-zA-Z0-9_/\.]+)" ' % look4Component , myContent )
        r=list(set(r)) #remove duplicates, no need to check for the same component several times

        printDEBUG("Found %s:\n" % (look4Component))
        #print r
        if r:
            for myComponent in set(r):
                #print" [UserSkin] checks if %s exists" % myComponent
                if look4Component == 'pixmap':
                    #printDEBUG("%s\n%s\n" % (myComponent,myPath + myComponent))
                    if myComponent.startswith('/'):
                        if not path.exists(myComponent):
                            updateLackOfFile(myComponent, '\n')
                    else:
                        if not path.exists(myPath + myComponent):
                            updateLackOfFile(myComponent)
                else:
                    if not path.exists(myPath + myComponent + ".pyo") and not path.exists(myPath + myComponent + ".py"):
                        updateLackOfFile(myComponent)
        return
    
    def readXMLfile(self, XMLfilename, XMLsection): #sections:ALLSECTIONS|fonts|
        myPath=path.realpath(XMLfilename)
        if not path.exists(myPath):
            remove(XMLfilename)
            return ''
        filecontent = ''
        if XMLsection == 'ALLSECTIONS':
            sectionmarker = True
        else:
            sectionmarker = False
        with open (XMLfilename, "r") as myFile:
            for line in myFile:
                if line.find('<skin>') >= 0 or line.find('</skin>') >= 0:
                    continue
                if line.find('<%s' %XMLsection) >= 0 and sectionmarker == False:
                    sectionmarker = True
                elif line.find('</%s>' %XMLsection) >= 0 and sectionmarker == True:
                    sectionmarker = False
                    filecontent = filecontent + line
                if sectionmarker == True:
                    filecontent = filecontent + line
            myFile.close()
        return filecontent

##### userBARs #####        
    def getCurrentBar(self):
        myfile = SkinPath + self.user_bar_link
        printDEBUG("[UserSkin:getCurrentBar] myfile='%s'" % myfile)
        if not path.exists(myfile):
            return (self.default_user_bar_link, self.default_user_bar_link)
        else:
            filename = path.realpath(myfile)
            filename = path.basename(filename)
            friendly_name = filename.replace("bar_", "").replace("_", " ")
            return (filename, friendly_name)

    def getPossibleBars(self):
        #printDEBUG("[UserSkin:getPossibleBars] >>>")
        mylist = []
        if listdir(SkinPath + "allBars/"):
            for f in sorted(listdir(SkinPath + "allBars/"), key=str.lower):
                fpath = path.join(SkinPath + "allBars/", f)
                printDEBUG("[UserSkin:getPossibleBars] f='%s'" % f)
                if path.isdir(fpath) and f.startswith('bar_') and f.find('.') > 1:
                    friendly_name = f.split(".", 1)[0]
                    friendly_name = friendly_name.replace("bar_", "").replace("_", " ")
                    mylist.append((f, _(friendly_name)))
        if len(mylist) == 0:
            mylist.insert(0, self.OnlyDefault)
        else:
            mylist.insert(0, self.defaults)
        return mylist

#################################################################################################################
from j00zekFileList import FileList
class TreeUserSkinScreens(Screen):
    skin = """
  <screen position="0,0" size="1280,720" title="UserSkin Setup" backgroundColor="transparent" flags="wfNoBorder">
    <eLabel position="0,0" size="1280,720" zPosition="-15" backgroundColor="#20000000" />
    <eLabel position=" 55,100" size="725,515" zPosition="-10" backgroundColor="#20606060" />
    <eLabel position="785,295" size="445,320" zPosition="-10" backgroundColor="#20606060" />
    <eLabel position="785,100" size="135,190" zPosition="-10" backgroundColor="#20606060" />
    <eLabel position="925,100" size="305,190" zPosition="-10" backgroundColor="#20606060" />
    <eLabel position=" 55,620" size="290,55" zPosition="-10" backgroundColor="#20b81c46" />
    <eLabel position="350,620" size="290,55" zPosition="-10" backgroundColor="#20009f3c" />
    <eLabel position="645,620" size="290,55" zPosition="-10" backgroundColor="#209ca81b" />
    <eLabel position="940,620" size="290,55" zPosition="-10" backgroundColor="#202673ec" />
    <eLabel position=" 55,675" size="290, 5" zPosition="-10" backgroundColor="#20b81c46" />
    <eLabel position="350,675" size="290, 5" zPosition="-10" backgroundColor="#20009f3c" />
    <eLabel position="645,675" size="290, 5" zPosition="-10" backgroundColor="#209ca81b" />
    <eLabel position="940,675" size="290, 5" zPosition="-10" backgroundColor="#202673ec" />
    <!--widget source="session.VideoPicture" render="Pig" position="935,115" zPosition="3" size="284,160" backgroundColor="#ff000000">
    </widget-->
    <widget source="Title" render="Label" position="70,47" size="950,43" font="Regular;35" foregroundColor="#00ffffff" backgroundColor="#004e4e4e" transparent="1" />
    <widget name="filelist" position="70,115" size="700,480" zPosition="1" font="Regular;20" transparent="1" scrollbarMode="showOnDemand"/>
    <widget name="PreviewPicture" position="808,342" size="400,225" alphatest="on" />
    <widget source="key_red" render="Label" position="70,635" size="260,25" zPosition="1" font="Regular;20" halign="left" foregroundColor="#00ffffff" backgroundColor="#20b81c46" transparent="1" />
    <widget source="key_green" render="Label" position="365,635" size="260,25" zPosition="1" font="Regular;20" halign="left" foregroundColor="#00ffffff" backgroundColor="#20009f3c" transparent="1" />
    <widget source="key_yellow" render="Label" position="650,635" size="260,25" zPosition="1" font="Regular;20" halign="left" foregroundColor="#00ffffff" transparent="1" />
  </screen>
"""

    EditScreen = False
    DeleteScreen = False
    
    def __init__(self, session):
        Screen.__init__(self, session)
        self.session = session
        
        myTitle=_("UserSkin %s - additional screens") %  UserSkinInfo
        self.setTitle(myTitle)
        try:
            self["title"] = StaticText(myTitle)
        except:
            pass
        
        self["key_red"] = StaticText(_("Exit"))
        self["key_green"] = StaticText("")
        self["key_yellow"] = StaticText("")
        
        self["PreviewPicture"] = Pixmap()
        
        self.LastFolderSelected = None
        
        self["shortcuts"] = ActionMap(["TreeUserSkinActions"],
        {
            "runMenuEntry": self.runMenuEntry,
            "cancel": self.keyCancel,
            "green": self.keyGreen,
            "yellow": self.keyYellow,
            "lineUp": self.lineUp,
            "lineDown": self.lineDown,
            "pageUp": self.pageUp,
            "pageDown": self.pageDown,
        }, -2)
        
        self.currentSkin = CurrentSkinName
        #self.screen_dir = "allScreens"
        self.allScreens_dir = SkinPath + "allScreens/"
        self.allPreviews_dir = SkinPath + "allPreviews/"
        self.UserSkin_Selections_dir = SkinPath + "UserSkin_Selections/"
        if path.exists("%sUserSkinpics/install.png" % SkinPath):
            printDEBUG("SkinConfig is loading %sUserSkinpics/install.png" % SkinPath)
            self.enabled_pic = LoadPixmap(cached=True, path="%sUserSkinpics/install.png" % SkinPath)
        else:
            self.enabled_pic = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/UserSkin/pic/install.png"))
        #check if we have preview files
        isPreview=0
        for xpreview in listdir(self.allPreviews_dir):
            if len(xpreview) > 4 and  xpreview[-4:] == ".png":
                isPreview += 1
            if isPreview >= 2:
                break
        if self.currentSkin == "infinityHD-nbox-tux-full" and isPreview < 2:
            printDEBUG("no preview files :(")
            if path.exists("%sUserSkinpics/install.png" % SkinPath):
                printDEBUG("SkinConfig is loading %sUserSkinpics/opkg.png" % SkinPath)
                self.disabled_pic = LoadPixmap(cached=True, path="%sUserSkinpics/opkg.png" % SkinPath)
            else:
                self.disabled_pic = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/UserSkin/pic/opkg.png"))
            self['key_blue'].setText(_('Install from OPKG'))
        else:
            if path.exists("%sUserSkinpics/install.png" % SkinPath):
                printDEBUG("SkinConfig is loading %sUserSkinpics/remove.png" % SkinPath)
                self.disabled_pic = LoadPixmap(cached=True, path="%sUserSkinpics/remove.png" % SkinPath)
            else:
                self.disabled_pic = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/UserSkin/pic/remove.png"))
        
        self.filelist = FileList(self.allScreens_dir)
        self["filelist"] = self.filelist

        self.onLayoutFinish.append(self.__onLayoutFinish)
        self.PreviewTimer = eTimer()
        self.PreviewTimer.callback.append(self.PreviewTimerCB)

    def endrun(self):
        return
     
    def NotUsedselectinChanged(self):
        print "> self.selectionChanged"
        sel = self["menu"].getCurrent()
        self.setPicture(sel[0])
        #print sel
        if sel[3] == self.enabled_pic:
            #self["key_green"].setText("")
            #self.EditScreen = False
            self["key_green"].setText(_("Edit"))
            self.EditScreen = True
            self["key_yellow"].setText("")
            self.DeleteScreen = False
        elif sel[3] == self.disabled_pic:
            self["key_green"].setText(_("Edit"))
            self.EditScreen = True
            self["key_yellow"].setText(_("Delete"))
            self.DeleteScreen = True

    def PreviewTimerCB(self):
        def UpdatePreviewPicture(PreviewFileName):
            self["PreviewPicture"].instance.setScale(1)
            self["PreviewPicture"].instance.setPixmap(LoadPixmap(path=PreviewFileName))
            self["PreviewPicture"].show()

        self.PreviewTimer.stop()
        
        if self["filelist"].getSelection()[1] == True: # isDir
            self["PreviewPicture"].hide()
            return

        pic =  self.filelist.getFilename()[:-4]
        if path.exists(self.allPreviews_dir + "preview_" + pic + '.png'):
            UpdatePreviewPicture(self.allPreviews_dir + "preview_" + pic + '.png')
        elif path.exists(self.allPreviews_dir + "preview_" + pic + '.jpg'):
            UpdatePreviewPicture(self.allPreviews_dir + "preview_" + pic + '.jpg')
        elif path.exists(self.allPreviews_dir + pic + '.png'):
            UpdatePreviewPicture(self.allPreviews_dir + pic + '.png')
        elif path.exists(self.allPreviews_dir + pic + '.jpg'):
            UpdatePreviewPicture(self.allPreviews_dir + pic + '.jpg')
        else:
            self["PreviewPicture"].hide()
    
    def runMenuEntry(self):
        selection = self["filelist"].getSelection()
        if selection is None:
            return
        elif selection[1] == True: # isDir
            if selection[0] is not None and self.filelist.getCurrentDirectory() is not None and \
                    len(selection[0]) > len(self.filelist.getCurrentDirectory()) or self.LastFolderSelected == None:
                self.LastFolderSelected = selection[0]
                self["filelist"].changeDir(selection[0], "FakeFolderName")
            else:
                print "Folder Down"
                self["filelist"].changeDir(selection[0], self.LastFolderSelected)
            return
        else: #file selected
            d = self.filelist.getCurrentDirectory()
            if d is None:
                d=""
            elif not d.endswith('/'):
                d +='/'
            f = self.filelist.getFilename()
            printDEBUG("self.selectFile>> " + d + f)
            if path.exists(self.UserSkin_Selections_dir + f):
                remove(self.UserSkin_Selections_dir + f)
            else:
                try:
                    symlink(d + f, self.UserSkin_Selections_dir + f)
                except:
                    system('ln -sf %s %s' %(d + f,self.UserSkin_Selections_dir + f))
            self.__refreshList()

    def keyGreen(self):
        if self.EditScreen == True:
            from editscreens import UserSkinEditScreens
            self.session.openWithCallback(self.__refreshList,UserSkinEditScreens, ScreenFile = self.filelist.getCurrentDirectory() + "/" + self.filelist.getFilename())
        else:
            print "Nothing to Edit :("
            
    def keyYellow(self):
        def keyYellowRet(result):
            if result is None or result is False:
                printDEBUG("Deletion cancelled.")
            else:
                remove(self.filelist.getCurrentDirectory() + "/" + self.filelist.getFilename())
                pic = self.filelist.getFilename().replace(".xml", ".png")
                if path.exists(SkinPath + "allPreviews/preview_" + pic):
                    remove(SkinPath + "allPreviews/preview_" + pic)
                self.__refreshList()

        if self.DeleteScreen == True:
            self.session.openWithCallback(keyYellowRet, MessageBox, _("Are you sure you want delete the screen?"), MessageBox.TYPE_YESNO, default = False)
        else:
            print "Nothing to Delete ;)"
            
    def keyCancel(self):
        self.close()
####################### FOR NEW TREE SELECTOR ###################################
    def __onLayoutFinish(self):
        self["filelist"].changeDir(self.allScreens_dir)
        self["filelist"].refresh()

    def __refreshList(self):
        self["filelist"].refresh()
       
    def pageUp(self):
        if self["filelist"].getSelectedIndex() == 0:
            self["filelist"].moveToIndex(len(self["filelist"].getFileList())-1)
        else:
            self["filelist"].pageUp()
        self.setInfo()

    def pageDown(self):
        if self["filelist"].getSelectedIndex() == (len(self["filelist"].getFileList())-1):
            self["filelist"].moveToIndex(0)
        else:
            self["filelist"].pageDown()
        self.setInfo()

    def lineUp(self):
        if self["filelist"].getSelectedIndex() == 0:
            self["filelist"].moveToIndex(len(self["filelist"].getFileList())-1)
        else:
            self["filelist"].up()
        self.setInfo()

    def lineDown(self):
        if self["filelist"].getSelectedIndex() == (len(self["filelist"].getFileList())-1):
            self["filelist"].moveToIndex(0)
        else:
            self["filelist"].down()
        self.setInfo()
        
    def setInfo(self):
        selection = self["filelist"].getSelection()
        if selection is None:
            return
        elif selection[1] == True: # isDir
            self["key_green"].setText("")
            self.EditScreen = False
            self["key_yellow"].setText("")
            self.DeleteScreen = False
            self["PreviewPicture"].hide()
        else:
            self["key_green"].setText(_("Edit"))
            self.EditScreen = True
            if path.exists(self.UserSkin_Selections_dir + self.filelist.getFilename()):
                self["key_yellow"].setText("")
                self.DeleteScreen = False
            else:
                self["key_yellow"].setText(_("Delete"))
                self.DeleteScreen = True

            self.PreviewTimer.start(100,False)
            
    def __getCurrentDir(self):
        d = self.filelist.getCurrentDirectory()
        if d is None:
            d=""
        elif not d.endswith('/'):
            d +='/'
        return d
