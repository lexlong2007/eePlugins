#by Taapat taapat@gmail.com mod @j00zek

from Components.ActionMap import ActionMap
from Components.config import *
from Components.Console import Console
from Components.ConfigList import ConfigListScreen
from Components.Label import Label
from Components.Sources.List import List
from Components.ScrollLabel import ScrollLabel
from Plugins.Plugin import PluginDescriptor
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Tools.Directories import resolveFilename, SCOPE_PLUGINS, pathExists
from Tools.LoadPixmap import LoadPixmap

from enigma import eTimer
from os import path as os_path, mkdir as os_mkdir, remove, listdir as os_listdir

import threading

from Components.Language import language
import gettext
from os import environ
    
def localeInit():
    lang = language.getLanguage()[:2]
    environ["LANGUAGE"] = lang
    gettext.bindtextdomain("plugin-AlternativeSoftCamManager", \
        resolveFilename(SCOPE_PLUGINS, 'Extensions/AlternativeSoftCamManager/locale'))

def _(txt):
    t = gettext.dgettext("plugin-AlternativeSoftCamManager", txt)
    if t == txt:
            t = gettext.gettext(txt)
            print "Lack of translation for '%s'" % t
    return t

localeInit()
language.addCallback(localeInit)

config.plugins.AltSoftcam = ConfigSubsection()
config.plugins.AltSoftcam.enabled = ConfigYesNo(default = False)
config.plugins.AltSoftcam.OsCamonly = ConfigYesNo(default = True)
if open('/proc/cpuinfo', 'r').read().lower().find('armv7') > -1:
    config.plugins.AltSoftcam.actcam = ConfigText(default = "oscam-svn11534-arm-ssl-libusb")
elif open('/proc/cpuinfo', 'r').read().lower().find('mips') > -1:
    config.plugins.AltSoftcam.actcam = ConfigText(default = "oscam-svn11534-mipsel-ssl100")
else:
    config.plugins.AltSoftcam.actcam = ConfigText(default = _("none"))
config.plugins.AltSoftcam.camdir = ConfigDirectory(default = "/usr/lib/enigma2/python/Plugins/Extensions/AlternativeSoftCamManager/CAMbin")
config.plugins.AltSoftcam.camconfig = ConfigDirectory(default = "/usr/lib/enigma2/python/Plugins/Extensions/AlternativeSoftCamManager/CAMconfig")
AltSoftcamConfigError = False
if not os_path.isdir(config.plugins.AltSoftcam.camconfig.value):
    config.plugins.AltSoftcam.camconfig.value = _("none")
    AltSoftcamConfigError = True
if not os_path.isdir(config.plugins.AltSoftcam.camdir.value):
    config.plugins.AltSoftcam.camdir.value = _("none")
    AltSoftcamConfigError = True

def getcamcmd(cam):
    if "oscam" in cam.lower():
        return config.plugins.AltSoftcam.camdir.value + "/" + cam + " -c " + config.plugins.AltSoftcam.camconfig.value + "/"
    elif "softcam" in cam.lower():
        return config.plugins.AltSoftcam.camdir.value + "/" + cam + " -c " + config.plugins.AltSoftcam.camconfig.value + "/"
    elif "smartcard-reader" in cam.lower():
        return config.plugins.AltSoftcam.camdir.value + "/" + cam + " -c " + config.plugins.AltSoftcam.camconfig.value + "/"
    elif "wicard" in cam.lower():
        return config.plugins.AltSoftcam.camdir.value + "/" + cam + " -d -c " + config.plugins.AltSoftcam.camconfig.value + "/wicardd.conf"
    elif "camd3" in cam.lower():
        return config.plugins.AltSoftcam.camdir.value + "/" + cam + " " + config.plugins.AltSoftcam.camconfig.value + "/camd3.config"
    elif "mbox" in cam.lower():
        return config.plugins.AltSoftcam.camdir.value + "/" + cam + " " + config.plugins.AltSoftcam.camconfig.value + "/mbox.cfg"
    elif "mpcs" in cam.lower():
        return config.plugins.AltSoftcam.camdir.value + "/" + cam + " -c " + config.plugins.AltSoftcam.camconfig.value
    elif "newcs" in cam.lower():
        return config.plugins.AltSoftcam.camdir.value + "/" + cam + " -C " + config.plugins.AltSoftcam.camconfig.value + "/newcs.conf"
    elif "vizcam" in cam.lower():
        return config.plugins.AltSoftcam.camdir.value + "/" + cam + " -b -c " + config.plugins.AltSoftcam.camconfig.value + "/"
    elif "rucam" in cam.lower():
        return config.plugins.AltSoftcam.camdir.value + "/" + cam + " -b"
    else:
        return config.plugins.AltSoftcam.camdir.value + "/" + cam

