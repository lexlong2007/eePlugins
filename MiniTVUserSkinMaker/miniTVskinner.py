# -*- coding: utf-8 -*-
from inits import *
from inits import translate as _
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
from Components.Sources.StaticText import StaticText
from Components.Pixmap import Pixmap, MovingPixmap
from Components.Slider import Slider
from Components.MenuList import MenuList
from Components.Pixmap import Pixmap
import skin #we use loadSkin, dom_screens


import glob, re, os, random, time

def miniTVskinnerInitiator(session, **kwargs):
    def runLCDskin(retDict = None, initRun = False):
        if retDict is not None and len(retDict) > 0:
            session.openWithCallback(runLCDskin,miniTVskinner, retDict )
            return        
    session.openWithCallback(runLCDskin,miniTVskinner, {} )
    return

class miniTVskinner(Screen):
    def __init__(self, session, loadedDesigns):
        if getDesktop(1).size().width() >= getDesktop(2).size().width():
            self.desktopID = 1
        else:
            self.desktopID = 2
          
        if fileExists('/usr/local/e2'): #fake LCD size for enigma2-pc
            self.LCDwidth = 480
            self.LCDheight = 320
            self.imageType = 'enigma2-PC'
        else:
            self.LCDwidth = getDesktop(self.desktopID).size().width()
            self.LCDheight = getDesktop(self.desktopID).size().height()
            if fileExists('/usr/lib/enigma2/python/Plugins/SystemPlugins/VTIPanel'):
                self.imageType = 'VTI'
            elif fileExists('/usr/lib/enigma2/python/Blackhole'):
                self.imageType = 'BlackHole'
            elif fileExists('/usr/lib/enigma2/python/Plugins/Extensions/Infopanel'):
                self.imageType = 'OpenATV'
            else:
                self.imageType = _('Unknown image')
              
        self.skin = """
        <screen name="MiniTVskinner" title="miniTV skin creator (c) j00zek on %s, display %d (%dx%d)" position="center,center" size="1280,720">
            <eLabel position="0,0" size="800,460" zPosition="-10" backgroundColor="#00222222" />
            <eLabel position="0,0" size="%d,%d" zPosition="-9" backgroundColor="#00555555" />
          <!-- active WIDGET description -->
            <widget source="WidgetParams" render="Listbox" position="0,470" size="800,260" scrollbarMode="showOnDemand" zPosition="10" backgroundColor="#080808" >
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
            <ePixmap pixmap="%spic/wdg_btn_TV.png" position="1258,620" size="60,30" alphatest="on" zPosition="10" />
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
          <!-- WIDGETS -->\n""" % (self.imageType, self.desktopID, self.LCDwidth, self.LCDheight, self.LCDwidth+2, self.LCDheight+2, PluginPath, PluginPath)
          
        self.skinLCD = '<screen name="MiniTVskinner_summary" position="center,center" size="%d,%d">' % (self.LCDwidth, self.LCDheight)
    
        if loadedDesigns is None or len(loadedDesigns) ==0 :
            self.WidgetsDict = getWidgetsDefinitions(PluginPath + '/LCDskin/', self.LCDwidth, self.LCDheight)
        else:
            self.WidgetsDict = loadedDesigns
            
        for widget in self.WidgetsDict:
            self.skin += '          ' + self.WidgetsDict[widget]['previewXML'] + '\n'
            self.skinLCD +=  '          ' + self.WidgetsDict[widget]['previewXML'] + '\n'
                        
        self.skin += '\n</screen>'
        self.skinLCD += '\n</screen>'
        
        #printDEBUG(self.skin)
        self.session = session
        Screen.__init__(self, session)

        self["actions"]  = ActionMap(["miniTVskinnerActions"], {
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
            "KeyInfo" : self.changePixmapPath,
            "key7" : self.changeFonttype,
            "key9" : self.FontSizeUp,
            "key3" : self.FontSizeDown,
            "key1" : self.changeforegroundColor,
            "key0" : self.backgroundColor,
            "key5" : self.changeStep,
            "keyTV": self.previewSkin,
        }, -1)
        
        #addFont(resolveFilename(SCOPE_FONTS,"meteocons.ttf"), "Meteo", 100, False)

        self.step = 5
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

        self.onLayoutFinish.append(self.start)

    def start(self):
        self.setTitle(_('miniTV skin creator %s system: %s, display %d (%dx%d)') % (UserSkinInfo, self.imageType, self.desktopID, self.LCDwidth, self.LCDheight))
        l = self.WidgetsList
        self["Widgetslist"].list = l
        self.currIndex=self["Widgetslist"].getIndex()
        self.currWidgetName = self.WidgetsList[self.currIndex][4]
        
        self.miniTVdesignsPath = resolveFilename(SCOPE_CONFIG, 'miniTVdesigns')
        if not fileExists(self.miniTVdesignsPath):
            os.mkdir(self.miniTVdesignsPath)  

        if not self.selectionChanged in self["Widgetslist"].onSelectionChanged:
            self["Widgetslist"].onSelectionChanged.append(self.selectionChanged)
            
        self.colorNamesList = []
        for color in skin.colorNames:
          if color not in self.colorNamesList:
              self.colorNamesList.append((color,color))
        with open(PluginPath + '/LCDskin/_AdditionalColors', 'r') as f:
            for line in f:
                lineParts = line.strip().split(':')
                if len(lineParts) == 2 and lineParts[1] not in self.colorNamesList:
                    self.colorNamesList.append( (lineParts[0],lineParts[1]) )
          

        self.myLCDconfig = None
        self.vfdSkinFileName = None
        try:
            if config.skin.primary_vfdskin.value == '': pass # exists in VTI only
            myLCDconfig = config.skin.primary_vfdskin
            self.vfdSkinFileName = resolveFilename(SCOPE_SKIN, 'vfd_skin/skin_vfd_UserSkin.xml')
        except Exception:
            try:
                if config.skin.display_skin.value == '': pass # exists in openATV
                if fileExists(resolveFilename(SCOPE_SKIN, 'display/')):
                    myLCDconfig = config.skin.display_skin
                    if not fileExists(resolveFilename(SCOPE_SKIN, 'display/Userskin/')):
                        os.mkdir(resolveFilename(SCOPE_SKIN, 'display/Userskin/'))
                    self.vfdSkinFileName = resolveFilename(SCOPE_SKIN, 'display/Userskin/skin_display.xml')
            except Exception, e:
                printDEBUG('System does not have known vfd skin attributes, error: %s' % str(e))
                self['yellow'].hide()
                
        self.fontsList = getLoadedFonts(resolveFilename(SCOPE_SKIN, ''), self.vfdSkinFileName, CurrentSkinName)
        self.selectionChanged()

    def changeStep(self):
        if self.step == 5:
           self.step = 1
        else:
           self.step = 5
        if self["Widgetslist"].getCurrent()[1] == "":
           self.showWidgetInfo()
