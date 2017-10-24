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
        self.skin = """
        <screen name="MiniTVskinner" title="miniTV (%dx%d) skin creator mod j00zek on %s" position="center,center" size="1280,720">
            <eLabel position="0,0" size="800,460" zPosition="-10" backgroundColor="#00222222" />
            <eLabel position="0,0" size="%d,%d" zPosition="-9" backgroundColor="#00555555" />
          <!-- active WIDGET description -->
            <widget source="WidgetParams" render="Listbox" position="0,480" size="800,240" scrollbarMode="showOnDemand" zPosition="10" backgroundColor="#080808" >
                <convert type="TemplatedMultiContent">
                    {"template": [
                        MultiContentEntryText(pos = (0,0), size = (774, 26), font=0, flags = RT_HALIGN_LEFT|RT_VALIGN_CENTER, text = 0, color=0x808080, color_sel=0xffffff ),
                        MultiContentEntryPixmapAlphaTest(pos = (696, 0), size = (104, 26), png = 1),
                        ],
                        "fonts": [gFont("Regular", 22)],
                        "itemHeight": 28
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
          <!-- Widgets list on right -->
            <widget name="InfoLine" position="810,5" size="410,30" zPosition="5" transparent="0" halign="left" valign="top" font="Regular;28" foregroundColor="yellow" />
            <ePixmap pixmap="%spic/wdg_btn_ch_plus_minus.png" position="1228,5" size="60,30" alphatest="on" zPosition="10" />
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
          <!-- WIDGETS -->\n""" % (self.LCDwidth, self.LCDheight, self.imageType, self.LCDwidth+2, self.LCDheight+2, PluginPath)
          
        self.skinLCD = '<screen name="MiniTVskinner_summary" position="center,center" size="%d,%d">' % (self.LCDwidth, self.LCDheight)
    
        if getDictDesigns() is None:
            self.WidgetsDict = getWidgetsDefinitions(PluginPath + '/LCDskin/', self.LCDwidth, self.LCDheight)
        else:
            self.WidgetsDict = getDictDesigns()
            setDictDesigns(None)
            
        for widget in self.WidgetsDict:
            self.skin += '          ' + self.WidgetsDict[widget]['previewXML'] + '\n'
            self.skinLCD +=  '          ' + self.WidgetsDict[widget]['previewXML'] + '\n'
                        
        self.skin += '\n</screen>'
        self.skinLCD += '\n</screen>'
        
        printDEBUG(self.skin)
        #self.skin = skin
        self.session = session
        Screen.__init__(self, session)

        self["actions"]  = ActionMap(["UserSkinMiniTVmakerActions"], {
            "keyCancel": self.keyCancel,
            "keyOK": self.KeyOK,
            "keyLeft": self.KeyLeft,
            "keyRight": self.KeyRight,
            "keyUp": self.KeyUp,
            "keyDown": self.KeyDown,
            "keyChannelUp" : self.listUP,
            "keyChannelDown" : self.listDown,
            "keyMenu" : self.widgetConfig,
            "keyRed" : self.KeyRed,
            "keyGreen": self.KeyGreen,
            "keyYellow": self.KeyYellow,
            "keyBlue" : self.KeyBlue,
            "key2" : self.heightDecrease,
            "key8" : self.heightIncrease,
            "key4" : self.widthDecrease,
            "key6" : self.widthIncrease,
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
        
        #initiate dynamic widgets
        self.updateWidgetsList() #generates self.WidgetsList
        for widget in self.WidgetsList: #(widgetPic, widgetActiveState _(widgetName), widgetName, widgetInitscript, previewXML, widgetXML) #widgetActiveState=X then widget disabled
            printDEBUG('Executing:%s' % self.WidgetsDict[widget[4]]['widgetInitscript'])
            if self.WidgetsDict[widget[4]]['widgetInitscript'] != '':
                try:
                    exec(self.WidgetsDict[widget[4]]['widgetInitscript'])
                except Exception, e:
                    printDEBUG('EXCEPTION running init script for %s: %s' % (widget[4], str(e)))
            if self.WidgetsDict[widget[4]]['widgetActiveState'] != '':
                self[widget[4]].hide()

        self.wsize = "height"
        self.xsize = 0
        self.ysize = 0
        
        self.onLayoutFinish.append(self.start)

    def start(self):
        l = self.WidgetsList
        self["Widgetslist"].list = l
        self.currIndex=self["Widgetslist"].getIndex()
        self.currWidgetName = self.WidgetsList[self.currIndex][4]
        
        self.miniTVdesignsPath = resolveFilename(SCOPE_CONFIG, 'miniTVdesigns')
        if not fileExists(self.miniTVdesignsPath):
            os.mkdir(self.miniTVdesignsPath)  

        if not self.selectionChanged in self["Widgetslist"].onSelectionChanged:
            self["Widgetslist"].onSelectionChanged.append(self.selectionChanged)

        self.readSize()
        #self.showWidgetInfo()
        #self.readBackups()
        self.selectionChanged()

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
#### CHANGE WIDGET SIZE
    def heightDecrease(self):
        self.changeSize(0,-1)
      
    def widthDecrease(self):
        self.changeSize(-1,0)
      
    def heightIncrease(self):
        self.changeSize(0,1)
      
    def widthIncrease(self):
        self.changeSize(1,0)

    def readSize(self):
        sizeX = self[self.currWidgetName].instance.size().width()
        sizeY = self[self.currWidgetName].instance.size().height()
        return sizeX, sizeY

    def changeSize(self, stepX=0, stepY=0 ):
        if self["Widgetslist"].getCurrent()[1] == "":
            sizeX, sizeY = self.readSize()
            sizeX += stepX
            if sizeX < 1: sizeX = 1
            elif sizeX > self.LCDwidth: sizeX = self.LCDwidth
            sizeY += stepY
            if sizeY < 1: sizeY = 1
            elif sizeY > self.LCDheight: sizeY = self.LCDheight
            self[self.currWidgetName].instance.resize(eSize(sizeX,sizeY))
            self.updateWidgetXMLs('size', '%s,%s' %(sizeX,sizeY))
#### MOVING WIDGET
    def KeyRight(self, step=1):
        self.changePos(1, 0)
        
    def KeyLeft(self):
        self.changePos(-1, 0)

    def KeyDown(self):
        self.changePos(0, 1)

    def KeyUp(self):
        self.changePos(0, -1)

    def readPos(self):
        pos = self[self.currWidgetName].instance.position()
        return pos.x(),  pos.y()

    def changePos(self,stepX=0, stepY=0):
        if self["Widgetslist"].getCurrent()[1] == "":
            posX, posY = self.readPos()
            posX += stepX
            if posX < 0: posX = 0
            elif posX > self.LCDwidth: posX = self.LCDwidth
            posY += stepY
            if posY < 0: posY = 0
            elif posY > self.LCDheight: posY = self.LCDheight
            newPos = ePoint(posX, posY)
            self[self.currWidgetName].move(newPos)
            self.updateWidgetXMLs('position', '%s,%s' %(posX,posY))

#### Manipulate WIDGET XMLs >>>
    def updateWidgetXMLs(self, param, paramValue):
        self.WidgetsDict[self.currWidgetName]['previewXML'] = updateWidgetparam( self.WidgetsDict[self.currWidgetName]['previewXML'],param, paramValue)
        self.WidgetsDict[self.currWidgetName]['widgetXML'] = updateWidgetparam( self.WidgetsDict[self.currWidgetName]['widgetXML'],param, paramValue)
        self.showWidgetInfo()
#### WIDGETS LIST >>>
    def updateWidgetsList(self, refreshGUI = False):
        self.WidgetsList = []
        for widget in self.WidgetsDict:
            self.WidgetsList.append(( LoadPixmap(getPixmapPath(self.WidgetsDict[widget]['widgetPic'])),self.WidgetsDict[widget]['widgetActiveState'],
                                      self.WidgetsDict[widget]['widgetDisplayName'],self.WidgetsDict[widget]['widgetInfo'],widget))
        
        try: self.WidgetsList.sort(key=lambda t : tuple(str(t[2]).lower()))
        except Exception: self.WidgetsList.sort()
        
        if refreshGUI == True:
            try:
                self["Widgetslist"].UpdateList(self.WidgetsList)
            except Exception:
                print "Update assert error :(" #workarround to have it working on openpliPC
                myIndex=self["Widgetslist"].getIndex() #as an effect, index is cleared so we need to store it first
                self["Widgetslist"].setList(self.WidgetsList)
                self["Widgetslist"].setIndex(myIndex) #and restore
            self.selectionChanged()
      
    def showWidgetInfo(self):
        self["WidgetParams"].list = getWidgetParams(self.WidgetsDict[self.currWidgetName]['previewXML'])

    def listUP(self):
        self["Widgetslist"].selectPrevious()
        #self.showWidgetInfo()
        
    def listDown(self):
        if self.currIndex == len(self.WidgetsList) -1 :
            self["Widgetslist"].setIndex(0)
        else:
            self["Widgetslist"].selectNext()
        #self.showWidgetInfo()

    def selectionChanged(self):
        self.currIndex=self["Widgetslist"].getIndex()
        self.currWidgetName = self.WidgetsList[self.currIndex][4]
        self.showWidgetInfo()
        
    def KeyOK(self):
        self.currWidgetName = self.WidgetsList[self.currIndex][4]
        if self.WidgetsDict[self.currWidgetName]['widgetActiveState'] == 'X':
            self[self.currWidgetName].show()
            self.WidgetsDict[self.currWidgetName]['widgetActiveState'] = ''
        elif self.WidgetsDict[self.currWidgetName]['widgetActiveState'] == '':
            self[self.currWidgetName].hide()
            self.WidgetsDict[self.currWidgetName]['widgetActiveState'] = 'X'
        self.updateWidgetsList(refreshGUI=True)
#### LOAD DESIGNS >>>
    def KeyRed(self):
        savedDesigns = []
        for fileName in os.listdir(self.miniTVdesignsPath):
            if fileName.endswith('.design'):
                savedDesigns.append((fileName[:-7],"%s/%s" % (self.miniTVdesignsPath,fileName)))
        for fileName in os.listdir('%s/LCDskin/sharedDesigns' % (PluginPath) ):
            if fileName.endswith('.design'):
                savedDesigns.append((fileName[:-7],"%s/%s" % (self.miniTVdesignsPath,fileName)))
        if len(savedDesigns) == 0:
            self.session.openWithCallback(self.doNothing, MessageBox,_("No saved designs found"),  type = MessageBox.TYPE_INFO, timeout = 10, default = False)
        else:
            self.session.openWithCallback(self.KeyRedCallback, ChoiceBox, title = _("Select saved design to load:"), list = savedDesigns)
      
    def KeyRedCallback(self, ret):
        def _byteify(data, ignore_dicts = False):
            # if this is a unicode string, return its string representation
            if isinstance(data, unicode):
                return data.encode('utf-8')
            # if this is a list of values, return list of byteified values
            if isinstance(data, list):
                return [ _byteify(item, ignore_dicts=True) for item in data ]
            # if this is a dictionary, return dictionary of byteified keys and values
            # but only if we haven't already byteified it
            if isinstance(data, dict) and not ignore_dicts:
                return {
                    _byteify(key, ignore_dicts=True): _byteify(value, ignore_dicts=True)
                    for key, value in data.iteritems()
                }
            # if it's anything else, return it in its original form
            return data
        if ret:
            wDict={}
            import json
            try:
                with open(ret[1], 'r') as f:
                    wDict= _byteify(json.loads(f.read(), object_hook=_byteify), ignore_dicts=True)
                    f.close()
                for widget in wDict:
                  if widget in self.WidgetsDict:
                      self.WidgetsDict[widget] = wDict[widget]
                
                setDictDesigns(self.WidgetsDict)
                self.updateWidgetsList(True)      
                self.session.openWithCallback(self.cancelRet,MessageBox, _("Design %s\n ...has been loaded") % ret[0], type = MessageBox.TYPE_INFO, timeout=10)
            except Exception, e:
                printDEBUG("Error occured: %s" % str(e))
                self.session.open(MessageBox, "Error occured: %s" % str(e), type = MessageBox.TYPE_ERROR, timeout=10)
                
    def cancelRet(self, ret = None):
        self.close(234)
        
#### WRITE DESIGNS >>>
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
                self.KeyGreenwriteDesign(ret[0])
            else:
                from Screens.VirtualKeyBoard import VirtualKeyBoard
                self.session.openWithCallback(self.KeyGreenwriteDesign, VirtualKeyBoard, title=(_("Enter filename")), text = "")

    def KeyGreenwriteDesign(self, filename):
        if filename is not None and filename != '':
            import json
            try:
                with open('%s/%s.design' % (self.miniTVdesignsPath, filename), 'w') as f:
                    f.write(json.dumps(self.WidgetsDict, ensure_ascii=False))
                    f.close()
                self.session.open(MessageBox, _("File %s.design\n ...has been written") % filename, type = MessageBox.TYPE_INFO, timeout=10)
            except Exception, e:
                self.session.open(MessageBox, "Error occured: %s" % str(e), type = MessageBox.TYPE_ERROR, timeout=10)
#### WRITE DESIGNS <<<
    def KeyYellow(self):
        self.session.open(MessageBox, "KeyYellow" +' ' + _("action NOT ready yet"), type = MessageBox.TYPE_INFO, timeout=10)

    def KeyBlue(self):
        self.session.open(MessageBox, "KeyBlue" +' ' + _("action NOT ready yet"), type = MessageBox.TYPE_INFO, timeout=10)

    def doNothing(self, ret = None):
        return
      
    def keyCancel(self):
        self.close()

    def widgetConfig(self):
        self.session.open(MessageBox, "widgetConfig" +' ' + _("action NOT ready yet"), type = MessageBox.TYPE_INFO, timeout=10)

    def createSummary(self):
         return None
         #return miniTVskinnerLCDScreen
      
################################################################################################################################################################      
class miniTVskinnerLCDScreen(Screen):
    def __init__(self, session, parent):
        Screen.__init__(self, session, parent = parent)
        #/PluginBrowser.py
        #self.onShow.append(self.addWatcher)
        #self.onHide.append(self.removeWatcher)
        