def main(session, **kwargs):
    session.open(AltCamManager)

def StartCam(reason, **kwargs):
    global AltSoftcamConfigError
    if not AltSoftcamConfigError and config.plugins.AltSoftcam.actcam.value != "none" and config.plugins.AltSoftcam.enabled.value == True:
        if reason == 0: # Enigma start
            if not isCamRunning(config.plugins.AltSoftcam.actcam.value):
                StartCamThread(getcamcmd(config.plugins.AltSoftcam.actcam.value), config.plugins.AltSoftcam.actcam.value).start()
        elif reason == 1: # Enigma stop
            try:
                Console().ePopen("killall -9 %s" % config.plugins.AltSoftcam.actcam.value)
                print "[Alternative SoftCam Manager] stopping ", config.plugins.AltSoftcam.actcam.value
            except Exception: pass

def Plugins(**kwargs):
    return [
      PluginDescriptor(name = _("Alternative SoftCam Manager"), description = _("Start, stop, restart SoftCams, change settings."),
        where = [ PluginDescriptor.WHERE_PLUGINMENU, PluginDescriptor.WHERE_EXTENSIONSMENU ], icon = "images/softcam.png", fnc = main),
      PluginDescriptor(where = PluginDescriptor.WHERE_AUTOSTART, needsRestart = True, fnc = StartCam)
      ]

def isCamRunning(cam):
    status = False
    try:
        pids = [pid for pid in os_listdir('/proc') if pid.isdigit()]
        for pid in pids:
            cmdFile = os_path.join('/proc', pid, 'cmdline')
            if os_path.exists(cmdFile):
                with open(cmdFile, "r") as f:
                    fc = f.read()
                    f.close()
                if fc.find('oscam') > 0:
                    status = True
                    break
    except Exception:
        pass
    return status

######################################################################################
class StartCamThread(threading.Thread):
    def __init__(self, cmd, actcam):
        ''' Constructor. '''
        threading.Thread.__init__(self)
        self.name = 'StartCamThread'
        self.cmd = cmd
        self.actcam = actcam

    def run(self):
        from time import sleep
        sleep(1)
        try: 
            with open("/proc/sys/vm/drop_caches", "w") as f: f.write("1\n")
        except Exception:
            pass
        loop = 1
        try:
            while (loop < 6):
                Console().ePopen(self.cmd)
                sleep(0.5)
                if isCamRunning(self.actcam):
                    print "[Alternative SoftCam Manager] started: %s at %d try." % (self.actcam,loop)
                    break
                loop += 1
        except Exception, e:
            print "[Alternative SoftCam Manager] exception strating softcam: ", str(e)
