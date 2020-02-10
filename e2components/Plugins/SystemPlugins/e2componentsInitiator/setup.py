#######################################################################
#
#  Coded by j00zek (c)2020
#
#  Uszanuj moja prace i nie kasuj/zmieniaj informacji kto jest autorem renderera
#  Please respect my work and don't delete/change name of the renderer author
#
#  Nie zgadzam sie na wykorzystywanie tego skryptu w projektach platnych jak np. Graterlia!!!
#
#  Prosze NIE dystrybuowac tego skryptu w formie archwum zip, czy tar.gz
#  Zgadzam sie jedynie na dystrybucje z repozytorium opkg
#
################################################################################
from . import mygettext as _
from Components.config import *
from enigma import getDesktop
from Screens.Screen import Screen
from Components.ConfigList import ConfigListScreen
from Components.ActionMap import ActionMap
from os import path as os_path
######################################################################################
#config.plugins.j00zekCC.FakeEntry = NoSave(ConfigNothing())
######################################################################################
def buildList():
    Mlist = []
    #
    #self.list.append(getConfigListEntry(_(" "), config.plugins.j00zekCC.FakeEntry))
    Mlist.append(getConfigListEntry('\c00289496' + _("---Dynamic Font Size---")))
    Mlist.append(getConfigListEntry(_("Service Name minimum font size"), config.plugins.j00zekCC.j00zekLabelSN ))
    Mlist.append(getConfigListEntry(_("Event Name minimum font size"), config.plugins.j00zekCC.j00zekLabelEN ))
    #
    Mlist.append(getConfigListEntry(""))
    Mlist.append(getConfigListEntry('\c00289496' + _("---User paths---")))
    Mlist.append(getConfigListEntry(_("Picons animations user path:"), config.plugins.j00zekCC.PiconAnimation_UserPath ))
    Mlist.append(getConfigListEntry(_("Alternate user icons path:"), config.plugins.j00zekCC.AlternateUserIconsPath))
    #
    Mlist.append(getConfigListEntry(""))
    Mlist.append(getConfigListEntry('\c00289496' + _("---Scrolling text---")))
    Mlist.append(getConfigListEntry(_("Ammend Font size"), config.plugins.j00zekCC.rtFontSize))
    Mlist.append(getConfigListEntry(_("Type"), config.plugins.j00zekCC.rtType))
    Mlist.append(getConfigListEntry(_("Initial delay"), config.plugins.j00zekCC.rtStartDelay))
    Mlist.append(getConfigListEntry(_("Speed"), config.plugins.j00zekCC.rtStepTimeout))
    Mlist.append(getConfigListEntry(_("Repeats"), config.plugins.j00zekCC.rtRepeat))
    #
    Mlist.append(getConfigListEntry(""))
    Mlist.append(getConfigListEntry('\c00289496' + _("---Event description (EventName)---")))
    Mlist.append(getConfigListEntry(_("Information presented"),  config.plugins.j00zekCC.enDescrType ))
    Mlist.append(getConfigListEntry(_("Show TMDB rating at the begining (when available)"),  config.plugins.j00zekCC.enTMDBratingFirst ))
    #
    Mlist.append(getConfigListEntry(""))
    Mlist.append(getConfigListEntry('\c00289496' + _("---Frontend information---")))
    Mlist.append(getConfigListEntry(_("Show when FE is:"),  config.plugins.j00zekCC.feInfoType ))
    Mlist.append(getConfigListEntry(_("Title:"),  config.plugins.j00zekCC.feInfoTitle ))
    Mlist.append(getConfigListEntry(_("Service info:"),  config.plugins.j00zekCC.snINFOtype ))
    #
    Mlist.append(getConfigListEntry(""))
    Mlist.append(getConfigListEntry('\c00289496' + _("---SoftCam information---")))
    Mlist.append(getConfigListEntry(_("Show:"),  config.plugins.j00zekCC.ciFormat ))
        
    if getDesktop(1).size().width() < 320:
        Mlist.append(getConfigListEntry(""))
        Mlist.append(getConfigListEntry('\c00289496' + _("---VFD settings---")))
        Mlist.append(getConfigListEntry(_("Infobar summary"),  config.plugins.j00zekCC.snVFDtype ))
        try: #use system config when possible
            Mlist.append(getConfigListEntry(_("Scrolling delay (rollerCharVFD)"),  config.lcd.scroll_delay ))
            Mlist.append(getConfigListEntry(_("Scrolling speed (rollerCharVFD)"),  config.lcd.scroll_speed ))
        except Exception: #or own, when not
            Mlist.append(getConfigListEntry(_("Scrolling delay (rollerCharVFD)"),  config.plugins.j00zekCC.scroll_delay ))
            Mlist.append(getConfigListEntry(_("Scrolling speed (rollerCharVFD)"),  config.plugins.j00zekCC.scroll_speed ))
        Mlist.append(getConfigListEntry(_("Standby clock"),  config.plugins.j00zekCC.clockVFDstdby ))
        Mlist.append(getConfigListEntry(_("Standby clock position"),  config.plugins.j00zekCC.clockVFDpos ))
    #self.list.append(getConfigListEntry(_("XXXX"), XXXX ))
    return Mlist
  
