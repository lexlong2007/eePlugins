from __init__ import mygettext as _
import os
# GUI (Screens)
from Components.ConfigList import ConfigListScreen
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen

# GUI (Summary)
from Screens.Setup import SetupSummary

# GUI (Components)
from Components.ActionMap import ActionMap
from Components.Sources.StaticText import StaticText

# Configuration
from Components.config import *

config.plugins.streamlinksrv = ConfigSubsection()
config.plugins.streamlinksrv.generateBouquet = NoSave(ConfigNothing())
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
config.plugins.streamlinksrv.WPpassword = ConfigText()
config.plugins.streamlinksrv.WPbouquet = NoSave(ConfigNothing())
# teleelevidenie
config.plugins.streamlinksrv.TELEusername = ConfigText()
config.plugins.streamlinksrv.TELEpassword = ConfigText()
config.plugins.streamlinksrv.TELEbouquet = NoSave(ConfigNothing())

if os.path.exists("/tmp/StreamlinkConfig.log"):
    os.remove("/tmp/StreamlinkConfig.log")
 
class StreamlinkConfiguration(Screen, ConfigListScreen):
    def buildList(self):
        Mlist = []
        # pilot.wp.pl
        Mlist.append(getConfigListEntry('\c00289496' + _("*** %s configuration ***") % 'pilot.wp.pl'))
        Mlist.append(getConfigListEntry(_("Username:"), config.plugins.streamlinksrv.WPusername))
        Mlist.append(getConfigListEntry(_("Password:"), config.plugins.streamlinksrv.WPpassword))
        Mlist.append(getConfigListEntry(_("Press OK to create %s bouquet") % "userbouquet.WPPL.tv", config.plugins.streamlinksrv.WPbouquet))
        Mlist.append(getConfigListEntry(""))
        Mlist.append(getConfigListEntry('\c00289496' + _("*** %s configuration ***") % 'teleelevidenie')) #https://my.teleelevidenie.com/signin
        Mlist.append(getConfigListEntry(_("Username:"), config.plugins.streamlinksrv.TELEusername))
        Mlist.append(getConfigListEntry(_("Password:"), config.plugins.streamlinksrv.TELEpassword))
        Mlist.append(getConfigListEntry(_("Press OK to download %s bouquet") % "enigma2-hls", config.plugins.streamlinksrv.TELEbouquet))
        Mlist.append(getConfigListEntry(""))
        Mlist.append(getConfigListEntry('\c00289496' + _("*** Deamon configuration ***")))
        Mlist.append(getConfigListEntry(_("Enable deamon:"), config.plugins.streamlinksrv.enabled))
        Mlist.append(getConfigListEntry(_("Port number (127.0.0.1:X):"), config.plugins.streamlinksrv.PortNumber))
        Mlist.append(getConfigListEntry(_("Log level:"), config.plugins.streamlinksrv.logLevel))
        Mlist.append(getConfigListEntry(_("Log to file:"), config.plugins.streamlinksrv.logToFile))
        Mlist.append(getConfigListEntry(_("Clear log on each start:"), config.plugins.streamlinksrv.ClearLogFile))
        Mlist.append(getConfigListEntry(_("Save log file in:"), config.plugins.streamlinksrv.logPath))
        #Mlist.append()
        return Mlist

    def __init__(self, session):
        self.DBGlog('%s' % '__init__')
        from enigma import getDesktop
        if getDesktop(0).size().width() == 1920:
            self.skin = """<screen name="StreamlinkConfiguration" position="center,center" size="900,400" title="Streamlink configuration">
                            <eLabel position="5,0" size="690,2" backgroundColor="#aaaaaa" />
                            <widget name="config" position="20,20" size="860,330" zPosition="1" scrollbarMode="showOnDemand" />
                            <widget name="key_red"    position="20,360" zPosition="2" size="860,30" foregroundColor="red"   valign="center" halign="left" font="Regular;22" transparent="1" />
                            <widget name="key_green"  position="20,360" zPosition="2" size="860,30" foregroundColor="green"  valign="center" halign="center" font="Regular;22" transparent="1" />
                            <!--widget name="key_yellow" position="20,360" zPosition="2" size="860,30" foregroundColor="yellow" valign="center" halign="right" font="Regular;22" transparent="1" /-->
                          </screen>"""
        else:
            self.skin = """<screen name="StreamlinkConfiguration" position="center,center" size="700,200" title="Streamlink configuration">
                            <eLabel position="5,0" size="690,2" backgroundColor="#aaaaaa" />
                            <widget name="config" position="20,20" size="640,145" zPosition="1" scrollbarMode="showOnDemand" />
                            <widget name="key_red"    position="20,150" zPosition="2" size="660,30" foregroundColor="red" valign="center" halign="left" font="Regular;22" transparent="1" />
                            <widget name="key_green"  position="20,150" zPosition="2" size="660,30" foregroundColor="green" valign="center" halign="center" font="Regular;22" transparent="1" />
                            <!--widget name="key_yellow" position="20,150" zPosition="2" size="660,30" foregroundColor="yellow" valign="center" halign="right" font="Regular;22" transparent="1" /-->
                          </screen>"""
        Screen.__init__(self, session)

        # Summary
        self.setup_title = _("Streamlink Configuration" + ' NIE SKONCZONE!!!')
        self.onChangedEntry = []

        # Buttons
        self["key_red"] = StaticText(_("Cancel"))
        self["key_green"] = StaticText(_("Save"))

        # Define Actions
        self["actions"] = ActionMap(["StreamlinkConfiguration"],
            {
                "cancel": self.exit,
                "red"   : self.exit,
                "green" : self.save,
                "save":   self.save,
                "ok":     self.Okbutton,
            }, -2)
        ConfigListScreen.__init__(self, self.buildList(), session, on_change = self.changedEntry)
        if not self.selectionChanged in self["config"].onSelectionChanged:
            self["config"].onSelectionChanged.append(self.selectionChanged)
        self.onLayoutFinish.append(self.layoutFinished)
        self.doAction = None

    def save(self):
        for x in self["config"].list:
            if len(x) >= 2:
                x[1].save()
        configfile.save()
        if os.path.exists('/var/run/streamlink.pid'):
            os.system('/etc/init.d/streamlinksrv stop')
        if config.plugins.streamlinksrv.enabled.value:
            os.system('/etc/init.d/streamlinksrv start')
        self.close(None)
        
    def exit(self):
        self.close(None)
        
    def layoutFinished(self):
        os.system('/usr/lib/enigma2/python/Plugins/Extensions/StreamlinkConfig/plugins/installPackets.sh &')
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
                    self.doAction = ('wpConfig.py' , '/etc/enigma2/userbouquet.WPPL.tv', config.plugins.streamlinksrv.WPusername.value, config.plugins.streamlinksrv.WPpassword.value)
                elif currItem == config.plugins.streamlinksrv.TELEbouquet:
                    self.doAction = ('teleelevidenieConfig.py', '/etc/enigma2/teleelevidenie-hls.tv', config.plugins.streamlinksrv.TELEusername.value, config.plugins.streamlinksrv.TELEpassword.value)
                self.DBGlog('%s' % str(self.doAction))
                if not self.doAction is None:
                    bfn = self.doAction[1]
                    self.DBGlog('%s' % bfn)
                    if os.path.exists(bfn):
                        self.session.openWithCallback(self.OkbuttonConfirmed,MessageBox, _("Do you want to update '%s' file?") % bfn, MessageBox.TYPE_YESNO, default = False)
                    else:
                        self.session.openWithCallback(self.OkbuttonConfirmed,MessageBox, _("Do you want to create '%s' file?") % bfn, MessageBox.TYPE_YESNO, default = True)
        except Exception as e:
            self.DBGlog('%s' % str(e))
    
    def OkbuttonTextChangedConfirmed(self, ret ):
        curIndex = self["config"].getCurrentIndex()
        self["config"].list[curIndex][1].value = ret

    def OkbuttonConfirmed(self, ret = False):
        if ret == True:
            cmd = '/usr/bin/python /usr/lib/enigma2/python/Plugins/Extensions/StreamlinkConfig/plugins/%s %s %s %s %s' % (self.doAction[0], self.doAction[1], self.doAction[2], self.doAction[3], config.plugins.streamlinksrv.PortNumber.value)
            self.DBGlog('%s' % cmd)
            status = os.system(cmd)
            self.DBGlog('%s' % status)
            if status == 0:
                  self.session.openWithCallback(self.OkbuttonEnd,MessageBox, _("Action done properly"))
            else:
                  self.session.openWithCallback(self.OkbuttonEnd,MessageBox, _("Error running script, check log."))
              
    def OkbuttonEnd(self, ret = False):
        pass
