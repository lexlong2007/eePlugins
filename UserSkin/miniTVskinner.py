# -*- coding: utf-8 -*-
from inits import *

from Screens.ChannelSelection import SimpleChannelSelection, service_types_tv, service_types_radio
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Screens.VirtualKeyBoard import VirtualKeyBoard
from Screens.HelpMenu import HelpableScreen
from Screens.Standby import TryQuitMainloop
from enigma import getDesktop, eServiceCenter, eServiceReference, gFont, addFont, eListboxPythonMultiContent, RT_HALIGN_LEFT, RT_HALIGN_RIGHT, \
                    RT_HALIGN_CENTER, RT_VALIGN_CENTER, eLabel, eWidget, eSlider, fontRenderClass, ePoint, eSize, eDBoxLCD, ePicLoad, gPixmapPtr
from ServiceReference import ServiceReference
from Tools.LoadPixmap import LoadPixmap
from Tools.Directories import fileExists, resolveFilename, SCOPE_SKIN, SCOPE_FONTS
from Plugins.Plugin import PluginDescriptor
from Components.Label import Label
from Components.ActionMap import ActionMap, HelpableActionMap
from Components.AVSwitch import AVSwitch
from Components.config import config, ConfigSelection, getConfigListEntry, ConfigText, ConfigYesNo, ConfigSubsection, NoSave
from Components.ConfigList import ConfigListScreen
from Components.Sources.StaticText import StaticText
from Components.Pixmap import Pixmap, MovingPixmap
from Components.Slider import Slider
from Components.FileList import FileList
from Components.MenuList import MenuList
from Components.Pixmap import Pixmap
#from twisted.internet import defer
#from twisted.web.client import downloadPage, getPage, error
from PIL import Image
from skin import loadSkin
from translate import _

import glob, re, os, random, time

isVTI = None
#configure for VTI or openATV
try:
    if config.skin.primary_vfdskin.value == '': pass # exists in VTI only
    myLCDconfig = config.skin.primary_vfdskin
    isVTI = True
    skinPath=resolveFilename(SCOPE_SKIN, 'vfd_skin/skin_vfd_UserSkin.xml')
except:
    try:
        if config.skin.display_skin.value == '': pass # exists in openATV
    except:
        print "Unknown IMAGE"
        config.skin.display_skin = ConfigText(default = 'fake display_skin')
    myLCDconfig = config.skin.display_skin
    isVTI = False
    skinPath=resolveFilename(SCOPE_SKIN, 'display/Userskin/skin_display.xml')
    #required stuff config (VTI has all already)
    if not fileExists(resolveFilename(SCOPE_FONTS,"meteocons.ttf")):
        os.symlink(PluginPath + "LCDskin/meteocons.ttf", resolveFilename(SCOPE_FONTS,"meteocons.ttf"))
    if not fileExists(resolveFilename(SCOPE_SKIN, 'display/')):
        os.mkdir(resolveFilename(SCOPE_SKIN, 'display/'))
    if not fileExists(resolveFilename(SCOPE_SKIN, 'display/Userskin/')):
        os.mkdir(resolveFilename(SCOPE_SKIN, 'display/Userskin/'))