######################################################################################
class AltCamManager(Screen):
    skin = """
<screen position="center,center" size="830,370" title="SoftCam manager">
  <eLabel position="5,0" size="820,2" backgroundColor="#aaaaaa" />
  <widget source="list" render="Listbox" position="10,15" size="540,300" scrollbarMode="showOnDemand">
    <convert type="TemplatedMultiContent">
        {"template": [
            MultiContentEntryPixmapAlphaTest(pos = (5, 5), size = (51, 40), png = 1), 
            MultiContentEntryText(pos = (65, 10), size = (475, 40), font=0, flags = RT_HALIGN_LEFT, text = 0), 
            MultiContentEntryText(pos = (5, 25), size = (51, 16), font=1, flags = RT_HALIGN_CENTER, text = 2), 
                ],
    "fonts": [gFont("Regular", 26),gFont("Regular", 12)],
    "itemHeight": 50
    }
    </convert>
  </widget>
  <eLabel halign="center" position="590,10" size="210,35" font="Regular;20" text="Ecm info" transparent="1" />
  <widget name="status" position="560,50" size="320,300" font="Regular;16" halign="left" noWrap="1" />
  <eLabel position="12,358" size="148,2" backgroundColor="#00ff2525" />
  <eLabel position="231,358" size="148,2" backgroundColor="#00389416" />
  <eLabel position="449,358" size="148,2" backgroundColor="#00baa329" />
  <eLabel position="670,358" size="148,2" backgroundColor="#006565ff" />
  <widget name="key_red" position="12,328" zPosition="2" size="148,30" valign="center" halign="center" font="Regular;22" transparent="1" />
  <widget name="key_green" position="231,328" zPosition="2" size="148,30" valign="center" halign="center" font="Regular;22" transparent="1" />
  <widget name="key_yellow" position="449,328" zPosition="2" size="148,30" valign="center" halign="center" font="Regular;22" transparent="1" />
  <widget name="key_blue" position="670,328" zPosition="2" size="148,30" valign="center" halign="center" font="Regular;22" transparent="1" />
</screen>"""

    def __init__(self, session):
        Screen.__init__(self, session)
        self.Console = Console()
        self["key_red"] = Label(_("Stop"))
        self["key_green"] = Label(_("Start"))
        self["key_yellow"] = Label(_("Restart"))
        self["key_blue"] = Label(_("Setup"))
        self["actions"] = ActionMap(["OkCancelActions", "ColorActions"],
            {
                "cancel": self.cancel,
                "ok": self.ok,
                "green": self.start,
                "red": self.stop,
                "yellow": self.restart,
                "blue": self.setup
            }, -1)
        self["status"] = ScrollLabel()
        self["list"] = List([])
        self.actcam = config.plugins.AltSoftcam.actcam.value
        self.camstartcmd = ""
        self.CreateInfo()
        self.Timer = eTimer()
        self.Timer.callback.append(self.listecminfo)
        self.Timer.start(1000*4, False)
        self.title = _("SoftCam Manager")

    def CreateInfo(self):
        global AltSoftcamConfigError
        if not AltSoftcamConfigError:
            self.StartCreateCamlist()
            self.listecminfo()

    def listecminfo(self):
        listecm = ""
        try:
            ecmfiles = open("/tmp/ecm.info", "r")
            for line in ecmfiles:
                if line[32:]:
                    linebreak = line[23:].find(' ') + 23
                    listecm += line[0:linebreak]
                    listecm += "\n" + line[linebreak + 1:]
                else:
                    listecm += line
            self["status"].setText(listecm)
            ecmfiles.close()
        except:
            self["status"].setText(_("No /tmp/ecm.info file!!!"))

    def StartCreateCamlist(self):
        cmd = "ls %s" % config.plugins.AltSoftcam.camdir.value
        self.Console.ePopen(cmd, self.CamListStart)

    def CamListStart(self, result, retval, extra_args):
        if not result.startswith('ls: '):
            self.softcamlist = result
            self.Console.ePopen("chmod 755 %s" % config.plugins.AltSoftcam.camdir.value)
            self.Console.ePopen("pidof %s" % self.actcam, self.CamActive)

    def CamActive(self, result, retval, extra_args):
        if result.strip():
            self.CreateCamList()
        else:
            for line in self.softcamlist.splitlines():
                if config.plugins.AltSoftcam.OsCamonly.value == True and line.lower().find("oscam") < 0:
                    continue
                if line != self.actcam:
                    self.Console.ePopen("pidof %s" % line, self.CamActiveFromList, line)
            self.Console.ePopen("echo 1", self.CamActiveFromList, "none")

    def CamActiveFromList(self, result, retval, extra_args):
        if result.strip():
            self.actcam = extra_args
            self.CreateCamList()

    def CreateCamList(self):
        self.list = []
        try:
            test = self.actcam
        except:
            self.actcam = "none"
            
        if self.actcam != "none" and pathExists(resolveFilename(SCOPE_PLUGINS, "Extensions/AlternativeSoftCamManager/images/actcam.png")):
            softpng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/AlternativeSoftCamManager/images/actcam.png"))
            try:
                self.list.append((self.actcam, softpng, self.checkcam(self.actcam)))
            except:
                print "[ASM] error loading self.actcam"

        if pathExists(resolveFilename(SCOPE_PLUGINS, "Extensions/AlternativeSoftCamManager/images/defcam.png")):
            softpng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/AlternativeSoftCamManager/images/defcam.png"))
            if len(self.softcamlist.splitlines()) > 0:
                for line in self.softcamlist.splitlines():
                    try:
                        if config.plugins.AltSoftcam.OsCamonly.value == True and line.lower().find("oscam") < 0:
                            continue
                        if line != self.actcam:
                            self.list.append((line, softpng, self.checkcam(line)))
                    except:
                        print "[ASM] error loading %s" % line
                        pass
        self["list"].setList(self.list)

    def checkcam (self, cam):
        if "oscam" in cam.lower():
            return "Oscam"
        elif "softcam" in cam.lower():
            return "SoftCAM"
        elif "smartcard-reader" in cam.lower():
            return "smartcard-reader"
        elif "mgcamd" in cam.lower():
            return "Mgcamd"
        elif "wicard" in cam.lower():
            return "Wicard"
        elif "camd3" in cam.lower():
            return "Camd3"
        elif "mcas" in cam.lower():
            return "Mcas"
        elif "cccam" in cam.lower():
            return "CCcam"
        elif "gbox" in cam.lower():
            return "Gbox"
        elif "ufs910camd" in cam.lower():
            return "Ufs910"
        elif "incubuscamd" in cam.lower():
            return "Incubus"
        elif "mpcs" in cam.lower():
            return "Mpcs"
        elif "mbox" in cam.lower():
            return "Mbox"
        elif "newcs" in cam.lower():
            return "Newcs"
        elif "vizcam" in cam.lower():
            return "Vizcam"
        elif "sh4cam" in cam.lower():
            return "Sh4CAM"
        elif "rucam" in cam.lower():
            return "Rucam"
        else:
            return cam[0:6]

    def start(self):
        global AltSoftcamConfigError
        if not AltSoftcamConfigError:
            self.camstart = self["list"].getCurrent()[0]
            if self.camstart != self.actcam:
                print "[Alternative SoftCam Manager] Start SoftCam"
                try: 
                    with open("/proc/sys/vm/drop_caches", "w") as f: f.write("1\n")
                except Exception:
                    pass
                self.Console.ePopen("chmod 755 %s/*oscam*" % config.plugins.AltSoftcam.camdir.value)
                self.camstartcmd = getcamcmd(self.camstart)
                msg = _("Starting %s") % self.camstart
                self.mbox = self.session.open(MessageBox, msg, MessageBox.TYPE_INFO)
                self.activityTimer = eTimer()
                self.activityTimer.timeout.get().append(self.Stopping)
                self.activityTimer.start(100, False)
            else:
                self.restart()

    def stop(self):
        if self.actcam != "none":
            try: 
                with open("/proc/sys/vm/drop_caches", "w") as f: f.write("1\n")
            except Exception:
                pass
            self.Console.ePopen("/etc/init.d/softcam stop;killall -9 %s" % self.actcam)
            print "[Alternative SoftCam Manager] stop ", self.actcam
            try:
                remove("/tmp/ecm.info")
            except Exception:
                pass
            msg  = _("Stopping %s") % self.actcam
            self.actcam = "none"
            self.mbox = self.session.open(MessageBox, msg, MessageBox.TYPE_INFO)
            self.activityTimer = eTimer()
            self.activityTimer.timeout.get().append(self.closestop)
            self.activityTimer.start(1000, False)

    def closestop(self):
        self.activityTimer.stop()
        self.mbox.close()
        self.CreateInfo()

    def restart(self):
        global AltSoftcamConfigError
        if not AltSoftcamConfigError:
            print "[Alternative SoftCam Manager] restart SoftCam"
            self.camstart = self.actcam
            if self.camstartcmd == "":
                self.camstartcmd = getcamcmd(self.camstart)
            msg  = _("Restarting %s") % self.actcam
            self.mbox = self.session.open(MessageBox, msg, MessageBox.TYPE_INFO)
            self.activityTimer = eTimer()
            self.activityTimer.timeout.get().append(self.Stopping)
            self.activityTimer.start(100, False)

    def Stopping(self):
        self.activityTimer.stop()
        if pathExists("/etc/init.d/softcam"):
            self.Console.ePopen("/etc/init.d/softcam stop")
        self.Console.ePopen("killall -9 %s" % self.actcam)
        print "[Alternative SoftCam Manager] stopping ", self.actcam
        self.activityTimer = eTimer()
        self.activityTimer.timeout.get().append(self.Starting)
        self.activityTimer.start(500, False)
        
    def Starting(self):
        self.activityTimer.stop()
        try:
            if pathExists("/tmp/ecm.info"):
                remove("/tmp/ecm.info")
            if pathExists("/tmp/pmt.tmp"):
                remove("/tmp/pmt.tmp")
        except Exception:
            pass
        self.actcam = self.camstart
        service = self.session.nav.getCurrentlyPlayingServiceReference()
        if service:
            self.session.nav.stopService()
        self.Console.ePopen(self.camstartcmd)
        print "[Alternative SoftCam Manager] started", self.camstartcmd
        if self.mbox:
            self.mbox.close()
        if service:
            self.session.nav.playService(service)
        self.CreateInfo()

    def ok(self):
        if self["list"].getCurrent()[0] != self.actcam:
            self.start()
        else:
            self.restart()

    def cancel(self):
        if config.plugins.AltSoftcam.actcam.value != self.actcam:
            config.plugins.AltSoftcam.actcam.value = self.actcam
            config.plugins.AltSoftcam.actcam.save()
        self.close()

    def setup(self):
        self.session.openWithCallback(self.CreateInfo, ConfigEdit)

