from __init__ import mygettext as _
from version import Version
import os
# GUI (Screens)
from Components.ActionMap import ActionMap
from Components.config import *
from Components.ConfigList import ConfigListScreen
from Components.Label import Label
#from Components.Sources.StaticText import StaticText
from Screens.ChoiceBox import ChoiceBox
from Screens.Console import Console
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Screens.Setup import SetupSummary

config.plugins.streamlinksrv = ConfigSubsection()
config.plugins.streamlinksrv.checkPackages = NoSave(ConfigNothing())
config.plugins.streamlinksrv.generateBouquet = NoSave(ConfigNothing())
config.plugins.streamlinksrv.modifyBouquet = NoSave(ConfigNothing())

config.plugins.streamlinksrv.enabled = ConfigYesNo(default = False)
config.plugins.streamlinksrv.logLevel = ConfigSelection(default = "info", choices = [("none", _("none")),
                                                                                    ("info", _("info")),
                                                                                    ("warning", _("warning")),
                                                                                    ("error", _("error")),
                                                                                    ("critical", _("critical")),
                                                                                    ("debug", _("debug")),
                                                                                    ("trace", _("trace")),
                                                                              ])
config.plugins.streamlinksrv.logToFile = ConfigEnableDisable(default = False)
config.plugins.streamlinksrv.ClearLogFile = ConfigEnableDisable(default = True)
config.plugins.streamlinksrv.logPath = ConfigSelection(default = "/home/root", choices = [("/home/root", "/home/root"), ("/tmp", "/tmp"), ("/hdd", "/hdd"), ])
config.plugins.streamlinksrv.PortNumber = ConfigSelection(default = "8088", choices = [("8088", "8088"), ("88", "88"), ])
# pilot.wp.pl
config.plugins.streamlinksrv.WPusername = ConfigText()
config.plugins.streamlinksrv.WPpassword = ConfigPassword()
config.plugins.streamlinksrv.WPbouquet = NoSave(ConfigNothing())
config.plugins.streamlinksrv.WPlogin = NoSave(ConfigNothing())
# teleelevidenie
config.plugins.streamlinksrv.TELEusername = ConfigText()
config.plugins.streamlinksrv.TELEpassword = ConfigPassword()
config.plugins.streamlinksrv.TELEbouquet = NoSave(ConfigNothing())
# remote E2
config.plugins.streamlinksrv.remoteE2address = ConfigText(default = "192.168.1.8")
config.plugins.streamlinksrv.remoteE2port = ConfigText(default = "8001")
config.plugins.streamlinksrv.remoteE2username = ConfigText(default = "root")
config.plugins.streamlinksrv.remoteE2password = ConfigPassword(default = "root")
config.plugins.streamlinksrv.remoteE2zap = ConfigEnableDisable(default = True)
config.plugins.streamlinksrv.remoteE2wakeup = ConfigEnableDisable(default = True)
config.plugins.streamlinksrv.remoteE2bouquet = NoSave(ConfigNothing())

if os.path.exists("/tmp/StreamlinkConfig.log"):
    os.remove("/tmp/StreamlinkConfig.log")
 