######################################################################################
class e2ComponentsConfig(Screen, ConfigListScreen):
    def buildList(self):
        self["config"].list = buildList()

    def __init__(self, session):
        from enigma import getDesktop
        if getDesktop(0).size().width() == 1920:
            self.skin = """<screen name="e2ComponentsConfig" position="center,center" size="900,400" title="e2components configuration">
                            <eLabel position="5,0" size="690,2" backgroundColor="#aaaaaa" />
                            <widget name="config" position="20,20" size="860,330" zPosition="1" scrollbarMode="showOnDemand" />
                            <widget name="key_red"    position="20,360" zPosition="2" size="860,30" foregroundColor="red"   valign="center" halign="left" font="Regular;22" transparent="1" />
                            <widget name="key_green"  position="20,360" zPosition="2" size="860,30" foregroundColor="green"  valign="center" halign="center" font="Regular;22" transparent="1" />
                            <widget name="key_yellow" position="20,360" zPosition="2" size="860,30" foregroundColor="yellow" valign="center" halign="right" font="Regular;22" transparent="1" />
                          </screen>"""
        else:
            self.skin = """<screen name="e2ComponentsConfig" position="center,center" size="700,200" title="e2components configuration">
                            <eLabel position="5,0" size="690,2" backgroundColor="#aaaaaa" />
                            <widget name="config" position="20,20" size="640,145" zPosition="1" scrollbarMode="showOnDemand" />
                            <widget name="key_red"    position="20,150" zPosition="2" size="660,30" foregroundColor="red" valign="center" halign="left" font="Regular;22" transparent="1" />
                            <widget name="key_green"  position="20,150" zPosition="2" size="660,30" foregroundColor="green" valign="center" halign="center" font="Regular;22" transparent="1" />
                            <widget name="key_yellow" position="20,150" zPosition="2" size="660,30" foregroundColor="yellow" valign="center" halign="right" font="Regular;22" transparent="1" />
                          </screen>"""
        Screen.__init__(self, session)
        self["key_red"] = Label(_("Exit"))
        self["key_green"] = Label(_("Save"))
        self["key_yellow"] = Label(_("Set Default value"))
        self["actions"] = ActionMap(["OkCancelActions", "ColorActions"],
            {
                "cancel": self.close,
                "ok": self.selectFolder,
                "red": self.close,
                "green": self.ok,
                "yellow": self.yellowButton,
            }, -2)
        ConfigListScreen.__init__(self, [], session)
        self.title = _("j00zek e2components configuration")
        self.buildList()

    def selectFolder(self):
        curIndex = self["config"].getCurrentIndex()
        currItem = self["config"].list[curIndex][1]
        currInfo = self["config"].list[curIndex][0]
        if isinstance(currItem, ConfigDirectory):
            if os_path.isdir(currItem.value):
                self.session.openWithCallback(boundFunction(self.selectFolderCallBack, curIndex), DirectorySelectorWidget, currDir=currItem.value, title=currInfo)
            else:
                self.session.openWithCallback(boundFunction(self.selectFolderCallBack, curIndex), DirectorySelectorWidget, currDir='/', title=currInfo)

    def selectFolderCallBack(self, curIndex, newPath):
        if None != newPath:
            self["config"].list[curIndex][1].value = newPath
            self.buildList()
            
    def yellowButton(self):
        curIndex = self["config"].getCurrentIndex()
        if isinstance(self["config"].list[curIndex][1], ConfigDirectory):
            self["config"].list[curIndex][1].value = _('not set')
        else:
            self["config"].list[curIndex][1].value = '0'
        self.buildList()

    def ok(self):
        from Screens.MessageBox import MessageBox
        self.session.openWithCallback(self.updateConfig, MessageBox, _("Are you sure you want to save this configuration?"))

    def updateConfig(self, ret = False):
        if ret == True:
            for x in self["config"].list:
                if len(x) >= 2:
                    x[1].save()
            configfile.save()
            self.close()

######################################################################################
from Components.Label import Label 
from Components.Sources.StaticText import StaticText
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
        from Components.FileList import FileList
        
        Screen.__init__(self, session)
        # for the skin: first try MediaPlayerDirectoryBrowser, then FileBrowser, this allows individual skinning
        #self.skinName = ["MediaPlayerDirectoryBrowser", "FileBrowser" ]
        self["key_red"]    = Label(_("Cancel"))
        #self["key_yellow"] = Label(_("Refresh"))
        self["key_blue"]   = Label(_(" "))
        self["key_green"]  = Label(_("Select"))
        self["curr_dir"]   = Label(_(" "))
        self.filelist      = FileList(directory=currDir, matchingPattern="", showFiles=False)
        self["filelist"]   = self.filelist
        self["FilelistActions"] = ActionMap(["SetupActions", "ColorActions"],
            {
                "green" : self.use,
                "red"   : self.exit,
                "yellow": self.yellowButton,
                "blue"  : self.blueButton,
                "ok"    : self.ok,
                "cancel": self.exit
            })
        self.title = title
        self.onLayoutFinish.append(self.layoutFinished)
        self.onClose.append(self.__onClose)

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

    def yellowButton(self):
        self["filelist"].refresh()

    def blueButton(self):
        return