######################################################################################
class ConfigEdit(Screen, ConfigListScreen):
    skin = """
<screen name="ConfigEdit" position="center,center" size="700,200" title="SoftCam configuration">
    <eLabel position="5,0" size="690,2" backgroundColor="#aaaaaa" />
    <widget name="config" position="20,20" size="660,145" zPosition="1" scrollbarMode="showOnDemand" />
    <eLabel position="85,180" size="166,2" backgroundColor="#00ff2525" />
    <eLabel position="455,180" size="166,2" backgroundColor="#00389416" />
    <widget name="key_red" position="85,150" zPosition="2" size="170,30" valign="center" halign="center" font="Regular;22" transparent="1" />
    <widget name="key_green" position="455,150" zPosition="2" size="170,30" valign="center" halign="center" font="Regular;22" transparent="1" />
</screen>"""

    def __init__(self, session):
        Screen.__init__(self, session)
        self["key_red"] = Label(_("Exit"))
        self["key_green"] = Label(_("Ok"))
        self["actions"] = ActionMap(["OkCancelActions", "ColorActions"],
            {
                "cancel": self.close,
                "ok": self.selectFolder,
                "green": self.ok,
                "red": self.close,
            }, -2)
        ConfigListScreen.__init__(self, [], session)
        self.camconfigold = config.plugins.AltSoftcam.camconfig.value
        self.camdirold = config.plugins.AltSoftcam.camdir.value
        self.list = []
        self.list.append(getConfigListEntry(_("Activate Alternative Softam Manager"), config.plugins.AltSoftcam.enabled))
        self.list.append(getConfigListEntry(_("Manage oscam only?"), config.plugins.AltSoftcam.OsCamonly))
        self.list.append(getConfigListEntry(_("SoftCam directory (press OK)"), config.plugins.AltSoftcam.camdir))
        self.list.append(getConfigListEntry(_("SoftCam config directory (press OK)"), config.plugins.AltSoftcam.camconfig))
        self["config"].list = self.list
        self.title = _("SoftCam configuration")

    def selectFolder(self):
        curIndex = self["config"].getCurrentIndex()
        currItem = self["config"].list[curIndex][1]
        if isinstance(currItem, ConfigDirectory):
            def SetDirPathCallBack(curIndex, newPath):
                if None != newPath: self["config"].list[curIndex][1].value = newPath
            from Tools.BoundFunction import boundFunction
            if currItem == config.plugins.AltSoftcam.camdir:
                titletxt=_("Select directory with binaries")
            elif currItem == config.plugins.AltSoftcam.camconfig:
                titletxt=_("Select directory with configs")
            else:
                titletxt=_("Select directory")
            if os_path.isdir(currItem.value):
                self.session.openWithCallback(boundFunction(SetDirPathCallBack, curIndex), DirectorySelectorWidget, currDir=currItem.value, title=titletxt)
            else:
                self.session.openWithCallback(boundFunction(SetDirPathCallBack, curIndex), DirectorySelectorWidget, currDir='/', title=titletxt)
    
    def ok(self):
        if self.camconfigold != config.plugins.AltSoftcam.camconfig.value \
            or self.camdirold != config.plugins.AltSoftcam.camdir.value:
            self.session.openWithCallback(self.updateConfig, MessageBox,
                (_("Are you sure you want to save this configuration?\n\n")))
        elif not os_path.isdir(self.camconfigold) or not os_path.isdir(self.camdirold):
            self.updateConfig(True)
        else:
            config.plugins.AltSoftcam.enabled.save()
            config.plugins.AltSoftcam.OsCamonly.save()
            self.close()

    def updateConfig(self, ret = False):
        if ret == True:
            global AltSoftcamConfigError
            msg = [ ]
            if not os_path.isdir(config.plugins.AltSoftcam.camconfig.value):
                msg.append("%s " % config.plugins.AltSoftcam.camconfig.value)
            if not os_path.isdir(config.plugins.AltSoftcam.camdir.value):
                msg.append("%s " % config.plugins.AltSoftcam.camdir.value)
            if msg == [ ]:
                if config.plugins.AltSoftcam.camconfig.value[-1] == "/":
                    config.plugins.AltSoftcam.camconfig.value = config.plugins.AltSoftcam.camconfig.value[:-1]
                if config.plugins.AltSoftcam.camdir.value[-1] == "/":
                    config.plugins.AltSoftcam.camdir.value = config.plugins.AltSoftcam.camdir.value[:-1]
                config.plugins.AltSoftcam.enabled.save()
                config.plugins.AltSoftcam.OsCamonly.save()
                config.plugins.AltSoftcam.camconfig.save()
                config.plugins.AltSoftcam.camdir.save()
                AltSoftcamConfigError = False
                self.close()
            else:
                AltSoftcamConfigError = True
                self.mbox = self.session.open(MessageBox,
                    _("Directory %s does not exist!\nPlease set the correct directorypath!")
                    % msg, MessageBox.TYPE_INFO, timeout = 5 )

######################################################################################
from Components.FileList import FileList
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