#### CHANGE COLORS
    def changeforegroundColor(self):
        self.changeColor('foregroundColor')
      
    def backgroundColor(self):
        self.changeColor('backgroundColor')

    def changeColor(self, param):
        if self["Widgetslist"].getCurrent()[1] == "":
            currColor = getWidgetParam(self.WidgetsDict[self.currWidgetName]['previewXML'], param)
            for i, Color in enumerate(self.colorNamesList):
                if currColor == Color[0] or currColor == Color[1]:
                    if i == len(self.colorNamesList)-1:
                        currColor = self.colorNamesList[0]
                    else:
                        currColor = self.colorNamesList[i+1]
                    if param == 'foregroundColor':
                        self[self.currWidgetName].instance.setForegroundColor(skin.parseColor(currColor[0]))
                    elif param == 'backgroundColor':
                        self[self.currWidgetName].instance.setBackgroundColor(skin.parseColor(currColor[0]))
                        self[self.currWidgetName].hide()
                        self[self.currWidgetName].show()
                    self.updateWidgetXMLs( param, currColor[0] )
                    self.session.summary.changeColor(param, skin.parseColor(currColor[0]))
                    break
                    
#### CHANGE FONT
    def changeFonttype(self):
        if self["Widgetslist"].getCurrent()[1] == "":
            fontParts = getWidgetParam(self.WidgetsDict[self.currWidgetName]['previewXML'], 'font')
            if fontParts is not None:
                fontParts = fontParts.split(';')
                fontType = fontParts[0]
                if fontType in self.fontsList:
                    for i,x in enumerate(self.fontsList):
                      if x == fontType:
                          if i == len(self.fontsList)-1:
                              fontType = self.fontsList[0]
                          else:
                              fontType = self.fontsList[i+1]
                          self[self.currWidgetName].instance.setFont(gFont(fontType , int(fontParts[1]) ) )
                          self.session.summary.setFontType(gFont(fontType , int(fontParts[1]) ) )
                          self.updateWidgetXMLs('font', '%s;%s' %(fontType,fontParts[1]))
                          break
                    
      
    def FontSizeUp(self):
        self.changeFontSize(step = 1)
      
    def FontSizeDown(self):
        self.changeFontSize(step = -1)

    def changeFontSize(self, step):
        if self["Widgetslist"].getCurrent()[1] == "":
            fontParts = getWidgetParam(self.WidgetsDict[self.currWidgetName]['previewXML'], 'font')
            if fontParts is not None:
                fontParts = fontParts.split(';')
                fontSize = int(fontParts[1]) + step
                if fontSize < 5: fontSize = 5
                elif fontSize > 200: fontSize = 200
                self[self.currWidgetName].instance.setFont(gFont(fontParts[0] , fontSize ) )
                self.session.summary.setFontSize(gFont(fontParts[0] , fontSize ))
                self.updateWidgetXMLs('font', '%s;%s' %(fontParts[0], fontSize ))