class miniTVskinner(Screen):
    LCDwidth = getDesktop(1).size().width()
    LCDheight = getDesktop(1).size().height()
    skin = """
        <screen name="MiniTVskinner" title="MiniTV (%dx%d) skin editor mod j00zek" position="center,center" size="1280,720">
            <widget name="LCDframe" position="0,0" size="%d,%d" zPosition="3" transparent="0" alphatest="blend" />
          <!-- MENU on left -->
            <eLabel position="45,480" size="5,25" zPosition="-10" backgroundColor="#20b81c46" />
            <widget name="red" position="55,480" size="485,25" zPosition="10" font="Regular;21" noWrap="1" halign="left" valign="center" transparent="1"/>
            <eLabel position="45,510" size="5,25" zPosition="-10" backgroundColor="#20009f3c" />
            <widget name="green" position="55,510" size="485,25" zPosition="10" font="Regular;21" noWrap="1" halign="left" valign="center"  transparent="1"/>
            <eLabel position="45,540" size="5,25" zPosition="-10" backgroundColor="#209ca81b" />
            <widget name="yellow" position="55,540" size="485,25" zPosition="10" font="Regular;21" noWrap="1" halign="left" valign="center"  transparent="1"/>
            <eLabel position="45,570" size="5,25" zPosition="-10" backgroundColor="#202673ec" />
            <widget name="blue" position="55,570" size="485,25" zPosition="10" font="Regular;21" noWrap="1" halign="left" valign="center"  transparent="1"/>
            <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/UserSkin/pic/left_right.png" position="13,600" size="25,25" alphatest="on" />
            <widget name="leftright" position="55,600" size="700,25" zPosition="10" font="Regular;21" noWrap="1" halign="left" valign="center" />
          <!-- LISTS on right -->
            <widget name="InfoLine" position="810,5" size="470,30" zPosition="5" transparent="0" halign="left" valign="top" font="Regular;28" foregroundColor="yellow" />
            <widget name="Widgetslist" position="810,40" size="470,550" itemHeight="30" scrollbarMode="showOnDemand" />
            <widget name="backuplist" position="810,40" size="470,550" itemHeight="30" scrollbarMode="showOnDemand" />
            <widget name="menulist" position="810,40" size="470,550" itemHeight="30" scrollbarMode="showOnDemand" />
          <!-- active WIDGET description -->
            <widget name="WidgetInfo" position="810,610" size="450,110" zPosition="10" font="Regular;21" noWrap="0" halign="left" valign="top" />
          <!-- WIDGETS -->
    
            <widget name="REC" position="20,15" size="55,42" zPosition="3" transparent="0" alphatest="blend"  />
            <widget name="CRYPT" position="75,15" size="55,42" zPosition="2" transparent="0" alphatest="blend" />
            <widget name="TELETEXT" position="130,15" size="55,42" zPosition="2" transparent="0" alphatest="blend" />
            <widget name="16x9" position="185,15" size="55,42" zPosition="2" transparent="0" alphatest="blend" />
            <widget name="DOLBY" position="240,15" size="55,42" zPosition="2" transparent="0" alphatest="blend" />
            <widget name="DATE" position="320,10" size="150,35" foregroundColor="white" backgroundColor="#000000" zPosition="2" transparent="0" halign="right" font="Regular;32" />
            <widget name="TIME" position="320,45" size="150,35" foregroundColor="white" backgroundColor="#000000" zPosition="2" transparent="0" halign="right" font="Regular;32" />
            <widget name="PICON" position="130,85" zPosition="4" size="220,132" transparent="1" alphatest="blend" />
            <widget name="EventName" position="10,220" foregroundColor="white" backgroundColor="#000000" size="460,40" zPosition="2" transparent="0" halign="left" valign="top" font="Regular;40" />
            <widget name="EventTime" position="10,270" size="460,30" zPosition="5" transparent="0" backgroundColor="white" />
            <widget name="WEATHER" position="50,350" size="50,50" zPosition="2" transparent="0" halign="left" valign="top" font="Meteo;50" />
            <widget name="WEATHERTEXT" position="50,400" size="50,34" foregroundColor="white" backgroundColor="#000000" zPosition="3" transparent="0" halign="left" valign="top" font="Regular;32" />
            <widget name="ANALOG_CLOCK" position="120,350" size="125,125" zPosition="3" transparent="0" alphatest="blend" />
            <widget name="ChannelName" position="350,350" size="100,42" foregroundColor="white" backgroundColor="#000000" zPosition="3" transparent="0" halign="left" valign="top" font="Regular;40" />
            <widget name="ChannelNumber" position="300,350" size="50,42" foregroundColor="white" backgroundColor="#000000" zPosition="3" transparent="0" halign="left" valign="top" font="Regular;40" />
            <widget name="TEMPINFO" position="300,400" size="150,35" foregroundColor="white" backgroundColor="#000000" zPosition="3" transparent="0" halign="left" valign="top" font="Regular;32" />
            <widget name="FANINFO" position="300,450" size="150,35" foregroundColor="white" backgroundColor="#000000" zPosition="3" transparent="0" halign="left" valign="top" font="Regular;32" />
            <widget name="REMAINING" position="450,450" size="100,35" foregroundColor="white" backgroundColor="#000000" zPosition="3" transparent="0" halign="left" valign="top" font="Regular;32" />
        </screen>""" % (LCDwidth, LCDheight, LCDwidth+2, LCDheight+2)
        
    def __init__(self, session):
        self.session = session
        Screen.__init__(self, session)

        self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions"], {
            "cancel": self.keyCancel,
            "ok": self.onoff,
            "left": self.left,
            "right": self.right,
            "up": self.up,
            "down": self.down,
            "red": self.keyCancel,
            "nextBouquet" : self.listUP,
            "prevBouquet" : self.listDown,
            "red" : self.switchlist,
            "blue" : self.piconPath,
            "green": self.selectType,
            "yellow": self.switchSize,
            "nextService": self.size_plus,
            "prevService": self.size_minus,
            "0" : self.switchlist,
        }, -1)
        
        addFont(resolveFilename(SCOPE_FONTS,"meteocons.ttf"), "Meteo", 100, False)

        self.keyLocked = True
        self.list = [("REC","1"), ("CRYPT","1"), ("TELETEXT","1"), ("16x9","1"), ("DOLBY","1"), ("DATE","1"), ("TIME","1"), ("PICON","1"), ("EventName","1"), ("EventTime","1"), ("WEATHER","0"), ("WEATHERTEXT","0"), ("ANALOG_CLOCK","0"), ("ChannelName","0"), ("ChannelNumber","0"), ("TEMPINFO","0"), ("FANINFO","0"), ("REMAINING", "0")]
        self.backuplist = []
        self.menulist = ["InfoBarSummary", "InfoBarMoviePlayerSummary", "StandbySummary", "EMCMoviePlayerSummary"]
        self.chooseMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
        self.chooseMenuList.l.setFont(0, gFont('Regular', 23))
        self.chooseMenuList.l.setItemHeight(50)
        self["Widgetslist"] = self.chooseMenuList
        self.chooseMenuList.setList(map(self.paintWidgetsList, self.list))

        self.chooseMenuList2 = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
        self.chooseMenuList2.l.setFont(0, gFont('Regular', 23))
        self.chooseMenuList2.l.setItemHeight(50)
        self["backuplist"] = self.chooseMenuList2
        self.chooseMenuList2.setList(map(self.paintBackupList, self.backuplist))

        self.chooseMenuList3 = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
        self.chooseMenuList3.l.setFont(0, gFont('Regular', 23))
        self.chooseMenuList3.l.setItemHeight(50)
        self["menulist"] = self.chooseMenuList3
        self["menulist"].hide()
        self.chooseMenuList3.setList(map(self.paintMenuList, self.menulist))

        self['InfoLine'] = Label(_("Select Widget:"))
        self['red'] = Label(_("Saved Skins"))
        self['green'] = Label(_("Save LCD Skin"))
        self['yellow'] = Label("")
        self['blue'] = Label(_("Picon Path: Loading.."))
        self['leftright'] = Label(_("Resize width/height"))
        self['WidgetInfo'] = Label(_("Widget Info:"))
        self['DATE'] = Label("22.12.2212")
        self['TIME'] = Label("22:45")
        self['EventName'] = Label("- Skin your MiniTV -")
        self['EventTime'] = Slider(0, 100)
        self['EventTime'].setValue(100)
        self['WEATHER'] = Label("B")
        self['WEATHERTEXT'] = Label("7 C")
        self['ChannelName'] = Label("TVP")
        self['ChannelNumber'] = Label("5")
        self['TEMPINFO'] = Label("TEMP: 38 C")
        self['FANINFO'] = Label("FAN: 670 rpm")
        self['REMAINING'] = Label("+ 124")
        #load when LaoutFinished
        self['LCDframe'] = Pixmap() 
        self['REC'] = Pixmap()
        self['CRYPT'] = Pixmap()
        self['PICON'] = Pixmap()
        self['TELETEXT'] = Pixmap()
        self['16x9'] = Pixmap()
        self['DOLBY'] = Pixmap()
        self['ANALOG_CLOCK'] = Pixmap()

        self.picon_path = resolveFilename(SCOPE_SKIN, "picon") + '/'
        self.xachse = 0
        self.yachse = 0
        self.wsize = "height"
        self.xsize = 0
        self.ysize = 0
        self.listmode = "Widgetslist"
        
        print "VFD Skin:", myLCDconfig.value

        #self.onExecBegin.append(self.getit)
        self.onLayoutFinish.append(self.start)

        self['yellow'].setText(_("Switch width/height (move with < >): %s") % self.wsize)
        self['blue'].setText(_("Picon Path: %s") % self.picon_path)

    def start(self):
        self["LCDframe"].instance.setPixmapFromFile(getPixmapPath('white_frame.png'))
        self["REC"].instance.setPixmapFromFile(getPixmapPath('icon_rec.png'))
        self["CRYPT"].instance.setPixmapFromFile(getPixmapPath('icon_crypt.png'))
        #self["PICON"].instance.setPixmapFromFile(getPixmapPath(''))
        self["TELETEXT"].instance.setPixmapFromFile(getPixmapPath('icon_txt.png'))
        self["16x9"].instance.setPixmapFromFile(getPixmapPath('16x9_blue.png'))
        self["DOLBY"].instance.setPixmapFromFile(getPixmapPath('icon_dolby.png'))
        self["ANALOG_CLOCK"].instance.setPixmapFromFile(getPixmapPath('styleclock.png'))

        self.readPiconFromPath(self.picon_path)
        self.readSize()
        self.showWidgetInfo()
        self.loadWidgets()
        self.readBackups()

    def loadWidgets(self):
        for widget,status in self.list:
            if int(status) == 1:
                self[widget].show()
            else:
                self[widget].hide()

    def switchlist(self):
        if self.listmode == "Widgetslist":
            self["Widgetslist"].hide()
            self["backuplist"].show()
            self.listmode = "backuplist"
            self['InfoLine'].setText("Gespeicherte Skin Elemente:")
            self.loadBackup()
        elif self.listmode == "backuplist":
            self["backuplist"].hide()
            self["Widgetslist"].show()
            self.listmode = "Widgetslist"
            self['InfoLine'].setText("Widget Auswahl:")

    def selectType(self):
        self.listmode = "menulist"
        self["Widgetslist"].hide()
        self["backuplist"].hide()
        self['InfoLine'].setText("Skin speichern als:")
        self["menulist"].show()

    def listUP(self):
        if self.listmode == "Widgetslist": 
            self["Widgetslist"].up()
            self.showWidgetInfo()
        elif self.listmode == "backuplist":
            self["backuplist"].up()
            self.loadBackup()
        elif self.listmode == "menulist":
            self["menulist"].up()
        
    def listDown(self):
        if self.listmode == "Widgetslist": 
            self["Widgetslist"].down()
            self.showWidgetInfo()
        elif self.listmode == "backuplist":
            self["backuplist"].down()
            self.loadBackup()
        elif self.listmode == "menulist":
            self["menulist"].down()

    def paintWidgetsList(self, entry):
        res = [entry]
        if int(entry[1]) == 1:
            farbe = 0xFFFFFF
            status = "ON"
        else:
            farbe = 0xFF0000
            status = "OFF"
        #return [entry, (eListboxPythonMultiContent.TYPE_TEXT, 0, 0, 500, 30, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, farbe, entry[0])]
        #res.append(MultiContentEntryText(pos=(0, 0), size=(500, 30), font=0, text=entry[0], color=farbe, flags=RT_HALIGN_CENTER|RT_VALIGN_CENTER))
        res.append((eListboxPythonMultiContent.TYPE_TEXT, 0, 0, 420, 30, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0], farbe))
        res.append((eListboxPythonMultiContent.TYPE_TEXT, 420, 0, 50, 30, 0, RT_HALIGN_RIGHT | RT_VALIGN_CENTER, status, farbe))
        return res

    def paintBackupList(self, entry):
        res = [entry]
        res.append((eListboxPythonMultiContent.TYPE_TEXT, 0, 0, 330, 30, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[0]))
        res.append((eListboxPythonMultiContent.TYPE_TEXT, 330, 0, 140, 30, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry[1]))
        return res

    def paintMenuList(self, entry):
        res = [entry]
        res.append((eListboxPythonMultiContent.TYPE_TEXT, 0, 0, 470, 30, 0, RT_HALIGN_LEFT | RT_VALIGN_CENTER, entry))
        return res

    def createIcon(self, filename):
        width, height = self.getPiconSize(filename)
        self['PICON'].instance.resize(eSize(int(width), int(height)))
        self.picload = ePicLoad()
        self["PICON"].instance.setPixmap(gPixmapPtr())
        scale = AVSwitch().getFramebufferScale()
        size = self["PICON"].instance.size()
        self.picload.setPara((size.width(), size.height(), scale[0], scale[1], False, 1, "#FF000000"))
        if self.picload.startDecode(filename, 0, 0, False) == 0:
            ptr = self.picload.getData()
            if ptr != None:
                self["PICON"].instance.setPixmap(ptr)
                self["PICON"].show()

    def showWidgetInfo(self):
        self.readSize()
        myInfo  = _('Widget position: %sx%s') % ( self[self.widgetLabel].instance.position().x(), self[self.widgetLabel].instance.position().y() )
        myInfo += ', '
        myInfo += _('size: %sx%s') % ( self[self.widgetLabel].instance.size().width(), self[self.widgetLabel].instance.size().height() )
        myInfo += '\n'
        myInfo += _('Font: XXX')
        myInfo += ', '
        myInfo += _('size: YYY')
        myInfo += '\n'
        myInfo += _('Colors text: XXX')
        myInfo += ', '
        myInfo += _('background: YYY')
        myInfo += '\n'
        myInfo += _('Path: /aqq\n')
        self['WidgetInfo'].setText(myInfo)

    def switchSize(self):
        if self.wsize == "width":
            self.wsize = "height"
        else:
            self.wsize = "width"
        self['yellow'].setText("Switch width/height (move with < >): %s" % self.wsize)

    def size_minus(self):
        if self["Widgetslist"].getCurrent()[0][1] == "0" or self.listmode == "backuplist" or self.listmode == "menulist":
            return
        self.readSize()
        if self.wsize == "width":
            self.xsize -= 5
            self[self.widgetLabel].instance.resize(eSize(self.xsize,self.ysize))
        else:
            self.ysize -= 5
            self[self.widgetLabel].instance.resize(eSize(self.xsize,self.ysize))

        if str(type(self[self.widgetLabel])) == "<class 'Components.Pixmap.Pixmap'>":
            self[self.widgetLabel].instance.setScale(3)
        elif str(type(self[self.widgetLabel])) == "<class 'Components.Slider.Slider'>":
            pass
        else:
            if self.wsize == "height":
                if self.widgetLabel == "WEATHER":
                    self[self.widgetLabel].instance.setFont(gFont('Meteo', self.ysize))
                else:
                    self[self.widgetLabel].instance.setFont(gFont('VFD', self.ysize-2))
        self.showWidgetInfo()

    def size_plus(self):
        if self["Widgetslist"].getCurrent()[0][1] == "0" or self.listmode == "backuplist" or self.listmode == "menulist":
            return
        self.readSize()
        if self.wsize == "width":
            self.xsize += 5
            self[self.widgetLabel].instance.resize(eSize(self.xsize,self.ysize))
        else:
            self.ysize += 5
            self[self.widgetLabel].instance.resize(eSize(self.xsize,self.ysize))

        if str(type(self[self.widgetLabel])) == "<class 'Components.Pixmap.Pixmap'>":
            self[self.widgetLabel].instance.setScale(3)
        elif str(type(self[self.widgetLabel])) == "<class 'Components.Slider.Slider'>":
            pass
        else:
            if self.wsize == "height":
                if self.widgetLabel == "WEATHER":
                    self[self.widgetLabel].instance.setFont(gFont('Meteo', self.ysize))
                else:
                    self[self.widgetLabel].instance.setFont(gFont('VFD', self.ysize-2))
        self.showWidgetInfo()

    def readSize(self):
        self.widgetLabel = self["Widgetslist"].getCurrent()[0][0]
        self.xsize = self[self.widgetLabel].instance.size().width()
        self.ysize = self[self.widgetLabel].instance.size().height()
        print self.widgetLabel, self.xsize, self.ysize

    def piconPath(self):
        if self.picon_path == "/usr/share/enigma2/picon/":
            self.picon_path = "/usr/share/enigma2/piconlcd/"
            self['blue'].setText("Picon Path: %s" % self.picon_path)
        else:
            self.picon_path = "/usr/share/enigma2/picon/"
            self['blue'].setText("Picon Path: %s" % self.picon_path)
        self.readPiconFromPath(self.picon_path)

    def readPiconFromPath(self, path):
        self.filelist = glob.glob(path+"*.png")
        if len(self.filelist) > 0:
            self.createIcon(random.choice(self.filelist))

    def writeBackup(self, wtype):
        zeit = time.strftime("%d.%m.%Y - %H:%M:%S")
        b = "<backup>\n<type>%s</type>\n<date>%s</date>\n" % (wtype, zeit)
        for widgetName, widgetActive in self.list:
            print "name:", widgetName
            print type(self[widgetName])
            if str(type(self[widgetName])) == "<class 'Components.Pixmap.Pixmap'>":
                b += "<widgetname>%s</widgetname><active>%s</active><position>%s,%s</position><size>%s,%s</size><font>%s</font>\n" % (widgetName, widgetActive, self[widgetName].instance.position().x(), self[widgetName].instance.position().y(), self[widgetName].instance.size().width(), self[widgetName].instance.size().height(), None) 
            elif str(type(self[widgetName])) == "<class 'Components.Slider.Slider'>":
                b += "<widgetname>%s</widgetname><active>%s</active><position>%s,%s</position><size>%s,%s</size><font>%s</font>\n" % (widgetName, widgetActive, self[widgetName].instance.position().x(), self[widgetName].instance.position().y(), self[widgetName].instance.size().width(), self[widgetName].instance.size().height(), None) 
            else:
                b += "<widgetname>%s</widgetname><active>%s</active><position>%s,%s</position><size>%s,%s</size><font>%s</font>\n" % (widgetName, widgetActive, self[widgetName].instance.position().x(), self[widgetName].instance.position().y(), self[widgetName].instance.size().width(), self[widgetName].instance.size().height(), self[widgetName].instance.size().height()-2) 
        b += "</backup>\n"
        print b
        f = open(PluginPath + 'LCDskin/backups.xml','a')
        f.write(b)
        f.close()
        self.readBackups()

    def readBackups(self):
        file = open(PluginPath + 'LCDskin/backups.xml', 'r')
        backup_raw = file.read()
        file.close()

        self.backuplist = []
        backups = re.findall('<backup>(.*?)</backup>', backup_raw, re.S)
        print "FOUND %s Backups" % str(len(backups))
        for backup in backups:
            which = re.findall('<type>(.*?)</type>', backup)[0]
            zeit = re.findall('<date>(.*?)</date>', backup)[0]
            #print which, zeit
            raws = re.findall('<widgetname>(.*?)</widgetname><active>(.*?)</active><position>(.*?),(.*?)</position><size>(.*?),(.*?)</size><font>(.*?)</font>', backup, re.S)
            if raws:
                raw_list = []
                for raw in raws: 
                    (widgetName, active, pos_x, pos_y, size_x, size_y, font) = raw
                    #print widgetName, active, pos_x, pos_y, size_x, size_y, font
                    raw_list.append((widgetName, active, pos_x, pos_y, size_x, size_y, font))
                self.backuplist.append((which, zeit, raw_list))
        self.backuplist.reverse()
        self.chooseMenuList2.setList(map(self.paintBackupList, self.backuplist))

    def loadBackup(self):
        if self.listmode == "backuplist":
            selected_raw_list = self["backuplist"].getCurrent()[0][2]
            self.list = []
            for widgetName, active, pos_x, pos_y, size_x, size_y, font in selected_raw_list:
                print widgetName, active, pos_x, pos_y, size_x, size_y, font
                self.list.append((widgetName, active))
                if active == "1":
                    self[widgetName].move(ePoint(int(pos_x), int(pos_y)))
                    self[widgetName].instance.resize(eSize(int(size_x), int(size_y)))
                    self[widgetName].show()
                    if font != "None":
                        if widgetName == "WEATHER":
                            self[widgetName].instance.setFont(gFont('Meteo', int(font)))
                        else:
                            self[widgetName].instance.setFont(gFont('VFD', int(font)))
                    if str(type(self[widgetName])) == "<class 'Components.Pixmap.Pixmap'>":
                        self[widgetName].instance.setScale(3)
                else:
                    self[widgetName].hide()
            self.chooseMenuList.setList(map(self.paintWidgetsList, self.list))

    def writeSkinFile(self, which):
        screenPart = ""
        screenPart += '\n<screen name="%s" position="0,0" size="480,320" id="1">\n' % which
        for widget,status in self.list:
            if int(status) == 1:
                skinPart = self.getWidgetSkinPart(widget, which)
                if skinPart is not None:
                    print "Write %s Widget to SkinFile" % (widget)
                    print skinPart
                    screenPart += skinPart

        screenPart += '</screen>\n'
        #skinfile += '</skin>'

        if not fileExists('/usr/share/enigma2/vfd_skin/skin_vfd_miniTvSkinner.xml'):
            file = open('/usr/lib/enigma2/python/Plugins/Extensions/MiniTVskinner/skin_vfd_default.xml', 'r')
        else:
            file = open('/usr/share/enigma2/vfd_skin/skin_vfd_miniTvSkinner.xml', 'r')
        skinBase = file.read()
        file.close()
        if re.search(which, skinBase, re.S|re.I):
            pattern = re.compile('<screen name="'+which+'" position="0,0" size="480,320" id="1">(.*?)</screen>', re.S|re.I)
            skinFile = re.sub(pattern, screenPart, skinBase)
        else:
            #pattern = re.compile('<screen name="'+which+'" position="0,0" size="480,320" id="1">(.*?)</screen>', re.S|re.I)
            skinFile = re.sub('</skin>', screenPart+'\n</skin>', skinBase)
        
        print skinFile
        f = open('/usr/share/enigma2/vfd_skin/skin_vfd_miniTvSkinner.xml', 'w')
        f.write(skinFile)
        f.close()
        
        if myLCDconfig.value != "vfd_skin/skin_vfd_miniTvSkinner.xml":
            print "set new VFD Skin..", myLCDconfig.value
            myLCDconfig.value = "vfd_skin/skin_vfd_miniTvSkinner.xml"
            myLCDconfig.save()
        loadSkin("/usr/share/enigma2/vfd_skin/skin_vfd_miniTvSkinner.xml")
        restartbox = self.session.openWithCallback(self.restartGUI,MessageBox,_("GUI needs a restart to apply a new skin\nDo you want to Restart the GUI now?"), MessageBox.TYPE_YESNO)
        restartbox.setTitle(_("Restart GUI now?"))

        #eDBoxLCD.getInstance().update()

    def restartGUI(self, answer):
        if answer is True:
            self.session.open(TryQuitMainloop, 3)

    def getWidgetSkinPart(self, widgetName, which):
        skinPart = ""
        if widgetName == "REC":
            skinPart += '<widget source="session.RecordState" render="Pixmap" pixmap="vfd_icons/REC_red.png" position="%s,%s" size="%s,%s" alphatest="blend">\n' % (self[widgetName].instance.position().x(), self[widgetName].instance.position().y(), self[widgetName].instance.size().width(), self[widgetName].instance.size().height())
            skinPart += '<convert type="ConditionalShowHide" />\n'
            skinPart += '</widget>\n'
            return skinPart
        elif widgetName == "CRYPT":
            skinPart += '<widget source="session.CurrentService" render="Pixmap" pixmap="vfd_icons/CRYPT_grey.png" position="%s,%s" size="%s,%s" alphatest="blend">\n' % (self[widgetName].instance.position().x(), self[widgetName].instance.position().y(), self[widgetName].instance.size().width(), self[widgetName].instance.size().height())
            skinPart += '<convert type="ServiceInfo">IsCrypted</convert>\n'
            skinPart += '<convert type="ConditionalShowHide" />\n'
            skinPart += '</widget>\n'
            return skinPart
        elif widgetName == "TELETEXT":
            skinPart += '<widget source="session.CurrentService" render="Pixmap" pixmap="vfd_icons/TELETEXT_yellow.png" position="%s,%s" size="%s,%s" alphatest="blend">\n' % (self[widgetName].instance.position().x(), self[widgetName].instance.position().y(), self[widgetName].instance.size().width(), self[widgetName].instance.size().height())
            skinPart += '<convert type="ServiceInfo">HasTelext</convert>\n'
            skinPart += '<convert type="ConditionalShowHide" />\n'
            skinPart += '</widget>\n'
            return skinPart
        elif widgetName == "16x9":
            skinPart += '<widget source="session.CurrentService" render="Pixmap" pixmap="vfd_icons/16x9_blue.png" position="%s,%s" size="%s,%s" alphatest="blend">\n' % (self[widgetName].instance.position().x(), self[widgetName].instance.position().y(), self[widgetName].instance.size().width(), self[widgetName].instance.size().height())
            skinPart += '<convert type="ServiceInfo">IsWidescreen</convert>\n'
            skinPart += '<convert type="ConditionalShowHide" />\n'
            skinPart += '</widget>\n'
            return skinPart
        elif widgetName == "DOLBY":
            skinPart += '<widget source="session.CurrentService" render="Pixmap" pixmap="vfd_icons/DOLBY_green.png" position="%s,%s" size="%s,%s" alphatest="blend">\n' % (self[widgetName].instance.position().x(), self[widgetName].instance.position().y(), self[widgetName].instance.size().width(), self[widgetName].instance.size().height())
            skinPart += '<convert type="ServiceInfo">IsMultichannel</convert>\n'
            skinPart += '<convert type="ConditionalShowHide" />\n'
            skinPart += '</widget>\n'
            return skinPart
        elif widgetName == "DATE":
            skinPart += '<widget source="global.CurrentTime" render="Label" position="%s,%s" size="%s,%s" font="VFD;%s" halign="right">\n' % (self[widgetName].instance.position().x(), self[widgetName].instance.position().y(), self[widgetName].instance.size().width(), self[widgetName].instance.size().height(), self[widgetName].instance.size().height())
            skinPart += '<convert type="ClockToText">Format:%d.%m.%Y</convert>\n'
            skinPart += '</widget>\n'
            return skinPart
        elif widgetName == "TIME":
            skinPart += '<widget source="global.CurrentTime" render="Label" position="%s,%s" size="%s,%s" font="VFD;%s" halign="right">\n' % (self[widgetName].instance.position().x(), self[widgetName].instance.position().y(), self[widgetName].instance.size().width(), self[widgetName].instance.size().height(), self[widgetName].instance.size().height())
            skinPart += '<convert type="ClockToText">Format:%H:%M</convert>\n'
            skinPart += '</widget>\n'
            return skinPart
        elif widgetName == "PICON":
            if self.picon_path == "/usr/share/enigma2/piconlcd/":
                skinPart += '<widget source="session.CurrentService" render="Picon" position="%s,%s" size="%s,%s" path="piconlcd" zPosition="4" transparent="1" alphatest="blend">\n' % (self[widgetName].instance.position().x(), self[widgetName].instance.position().y(), self[widgetName].instance.size().width(), self[widgetName].instance.size().height())
            else:
                skinPart += '<widget source="session.CurrentService" render="Picon" position="%s,%s" size="%s,%s" zPosition="4" transparent="1" alphatest="blend">\n' % (self[widgetName].instance.position().x(), self[widgetName].instance.position().y(), self[widgetName].instance.size().width(), self[widgetName].instance.size().height())
            skinPart += '<convert type="ServiceName">Reference</convert>\n'
            skinPart += '</widget>\n'
            return skinPart
        elif widgetName == "EventName":
            skinPart += '<widget source="session.Event_Now" render="RollerCharLCDLong" noWrap="1" position="%s,%s" size="%s,%s" font="VFD;%s" halign="left" valign="top">\n' % (self[widgetName].instance.position().x(), self[widgetName].instance.position().y(), self[widgetName].instance.size().width(), self[widgetName].instance.size().height(), self[widgetName].instance.size().height()-2)
            skinPart += '<convert type="EventName">Name</convert>\n'
            skinPart += '</widget>\n'
            return skinPart
        elif widgetName == "EventTime":
            skinPart += '<widget source="session.Event_Now" render="Progress" position="%s,%s" size="%s,%s" borderWidth="2">\n' % (self[widgetName].instance.position().x(), self[widgetName].instance.position().y(), self[widgetName].instance.size().width(), self[widgetName].instance.size().height())
            skinPart += '<convert type="EventTime">Progress</convert>\n'
            skinPart += '</widget>\n'
            return skinPart
        elif widgetName == "WEATHERTEXT":
            skinPart += '<widget source="session.CurrentService" render="Label" position="%s,%s" size="%s,%s" font="VFD;%s" zPosition="10" halign="left" valign="center" transparent="1" noWrap="1">\n' % (self[widgetName].instance.position().x(), self[widgetName].instance.position().y(), self[widgetName].instance.size().width(), self[widgetName].instance.size().height(), self[widgetName].instance.size().height()-2)
            skinPart += '<convert type="VWeather">currentWeatherTemp</convert>\n'
            skinPart += '</widget>\n'
            skinPart += '<widget source="session.CurrentService" render="Label" position="%s,%s" size="%s,%s" font="VFD;%s" zPosition="11" halign="left" valign="center" transparent="1" noWrap="1">\n' % (self[widgetName].instance.position().x()+self[widgetName].instance.size().width(), self[widgetName].instance.position().y(), self[widgetName].instance.size().width(), self[widgetName].instance.size().height(), self[widgetName].instance.size().height()-2)
            skinPart += '<convert type="VWeather">CF</convert>\n'
            skinPart += '</widget>\n'
            return skinPart
        elif widgetName == "WEATHER":
            skinPart += '<widget source="session.CurrentService" render="Label" position="%s,%s" size="%s,%s" font="Meteo;%s" zPosition="10" halign="center" valign="center" transparent="1" noWrap="1">\n' % (self[widgetName].instance.position().x(), self[widgetName].instance.position().y(), self[widgetName].instance.size().width(), self[widgetName].instance.size().height(), self[widgetName].instance.size().height())
            skinPart += '<convert type="VWeather">currentWeatherCode</convert>\n'
            skinPart += '</widget>\n'
            return skinPart
        elif widgetName == "ANALOG_CLOCK": # position="1100,555" size="125,125"
            skinPart += '<ePixmap position="%s,%s" size="125,125" zPosition="1" pixmap="AtileHD/menu/styleclock.png" alphatest="blend" />\n' % (self[widgetName].instance.position().x(), self[widgetName].instance.position().y())
            skinPart += '<widget source="global.CurrentTime" render="VWatches" position="%s,%s" size="61,61" zPosition="4" alphatest="on">\n' % (self[widgetName].instance.position().x()+31, self[widgetName].instance.position().y()+33)
            skinPart += '<convert type="VExtraNumText">secHand</convert>\n'
            skinPart += '</widget>\n'
            skinPart += '<widget source="global.CurrentTime" render="VWatches" position="%s,%s" size="57,57" zPosition="3" alphatest="on">\n' % (self[widgetName].instance.position().x()+33, self[widgetName].instance.position().y()+35)
            skinPart += '<convert type="VExtraNumText">minHand</convert>\n'
            skinPart += '</widget>\n'
            skinPart += '<widget source="global.CurrentTime" render="VWatches" position="%s,%s" size="41,41" zPosition="2" alphatest="on">\n' % (self[widgetName].instance.position().x()+41, self[widgetName].instance.position().y()+43)
            skinPart += '<convert type="VExtraNumText">hourHand</convert>\n'
            skinPart += '</widget>\n'
            return skinPart
        elif widgetName == "TEMPINFO":
            skinPart += '<widget source="session.CurrentService" render="Label" position="%s,%s" size="%s,%s" font="VFD;%s" zPosition="4" halign="center" valign="center" transparent="1" noWrap="1">\n' % (self[widgetName].instance.position().x(), self[widgetName].instance.position().y(), self[widgetName].instance.size().width(), self[widgetName].instance.size().height(), self[widgetName].instance.size().height())
            skinPart += '<convert type="VtiInfo">TempInfo</convert>\n'
            skinPart += '</widget>\n'
            return skinPart
        elif widgetName == "ChannelName":
            skinPart += '<widget source="session.CurrentService" render="Label" position="%s,%s" size="%s,%s" font="VFD;%s" halign="left" valign="center" transparent="1" text="123">\n' % (self[widgetName].instance.position().x(), self[widgetName].instance.position().y(), self[widgetName].instance.size().width(), self[widgetName].instance.size().height(), self[widgetName].instance.size().height()-2)
            skinPart += '<convert type="ServiceName">Name</convert>\n'
            skinPart += '</widget>\n'
            return skinPart
        elif widgetName == "ChannelNumber":
            skinPart += '<widget source="session.CurrentService" render="Label" position="%s,%s" size="%s,%s" font="VFD;%s" halign="left" valign="center" transparent="1" text="123">\n' % (self[widgetName].instance.position().x(), self[widgetName].instance.position().y(), self[widgetName].instance.size().width(), self[widgetName].instance.size().height(), self[widgetName].instance.size().height()-2)
            skinPart += '<convert type="ExtendedServiceInfo">ServiceNumber</convert>\n'
            skinPart += '</widget>\n'
            return skinPart
        elif widgetName == "FANINFO":
            skinPart += '<widget source="session.CurrentService" render="Label" position="%s,%s" size="%s,%s" font="VFD;%s" zPosition="4" halign="center" valign="center" transparent="1" noWrap="1">\n' % (self[widgetName].instance.position().x(), self[widgetName].instance.position().y(), self[widgetName].instance.size().width(), self[widgetName].instance.size().height(), self[widgetName].instance.size().height()-2)
            skinPart += '<convert type="VtiInfo">FanInfo</convert>\n'
            skinPart += '</widget>\n'
            return skinPart
        elif widgetName == "REMAINING":
            # ["InfoBarSummary", "InfoBarMoviePlayerSummary", "StandbySummary"]
            if which == "InfoBarMoviePlayerSummary":
                skinPart += '<widget source="session.CurrentService" render="Label" position="%s,%s" size="%s,%s" font="VFD;%s" halign="left" valign="top">\n' % (self[widgetName].instance.position().x(), self[widgetName].instance.position().y(), self[widgetName].instance.size().width(), self[widgetName].instance.size().height(), self[widgetName].instance.size().height()-2)
                skinPart += '<convert type="ServicePosition">Remaining</convert>\n'
                skinPart += '</widget>\n'
            elif which == "InfoBarSummary":
                skinPart += '<widget source="session.Event_Now" render="Label" position="%s,%s" size="%s,%s" font="VFD;%s" halign="left" valign="top">\n' % (self[widgetName].instance.position().x(), self[widgetName].instance.position().y(), self[widgetName].instance.size().width(), self[widgetName].instance.size().height(), self[widgetName].instance.size().height()-2)
                skinPart += '<convert type="EventTime">Remaining</convert>\n'
                skinPart += '<convert type="RemainingToText">InMinutes</convert>\n'
                skinPart += '</widget>\n'
            return skinPart
        else:
            return None
        
    def getPiconSize(self, filename):
        im = Image.open(filename)
        width, height = im.size
        print width, height
        return width, height

    def onoff(self):
        if self.listmode == "Widgetslist":
            widgetLabelName = self["Widgetslist"].getCurrent()[0][0]
            widgetLabelStatus = self["Widgetslist"].getCurrent()[0][1]
            if int(widgetLabelStatus) == 0:
                self[widgetLabelName].show()
                self.changeWidgetStatus(widgetLabelName, "1")
            else:
                self[widgetLabelName].hide()
                self.changeWidgetStatus(widgetLabelName, "0")
        elif self.listmode == "backuplist":
            self.switchlist()
        elif self.listmode == "menulist":
            choose = self["menulist"].getCurrent()[0]
            print choose
            self.writeSkinFile(choose)
            self["Widgetslist"].hide()
            self.listmode = "backuplist"
            self['InfoLine'].setText("Saved skins:")
            self["backuplist"].show()
            self.writeBackup(choose)
            self["menulist"].hide()

    def changeWidgetStatus(self, widgetLabelName, currentStatus):
        dumpList = []
        for name,status in self.list:
            if name == widgetLabelName:
                dumpList.append((name, currentStatus))
            else:
                dumpList.append((name, status))
        self.list = dumpList
        self.chooseMenuList.setList(map(self.paintWidgetsList, self.list))

    def readPos(self):
        self.widgetLabel = self["Widgetslist"].getCurrent()[0][0]
        print self.widgetLabel
        pos = self[self.widgetLabel].instance.position()
        self.xachse = pos.x()
        self.yachse = pos.y()

    def right(self):
        if self["Widgetslist"].getCurrent()[0][1] == "0" or self.listmode == "backuplist" or self.listmode == "menulist":
            return
        self.readPos()
        self.xachse += 5
        newPos = ePoint(self.xachse,self.yachse)
        self[self.widgetLabel].move(newPos)
        self.showWidgetInfo()
        
    def left(self):
        if self["Widgetslist"].getCurrent()[0][1] == "0" or self.listmode == "backuplist" or self.listmode == "menulist":
            return
        self.readPos()
        self.xachse -= 5
        newPos = ePoint(self.xachse,self.yachse)
        self[self.widgetLabel].move(newPos)
        self.showWidgetInfo()

    def down(self):
        if self["Widgetslist"].getCurrent()[0][1] == "0" or self.listmode == "backuplist" or self.listmode == "menulist":
            return
        self.readPos()
        self.yachse += 5
        newPos = ePoint(self.xachse,self.yachse)
        self[self.widgetLabel].move(newPos)
        self.showWidgetInfo()

    def up(self):
        if self["Widgetslist"].getCurrent()[0][1] == "0" or self.listmode == "backuplist" or self.listmode == "menulist":
            return
        self.readPos()
        self.yachse -= 5
        newPos = ePoint(self.xachse,self.yachse)
        self[self.widgetLabel].move(newPos)
        self.showWidgetInfo()

    def keyCancel(self):
        if self.listmode == "menulist":
            self.listmode = "Widgetslist"
            self["menulist"].hide()
            self["backuplist"].hide()
            self["Widgetslist"].show()
            self['InfoLine'].setText("Select widget:")
        else:
            self.close(None)
