# -*- coding: utf-8 -*-
# @j00zek 2020

from __init__ import *
from __init__ import translate as _ 

from Components.ActionMap import ActionMap
from Components.config import *
from Components.MenuList import MenuList
from Components.ScrollLabel import ScrollLabel
from Components.Sources.StaticText import StaticText

from enigma import eConsoleAppContainer, getDesktop

from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
#
from os import system as os_system, popen as os_popen, path as os_path

config.plugins.IPTVplayersManager = ConfigSubsection()
config.plugins.IPTVplayersManager.InstallPath = ConfigText(default = PluginsExtensionsPath, fixed_size = False)
config.plugins.IPTVplayersManager.installAsFork = ConfigYesNo(default = True)

def substring_2_translate(text):
    to_translate = text.split('_(', 2)
    text = to_translate[1]
    to_translate = text.split(')', 2)
    text = to_translate[0]
    return text

def __(txt):
    if txt.find('_(') == -1:
        txt = _(txt)
    else:
        index = 0
        while txt.find('_(') != -1:
            tmptxt = substring_2_translate(txt)
            translated_tmptxt = _(tmptxt)
            txt = txt.replace('_(' + tmptxt + ')', translated_tmptxt)
            index += 1
            if index == 10: #max 10 translations per one txt
                break

    return txt

class translatedConsole(Screen):
    if getDesktop(0).size().width() == 1920: 
        skin = """
        <screen position="center,center" size="1250,450" title="Instalacja..." >
            <widget name="text" position="0,0" size="1250,450" font="Console;24" />
        </screen>"""
    else:
        skin = """
        <screen position="center,center" size="650,450" title="Instalacja..." >
            <widget name="text" position="0,0" size="650,450" font="Console;14" />
        </screen>"""
        
    def __init__(self, session, title = "translatedConsole", cmdlist = None, finishedCallback = None, closeOnSuccess = False):
        Screen.__init__(self, session)

        self.finishedCallback = finishedCallback
        self.closeOnSuccess = closeOnSuccess
        self.errorOcurred = False
        self.doReboot = False

        self["text"] = ScrollLabel("")
        self["actions"] = ActionMap(["WizardActions", "DirectionActions"], 
        {
            "ok": self.cancel,
            "back": self.cancel,
            "up": self["text"].pageUp,
            "down": self["text"].pageDown
        }, -1)
        
        self.cmdlist = cmdlist
        self.newtitle = title.replace('\t',' ').replace('  ',' ').strip()
        
        self.onShown.append(self.updateTitle)
        
        self.container = eConsoleAppContainer()
        self.run = 0
        self.container.appClosed.append(self.runFinished)
        self.container.dataAvail.append(self.dataAvail)
        self.onLayoutFinish.append(self.startRun) # dont start before gui is finished

    def updateTitle(self):
        self.setTitle(self.newtitle)

    def startRun(self):
        self["text"].setText("" + "\n\n")
        print "TranslatedConsole: executing in run", self.run, " the command:", self.cmdlist[self.run]
        if self.container.execute(self.cmdlist[self.run]): #start of container application failed...
            self.runFinished(-1) # so we must call runFinished manual

    def runFinished(self, retval):
        if retval:
            self.errorOcurred = True
        self.run += 1
        if self.run != len(self.cmdlist):
            if self.container.execute(self.cmdlist[self.run]): #start of container application failed...
                self.runFinished(-1) # so we must call runFinished manual
        else:
            self["text"].lastPage()
            if self.finishedCallback is not None:
                self.finishedCallback()
            if not self.errorOcurred and self.closeOnSuccess:
                self.cancel()

    def cancel(self):
        from Screens.MessageBox import MessageBox
          
        def rebootQuestionAnswered(ret):
            if ret:
                from enigma import quitMainloop
                quitMainloop(3)
            try: self.close()
            except: pass
            return
            
        if self.run == len(self.cmdlist):
            self.container.appClosed.remove(self.runFinished)
            self.container.dataAvail.remove(self.dataAvail)
            if self.doReboot:
                self.session.openWithCallback(rebootQuestionAnswered, MessageBox,_("Restart GUI now?"),  type = MessageBox.TYPE_YESNO, timeout = 10, default = False)
            else:
                self.close()

    def dataAvail(self, str):
        if str.find("[doReboot]") > -1: 
            self.doReboot = True
            str = str.replace("[doReboot]",'')
        self["text"].setText(self["text"].getText() + __(str))
        self["text"].lastPage()

######################################################################################