#### CHANGE WIDGET SIZE
    def heightDecrease(self):
        self.changeSize(0,-self.step)
      
    def widthDecrease(self):
        self.changeSize(-self.step,0)
      
    def heightIncrease(self):
        self.changeSize(0,self.step)
      
    def widthIncrease(self):
        self.changeSize(self.step,0)

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
            self.updateSize(sizeX, sizeY)
#### MOVING WIDGET
    def KeyRight(self, step=1):
        self.changePos(self.step, 0)
        
    def KeyLeft(self):
        self.changePos(-self.step, 0)

    def KeyDown(self):
        self.changePos(0, self.step)

    def KeyUp(self):
        self.changePos(0, -self.step)

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
            self.session.summary.moveWidget(newPos)
            self.updateWidgetXMLs('position', '%s,%s' %(posX,posY))

    def changePixmapPath(self):
        if self["Widgetslist"].getCurrent()[1] == "":
            if hasWidgetAttrib(self.WidgetsDict[self.currWidgetName]['previewXML'], 'picontype'):
                picontype = getWidgetParam(self.WidgetsDict[self.currWidgetName]['previewXML'], 'picontype')
                if picontype == 'picon':
                    self.updateWidgetXMLs('picontype', 'xpicon')
                    ppreview = 'XPicon.png'
                elif picontype == 'xpicon':
                    self.updateWidgetXMLs('picontype', 'zzpicon')
                    ppreview = 'ZPicon.png'
                else:
                    self.updateWidgetXMLs('picontype', 'picon')
                    ppreview = 'Picon.png'
                self.updateWidgetXMLs('pixmap', ppreview)
                self[self.currWidgetName].instance.setPixmapFromFile('%spic/%s' % (getPluginPath(), ppreview) )
                from PIL import Image
                width, height = Image.open('%spic/%s' % (getPluginPath(), ppreview)).size
                self.updateSize(width,height)
                self.updateWidgetXMLs('size', '%s,%s' %(width,height))
            else:
                PixmapPath = getWidgetParam(self.WidgetsDict[self.currWidgetName]['previewXML'], 'pixmap')
                if PixmapPath is not None:
                    def SetDirPathCallBack(newPath = None):
                        if None != newPath:
                            self.updateWidgetXMLs('pixmap', newPath)
                            self[self.currWidgetName].instance.setPixmapFromFile(newPath)
                            from PIL import Image
                            width, height = Image.open(newPath).size
                            self.updateSize(width,height)
                            self.updateWidgetXMLs('size', '%s,%s' %(width,height))
                    self.session.openWithCallback(SetDirPathCallBack, miniTVmakerFileBrowser, currDir=os.path.dirname(PixmapPath), title=_("Select file"))
        
