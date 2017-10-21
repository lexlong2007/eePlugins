# -*- coding: utf-8 -*-
from inits import *
from debug import printDEBUG
from translate import _
from manageXML import *

from Components.Sources.List import List
from Screens.ChoiceBox import ChoiceBox
from Screens.MessageBox import MessageBox

from Screens.ChannelSelection import SimpleChannelSelection, service_types_tv, service_types_radio
from Screens.Screen import Screen
from Screens.HelpMenu import HelpableScreen
from Screens.Standby import TryQuitMainloop
from enigma import getDesktop, eServiceCenter, eServiceReference, gFont, addFont, eListboxPythonMultiContent, RT_HALIGN_LEFT, RT_HALIGN_RIGHT, \
                    RT_HALIGN_CENTER, RT_VALIGN_CENTER, RT_VALIGN_TOP, RT_VALIGN_BOTTOM, \
                      eLabel, eWidget, eSlider, fontRenderClass, ePoint, eSize, eDBoxLCD, ePicLoad, gPixmapPtr
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
from PIL import Image
import skin #we use loadSkin, dom_screens


import glob, re, os, random, time

isVTI = None
imageType = 'Unknown'
#configure for VTI or openATV
try:
    if config.skin.primary_vfdskin.value == '': pass # exists in VTI only
    myLCDconfig = config.skin.primary_vfdskin
    isVTI = True
    skinPath=resolveFilename(SCOPE_SKIN, 'vfd_skin/skin_vfd_UserSkin.xml')
    imageType ='VTI'
