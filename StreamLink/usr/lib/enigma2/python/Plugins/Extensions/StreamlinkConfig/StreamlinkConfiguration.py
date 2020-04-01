from __init__ import mygettext as _
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
config.plugins.streamlinksrv.logLevel = ConfigSelection(default = "info", choices = [("none", _("none")),
                                                                                    ("info", _("info")),
                                                                                    ("warning", _("warning")),
                                                                                    ("error", _("error")),
                                                                                    ("critical", _("critical")),
                                                                                    ("debug", _("debug")),
                                                                                    ("trace", _("trace")),
                                                                              ])
config.plugins.streamlinksrv.logToFile = ConfigEnableDisable(default = False)
config.plugins.streamlinksrv.logPath = ConfigSelection(default = "/home/root", choices = [("/home/root", "/home/root"), ("/tmp", "/tmp"), ("/hdd", "/hdd"), ])
config.plugins.streamlinksrv.PortNumber = ConfigSelection(default = "8088", choices = [("8088", "8088"), ("88", "88"), ])

class StreamlinkConfiguration(Screen, ConfigListScreen):
    def buildList(self):
        Mlist = []
        Mlist.append(getConfigListEntry('\c00289496' + _("*** %s configuration ***" % 'pilot.wp.pl')))
        Mlist.append(getConfigListEntry(""))
        Mlist.append(getConfigListEntry('\c00289496' + _("*** Deamon configuration ***")))
        Mlist.append(getConfigListEntry(_("Port number (127.0.0.1:X):"), config.plugins.streamlinksrv.PortNumber))
        Mlist.append(getConfigListEntry(_("Log level:"), config.plugins.streamlinksrv.logLevel))
        Mlist.append(getConfigListEntry(_("Log to file:"), config.plugins.streamlinksrv.logToFile))
        Mlist.append(getConfigListEntry(_("Save log file in:"), config.plugins.streamlinksrv.logPath))
        #Mlist.append()
        return Mlist

    def __init__(self, session):
        Screen.__init__(self, session)
        self.skinName = [ "StreamlinkConfiguration", "StartupToStandbyConfiguration", "Setup" ]

        # Summary
        self.setup_title = _("Streamlink Configuration")
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