#### Manipulate WIDGET XMLs >>>
    def widgetConfigRet(self, reloadSelf = False, parametersDict = {} ):
        if reloadSelf == True:
            for param in parametersDict:
                self.updateWidgetXMLs(param, parametersDict[param])
                self.close(self.WidgetsDict)
      
    def widgetConfig(self):
        if self["Widgetslist"].getCurrent()[1] == "":
            parametersDict = getWidgetParams4Config(self.WidgetsDict[self.currWidgetName]['previewXML'])
            self.session.openWithCallback(self.widgetConfigRet,miniTVskinnerWidgetConfig, parametersDict, self.currWidgetName)

    def updateWidgetXMLs(self, param, paramValue):
        self.WidgetsDict[self.currWidgetName]['previewXML'] = updateWidgetparam( self.WidgetsDict[self.currWidgetName]['previewXML'],param, paramValue)
        self.WidgetsDict[self.currWidgetName]['widgetXML'] = updateWidgetparam( self.WidgetsDict[self.currWidgetName]['widgetXML'],param, paramValue)
        self.showWidgetInfo()

    def updateSize(self, sizeX, sizeY ):
        self[self.currWidgetName].instance.resize(eSize(sizeX,sizeY))
        self.session.summary.sizeWidget(eSize(sizeX,sizeY))
        
        self.updateWidgetXMLs('size', '%s,%s' %(sizeX,sizeY))
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
        if self["Widgetslist"].getCurrent()[1] == "":
            self["WidgetParams"].list = getWidgetParams(self.WidgetsDict[self.currWidgetName]['previewXML'], self.step)
        else:
            self["WidgetParams"].list = [(_('Press OK to enable widget'), LoadPixmap(getPixmapPath('wdg_btn_no_button.png')))]

    def listUP(self):
        if self.currIndex == 0:
            self["Widgetslist"].setIndex(len(self.WidgetsList) -1)
        else:
            self["Widgetslist"].selectPrevious()
        
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
            self.session.summary.showWidget(True)
            self.WidgetsDict[self.currWidgetName]['widgetActiveState'] = ''
        elif self.WidgetsDict[self.currWidgetName]['widgetActiveState'] == '':
            self[self.currWidgetName].hide()
            self.session.summary.showWidget(False)
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
                savedDesigns.append((fileName[:-7],'%s/LCDskin/sharedDesigns/%s' % (PluginPath,fileName)))
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
                
                self.updateWidgetsList(True)      
                self.session.openWithCallback(self.cancelRet,MessageBox, _("Design %s\n ...has been loaded") % ret[0], type = MessageBox.TYPE_INFO, timeout=10)
            except Exception, e:
                printDEBUG("Error occured: %s" % str(e))
                self.session.open(MessageBox, "Error occured: %s" % str(e), type = MessageBox.TYPE_ERROR, timeout=10)
                
    def cancelRet(self, ret = None):
        self.close(self.WidgetsDict)
        
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
            wDict = {}
            for widget in self.WidgetsDict:
                if self.WidgetsDict[widget]['widgetActiveState'] != 'X': #only active widgets
                    wDict[widget] = self.WidgetsDict[widget]
            if len(wDict) > 0:
                try:
                    with open('%s/%s.design' % (self.miniTVdesignsPath, filename), 'w') as f:
                        f.write(json.dumps(wDict, ensure_ascii=False, indent=2))
                        f.close()
                    self.session.open(MessageBox, _("File %s.design\n ...has been written") % filename, type = MessageBox.TYPE_INFO, timeout=10)
                    return
                except Exception, e:
                    self.session.open(MessageBox, "Error occured: %s" % str(e), type = MessageBox.TYPE_ERROR, timeout=10)
                    return
            else:
                self.session.open(MessageBox, _("No active widgets to save"), type = MessageBox.TYPE_INFO, timeout=10)
                return
              