except:
    try:
        if config.skin.display_skin.value == '': pass # exists in openATV
        imageType ='openATV'
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
    def __init__(self, session):
        if fileExists('/usr/local/e2'): #fake LCD size for enigma2-pc
            self.LCDwidth = 481
            self.LCDheight = 321
            self.imageType = 'enigma2-PC'
        else:
            self.LCDwidth = getDesktop(1).size().width()
            self.LCDheight = getDesktop(1).size().height()
            self.imageType = 'AQQ'
        skin = """
        <screen name="MiniTVskinner" title="miniTV (%dx%d) skin creator mod j00zek on %s" position="center,center" size="1280,720">
            <eLabel position="0,0" size="%d,%d" zPosition="-10" backgroundColor="#00aaaaaa" />
          <!-- active WIDGET description -->
            <widget source="WidgetParams" render="Listbox" position="0,480" size="800,240" scrollbarMode="showOnDemand" zPosition="10" backgroundColor="#080808" >
                <convert type="TemplatedMultiContent">
                    {"template": [
                        MultiContentEntryText(pos = (0,0), size = (800, 22), font=0, flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0, color=0x808080, color_sel=0xffffff ),
                        ],
                        "fonts": [gFont("Regular", 20)],
                        "itemHeight": 22
                    }
                </convert>
            </widget>
          <!-- Bottom MENU -->
            <eLabel position="810,620" size="5,25" zPosition="-10" backgroundColor="#20b81c46" />
            <widget name="red" position="820,620" size="485,25" zPosition="10" font="Regular;21" noWrap="1" halign="left" valign="center" transparent="1"/>
            <eLabel position="810,645" size="5,25" zPosition="-10" backgroundColor="#20009f3c" />
            <widget name="green" position="820,645" size="485,25" zPosition="10" font="Regular;21" noWrap="1" halign="left" valign="center"  transparent="1"/>
            <eLabel position="810,670" size="5,25" zPosition="-10" backgroundColor="#209ca81b" />
            <widget name="yellow" position="820,670" size="485,25" zPosition="10" font="Regular;21" noWrap="1" halign="left" valign="center"  transparent="1"/>
            <eLabel position="810,695" size="5,25" zPosition="-10" backgroundColor="#202673ec" />
            <widget name="blue" position="820,695" size="485,25" zPosition="10" font="Regular;21" noWrap="1" halign="left" valign="center"  transparent="1"/>
            <!--ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/UserSkin/pic/left_right.png" position="1013,695" size="25,25" alphatest="on" />
            <widget name="leftright" position="1055,695" size="700,25" zPosition="10" font="Regular;21" noWrap="1" halign="left" valign="center" /-->
          <!-- Widgets list on right -->
            <widget name="InfoLine" position="810,5" size="470,30" zPosition="5" transparent="0" halign="left" valign="top" font="Regular;28" foregroundColor="yellow" />
            <widget source="Widgetslist" render="Listbox" position="810,40" size="470,550" scrollbarMode="showOnDemand" zPosition="10" backgroundColor="#20a0a0a0">
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
          <!-- WIDGETS -->\n""" % (self.LCDwidth, self.LCDheight, self.imageType, self.LCDwidth+2, self.LCDheight+2)
          
        skinLCD = '<screen name="MiniTVskinner_summary" position="center,center" size="%d,%d">' % (self.LCDwidth, self.LCDheight)
    
        self.WidgetsDict = getWidgetsDefinitions(PluginPath + '/LCDskin/')
        self.WidgetsList = []
        for widget in self.WidgetsDict:
            skin += '          ' + self.WidgetsDict[widget]['previewXML'] + '\n'
            skinLCD +=  '          ' + self.WidgetsDict[widget]['previewXML'] + '\n'
            self.WidgetsList.append(( LoadPixmap(getPixmapPath(self.WidgetsDict[widget]['widgetPic'])),self.WidgetsDict[widget]['widgetActiveState'],
                                      self.WidgetsDict[widget]['widgetDisplayName'],self.WidgetsDict[widget]['widgetInfo'],widget))
                        
        skin += '\n</screen>'
        skinLCD += '\n</screen>'
        
        printDEBUG(skin)
        self.skin = skin
        self.session = session
        Screen.__init__(self, session)

        self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "WizardActions", "ColorActions", "SetupActions", "NumberActions", "MenuActions", "EPGSelectActions"], {
            "cancel": self.keyCancel,
            "ok": self.KeyOK,
            "left": self.KeyLeft,
            "right": self.KeyRight,
            "up": self.KeyUp,
            "down": self.KeyDown,
            "red": self.keyCancel,
            "nextBouquet" : self.listUP,
            "prevBouquet" : self.listDown,
            "red" : self.KeyRed,
            "green": self.KeyGreen,
            "yellow": self.KeyYellow,
            "blue" : self.KeyBlue,
            "2" : self.heightDecrease,
            "8" : self.heightIncrease,
            "4" : self.widthDecrease,
            "6" : self.widthIncrease,
        }, -1)
        
        addFont(resolveFilename(SCOPE_FONTS,"meteocons.ttf"), "Meteo", 100, False)

        self.keyLocked = True
        self.backuplist = []
        self.menulist = open(PluginPath + '/LCDskin/_selection_screens', 'r').readlines()
        self["Widgetslist"] = List()
        self["Widgetslist"].list = []
        self["WidgetParams"] = List()
        self["WidgetParams"].list = []

        self.chooseMenuList3 = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
        self.chooseMenuList3.l.setFont(0, gFont('Regular', 23))
        self.chooseMenuList3.l.setItemHeight(50)

        self['InfoLine'] = Label(_("Select Widget:"))
        self['red'] = Label(_("Load saved design"))
        self['green'] = Label(_("Save design"))
        self['yellow'] = Label(_("Save as LCD skin"))
        self['blue'] = Label(_("Save as UserSkin skin"))
        #self['leftright'] = Label(_("Resize width/height"))
        
        #initiate dynamic widgets
        for widget in self.WidgetsList: #(widgetPic, widgetActiveState _(widgetName), widgetName, widgetInitscript, previewXML, widgetXML) #widgetActiveState=X then widget disabled
            printDEBUG('Executing:%s' % self.WidgetsDict[widget[4]]['widgetInitscript'])
            if self.WidgetsDict[widget[4]]['widgetInitscript'] != '':
                try:
                    exec(self.WidgetsDict[widget[4]]['widgetInitscript'])
                except Exception, e:
                    printDEBUG('EXCEPTION running init script for %s:' % (widget, str(e)))

        self.xachse = 0
        self.yachse = 0
        self.wsize = "height"
        self.xsize = 0
        self.ysize = 0
        
        self.onLayoutFinish.append(self.start)

    def start(self):
        l = self.WidgetsList #(widgetPic, widgetActiveState, _(widgetName), widgetName, widgetInitscript, previewXML, widgetXML) #widgetActiveState=X then widget disabled
        l.sort()
        self["Widgetslist"].list = l
        self.currIndex=self["Widgetslist"].getIndex()
        
        self.miniTVskinsPath = resolveFilename(SCOPE_CONFIG, 'miniTVskins')
        if not fileExists(self.miniTVskinsPath):
            os.mkdir(miniTVskinsPath)  

        if not self.selectionChanged in self["Widgetslist"].onSelectionChanged:
            self["Widgetslist"].onSelectionChanged.append(self.selectionChanged)

        #self.readSize()
        #self.showWidgetInfo()
        #self.readBackups()

    def listUP(self):
        self["Widgetslist"].selectPrevious()
        self.showWidgetInfo()
        
    def listDown(self):
        if self.currIndex == len(self.WidgetsList) -1 :
            self["Widgetslist"].setIndex(0)
        else:
            self["Widgetslist"].selectNext()
        self.showWidgetInfo()

    def showWidgetInfo(self):
        return
        self.readSize()
        myInfo  = _('Active Widget:\n')
        myInfo += _('Position: %sx%s') % ( self[self.widgetLabel].instance.position().x(), self[self.widgetLabel].instance.position().y() )
        myInfo += '\n'
        myInfo += _('size: %sx%s') % ( self[self.widgetLabel].instance.size().width(), self[self.widgetLabel].instance.size().height() )
        myInfo += '\n'
        myInfo += _('Font: XXX')
        myInfo += '\n'
        myInfo += _('size: YYY')
        myInfo += '\n'
        myInfo += _('Text color: XXX')
        myInfo += '\n'
        myInfo += _('Background color: YYY')
        myInfo += '\n'
        myInfo += _('Path: /aqq\n')

    def heightDecrease(self):
        self.changeSize('height', -2)
      
    def widthDecrease(self):
        self.changeSize('width', -2)
      
    def heightIncrease(self):
        self.changeSize('height', 2)
      
    def widthIncrease(self):
        self.changeSize('width', 2)

    def changeSize(self, Dimension, Value ):
        if self["Widgetslist"].getCurrent()[0][1] == "0":
            return
        self.readSize()
        if Dimension == "width":
            self.xsize += Value
            self[self.widgetLabel].instance.resize(eSize(self.xsize,self.ysize))
        else:
            self.ysize += Value
            self[self.widgetLabel].instance.resize(eSize(self.xsize,self.ysize))

        if str(type(self[self.widgetLabel])) == "<class 'Components.Pixmap.Pixmap'>":
            self[self.widgetLabel].instance.setScale(3)
        elif str(type(self[self.widgetLabel])) == "<class 'Components.Slider.Slider'>":
            pass
        else:
            if Dimension == "height":
                if self.widgetLabel == "WEATHER":
                    self[self.widgetLabel].instance.setFont(gFont('Meteo', self.ysize))
                else:
                    self[self.widgetLabel].instance.setFont(gFont('Regular', self.ysize-2))
        self.showWidgetInfo()

    def readSize(self):
        return
        self.widgetLabel = self["Widgetslist"].getCurrent()[0][0]
        self.xsize = self[self.widgetLabel].instance.size().width()
        self.ysize = self[self.widgetLabel].instance.size().height()
        print self.widgetLabel, self.xsize, self.ysize

    def writeDesign(self, filename):
        if filename is not None and filename != '':
            self.session.open(MessageBox, "writeDesign " + filename + '\n' + _("action NOT ready yet"), type = MessageBox.TYPE_INFO, timeout=10)

    def readBackups(self):
        self.backuplist = []
        for fileName in os.listdir(miniTVskinsPath):
            if fileName.endswith('.backup'):
                fileName = fileName[:-7]
                fileParts = fileName.split(',')
                if len(fileParts) == 2:
                    self.backuplist.append((fileParts[0],fileParts[1]))
        self.backuplist.reverse()

    def writeSkinFile(self, which):
        screenPart = ""
        screenPart += '\n<screen name="%s" position="0,0" size="480,320" id="1">\n' % which
        for widget,status in self.WidgetsList:
            if int(status) == 1:
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
        
        f = open('/usr/share/enigma2/vfd_skin/skin_vfd_miniTvSkinner.xml', 'w')
        f.write(skinFile)
        f.close()
        
        if myLCDconfig.value != "vfd_skin/skin_vfd_miniTvSkinner.xml":
            print "set new VFD Skin..", myLCDconfig.value
            myLCDconfig.value = "vfd_skin/skin_vfd_miniTvSkinner.xml"
            myLCDconfig.save()
        skin.loadSkin("/usr/share/enigma2/vfd_skin/skin_vfd_miniTvSkinner.xml")
        restartbox = self.session.openWithCallback(self.restartGUI,MessageBox,_("GUI needs a restart to apply a new skin\nDo you want to Restart the GUI now?"), MessageBox.TYPE_YESNO)
        restartbox.setTitle(_("Restart GUI now?"))

        #eDBoxLCD.getInstance().update()

    def restartGUI(self, answer):
        if answer is True:
            self.session.open(TryQuitMainloop, 3)

    def getPiconSize(self, filename):
        im = Image.open(filename)
        width, height = im.size
        print width, height
        return width, height

    def KeyOK(self):
        widgetLabelName = self.WidgetsList[self.currIndex][2] #(widgetPic, widgetActiveState, _(widgetName), widgetName, widgetInitscript, previewXML, widgetXML) #widgetActiveState=X then widget disabled
        widgetLabelStatus = self.WidgetsList[self.currIndex][1]
        if widgetLabelStatus == 'X':
            self[widgetLabelName].show()
            self.WidgetsList[self.currIndex][1] = ''
        elif widgetLabelStatus == '':
            self[widgetLabelName].hide()
            self.WidgetsList[self.currIndex][1] = 'X'

    def changeWidgetStatus(self, widgetLabelName, currentStatus):
        dumpList = []
        for name,status in self.WidgetsList:
            if name == widgetLabelName:
                dumpList.append((name, currentStatus))
            else:
                dumpList.append((name, status))
        self.WidgetsList = dumpList
        self.chooseMenuList.setList(map(self.paintWidgetsList, self.WidgetsList))

    def readPos(self):
        self.widgetLabel = self["Widgetslist"].getCurrent()[0][0]
        print self.widgetLabel
        pos = self[self.widgetLabel].instance.position()
        self.xachse = pos.x()
        self.yachse = pos.y()

    def selectionChanged(self):
        self.currIndex=self["Widgetslist"].getIndex()
        self.currwidgetName = self.WidgetsList[self.currIndex][4]
        myList = self.WidgetsDict[self.currwidgetName]['widgetParams']
        print myList
        self["WidgetParams"].list = myList
      
    def KeyRight(self):
        try:
            if self["Widgetslist"].getCurrent()[0][1] == "0":
                return
        except Exception:
            return
        self.readPos()
        self.xachse += 5
        if self.xachse < self.LCDwidth:
            newPos = ePoint(self.xachse,self.yachse)
            self[self.widgetLabel].move(newPos)
            self.showWidgetInfo()
        
    def KeyLeft(self):
        try:
            if self["Widgetslist"].getCurrent()[0][1] == "0":
                return
        except Exception:
            return
        self.readPos()
        self.xachse -= 5
        if self.xachse < 0:
            self.xachse = 0
        newPos = ePoint(self.xachse,self.yachse)
        self[self.widgetLabel].move(newPos)
        self.showWidgetInfo()

    def KeyDown(self):
        try:
            if self["Widgetslist"].getCurrent()[0][1] == "0":
                return
        except Exception:
            return
        self.readPos()
        self.yachse += 5
        if self.yachse < self.LCDheight:
            newPos = ePoint(self.xachse,self.yachse)
            self[self.widgetLabel].move(newPos)
            self.showWidgetInfo()

    def KeyUp(self):
        try:
            if self["Widgetslist"].getCurrent()[0][1] == "0":
                return
        except Exception:
            return
        self.readPos()
        self.yachse -= 5
        if self.yachse < 0:
            self.yachse = 0
        newPos = ePoint(self.xachse,self.yachse)
        self[self.widgetLabel].move(newPos)
        self.showWidgetInfo()

    def KeyRed(self):
        savedDesigns = []
        for fileName in os.listdir(self.miniTVskinsPath):
            if fileName.endswith('.backup'):
                savedDesigns.append((fileName[:-7],fileName))
        if len(savedDesigns) == 0:
            self.session.openWithCallback(self.doNothing, MessageBox,_("No saved designs found"),  type = MessageBox.TYPE_INFO, timeout = 10, default = False)
        else:
            self.session.openWithCallback(self.KeyRedCallback, ChoiceBox, title = _("Select saved design to load:"), list = savedDesigns)
      
    def KeyRedCallback(self, ret):
        if ret:
            self.session.open(MessageBox, "Load\n" + self.miniTVskinsPath + ret[1] + '\n' + _("action NOT ready yet"), type = MessageBox.TYPE_INFO, timeout=10)
      
    def KeyGreen(self):
        currentTime = time.strftime("%d.%m.%Y - %H:%M:%S")
        myList = []
        with open(PluginPath + '/LCDskin/_selection_screens', 'r') as f:
            for line in f:
                myList.append(('%s-%s' % (line.strip(), currentTime), True))
        myList.append((_('I want to enter own name'),False))
        self.session.openWithCallback(self.KeyGreenCallback, ChoiceBox, title = _("Save as:"), list = myList)
        
    def KeyGreenCallback(self, ret):
        if ret:
            if ret[1] == True:
                self.writeDesign(ret[0])
            else:
                from Screens.VirtualKeyBoard import VirtualKeyBoard
                self.session.openWithCallback(self.writeDesign, VirtualKeyBoard, title=(_("Enter filename")), text = "")

    def KeyYellow(self):
        self.session.open(MessageBox, "KeyYellow" +' ' + _("action NOT ready yet"), type = MessageBox.TYPE_INFO, timeout=10)

    def KeyBlue(self):
        self.session.open(MessageBox, "KeyBlue" +' ' + _("action NOT ready yet"), type = MessageBox.TYPE_INFO, timeout=10)

    def doNothing(self, ret = None):
        return
      
    def keyCancel(self):
        self.close()
