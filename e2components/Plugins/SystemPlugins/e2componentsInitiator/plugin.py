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
from Components.config import *
from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen 
from Components.ConfigList import ConfigListScreen
from Components.ActionMap import ActionMap 
from os import path as os_path
######################################################################################
def sessionstart(session, **kwargs):
    try:
        if reason == 0:
            #from Components.Sources.mySource import mySource
            #session.screen['mySource'] = mySource()
            print "e2components config initiated"
    except Exception, e:
        print "Exception: %s" % str(e)

def Plugins(**kwargs):
    return [PluginDescriptor(where=[PluginDescriptor.WHERE_SESSIONSTART], fnc=sessionstart)]
######################################################################################
MinFontChoices = [ ("OFF", _("Defined in skin")) , ("0.75", _("3/4 of defined font")) , ("0,67", _("2/3 of defined font")) , ("0,5", _("1/2 of defined font")) ]
######################################################################################

config.plugins.j00zekCC = ConfigSubsection()
config.plugins.j00zekCC.FakeEntry = NoSave(ConfigNothing()) 

config.plugins.j00zekCC.PiconAnimation_UserPath = ConfigDirectory(default = _('default'))  
config.plugins.j00zekCC.j00zekFEicon_UserPath = ConfigDirectory(default = _('default'))
config.plugins.j00zekCC.j00zekVRicon_UserPath = ConfigDirectory(default = _('default'))
#j00zekLabel
config.plugins.j00zekCC.MinFontSize = ConfigSelection(default = "OFF", choices = MinFontChoices )
config.plugins.j00zekCC.InfoBarMinFontSize = ConfigSelection(default = "OFF", choices = MinFontChoices )
config.plugins.j00zekCC.CHListMinFontSize = ConfigSelection(default = "OFF", choices = MinFontChoices )
config.plugins.j00zekCC.LcdMinFontSize = ConfigSelection(default = "OFF", choices = MinFontChoices )
#runningText
config.plugins.j00zekCC.rtType = ConfigSelection(default = "OFF", choices =  [ ("OFF", _("Defined in skin")), ("0", _("NONE")), ("1", _("RUNNING")), ("2", _("SWIMMING")), ("3", _("AUTO"))])
config.plugins.j00zekCC.rtDirection = ConfigSelection(default = "OFF", choices =   [ ("OFF", _("Defined in skin")), ("0", _("LEFT")), ("1", _("RIGHT")), ("2", _("TOP")), ("3", _("BOTTOM")) ])
config.plugins.j00zekCC.rtInitialDelay = ConfigSelection(default = "OFF", choices =   [ ("OFF", _("Defined in skin")), ("1", _("1")), ("2", _("2")), ("3", _("3")) ])
config.plugins.j00zekCC.rtSpeed = ConfigSelection(default = "OFF", choices =   [ ("OFF", _("Defined in skin")), ("1", _("1")), ("2", _("2")), ("3", _("3")) ])
#EventName
config.plugins.j00zekCC.enDescrType = ConfigSelection(default = "OFF", choices =   [ ("OFF", _("Defined in skin")), ("1", _("SHORT_DESCRIPTION")), ("2", _("EXTENDED_DESCRIPTION")), ("3", _("FULL_DESCRIPTION")) ])
#ConfigYesNo(default = False) #ConfigText(default = _("none")) #("", _(""))
######################################################################################
class e2ComponentsConfig(Screen, ConfigListScreen):
    def buildList(self):
        self.list = []
        #
        self.list.append(getConfigListEntry(_("---User paths---"), config.plugins.j00zekCC.FakeEntry))
        self.list.append(getConfigListEntry(_("\tPicons animations user path:"), config.plugins.j00zekCC.PiconAnimation_UserPath ))
        self.list.append(getConfigListEntry(_("FEicons user path:"), config.plugins.j00zekCC.j00zekFEicon_UserPath))
        self.list.append(getConfigListEntry(_("VRicons user path:"), config.plugins.j00zekCC.j00zekVRicon_UserPath ))
        #
        self.list.append(getConfigListEntry(_(" "), config.plugins.j00zekCC.FakeEntry))
        self.list.append(getConfigListEntry(_("---Dynamic Font Size (j00zekLabel)---"), config.plugins.j00zekCC.FakeEntry))
        self.list.append(getConfigListEntry(_("Standard minimum font size"), config.plugins.j00zekCC.MinFontSize ))
        self.list.append(getConfigListEntry(_("Minimum font size on Infobar"), config.plugins.j00zekCC.InfoBarMinFontSize ))
        self.list.append(getConfigListEntry(_("Minimum font size on Channels list"), config.plugins.j00zekCC.CHListMinFontSize ))
        self.list.append(getConfigListEntry(_("Minimum font size on LCD"), config.plugins.j00zekCC.LcdMinFontSize ))
        #
        self.list.append(getConfigListEntry(_(" "), config.plugins.j00zekCC.FakeEntry))
        self.list.append(getConfigListEntry(_("---Scrolling text (RunningText)---"), config.plugins.j00zekCC.FakeEntry))
        self.list.append(getConfigListEntry(_("Type"), config.plugins.j00zekCC.rtType))
        self.list.append(getConfigListEntry(_("Direction"), config.plugins.j00zekCC.rtDirection))
        self.list.append(getConfigListEntry(_("Initial delay"), config.plugins.j00zekCC.rtInitialDelay))
        self.list.append(getConfigListEntry(_("Speed"), config.plugins.j00zekCC.rtSpeed))
        #
        self.list.append(getConfigListEntry(_(" "), config.plugins.j00zekCC.FakeEntry))
        self.list.append(getConfigListEntry(_("---Event description (EventName)---"), config.plugins.j00zekCC.FakeEntry))
        self.list.append(getConfigListEntry(_("Information presented"),  config.plugins.j00zekCC.enDescrType ))
        
        #self.list.append(getConfigListEntry(_("XXXX"), XXXX ))
        self["config"].list = self.list

    def __init__(self, session):
        from enigma import getDesktop
        if getDesktop(0).size().width() == 1920:
            self.skin = """<screen name="ConfigEdit" position="center,center" size="900,400" title="e2components configuration">
                            <eLabel position="5,0" size="690,2" backgroundColor="#aaaaaa" />
                            <widget name="config" position="20,20" size="860,345" zPosition="1" scrollbarMode="showOnDemand" />
                            <widget name="key_red"    position="20,350" zPosition="2" size="860,30" foregroundColor="red"   valign="center" halign="left" font="Regular;22" transparent="1" />
                            <widget name="key_green"  position="20,350" zPosition="2" size="860,30" foregroundColor="green"  valign="center" halign="center" font="Regular;22" transparent="1" />
                            <widget name="key_yellow" position="20,350" zPosition="2" size="860,30" foregroundColor="yellow" valign="center" halign="right" font="Regular;22" transparent="1" />
                          </screen>"""
        else:
            self.skin = """<screen name="ConfigEdit" position="center,center" size="700,200" title="e2components configuration">
                            <eLabel position="5,0" size="690,2" backgroundColor="#aaaaaa" />
                            <widget name="config" position="20,20" size="660,145" zPosition="1" scrollbarMode="showOnDemand" />
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
        self.title = _("e2components configuration")
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
            self["config"].list[curIndex][1].value = _('default')
        self.buildList()

    def ok(self):
        self.session.openWithCallback(self.updateConfig, MessageBox, _("Are you sure you want to save this configuration?"))

    def updateConfig(self, ret = False):
        if ret == True:
            for x in self["config"].list:
                x[1].save()
            configfile.save()
            self.close()

######################################################################################
from Components.FileList import FileList
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