#### WRITE SKINS >>>
    def KeyYellow(self):
        if self.vfdSkinFileName is not None:
            self.session.open(MessageBox, "KeyYellow" +' ' + _("action NOT ready yet"), type = MessageBox.TYPE_INFO, timeout=10)

    def KeyBlue(self):
        self.selectScreen('UserSkin')

    def selectScreen(self, skinType ):
        myList = []
        with open(PluginPath + '/LCDskin/_selection_screens', 'r') as f:
            for line in f:
                myList.append((line.strip(),line.strip()))
        if len(myList) > 1:
            self.session.openWithCallback(boundFunction(self.selectScreenRet, skinType), ChoiceBox, title = _("Save as:"), list = myList)
    
    def selectScreenRet(self, skinType=None , screenName = None):
        if screenName is not None:
            currentTime = time.strftime("%d.%m.%Y - %H:%M:%S")
            if skinType == 'UserSkin':
                self.session.openWithCallback(boundFunction(self.writeSkinFile, skinType, screenName[0]), VirtualKeyBoard, title=(_("Enter filename")), text = '%s %s' % (screenName[0], currentTime))
            else:
                self.writeSkinFile(skinType, screenName[0], self.vfdSkinFileName)
      
    def writeSkinFile(self, skinType=None , screenName = None, filename = None):
        if filename is None:
            self.session.openWithCallback(self.doNothing, MessageBox,_("Filename not selected, skin won't be saved!"),  type = MessageBox.TYPE_INFO, timeout = 10, default = False)
            return
        elif filename[1] != '/':
            if not filename.startswith('skin_'):
                filename = 'skin_' + filename
            if not filename.endswith('.xml'):
                filename += '.xml'
            filename = '%sallScreens/LCD/%s' % (SkinPath, filename)
            if not fileExists('%sallScreens' % (SkinPath)):
                os.mkdir('%sallScreens' % (SkinPath))  
            if not fileExists('%sallScreens/LCD' % (SkinPath)):
                os.mkdir('%sallScreens/LCD' % (SkinPath))  

        screenPart = ""
        #screenPart += '\n<screen name="%s" position="0,0" size="%s,%s" id="%s">\n' % ( screenName, self.LCDwidth, self.LCDheight, self.desktopID )
        screenPart += '\n<screen name="%s" position="0,0" size="%s,%s">\n' % ( screenName, self.LCDwidth, self.LCDheight )
        for widget in self.WidgetsDict:
            if self.WidgetsDict[widget]['widgetActiveState'] == '':
                print "Write %s Widget to SkinFile" % (widget)
                screenPart += self.WidgetsDict[widget]['widgetXML'] + '\n'
        screenPart += '</screen>\n'
        if fileExists(filename):
          with open(filename, 'r') as f:
              skinBase = f.read()
              f.close()
        else:
              skinBase = '<skin>\n</skin>\n'

        if re.search(screenName, skinBase, re.S|re.I):
            pattern = re.compile('<screen name="'+screenName+'" position="0,0" size="480,320" id="1">(.*?)</screen>', re.S|re.I)
            skinFile = re.sub(pattern, screenPart, skinBase)
        else:
            #pattern = re.compile('<screen name="'+screenName+'" position="0,0" size="480,320" id="1">(.*?)</screen>', re.S|re.I)
            skinFile = re.sub('</skin>', screenPart+'\n</skin>', skinBase)
        
        with open(filename, 'w') as f:
            f.write(skinFile)
            f.close()
        
        skin.loadSkin(filename)
        if skinType == 'UserSkin':
            restartbox = self.session.openWithCallback(self.doNothing,MessageBox,_("Skin has been written in .../LCD folder\nActivate it in UserSkin:\n'Skin personalization/UserSkin additional screens'"), MessageBox.TYPE_INFO)
        elif myLCDconfig.value == self.vfdSkinFileName:
            restartbox = self.session.openWithCallback(self.restartGUI,MessageBox,_("GUI needs a restart to apply a new skin\nDo you want to Restart the GUI now?"), MessageBox.TYPE_YESNO)
            restartbox.setTitle(_("Restart GUI now?"))
        else:
            restartbox = self.session.openWithCallback(self.doNothing,MessageBox,_("Skin has been written.\nAcrivate it in Menu/System/"), MessageBox.TYPE_INFO)

    def restartGUI(self, answer):
        if answer is True:
            self.session.open(TryQuitMainloop, 3)

    def doNothing(self, ret = None):
        return
      
    def keyCancel(self):
        self.close()

    def createSummary(self):
         return miniTVskinnerLCDScreen
       
    def previewSkin(self):
        previewSkin = '<screen name="miniTVskinnerPreviewSkin" title="%s" position="center,center" size="%d,%d" backgroundColor="black">\n' % (_('Preview skin'), self.LCDwidth, self.LCDheight)
        for widget in self.WidgetsDict:
            if self.WidgetsDict[widget]['widgetActiveState'] == '':
                previewSkin += self.WidgetsDict[widget]['widgetXML'] + '\n'
        previewSkin += '</screen>\n'
        self.session.openWithCallback(self.doNothing,miniTVskinnerPreviewSkin, previewSkin)
      
