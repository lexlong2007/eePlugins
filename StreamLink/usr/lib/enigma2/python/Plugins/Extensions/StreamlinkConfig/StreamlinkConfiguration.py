from __init__ import mygettext as _
import os
# GUI (Screens)
from Screens.Screen import Screen
from Components.ConfigList import ConfigListScreen

# GUI (Summary)
from Screens.Setup import SetupSummary

# GUI (Components)
from Components.ActionMap import ActionMap
from Components.Sources.StaticText import StaticText

# Configuration
from Components.config import *

config.plugins.streamlinksrv = ConfigSubsection()
config.plugins.streamlinksrv.generateBouquet = NoSave(ConfigNothing())
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

class StreamlinkConfiguration(Screen, ConfigListScreen):
    def buildList(self):
        Mlist = []
        # pilot.wp.pl
        Mlist.append(getConfigListEntry('\c00289496' + _("*** %s configuration ***") % 'pilot.wp.pl'))
        Mlist.append(getConfigListEntry(_("Username:"), config.plugins.streamlinksrv.WPusername))
        Mlist.append(getConfigListEntry(_("Password:"), config.plugins.streamlinksrv.WPpassword))
        Mlist.append(getConfigListEntry(_("Press OK to create ") + "userbouquet.WPPL.tv", config.plugins.streamlinksrv.generateBouquet))
        Mlist.append(getConfigListEntry(""))
        Mlist.append(getConfigListEntry('\c00289496' + _("*** Deamon configuration ***")))
        Mlist.append(getConfigListEntry(_("Port number (127.0.0.1:X):"), config.plugins.streamlinksrv.PortNumber))
        Mlist.append(getConfigListEntry(_("Log level:"), config.plugins.streamlinksrv.logLevel))
        Mlist.append(getConfigListEntry(_("Log to file:"), config.plugins.streamlinksrv.logToFile))
        Mlist.append(getConfigListEntry(_("Clear log on each start:"), config.plugins.streamlinksrv.ClearLogFile))
        Mlist.append(getConfigListEntry(_("Save log file in:"), config.plugins.streamlinksrv.logPath))
        #Mlist.append()
        return Mlist

    def __init__(self, session):
        Screen.__init__(self, session)
        self.skinName = [ "StreamlinkConfiguration", "StartupToStandbyConfiguration", "Setup" ]

        # Summary
        self.setup_title = _("Streamlink Configuration" + ' NIE SKONCZONE!!!')
        self.onChangedEntry = []

        # Buttons
        self["key_red"] = StaticText(_("Cancel"))
        self["key_green"] = StaticText(_("OK"))

        # Define Actions
        self["actions"] = ActionMap(["SetupActions", "ColorActions"],
            {
                "cancel": self.exit,
                "red"   : self.exit,
                "green" : self.save,
                "save":   self.save,
                "ok":     self.Okbutton,
            }
        )
        ConfigListScreen.__init__(self, [], session, on_change = self.changed)
        self["config"].list = self.buildList()
        # Trigger change
        self.changed()
        self.onLayoutFinish.append(self.layoutFinished)

    def save(self):
        for x in self["config"].list:
            if len(x) >= 2:
                x[1].save()
        configfile.save()
        self.close(None)
        
    def exit(self):
        self.close(None)
        
    def layoutFinished(self):
        self.setTitle(self.setup_title)

    def changed(self):
        for x in self.onChangedEntry:
            x()

    def getCurrentEntry(self):
        return self["config"].getCurrent()[0]

    def getCurrentValue(self):
        return str(self["config"].getCurrent()[1].getText())

    def createSummary(self):
        return SetupSummary

    def Okbutton(self):
        open("/tmp/streamlink.txt", "w").write('%s\n' % 'Okbutton')
        try:
            if self["config"].getCurrent()[1] == config.plugins.streamlinksrv.generateBouquet:
                open("/tmp/streamlink.txt", "a").write('%s\n' % str(e))
                for bouquet in ('userbouquet.WPPL.tv',):
                    open("/tmp/streamlink.txt", "a").write('bouquet="%s"\n' % bouquet)
                    open("/tmp/streamlink.txt", "a").write('self["config"].getCurrent()[0]="%s"\n' % self["config"].getCurrent()[0])
                    if bouquet in self["config"].getCurrent()[0]:
                        if os.path.exists('/etc/enigma2/%s' % bouquet):
                            self.session.openWithCallback(self.OkbuttonConfirmed,MessageBox, _("Do you want to update '%s' file?") % bouquet, MessageBox.TYPE_YESNO, default = False)
                        else:
                            self.session.openWithCallback(self.OkbuttonConfirmed,MessageBox, _("Do you want to create '%s' file?") % bouquet, MessageBox.TYPE_YESNO, default = True)
                        break
        except Exception as e:
            open("/tmp/streamlink.txt", "a").write('%s\n' % str(e))
            print str(e)
    
    def OkbuttonConfirmed(self, ret = False):
        if ret == True:
            pass