class j00zekIPTVmgr(Screen,):
    def __init__(self, session, MenuFolder = "" , MenuFile = '', MenuTitle = 'j00zekIPTVmgr'):
        
        self.myList = []
        self.list = []
        self.myPath = MenuFolder
        self.MenuFile = MenuFile
        self.OptionScript = ""
        self.PIC = ""
        picHeight = 0
        self.MenuTitle = MenuTitle

        if getDesktop(0).size().width() == 1920: 
            skin  = """
    <screen name="j00zekIPTVmgr" position="center,center" size="820,540" title="j00zekIPTVmgr" >
        <widget source="InstallPath"     render="Label" position="10,0"   size="800,60" font="Regular;24" foregroundColor="#6DABBF" valign="center" halign="center" noWrap="0" />
        <widget source="installAsFork"   render="Label" position="10,80"  size="800,30" font="Regular;24" foregroundColor="#6DABBF" valign="center" halign="center" noWrap="0" />
        <widget name="list" position="10,130" font="Regular;22" size="800,400" scrollbarMode="showOnDemand" />
        <widget source="key_red"    render="Label" position="10,500" foregroundColor="red"    size="800,30" zPosition="1" font="Regular;24" valign="center" halign="left" transparent="1" />
        <widget source="key_green"  render="Label" position="10,500" foregroundColor="green"  size="800,30" zPosition="1" font="Regular;24" valign="center" halign="center" transparent="1" />
        <widget source="key_yellow" render="Label" position="10,500" foregroundColor="yellow" size="800,30" zPosition="1" font="Regular;24" valign="center" halign="right" transparent="1" />
    </screen>"""
        else:
            skin  = """
    <screen name="j00zekIPTVmgr" position="center,center" size="620,540" title="j00zekIPTVmgr" >
        <widget source="InstallPath"     render="Label" position="10,0"  size="600,40" font="Regular;18" foregroundColor="#6DABBF" valign="center" halign="center" noWrap="0" />
        <widget source="installAsFork"   render="Label" position="10,60" size="600,20" font="Regular;18" foregroundColor="#6DABBF" valign="center" halign="center" noWrap="0" />
        <widget name="list" position="5,100" font="Regular;20" size="600,430" scrollbarMode="showOnDemand" />
        <widget source="key_red"    render="Label" position="10,500" foregroundColor="red"    size="600,30" zPosition="1" font="Regular;20" valign="center" halign="left" transparent="1" />
        <widget source="key_green"  render="Label" position="10,500" foregroundColor="green"  size="600,30" zPosition="1" font="Regular;20" valign="center" halign="center" transparent="1" />
        <widget source="key_yellow" render="Label" position="10,500" foregroundColor="yellow" size="600,30" zPosition="1" font="Regular;20" valign="center" halign="right" transparent="1" />
    </screen>"""

        self.skin = skin
        self.session = session
        Screen.__init__(self, session)

        self["list"] = MenuList(self.list)
        
        self["actions"] = ActionMap(["OkCancelActions", "ColorActions"],
            {"ok": self.run,
            "cancel": self.close,
            "red": self.redButton,
            "green": self.greenButton,
            "yellow": self.yellowButton,
            }, -1)

        self.visible = True
        self["key_red"] = StaticText(_("Installation type"))
        self["key_green"] = StaticText(_("(Re)Install"))
        self["key_yellow"] = StaticText(_("Change path"))
        self["InstallPath"] = StaticText("")
        self["installAsFork"] = StaticText("")
        self.onLayoutFinish.append(self.updateData) # dont start before gui is finished
        
    def updateData(self):
        self.setTitle(self.MenuTitle)
        self.endrun() #reloadsList
    
    def yellowButton(self):
        self.selectFolder()
      
    def redButton(self):
        config.plugins.IPTVplayersManager.installAsFork.value = not config.plugins.IPTVplayersManager.installAsFork.value
        config.plugins.IPTVplayersManager.installAsFork.save()
        self.endrun() #reloadsList
        
    def greenButton(self):
        self.run()
  
    def YESNO(self, decyzja):
        if decyzja is False:
            return
        os_system("%s"  %  self.OptionScript)

    def run(self):
        selecteditem = self["list"].getCurrent()
        if selecteditem is not None:
            for opcja in self.myList:
                if opcja[0] == selecteditem:
                    ClearMemory()
                    self.OptionScript = opcja[2]
                    self.OptionScript = self.OptionScript.replace('[InstallPath]', config.plugins.IPTVplayersManager.InstallPath.value)
                    self.OptionScript = self.OptionScript.replace('[installAsFork]', str(config.plugins.IPTVplayersManager.installAsFork.value))
                    
                    if opcja[1] == "CONSOLE":
                        self.session.openWithCallback(self.endrun ,translatedConsole, title = "%s" % selecteditem, cmdlist = [ ('chmod 775 %s 2>/dev/null' %  self.OptionScript),('%s' %  self.OptionScript) ])
                    if opcja[1] == "YESNO":
                        self.session.openWithCallback(self.YESNO ,MessageBox,_("Execute %s?") % selecteditem, MessageBox.TYPE_YESNO)
                    if opcja[1] == "SILENT":
                        os_system("%s"  %  self.OptionScript)
                        self.endrun()
                    elif opcja[1] == "RUN":
                        os_system("%s"  %  self.OptionScript)
                        self.session.openWithCallback(self.endrun,MessageBox,_("%s executed!") %( selecteditem ), MessageBox.TYPE_INFO, timeout=5)
                    elif opcja[1] == "MSG":
                        msgline = ""
                        popenret = os_popen( self.OptionScript)
                        for readline in popenret.readlines():
                            msgline += readline
                        self.session.openWithCallback(self.endrun,MessageBox, "%s" %( msgline ), MessageBox.TYPE_INFO, timeout=15)
                    elif opcja[1] == "PYEXEC":
                        try:
                            exec(self.OptionScript)
                            self.endrun()
                        except Exception:
                            pass
                    elif opcja[1] == "DEF":
                        try:
                            exec(self.OptionScript, globals, locals)
                            self.endrun()
                        except Exception as e:
                            self.session.openWithCallback(self.endrun,MessageBox, "Executing'%s' EXCEPTION: %s" % (self.OptionScript,str(e)), MessageBox.TYPE_INFO, timeout=15)
                            
    def endrun(self, ret =0):
        self["InstallPath"].setText( _("Install path: %s") % config.plugins.IPTVplayersManager.InstallPath.value)
        if config.plugins.IPTVplayersManager.installAsFork.value:
            self["installAsFork"].setText( _("Each fork will be installed in own directory"))
        else:
            self["installAsFork"].setText( _("Each fork will be installed in IPTVplayer directory"))
        self.clearLIST()
        self.reloadLIST()

    def SkryptOpcjiWithFullPath(self, txt):
        if txt.startswith('/'):
            return txt
        else:
            return ('%s/%s') %(self.myPath,txt)
            
    def clearLIST(self):
        while len(self.list) > 0: #czyścimy listę w ten dziwny sposób, aby GUI działało, bo nie zmienimy obiektów ;)
            del self.myList[-1]
            del self.list[-1]
        self["list"].hide()
        self["list"].show()

    def reloadLIST(self):
        if os_path.exists(self.MenuFile) is True:
            self["list"].hide()
            with open (self.MenuFile, "r") as myMenufile:
                for MenuItem in myMenufile:
                    MenuItem = MenuItem.rstrip('\n') 
                    if not MenuItem or MenuItem[0] == '#': #omijamy komentarze
                        continue
                    #interesują nas tylko pozycje menu
                    if MenuItem[0:5] == "ITEM|":
                        #teraz bierzemy pod uwage tylko te linie co mają odpowiednią ilość |
                        #print MenuItem
                        skladniki = MenuItem.replace("ITEM|","").split('|')
                        if len(skladniki) == 3:
                            (NazwaOpcji, TypOpcji, SkryptOpcji) = skladniki
                            if NazwaOpcji != "":
                                NazwaOpcji = __(NazwaOpcji)
                                #NazwaOpcji = NazwaOpcji.replace(NazwaOpcji[:3],_(NazwaOpcji[:3]))
                                
                            if TypOpcji not in ('PYEXEC','DEF'):
                                SkryptOpcji = self.SkryptOpcjiWithFullPath(SkryptOpcji)
                            self.myList.append( (NazwaOpcji, TypOpcji, SkryptOpcji) )
                            self.list.append( NazwaOpcji )
                myMenufile.close()
            myIdx = self["list"].getSelectionIndex()
            if myIdx > len(self.list) -1:
                self["list"].moveToIndex(len(self.list) -1)
            self["list"].show()

    def selectFolder(self):
        def SetDirPathCallBack(newPath = None):
            if None != newPath:
                config.plugins.IPTVplayersManager.InstallPath.value = newPath
                config.plugins.IPTVplayersManager.InstallPath.save()
            self.endrun()
        self.session.openWithCallback(SetDirPathCallBack, DirectorySelectorWidget, currDir=config.plugins.IPTVplayersManager.InstallPath.value, title=_("Select forks installation folder"))