################################################################################################################################################################      
class miniTVskinnerLCDScreen(Screen):
    def __init__(self, session, parent):
        Screen.__init__(self, session, parent = parent)
        self.skin = self.parent.skinLCD
        
        #initiate dynamic widgets
        for widget in self.parent.WidgetsList: #(widgetPic, widgetActiveState _(widgetName), widgetName, widgetInitscript, previewXML, widgetXML) #widgetActiveState=X then widget disabled
            printDEBUG('Executing:%s' % self.parent.WidgetsDict[widget[4]]['widgetInitscript'])
            if self.parent.WidgetsDict[widget[4]]['widgetInitscript'] != '':
                try:
                    exec(self.parent.WidgetsDict[widget[4]]['widgetInitscript'])
                except Exception, e:
                    printDEBUG('EXCEPTION running init script for %s: %s' % (widget[4], str(e)))
            if self.parent.WidgetsDict[widget[4]]['widgetActiveState'] != '':
                self[widget[4]].hide()

    def showWidget(self , state):
        if state == True:
            self[self.parent.currWidgetName].show()
        else:
            self[self.parent.currWidgetName].hide()

    def moveWidget(self, newPos):
        self[self.parent.currWidgetName].move(newPos)

    def sizeWidget(self, newSize):
        self[self.parent.currWidgetName].instance.resize(newSize)

    def setFontSize(self, fontData):
        self[self.parent.currWidgetName].instance.setFont(fontData)

    def setFontType(self, fontData):
        self[self.parent.currWidgetName].instance.setFont(fontData)
 
    def changeColor(self, param, color):
        if param == 'foregroundColor':
            self[self.parent.currWidgetName].instance.setForegroundColor(color)
        elif param == 'backgroundColor':
            self[self.parent.currWidgetName].instance.setBackgroundColor(color)
            self[self.parent.currWidgetName].hide()
            self[self.parent.currWidgetName].show()

################################################################################################################################################################
class miniTVskinnerPreviewSkin(Screen):
    def __init__(self, session, previewSkin):
        self.skin = previewSkin
        printDEBUG("!!!!!!!!!! PREVIEW !!!!!!!!!!")
        printDEBUG(self.skin)
        self.session = session
        Screen.__init__(self, session)

        self["actions"]  = ActionMap(["miniTVskinnerActions"], {
            "keyCancel": self.close,
            "keyOK": self.close,
        }, -1)
################################################################################################################################################################
from Components.Button import Button
from Components.config import *
from Components.ConfigList import ConfigListScreen
from Screens.VirtualKeyBoard import VirtualKeyBoard
from Tools.BoundFunction import boundFunction
from Components.FileList import FileList

class miniTVmakerFileBrowser(Screen):
        skin ="""
  <screen name="miniTVmakerFileBrowser" position="center,center" size="870,690" title=" " flags="wfNoBorder" backgroundColor="#20606060">
    <widget name="InfoLine" position="0,0" zPosition="2" size="860,30" valign="center" halign="center" font="Regular;24" transparent="1" />
    <widget name="filelist" position="10,40" size="850,640" itemHeight="35" font="Roboto_HD; 26" scrollbarMode="showOnDemand"/>
  </screen>"""
        def __init__(self, session,currDir,title):
                Screen.__init__(self, session)
                self.title = title
                self.currDir = currDir
                self["filelist"] = FileList(self.currDir, matchingPattern = "(?i)^.*\.(png|jpg)")
                self["FilelistActions"] = ActionMap(["OkCancelActions", "ColorActions"],
                        {
                                "ok": self.ok,
                                "cancel": self.exit
                        })
                self["InfoLine"] = Label(self.currDir)
                self.onLayoutFinish.append(self.layoutFinished)
                
        def layoutFinished(self):
                self.setTitle(self.title)
                
        def tgz(self):
                self.tgzret = os.system("tar zxf \"%s\" -C /" % self.filename)
                
        def ok(self):
                if self["filelist"].canDescent(): # isDir
                        self["filelist"].descent()
                        self["InfoLine"].setText(self["filelist"].getCurrentDirectory())
                else:
                        filename = self["filelist"].getCurrentDirectory() + '/' + self["filelist"].getFilename()
                        self.close(filename)
                        
        def exit(self):
                self.close()