class StreamlinkConfiguration(Screen, ConfigListScreen):
    from enigma import getDesktop
    if getDesktop(0).size().width() == 1920: #definicja skin-a musi byc tutaj, zeby vti sie nie wywalalo na labelach, inaczje trzeba uzywasc zrodla statictext
        skin = """<screen name="StreamlinkConfiguration" position="center,center" size="1000,700" title="Streamlink configuration">
                            <widget name="config" position="20,20" size="960,600" zPosition="1" scrollbarMode="showOnDemand" />
                            <widget name="key_red"    position="20,630" zPosition="2" size="960,30" foregroundColor="red"   valign="center" halign="left" font="Regular;22" transparent="1" />
                            <widget name="key_green"  position="20,630" zPosition="2" size="960,30" foregroundColor="green"  valign="center" halign="center" font="Regular;22" transparent="1" />
                            <widget name="key_yellow" position="20,630" zPosition="2" size="960,30" foregroundColor="yellow" valign="center" halign="right" font="Regular;22" transparent="1" />
                          </screen>"""
    else:
        skin = """<screen name="StreamlinkConfiguration" position="center,center" size="700,200" title="Streamlink configuration">
                            <widget name="config" position="20,20" size="640,145" zPosition="1" scrollbarMode="showOnDemand" />
                            <widget name="key_red"    position="20,150" zPosition="2" size="660,30" foregroundColor="red" valign="center" halign="left" font="Regular;22" transparent="1" />
                            <widget name="key_green"  position="20,150" zPosition="2" size="660,30" foregroundColor="green" valign="center" halign="center" font="Regular;22" transparent="1" />
                            <widget name="key_yellow" position="20,150" zPosition="2" size="660,30" foregroundColor="yellow" valign="center" halign="right" font="Regular;22" transparent="1" />
                          </screen>"""
    def buildList(self):
        Mlist = []
        # pilot.wp.pl
        #Mlist.append(getConfigListEntry("", NoSave(ConfigNothing()) ))
        Mlist.append(getConfigListEntry('\c00289496' + _("*** %s configuration ***") % 'pilot.wp.pl'))
        Mlist.append(getConfigListEntry(_("Username:"), config.plugins.streamlinksrv.WPusername))
        Mlist.append(getConfigListEntry(_("Password:"), config.plugins.streamlinksrv.WPpassword))
        Mlist.append(getConfigListEntry(_("Check login credentials"), config.plugins.streamlinksrv.WPlogin))
        Mlist.append(getConfigListEntry(_("Press OK to create %s bouquet") % "userbouquet.WPPL.tv", config.plugins.streamlinksrv.WPbouquet))
        Mlist.append(getConfigListEntry(""))
        Mlist.append(getConfigListEntry('\c00289496' + _("*** remote E2 helper ***")))
        Mlist.append(getConfigListEntry(_("IP address:"), config.plugins.streamlinksrv.remoteE2address))
        Mlist.append(getConfigListEntry(_("Streaming port:"), config.plugins.streamlinksrv.remoteE2port))
        Mlist.append(getConfigListEntry(_("Username:"), config.plugins.streamlinksrv.remoteE2username))
        Mlist.append(getConfigListEntry(_("Password:"), config.plugins.streamlinksrv.remoteE2password))
        Mlist.append(getConfigListEntry(_("Wakeup if remote E2 in standby:"), config.plugins.streamlinksrv.remoteE2wakeup))
        Mlist.append(getConfigListEntry(_("Zap before stream workarround:"), config.plugins.streamlinksrv.remoteE2zap))
        Mlist.append(getConfigListEntry(_("Press OK to select and download %s bouquet") % "userbouquet.remoteE2.tv", config.plugins.streamlinksrv.remoteE2bouquet))
        
        Mlist.append(getConfigListEntry(""))
        Mlist.append(getConfigListEntry('\c00289496' + _("*** %s configuration ***") % 'teleelevidenie')) #https://my.teleelevidenie.com/signin
        Mlist.append(getConfigListEntry(_("Username:"), config.plugins.streamlinksrv.TELEusername))
        Mlist.append(getConfigListEntry(_("Password:"), config.plugins.streamlinksrv.TELEpassword))
        Mlist.append(getConfigListEntry(_("Press OK to download %s bouquet") % "enigma2-hls", config.plugins.streamlinksrv.TELEbouquet))
        Mlist.append(getConfigListEntry(""))
        #Mlist.append(getConfigListEntry(""))
        Mlist.append(getConfigListEntry('\c00289496' + _("*** Deamon configuration ***")))
        Mlist.append(getConfigListEntry(_("Enable deamon:"), config.plugins.streamlinksrv.enabled))
        Mlist.append(getConfigListEntry(_("Port number (127.0.0.1:X):"), config.plugins.streamlinksrv.PortNumber))
        Mlist.append(getConfigListEntry(_("Log level:"), config.plugins.streamlinksrv.logLevel))
        Mlist.append(getConfigListEntry(_("Log to file:"), config.plugins.streamlinksrv.logToFile))
        Mlist.append(getConfigListEntry(_("Clear log on each start:"), config.plugins.streamlinksrv.ClearLogFile))
        Mlist.append(getConfigListEntry(_("Save log file in:"), config.plugins.streamlinksrv.logPath))
        #Mlist.append()
        return Mlist

    def __init__(self, session, args=None):
        self.DBGlog('%s' % '__init__')
        Screen.__init__(self, session)
        self.session = session
        ConfigListScreen.__init__(self, self.buildList(), on_change = self.changedEntry)

        # Summary
        self.setup_title = _("Streamlink Configuration" + ' v.' + Version)
        self.onChangedEntry = []

        # Buttons
        self["key_red"] = Label(_("Cancel"))
        self["key_green"] = Label(_("Save"))
        self["key_yellow"] = Label(_("Check status"))

        # Define Actions
        self["actions"] = ActionMap(["StreamlinkConfiguration"],
            {
                "cancel": self.exit,
                "red"   : self.exit,
                "green" : self.save,
                "yellow": self.yellow,
                "save":   self.save,
                "ok":     self.Okbutton,
            }, -2)
        if not self.selectionChanged in self["config"].onSelectionChanged:
            self["config"].onSelectionChanged.append(self.selectionChanged)
        self.onLayoutFinish.append(self.layoutFinished)
        self.doAction = None

    def saveConfig(self):
        for x in self["config"].list:
            if len(x) >= 2:
                x[1].save()
        configfile.save()

    def save(self):
        self.saveConfig()
        if os.path.exists('/var/run/streamlink.pid'):
            os.system('/etc/init.d/streamlinksrv stop')
        if config.plugins.streamlinksrv.enabled.value:
            os.system('/etc/init.d/streamlinksrv start')
        self.close(None)
        
    def doNothing(self, ret = False):
        return
      
    def yellow(self):
        def yellowRet(ret = False):
            if ret:
                mtitle = _('(Re)installing required packages...')
                cmd = '/usr/lib/enigma2/python/Plugins/Extensions/StreamlinkConfig/plugins/installPackets.sh forceReinstall'
            else:
                mtitle = _('Checking state of required packages...')
                cmd = '/usr/lib/enigma2/python/Plugins/Extensions/StreamlinkConfig/plugins/installPackets.sh'
            self.session.openWithCallback(self.doNothing ,Console, title = mtitle, cmdlist = [ cmd ])
        self.session.openWithCallback(yellowRet, MessageBox, _("Do you want to force packets reinstallation?"), MessageBox.TYPE_YESNO, default = False)
        
    def exit(self):
        self.close(None)
        
    def layoutFinished(self):
        if os.path.exists('/usr/lib/enigma2/python/Plugins/Extensions/StreamlinkConfig/1stRun'):
            if os.path.exists('/var/run/streamlink.pid'):
                os.system('/usr/lib/enigma2/python/Plugins/Extensions/StreamlinkConfig/plugins/installPackets.sh &')
            else:
                os.system('/usr/lib/enigma2/python/Plugins/Extensions/StreamlinkConfig/plugins/installPackets.sh forceReinstall &')
            os.remove('/usr/lib/enigma2/python/Plugins/Extensions/StreamlinkConfig/1stRun')
        self.setTitle(self.setup_title)

    def changedEntry(self):
        self.DBGlog('%s' % 'changedEntry()')
        try:
            for x in self.onChangedEntry:
                x()
        except Exception as e:
            self.DBGlog('%s' % str(e))

    def selectionChanged(self):
        self.DBGlog('%s' % 'selectionChanged(%s)' % self["config"].getCurrent()[0])

    def getCurrentEntry(self):
        return self["config"].getCurrent()[0]

    def getCurrentValue(self):
        return str(self["config"].getCurrent()[1].getText())

    def createSummary(self):
        return SetupSummary

    def DBGlog(self, text):
        open("/tmp/StreamlinkConfig.log", "a").write('%s\n' % str(text))
        
    def Okbutton(self):
        self.DBGlog('%s' % 'Okbutton')
        try:
            self.doAction = None
            curIndex = self["config"].getCurrentIndex()
            selectedItem = self["config"].list[curIndex]
            if len(selectedItem) == 2:
                currItem = selectedItem[1]
                currInfo = selectedItem[0]
                if isinstance(currItem, ConfigText):
                    from Screens.VirtualKeyBoard import VirtualKeyBoard
                    self.session.openWithCallback(self.OkbuttonTextChangedConfirmed, VirtualKeyBoard, title=(currInfo), text = currItem.value)
                elif currItem == config.plugins.streamlinksrv.WPbouquet:
                    if config.plugins.streamlinksrv.WPusername.value == '' or config.plugins.streamlinksrv.WPpassword.value == '':
                        self.session.openWithCallback(self.doNothing,MessageBox, _("Username & Password are required!"), MessageBox.TYPE_INFO, timeout = 5)
                        return
                    else:
                        self.doAction = ('wpBouquet.py' , '/etc/enigma2/userbouquet.WPPL.tv', config.plugins.streamlinksrv.WPusername.value, config.plugins.streamlinksrv.WPpassword.value)
                elif currItem == config.plugins.streamlinksrv.WPlogin:
                    if config.plugins.streamlinksrv.WPusername.value == '' or config.plugins.streamlinksrv.WPpassword.value == '':
                        self.session.openWithCallback(self.doNothing,MessageBox, _("Username & Password are required!"), MessageBox.TYPE_INFO, timeout = 5)
                        return
                    else:
                        self.saveConfig()
                        cmd = '/usr/bin/python /usr/lib/enigma2/python/Plugins/Extensions/StreamlinkConfig/plugins/wpBouquet.py checkLogin'
                        self.session.openWithCallback(self.doNothing ,Console, title = _('Credentials verification'), cmdlist = [ cmd ])
                        return
                elif currItem == config.plugins.streamlinksrv.TELEbouquet:
                    if config.plugins.streamlinksrv.TELEusername.value == '' or config.plugins.streamlinksrv.TELEpassword.value == '':
                        self.session.openWithCallback(self.doNothing,MessageBox, _("Username & Password are required!"), MessageBox.TYPE_INFO, timeout = 5)
                        return
                    else:
                        self.doAction = ('teleelevidenieBouquet.py', '/etc/enigma2/teleelevidenie-hls.tv', config.plugins.streamlinksrv.TELEusername.value, config.plugins.streamlinksrv.TELEpassword.value)
                elif currItem == config.plugins.streamlinksrv.remoteE2bouquet:
                    from StreamingChannelConverter import StreamingChannelFromServerScreen
                    session.openWithCallback(self.doNothing, StreamingChannelFromServerScreen) 
                self.DBGlog('%s' % str(self.doAction))
                if not self.doAction is None:
                    bfn = self.doAction[1]
                    self.DBGlog('%s' % bfn)
                    if os.path.exists(bfn):
                        self.cmdTitle = _('Updating %s...') % bfn
                        self.session.openWithCallback(self.OkbuttonConfirmed, MessageBox, _("Do you want to update '%s' file?") % bfn, MessageBox.TYPE_YESNO, default = False)
                    else:
                        self.cmdTitle = _('Creating %s...') % bfn
                        self.session.openWithCallback(self.OkbuttonConfirmed, MessageBox, _("Do you want to create '%s' file?") % bfn, MessageBox.TYPE_YESNO, default = True)
        except Exception as e:
            self.DBGlog('%s' % str(e))
    
    def OkbuttonTextChangedConfirmed(self, ret ):
        curIndex = self["config"].getCurrentIndex()
        self["config"].list[curIndex][1].value = ret

    def OkbuttonConfirmed(self, ret = False):
        if ret:
            if os.path.exists("/usr/lib/enigma2/python/Plugins/SystemPlugins/ServiceApp/serviceapp.so"):
                choicesList = [("gstreamer (root 4097)","4097"),("ServiceApp gstreamer (root 5001)","5001"), ("ServiceApp ffmpeg (root 5002)","5002"),("Hardware (root 1)","1")]
            else:
                choicesList = [("gstreamer (root 4097)","4097"),("Hardware (root 1)","1"),(_("ServiceApp not installed!"), None)]
            self.session.openWithCallback(self.SelectedFramework, ChoiceBox, title = _("Select Multiframework"), list = choicesList)

    def SelectedFramework(self, ret):
        if not ret or ret == "None":
            ret = (None,'4097')
        cmd = '/usr/bin/python /usr/lib/enigma2/python/Plugins/Extensions/StreamlinkConfig/plugins/%s %s %s %s %s %s' % (self.doAction[0], self.doAction[1], self.doAction[2], self.doAction[3],
                                                                                                                         config.plugins.streamlinksrv.PortNumber.value, ret[1]
                                                                                                                         )
        self.DBGlog('%s' % cmd)
        self.session.openWithCallback(self.reloadBouquets ,Console, title = self.cmdTitle, cmdlist = [ cmd ])
        #status = os.system(cmd)
        #self.DBGlog('%s' % status)
        #if status == 0:
        #    self.session.openWithCallback(self.doNothing,MessageBox, _("Action done properly"), MessageBox.TYPE_INFO, timeout = 5)
        #else:
        #    self.session.openWithCallback(self.doNothing,MessageBox, _("Error running script, check log."), MessageBox.TYPE_INFO, timeout = 5)
    def reloadBouquets(self, ret = False):
        from enigma import eDVBDB
        eDVBDB.getInstance().reloadBouquets()
        self.session.openWithCallback(self.doNothing,MessageBox, _("Bouquets has been reloaded"), MessageBox.TYPE_INFO, timeout = 5)
        