######################################################################################
from Components.FileList import FileList
from Components.Label import Label 
from Components.Sources.StaticText import StaticText
#from Screens.HelpMenu import HelpableScreen
from Screens.VirtualKeyBoard import VirtualKeyBoard
from Tools.BoundFunction import boundFunction
class DirectorySelectorWidget(Screen):
    skin = """
    <screen name="DirectorySelectorWidget" position="center,center" size="620,440" title="">
            <widget name="key_red"      position="10,10"  zPosition="2"  size="600,35" valign="center"  halign="left"   font="Regular;22" transparent="1" foregroundColor="red" />
            <widget name="key_blue"     position="10,10"  zPosition="2"  size="600,35" valign="center"  halign="center" font="Regular;22" transparent="1" foregroundColor="blue" />
            <widget name="key_green"    position="10,10"  zPosition="2"  size="600,35" valign="center"  halign="right"  font="Regular;22" transparent="1" foregroundColor="green" />
            <widget name="key_yellow"   position="10,10"  zPosition="2"  size="600,35" valign="center"  halign="right"  font="Regular;22" transparent="1" foregroundColor="green" />
            <widget name="curr_dir"     position="10,50"  zPosition="2"  size="600,35" valign="center"  halign="left"   font="Regular;18" transparent="1" foregroundColor="white" />
            <widget name="filelist"     position="10,85"  zPosition="1"  size="580,335" transparent="1" scrollbarMode="showOnDemand" />
    </screen>"""
    def __init__(self, session, currDir, title="Select directory"):
        print("DirectorySelectorWidget.__init__ -------------------------------")
        Screen.__init__(self, session)
        # for the skin: first try MediaPlayerDirectoryBrowser, then FileBrowser, this allows individual skinning
        #self.skinName = ["MediaPlayerDirectoryBrowser", "FileBrowser" ]
        self["key_red"]    = Label(_("Cancel"))
        #self["key_yellow"] = Label(_("Refresh"))
        self["key_blue"]   = Label(_("New directory"))
        self["key_green"]  = Label(_("Select"))
        self["curr_dir"]   = Label(_(" "))
        self.filelist      = FileList(directory=currDir, matchingPattern="", showFiles=False)
        self["filelist"]   = self.filelist
        self["FilelistActions"] = ActionMap(["SetupActions", "ColorActions"],
            {
                "green" : self.use,
                "red"   : self.exit,
                "yellow": self.refresh,
                "blue"  : self.newDir,
                "ok"    : self.ok,
                "cancel": self.exit
            })
        self.title = title
        self.onLayoutFinish.append(self.layoutFinished)
        self.onClose.append(self.__onClose)

    def mkdir(newdir):
        """ Wrapper for the os.mkdir function
            returns status instead of raising exception
        """
        try:
            os_mkdir(newdir)
            sts = True
            msg = _('Directory "%s" has been created.') % newdir
        except:
            sts = False
            msg = _('Error creating directory "%s".') % newdir
            printExc()
        return sts,msg
    
    def __del__(self):
        print("DirectorySelectorWidget.__del__ -------------------------------")

    def __onClose(self):
        print("DirectorySelectorWidget.__onClose -----------------------------")
        self.onClose.remove(self.__onClose)
        self.onLayoutFinish.remove(self.layoutFinished)

    def layoutFinished(self):
        print("DirectorySelectorWidget.layoutFinished -------------------------------")
        self.setTitle(_(self.title))
        self.currDirChanged()

    def currDirChanged(self):
        self["curr_dir"].setText(_(self.getCurrentDirectory()))
        
    def getCurrentDirectory(self):
        currDir = self["filelist"].getCurrentDirectory()
        if currDir and os_path.isdir( currDir ):
            return currDir
        else:
            return "/"

    def use(self):
        self.close( self.getCurrentDirectory() )

    def exit(self):
        self.close(None)

    def ok(self):
        if self.filelist.canDescent():
            self.filelist.descent()
        self.currDirChanged()

    def refresh(self):
        self["filelist"].refresh()

    def newDir(self):
        currDir = self["filelist"].getCurrentDirectory()
        if currDir and os_path.isdir( currDir ):
            self.session.openWithCallback(boundFunction(self.enterPatternCallBack, currDir), VirtualKeyBoard, title = (_("Enter name")), text = "")

    def IsValidFileName(name, NAME_MAX=255):
        prohibited_characters = ['/', "\000", '\\', ':', '*', '<', '>', '|', '"']
        if isinstance(name, basestring) and (1 <= len(name) <= NAME_MAX):
            for it in name:
                if it in prohibited_characters:
                    return False
            return True
        return False
    
    def enterPatternCallBack(self, currDir, newDirName=None):
        if None != currDir and newDirName != None:
            sts = False
            if self.IsValidFileName(newDirName):
                sts,msg = self.mkdir(os_path.join(currDir, newDirName))
            else:
                msg = _("Incorrect directory name.")
            if sts:
                self.refresh()
            else:
                self.session.open(MessageBox, msg, type = MessageBox.TYPE_INFO, timeout=5)