################################################################################################################################################################
class miniTVskinnerWidgetConfig(Screen, ConfigListScreen):
    skin = """
    <screen name="miniTVskinnerWidgetConfig" position="center,center" size="640,500" title="miniTVskinner Widget Config" backgroundColor="#20606060" >

            <widget name="config" position="10,10" size="620,450" zPosition="1" transparent="0" scrollbarMode="showOnDemand" />
            <widget name="key_red" position="0,465" zPosition="2" size="200,35" valign="center" halign="center" font="Regular;22" transparent="1" foregroundColor="red" />
            <widget name="key_green" position="220,465" zPosition="2" size="200,35" valign="center" halign="center" font="Regular;22" transparent="1" foregroundColor="green" />
            <widget name="key_blue" position="440,465" zPosition="2" size="200,35" valign="center" halign="center" font="Regular;22" transparent="1" foregroundColor="#202673ec" />
    </screen>"""
    
    def __init__(self, session, paramsDict = {}, currWidgetName = '' ):
        Screen.__init__(self, session)

        ConfigListScreen.__init__(self, [], session)
        self["actions"] = ActionMap(["SetupActions", "ColorActions"],
            {
                "cancel": self.keyCancel,
                "red": self.keyCancel,
                "green": self.keySave,
                "blue": self.keyBlue,
                "ok": self.keyOK,
            }, -2)

        self["key_green"] = Label(_("Save"))
        self["key_red"] = Label(_("Cancel"))
        self["key_blue"] = Label(_("Show keyboard"))

        self.list=[]
        self.paramsDict = paramsDict
        self.currWidgetName = currWidgetName
        
        #self.list.append(getConfigListEntry(_("Download:"), myConfig.Version)) #debug|public
        
        self.onLayoutFinish.append(self.layoutFinished)

    def layoutFinished(self):
        self.setTitle(_('Widget attributes:'))
        for param in self.paramsDict:
            paramValue = self.paramsDict[param]
            if param == 'name':
                continue
            elif param == 'transparent':
                exec('self.%s = ConfigYesNo(default=%s)' %(param, int(paramValue)))
                exec('self.list.append(getConfigListEntry("%s", self.%s, "%s"))' % (_(param),param,param))
            elif param == 'zPosition':
                exec('self.%s = ConfigSelectionNumber(min= -10, max= 10, stepwidth = 1, default=%s)' %(param, int(paramValue)))
                exec('self.list.append(getConfigListEntry("%s", self.%s, "%s"))' % (_(param),param,param))
            elif param == 'font':
                fontParts = paramValue.split(';')
                exec('self.fontType = ConfigText( default="%s")' % fontParts[0])
                exec('self.list.append(getConfigListEntry("%s", self.fontType, "fontType"))' % _('fontType'))
                
                exec('self.fontSize = ConfigSelectionNumber(min= 5, max= 50, stepwidth = 1, default=%s)' % int(fontParts[1]) )
                exec('self.list.append(getConfigListEntry("%s", self.fontSize, "fontSize"))' % _('fontSize'))
            elif param == 'pixmap':
                exec('self.%s = ConfigDirectory( default = "%s")' %(param,paramValue))
                exec('self.list.append(getConfigListEntry("%s", self.%s, "%s"))' % (_(param),param,param))
            elif param == 'optionsDISABLED' and self.currWidgetName == 'miniTVRunningText':
                if 1: #try:
                    options = paramValue.split(',')
                    if len(options) > 0:
                      for o in options:
                          if '=' in o:
                              opt, optValue = (x.strip() for x in o.split('=', 1))
                          else:
                              opt, optValue = o.strip(), ""
                          print '******************** %s,%s;' % (opt, optValue)
                          if opt == "":
                              continue
                          elif opt in ("wrap", "nowrap"):
                              exec('self.option%s = ConfigSelection(default = "%s", choices = [("wrap", _("wrap")),("nowrap", _("nowrap"))])' %(opt,opt))
                              exec('self.list.append(getConfigListEntry("%s", self.option%s, "option%s"))' % (_('Option %s' % opt), opt,opt))
                          elif opt == "movetype":
                              exec('self.option%s = ConfigSelection(default = "%s", choices = [("none", _("none")),("running", _("running")),("swimming", _("swimming"))])' %(opt,optValue))
                              exec('self.list.append(getConfigListEntry("%s", self.option%s, "option%s"))' % (_('Option %s' % opt), opt,opt))
                          elif opt =="direction" and optValue in ("left","right","top","bottom"):
                              exec('self.option%s = ConfigSelection(default = "%s", choices = [("left", _("left")),("right", _("right")),("top", _("top")),("bottom", _("bottom"))])' %(opt,optValue))
                              exec('self.list.append(getConfigListEntry("%s", self.option%s, "option%s"))' % (_('Option %s' % opt), opt,opt))
                          elif opt == "step":
                              exec('self.option%s = ConfigSelectionNumber(min= 1, max= 10, stepwidth = 1, default=%s)' %(opt,optValue))
                              exec('self.list.append(getConfigListEntry("%s", self.option%s, "option%s"))' % (_('Option %s' % opt), opt,opt))
                          elif opt == "steptime":
                              exec('self.option%s = ConfigSelectionNumber(min= 25, max= 1000, stepwidth = 5, default=%s)' %(opt,optValue)) #in miliseconds
                              exec('self.list.append(getConfigListEntry("%s", self.option%s, "option%s"))' % (_('Option %s' % opt), opt,opt))
                          elif opt == "startdelay":
                              exec('self.option%s = ConfigSelectionNumber(min= 0, max= 2000, stepwidth = 10, default=%s)' %(opt,optValue)) #in miliseconds
                              exec('self.list.append(getConfigListEntry("%s", self.option%s, "option%s"))' % (_('Option %s' % opt), opt,opt))
                          elif opt == "pause":
                              exec('self.option%s = ConfigSelectionNumber(min= 0, max= 1000, stepwidth = 10, default=%s)' %(opt,optValue)) #in miliseconds
                              exec('self.list.append(getConfigListEntry("%s", self.option%s, "option%s"))' % (_('Option %s' % opt), opt,opt))
                          elif opt =="repeat":
                              exec('self.option%s = ConfigSelectionNumber(min= 0, max= 10, stepwidth = 1, default=%s)' %(opt,optValue)) 
                              exec('self.list.append(getConfigListEntry("%s", self.option%s, "option%s"))' % (_('Option %s' % opt), opt,opt))
                          elif opt =="always":
                              exec('self.option%s = ConfigSelectionNumber(min= 0, max= 1, stepwidth = 1, default=%s)' %(opt,optValue)) ## always move text
                              exec('self.list.append(getConfigListEntry("%s", self.option%s, "option%s"))' % (_('Option %s' % opt), opt,opt))
                              pass #self.mAlways = retValue(val, 0, self.mAlways)
                          elif opt =="startpoint":
                              exec('self.option%s = ConfigSelectionNumber(min= 0, max= 800, stepwidth = 10, default=%s)' %(opt,optValue)) ## always move text
                              exec('self.list.append(getConfigListEntry("%s", self.option%s, "option%s"))' % (_('Option %s' % opt), opt,opt))
                              pass #self.mStartPoint = int(val)
                          #elif opt == "oneshot":
                          #    pass #self.mOneShot = retValue(val, 0, self.mOneShot)
                          #elif opt == "pagedelay":
                          #    pass #self.mPageDelay = retValue(val, 0, self.mPageDelay)
                          #elif opt == "pagelength":
                          #    pass #self.mPageLength = retValue(val, 0, self.mPageLength)
                #except Exception:
                #    pass
            else:
                exec('self.%s = ConfigText(fixed_size=False, default = "%s")' %(param,paramValue))
                exec('self.list.append(getConfigListEntry("%s", self.%s, "%s"))' % (_(param),param,param))
        self["config"].list = self.list        
        
    def keyOK(self):
        curIndex = self["config"].getCurrentIndex()
        currItem = self["config"].list[curIndex][1]
        if isinstance(currItem, ConfigDirectory):
            def SetDirPathCallBack(curIndex = None, newPath = None):
                if None != newPath: self["config"].list[curIndex][1].value = newPath
            self.session.openWithCallback(boundFunction(SetDirPathCallBack, curIndex), miniTVmakerFileBrowser, currDir=os.path.dirname(currItem.value), title=_("Select file"))
        elif isinstance(currItem, ConfigText):
            self.keyBlue()

    def keySave(self):
        for x in self["config"].list:
            param = x[2]
            if isinstance(x[1], ConfigYesNo):
                if x[1].value:
                    paramValue = '1'
                else:
                    paramValue = '0'
            else:
                paramValue = str(x[1].value)
            if param in self.paramsDict:
                self.paramsDict[param] = paramValue
            elif param == 'fontType':
                fontParts = self.paramsDict['font'].split(';')
                fontParts[0] = self.paramsDict[param]
                self.paramsDict[param] = ';'.join(fontParts)
            elif param == 'fontSize':
                fontParts = self.paramsDict['font'].split(';')
                fontParts[1] = self.paramsDict[param]
                self.paramsDict[param] = ';'.join(fontParts)
            elif param.startswith('optionDISABLED'):
                pparm = '%s=%s' % (param[6:], paramValue)
                sparm = self.paramsDict['options']
                if pparm in ("wrap", "nowrap"):
                    if 'wrap' in sparm and paramValue != 'wrap':
                        self.paramsDict['options'] = re.sub('wrap', 'nowrap', sparm)
                    #elif :
                    #    self.paramsDict['options'] = re.sub('pparm=[^ ",]*', 'pparm=' + paramValue + ',', sparm)
                else:
                    self.paramsDict['options'] = re.sub('pparm=[^,]*,', 'pparm=' + paramValue + ',', sparm)
              
        self.close(True, self.paramsDict)

    def keyCancel(self):
        self.close(False, {})
        
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
