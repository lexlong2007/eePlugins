# -*- coding: utf-8 -*-
#######################################################################
#
#   Coded by j00zek (c)2014-2020
#
#######################################################################

from inits import * 
from Components.ActionMap import ActionMap
from Components.config import *
from Components.ConfigList import ConfigList, ConfigListScreen
from Components.Console import Console
from Components.FileList import FileList, EXTENSIONS
from Components.Label import Label
from enigma import eDVBDB, eServiceReference, eTimer, eConsoleAppContainer, getDesktop
from j00zekConsole import j00zekConsole
from os import system as os_system, remove as os_remove, chmod as os_chmod, symlink as os_symlink, path as os_path
from Screens.InfoBar import InfoBar
from Screens.ChoiceBox import ChoiceBox 
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Tools.BoundFunction import boundFunction
from Tools.Directories import fileExists, resolveFilename, pathExists, SCOPE_PLUGINS, SCOPE_SKIN_IMAGE

config.plugins.j00zek = ConfigSubsection()
j00zekConfig = config.plugins.j00zek
j00zekConfig.separator = NoSave(ConfigNothing())

j00zekConfig.chlistEnabled = ConfigYesNo(default = True)
j00zekConfig.chlistServerIP = ConfigText(default = "192.168.1.5", fixed_size = False)
j00zekConfig.chlistServerLogin = ConfigText(default = "root", fixed_size = False)
j00zekConfig.chlistServerPass = ConfigPassword(default = "root", fixed_size = False)
j00zekConfig.chlistServerHidden = ConfigYesNo(default = False)
j00zekConfig.syncPLtransponders = NoSave(ConfigYesNo(default = False))

j00zekConfig.BouquetsEnabled = ConfigYesNo(default = True)
j00zekConfig.BouquetsNC = ConfigSelection(default = "NA", choices = [("NA", "Nie odświerzaj"),
                                                                                      ("49188PL", "HotBird-PL"),
                                                                                      ("49188", "HotBird"),
                                                                                      ("49186", "HotBird & Astra")
                                                                                      ])
j00zekConfig.BouquetsCP = ConfigSelection(default = "NA", choices = [("NA", "Nie odświerzaj"),
                                                                                      ("CP", "Hotbird"),
                                                                                      #("CPPL", "Cyfrowy Polsat-PL")
                                                                                      ])

j00zekConfig.BouquetsClearLameDB = ConfigSelection(default = "norefresh", choices = [("all", "Tak, wszystkie satelity"),
                                                                                      ("pl", "Tak, tylko 'polskie' transpondery"),
                                                                                      ("norefresh", "Nie")
                                                                                      ])
j00zekConfig.BouquetsExcludeBouquet = ConfigYesNo(default = False)
#j00zekConfig.BouquetsExcludeBouquet.value = False
j00zekConfig.BouquetsAction = ConfigSelection(default = "prov", choices = [("prov", "Tworzenie bukietu z układem dostawcy"), ("1st", "Aktualizacja pierwszego bukietu na liście"), ("all", "Aktualizacja pierwszego i Tworzenie bukietu z układem dostawcy")])

j00zekConfig.Clear1st = ConfigYesNo(default = False)
j00zekConfig.ClearBouquets = ConfigYesNo(default = False)

#oscam synchro
j00zekConfig.BouquetsOscam = ConfigYesNo(default = True)
j00zekConfig.BouquetsOscamConfig = ConfigDirectory(default = 'NIEZNANY')
if j00zekConfig.BouquetsOscamConfig.value == 'NIEZNANY':
    try:
        if pathExists(config.plugins.AltSoftcam.camconfig.value):
            j00zekConfig.BouquetsOscamConfig.value = config.plugins.AltSoftcam.camconfig.value
    except:
        for folder in ['/etc/oscam','/var/keys']:
            if fileExists("%s/oscam.conf" % folder):
                j00zekConfig.BouquetsOscamConfig.value = folder
                break

j00zekConfig.Bouquets_srvid = ConfigYesNo(default = False) #PID > Name assigments "0100,0B01:428A|nc+|Filmbox Arthouse"

#local card config helpers
j00zekConfig.Bouquets_caid = ConfigSelection(default = "unknown", choices = [("unknown", 'Nie ustawiono'), ("0100", "NC+ Seca (0100)"), ("0B01", "NC+ Conax (0B01)"), ("0B01", "NC+ Mix"), ("1803", "Polsat (1803)")])
j00zekConfig.Bouquets_Packet = ConfigSelection(default = "unknown", choices = [("unknown", 'Nie ustawiono'), ("scan", "Skanowanie automatyczne")]) #, ("ncstart", "NC-Start+"), ("nccomfort", "NC-Comfort+"), ("ncextra", "NC-Extra+")])
j00zekConfig.Bouquets_services = ConfigYesNo(default = False) #Assigment of PIDs to [j00zekBouquets-packet] 
j00zekConfig.Bouquets_dvbapi = ConfigYesNo(default = False) #we need to know what packet user has

BackupFile='KopiaListyKanalow.tar.gz'

j00zekConfig.Znacznik = ConfigSelection(default = "#SERVICE 1:832:D:0:0:0:0:0:0:0:: ", 
                                        choices = [("#SERVICE 1:832:D:0:0:0:0:0:0:0:: ", "Pomijaj"),
                                                   ("#SERVICE 1:0:1:144B:5DC:13E:820000:0:0:0::---", "Wyświetlaj '---'"),
                                                   ("#SERVICE 1:0:1:144B:5DC:13E:820000:0:0:0::<puste>", "Wyświetlaj '<puste>'")
                                                  ])

#Convert from m3u files
j00zekConfig.m3uEnabled = ConfigYesNo(default = False)
j00zekConfig.m3uMode = ConfigSelection(default = "NA", choices = [("NA", "Nie aktualizuj"),
                                                                  ("m3u", "lokalnego pliku m3u"),
                                                                  ("url", "Plik pobierany ze strony")
                                                                 ])

j00zekConfig.m3ufile = ConfigDirectory(default = "/")
j00zekConfig.m3uURL = ConfigDirectory(default = "/")
j00zekConfig.m3uURLkeep = ConfigYesNo(default = False)
j00zekConfig.FrameworkType = ConfigSelection(default = "4097", choices = getMultiFramework())
j00zekConfig.m3uSplitMode = ConfigYesNo(default = False) # split languages or not
j00zekConfig.m3uFilter = ConfigYesNo(default = False)
j00zekConfig.m3uProxy = ConfigSelection(default = "proxyOFF", choices = [("proxyOFF", "bezpośrednie"),
                                                                  ("http://127.0.0.1:53422/play/?url=", "poprzez LiveProxy na porcie 53422"),
                                                                  ("http://127.0.0.1:8088/", "poprzez Streamlink na porcie 8088")
                                                                 ])
j00zekConfig.m3uAddIPTVmarker = ConfigSelection(default = "markerOFF", choices = [("markerOFF", "nie zmieniaj"),
                                                                  ("i", "dodaj i na początku nazwy"),
                                                                  ("IPTV", "dodaj IPTV na końcu nazwy")
                                                                 ])
j00zekConfig.m3uEPGmode = ConfigYesNo(default = False) #jak True to próbujemy znaleźć referencję kanału z Satki

##############################################################

class j00zekBouquets(Screen, ConfigListScreen):
    if getDesktop(0).size().width() >= 1920:
        skin = """
          <screen name="j00zekBouquets" position="345,93" size="1232,908" title="j00zekBouquets @j00zek" >
            <widget name="config" position="10,10" size="1095,645" zPosition="1" font="Regular;27" itemHeight="35" transparent="0" scrollbarMode="showOnDemand" />
            <widget name="key_red" position="91,849" size="200,27" zPosition="1" valign="center" halign="center" font="Regular;24" transparent="1" foregroundColor="red" />
            <widget name="key_green" position="378,849" size="200,27" zPosition="1" valign="center" halign="center" font="Regular;24" transparent="1" foregroundColor="green" />
            <widget name="key_yellow" position="665,849" size="200,27" zPosition="1" valign="center" halign="center" font="Regular;24" transparent="1" foregroundColor="yellow" />
            <widget name="key_blue" position="952,849" size="200,27" zPosition="1" valign="center" halign="center" font="Regular;24" transparent="1" foregroundColor="blue" />
          </screen>"""
    else:
        skin = """
          <screen name="j00zekBouquets" position="60,260" size="600,400" title="j00zekBouquets @j00zek" >
            <widget name="config" position="10,10" size="580,330" zPosition="1" transparent="0" scrollbarMode="showOnDemand" />
            <widget name="key_red" position="0,340" zPosition="2" size="300,30" valign="center" halign="center" font="Regular;22" transparent="1" foregroundColor="red" />
            <widget name="key_green" position="300,340" zPosition="2" size="300,30" valign="center" halign="center" font="Regular;22" transparent="1" foregroundColor="green" />
            <widget name="key_yellow" position="0,370" zPosition="2" size="300,30" valign="center" halign="center" font="Regular;22" transparent="1" foregroundColor="yellow" />
            <widget name="key_blue" position="300,370" zPosition="2" size="300,30" valign="center" halign="center" font="Regular;22" transparent="1" foregroundColor="blue" />
          </screen>"""

    onChangedEntry = [ ]
    LastIndex=0
    CurrIndex=0
    j00zekBouquetsBin=''
        
    def __init__(self, session):
        Screen.__init__(self, session)

        
        self.list = [ ]
        ConfigListScreen.__init__(self, self.list, session = session, on_change = self.changedEntry)
        self["actions"] = ActionMap(["j00zekBouquets"],
            {
                "cancel": self.keyCancel,
                "ok": self.keyOK,
                "red": self.keyRed,
                "green": self.keyGreen,
                "yellow": self.keyYellow,
                "blue": self.keyBlue,
            }, -2)

        self["key_red"] = Label('Załaduj z pliku tar.gz')
        self["key_green"] = Label('Utwórz archiwum tar.gz')
        self["key_blue"] = Label()
        self["key_yellow"] = Label()
        
        self.timer = eTimer()
        
        self.onLayoutFinish.append(self.layoutFinished)

    def layoutFinished(self):
        self.setTitle("Wersja %s" % Info)
        with open("/proc/sys/vm/drop_caches", "w") as f: f.write("1\n")
        self.runSetup()

    def runSetup(self):
        self.list = [ ]
        self.list.append(getConfigListEntry('Czyszczenie lamedb:', j00zekConfig.BouquetsClearLameDB))
        self.list.append(getConfigListEntry('Czyszczenie listy z nieużywanych bukietów:', j00zekConfig.ClearBouquets))
        self.list.append(getConfigListEntry(' ', j00zekConfig.separator))
        self.list.append(getConfigListEntry('--- Synchronizacja z tunera ---', j00zekConfig.chlistEnabled))
        if j00zekConfig.chlistEnabled.value == True:
            self["key_blue"].setText('Pobierz z tunera')
            self.list.append(getConfigListEntry('Pobierz listę z tunera:', j00zekConfig.chlistServerIP))
            self.list.append(getConfigListEntry("Konto:", j00zekConfig.chlistServerLogin))
            self.list.append(getConfigListEntry('Hasło:', j00zekConfig.chlistServerPass))
        else:
            self["key_blue"].setText('')
        
        self.list.append(getConfigListEntry(' ', j00zekConfig.separator))
        self.list.append(getConfigListEntry('--- Synchronizacja z satelity ---', j00zekConfig.BouquetsEnabled))
        if j00zekConfig.BouquetsEnabled.value == True:
            self["key_yellow"].setText('Pobierz z satelity')
            self.list.append(getConfigListEntry('nc+:', j00zekConfig.BouquetsNC))
            if j00zekConfig.BouquetsNC.value == '49188PL':
                self.list.append(getConfigListEntry('Synchronizuj listę TR,SID z web:', j00zekConfig.syncPLtransponders))
            self.list.append(getConfigListEntry('Cyfrowy Polsat:', j00zekConfig.BouquetsCP))
            if j00zekConfig.BouquetsNC.value != 'NA' or j00zekConfig.BouquetsCP.value != 'NA':
                self.list.append(getConfigListEntry('Akcja:', j00zekConfig.BouquetsAction))
                if j00zekConfig.BouquetsAction.value == '1st' or j00zekConfig.BouquetsAction.value == 'all':
                    self.list.append(getConfigListEntry("Usuń nieznane pozycje z bukietu:", j00zekConfig.Clear1st))
                self.list.append(getConfigListEntry("Pomiń zdefiniowane kanały:", j00zekConfig.BouquetsExcludeBouquet))
                self.list.append(getConfigListEntry('Puste miejsca na liście kanałów:', j00zekConfig.Znacznik))
                
                self.list.append(getConfigListEntry(" ", j00zekConfig.separator))                
                self.list.append(getConfigListEntry("--- Synchronizacja nazw kanałów w oscamie ---", j00zekConfig.BouquetsOscam))
                if j00zekConfig.BouquetsOscam.value is True:
                    self.list.append(getConfigListEntry('Katalog konfiguracyjny oscam-a (OK):', j00zekConfig.BouquetsOscamConfig))
                    if fileExists("%s/oscam.srvid" % j00zekConfig.BouquetsOscamConfig.value):
                        self.list.append(getConfigListEntry('Aktualizacja nazw serwisów:', j00zekConfig.Bouquets_srvid))
                    else:
                        j00zekConfig.Bouquets_srvid.value = False
                        self.list.append(getConfigListEntry("Nie znaleziono pliku oscam.srvid", j00zekConfig.separator))
        else:
            self["key_yellow"].setText('')

        self.list.append(getConfigListEntry(' ', j00zekConfig.separator))
        self.list.append(getConfigListEntry('--- Synchronizacja z m3u ---', j00zekConfig.m3uEnabled))
        if j00zekConfig.m3uEnabled.value == True:
            #self["key_blue"].setText('Pobierz z m3u')
            self.list.append(getConfigListEntry('Aktualizuj listę z:', j00zekConfig.m3uMode))
            if j00zekConfig.m3uMode.value == 'm3u':
                self.list.append(getConfigListEntry("Wybrany plik m3u (OK):", j00zekConfig.m3ufile))
            elif j00zekConfig.m3uMode.value == 'url':
                self.list.append(getConfigListEntry('Wybrany plik url (OK):', j00zekConfig.m3uURL))
                self.list.append(getConfigListEntry('Zapisz pobrany plik do %s:' % j00zekConfig.m3uURL.value.replace('.url','.m3u'), j00zekConfig.m3uURLkeep))
                
            self.list.append(getConfigListEntry('Tylko sekcje z pliku /etc/enigma2/JB_m3u_sections.cfg', j00zekConfig.m3uFilter))
            self.list.append(getConfigListEntry('Oddzielny bukiet dla każdej sekcji:', j00zekConfig.m3uSplitMode))
            self.list.append(getConfigListEntry('Wersja MultiFramework:', j00zekConfig.FrameworkType))
            self.list.append(getConfigListEntry('Połączenie:', j00zekConfig.m3uProxy))
            self.list.append(getConfigListEntry('Zmień nazwę kanału:', j00zekConfig.m3uAddIPTVmarker))
            self.list.append(getConfigListEntry('Korzystaj z referencji SAT dla EPG:', j00zekConfig.m3uEPGmode))
        else:
            pass #self["key_blue"].setText('')
            
        self["config"].list = self.list
        self["config"].setList(self.list)
    
    def changedEntry(self):
        print "Index: %d" % self["config"].getCurrentIndex()
        for x in self.onChangedEntry:
            x()

    def ConfigureJB(self):
        if pathExists('%scomponents/zapNC.config' % PluginPath) is False:
            self.ZapNC=("1:0:1:1139:2AF8:13E:820000:0:0:0:")
        else:
            with open('%scomponents/zapNC.config' % PluginPath, 'r') as ZAPconfig:
                tmp=ZAPconfig.readline().split('"')[1]
                self.ZapNC=(tmp)
                ZAPconfig.close()
        if pathExists('%scomponents/zapCP.config' % PluginPath) is False:
            self.ZapCP=("1:0:1:3396:3390:71:820000:0:0:0:")
        else:
            with open('%scomponents/zapCP.config' % PluginPath, 'r') as ZAPconfig:
                tmp=ZAPconfig.readline().split('"')[1]
                self.ZapCP=(tmp)
                ZAPconfig.close()
        self.BouquetsNCBin='%scomponents/j00zekBouquetsNC' % (PluginPath)
        self.BouquetsCPBin='%scomponents/j00zekBouquetsCP' % (PluginPath)
        self.ExcludedSIDsTemplate='%scomponents/excludedSIDs.template' % PluginPath
        self.ExcludedSIDsFileName='userbouquet.excludedSIDs.j00zekAutobouquet.tv'
        self.ExcludedSIDsFile='/etc/enigma2/%s' % self.ExcludedSIDsFileName
        self.IncludedTranspondersTemplate='%scomponents/PLtransponders.cfg' % PluginPath
        self.IncludedTranspondersFile='/tmp/transponders.PL'
        self.runlist = []
        self.runlist.append(('[ -f /tmp/.ChannelsNotUpdated ] && rm -f /tmp/.ChannelsNotUpdated 2>/dev/null'))
        if pathExists('%s/components/CheckType.sh' % PluginPath) is True:
            self.runlist.append(('chmod 755 %s/components/*.sh' % PluginPath))
            self.runlist.append(('%s/components/CheckType.sh' % PluginPath))
        
        self.ZapTo=""
        
        #tylko polskie transpondery
        if j00zekConfig.BouquetsNC.value.endswith('PL'):
            if not pathExists(self.IncludedTranspondersFile):
                os_symlink(self.IncludedTranspondersTemplate,self.IncludedTranspondersFile)
        else:
            if pathExists(self.IncludedTranspondersFile):
                os_remove(self.IncludedTranspondersFile)
        #kanaly do pominiecia
        if j00zekConfig.BouquetsExcludeBouquet.value == True:
            self.ExcludeSIDS="1"
            ExcludedSIDsFileNeedsUpdate=1
            if pathExists(self.ExcludedSIDsFile) is False:
                from shutil import copy as shutil_copy
                shutil_copy(self.ExcludedSIDsTemplate,self.ExcludedSIDsFile)
        else:
            self.ExcludeSIDS="0"
            ExcludedSIDsFileNeedsUpdate=0
            
        #sprawdzamy schemat pliku bouquets.tv
        hasNewline=1
        if j00zekConfig.BouquetsNC.value !="NA":
            ncNeedsUpdate=1
        else:
            ncNeedsUpdate=0
        if j00zekConfig.BouquetsCP.value !="NA":
            cpNeedsUpdate=1
        else:
            cpNeedsUpdate=0
                
        windowsEOL=''
        with open("/etc/enigma2/bouquets.tv", "r") as bouquetsTV:
            for line in bouquetsTV:
                if windowsEOL == '' and line.endswith('\r\n'):
                    windowsEOL='\r'
                if line.endswith('\n'):
                    hasNewline=1
                else:
                    hasNewline=0
                if line.find(self.ExcludedSIDsFileName) > 0:
                    ExcludedSIDsFileNeedsUpdate=0
                if line.find('userbouquet.ncplus.j00zekAutobouquet.tv') > 0:
                    ncNeedsUpdate=0
                if line.find('userbouquet.CP.j00zekAutobouquet.tv') > 0:
                    cpNeedsUpdate=0
            bouquetsTV.close()
        #dopisujemy nasze bukiety
        if ncNeedsUpdate == 1:
            with open("/etc/enigma2/bouquets.tv", "a") as bouquetsTV:
                if hasNewline == 0:
                    bouquetsTV.write('\n')
                bouquetsTV.write('#SERVICE 1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "userbouquet.ncplus.j00zekAutobouquet.tv" ORDER BY bouquet%s\n' % windowsEOL)
                bouquetsTV.close()
                hasNewline=1
        if cpNeedsUpdate == 1:
            with open("/etc/enigma2/bouquets.tv", "a") as bouquetsTV:
                if hasNewline == 0:
                    bouquetsTV.write('\n')
                bouquetsTV.write('#SERVICE 1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "userbouquet.CP.j00zekAutobouquet.tv" ORDER BY bouquet%s\n' % windowsEOL)
                bouquetsTV.close()
                hasNewline=1
        if ExcludedSIDsFileNeedsUpdate == 1:
            with open("/etc/enigma2/bouquets.tv", "a") as bouquetsTV:
                if hasNewline == 0:
                    bouquetsTV.write('\n')
                bouquetsTV.write('#SERVICE 1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "%s" ORDER BY bouquet%s\n' % (self.ExcludedSIDsFileName,windowsEOL))
                bouquetsTV.close()
        
        if j00zekConfig.BouquetsNC.value == '49188PL' and j00zekConfig.syncPLtransponders.value == True:
             self.runlist.append('%scomponents/SyncFromWeb.sh' % PluginPath)
        if j00zekConfig.BouquetsNC.value != 'NA':
            self.runlist.append("%s %s %s %s %s '%s'" % ( self.BouquetsNCBin, j00zekConfig.BouquetsNC.value, \
                                j00zekConfig.BouquetsAction.value, self.ZapNC, self.ExcludeSIDS, j00zekConfig.Znacznik.value))
            self.ZapTo=self.ZapNC
        if j00zekConfig.BouquetsCP.value != 'NA':
            self.runlist.append("%s %s %s %s %s '%s'" % ( self.BouquetsCPBin, j00zekConfig.BouquetsCP.value, \
                                j00zekConfig.BouquetsAction.value, self.ZapCP, self.ExcludeSIDS, j00zekConfig.Znacznik.value))
            if self.ZapTo == "":
                self.ZapTo = self.ZapCP
        if j00zekConfig.BouquetsAction.value in ("1st","all") and  j00zekConfig.Clear1st.value == True:
            self.runlist.append(('%s/components/clear1st.sh' % PluginPath))
        if j00zekConfig.ClearBouquets.value:
            self.runlist.append("%s/components/ClearBouquets" % PluginPath)
        return

    def ConfigOscamUpdate(self):
        if j00zekConfig.BouquetsOscam.value is True:
            self.runlist.append('%s/components/j00zekOscamUpdater "%s" "%s" "%s" "%s" "%s" "%s" "%s"' % (PluginPath, 
                                                                   j00zekConfig.Bouquets_srvid.value,
                                                                        j00zekConfig.Bouquets_caid.value,
                                                                             j00zekConfig.Bouquets_Packet.value,
                                                                                  j00zekConfig.Bouquets_services.value,
                                                                                       j00zekConfig.Bouquets_dvbapi.value,
                                                                                            j00zekConfig.BouquetsOscamConfig.value,
                                                                                                j00zekConfig.BouquetsAction.value))
        return
    
    def keyYellow(self):
        if j00zekConfig.BouquetsEnabled.value == False:
            return
        elif not os_path.exists('/usr/bin/dvbsnoop'):
            self.session.openWithCallback(self.doNothing ,MessageBox,"Brak dvbsnoop Spróbuj zainstalować z repozytorium. - kończę!!!", MessageBox.TYPE_INFO)
            return
        elif j00zekConfig.BouquetsNC.value != 'NA' or j00zekConfig.BouquetsCP.value != 'NA':
            self.SaveSettings()
            #stopping playing service
            self.prev_root = InfoBar.instance.servicelist.getRoot()
            self.prev_running_service = self.session.nav.getCurrentlyPlayingServiceReference()
            self.session.nav.stopService()
            #cleaningLAMEDB
            if j00zekConfig.BouquetsClearLameDB.value != "norefresh":
                self.ClearLameDB()
                self.BuildLameDB()
            else:
                eDVBDB.getInstance().loadServicelist('%scomponents/j00zekBouquets.lamedb' % PluginPath)
            #configuring excluded SIDs
            #zap to channel on transponder, we use it as hack to simplify selection of the NIM
            self.ConfigureJB()
            self.ConfigOscamUpdate()

            self.ZapToService(self.ZapTo)
            self.timer.callback.append(self.keyYellowStep2)
            self.timer.start(500,1) # j00zekBouquets waits for e2 to tune.
        return

    def keyYellowStep2(self):
        self.timer.callback.remove(self.keyYellowStep2)
        self.session.openWithCallback(self.keyYellowEndRun ,j00zekConsole, title = "j00zekBouquets v %s (%s, %s)" % (Info, j00zekConfig.BouquetsClearLameDB.value, j00zekConfig.BouquetsNC.value ) , cmdlist = self.runlist)
        
    def keyYellowEndRun(self, ret =0):
        self.reloadLAMEDB()
        self.ZapToPrevChannel()

    def ClearLameDB(self, ret =0):
        #e2 de facto dodaje nowe serwisy a nie przeladowuje lamedb, wiec musimy najperw wszystkie wykasowac...#
        #RESULT removeServices(int dvb_namespace=-1, int tsid=-1, int onid=-1, unsigned int orb_pos=0xFFFFFFFF);
        db = eDVBDB.getInstance()
        if j00zekConfig.BouquetsClearLameDB.value == "all":
            SatPositions=[50,70,90,100,130,160,192,215,235,255,260,284,305,313,330,360,390,400,420,450,490,530,550,570,600,620,642,685,705,720,750,800,852]
            for sat in SatPositions:
                db.removeServices(-1, -1, -1, sat)
        elif j00zekConfig.BouquetsClearLameDB.value == "pl":
            tsid=[0x001a,0x0064,0x0065,0x00c8,0x012c,0x0190,0x02bc,0x03e8,0x044c,0x0514,0x05dc,0x0640,0x1388,0x13ef,0x1518,
                  0x1af4,0x1b58,0x1c20,0x1ce8,0x1e14,0x1e78,0x1edc,0x1fa4,0x22c4,0x23f0,0x24b8,0x251c,0x2580,0x26ac,0x2af8,
                  0x2bc0,0x2c88,0x2cec,0x2d50,0x2db4,0x2e7c,0x2ee0,0x2f44,0x2fa8,0x3070,0x3138,0x319c,0x3200,0x332c,0x3390,
                  0x33f4,0x3c28,0x3cf0,0x3db8,0x3e1c]
            for ts in tsid:
                db.removeServices(-1, ts, -1, 130)

    def BuildLameDB(self):
        # ... teraz dodac to co potrzebujemy :)            
        eDVBDB.getInstance().loadServicelist('%scomponents/j00zekBouquets.lamedb' % PluginPath)
        eDVBDB.getInstance().saveServicelist()

    def reloadLAMEDB(self):
        eDVBDB.getInstance().reloadServicelist()
        eDVBDB.getInstance().reloadBouquets()

    def ZapToService(self, ZapTo):
        service = eServiceReference(ZapTo)
        InfoBar.instance.servicelist.clearPath()
        InfoBar.instance.servicelist.enterPath(service)
        InfoBar.instance.servicelist.setCurrentSelection(service)
        InfoBar.instance.servicelist.zap()
    
    def ZapToPrevChannel(self):
        if InfoBar.instance.servicelist.getRoot() != self.prev_root: #already in correct bouquet?
            InfoBar.instance.servicelist.clearPath()
            if InfoBar.instance.servicelist.getRoot() != self.prev_root:
                InfoBar.instance.servicelist.enterPath(InfoBar.instance.servicelist.bouquet_root)
            InfoBar.instance.servicelist.enterPath(self.prev_root)
        if self.prev_running_service:
            InfoBar.instance.servicelist.setCurrentSelection(self.prev_running_service) #select the service in servicelist
            self.session.nav.playService(self.prev_running_service)
    
    def keyBlue(self):
        self.SaveSettings()
        if j00zekConfig.chlistEnabled.value == True:
            self.session.openWithCallback(self.keyBlueYESNO ,MessageBox,'Pobrać z tunera %s teraz?' % j00zekConfig.chlistServerIP.value, MessageBox.TYPE_YESNO)
        return
        
    def keyBlueYESNO(self, ret):
        if ret is True:
            self.runlist = []
            self.runlist=[("%s/components/CHlistSynchro.sh %s %s %s" % (PluginPath,
                                                            j00zekConfig.chlistServerIP.value,
                                                              j00zekConfig.chlistServerLogin.value,
                                                                  j00zekConfig.chlistServerPass.value))]
            self.session.openWithCallback(self.j00zekConsoleEndRun ,j00zekConsole, title = "Channels list synchronization", cmdlist = self.runlist)
        return

    def keyRed(self):
        self.session.openWithCallback(self.keyRedYESNO ,MessageBox,"Załadować nową listę z pen-a teraz?", MessageBox.TYPE_YESNO)
        return
        
    def keyRedYESNO(self, ret):
        def SetDirPathCallBack(newPath):
            if None != newPath:
                confPath = resolveFilename(SCOPE_CONFIG, '')
                self.runlist = [('cd /'),
                                ('echo "Rozpakowywanie archiwum %s..."' % newPath),
                                ('tar -xzvf %s' % newPath)
                                ]
                self.session.openWithCallback(self.j00zekConsoleEndRun ,j00zekConsole, title = "Rozpakowywanie archiwum...", cmdlist = self.runlist, endText = '\nNowa lista zainstalowana, naciśnij OK')
            return
        if ret is True:
            self.session.openWithCallback(boundFunction(SetDirPathCallBack), DirectorySelectorWidget, currDir='/', title='Wybierz archiwum listy kanałów', FileMode=True, searchpattern="^.*\.(tgz|tar\.gz)")
        return
      
    def keyGreen(self):
        def SetDirPathCallBack(newPath):
            if None != newPath:
                if newPath.endswith('/'):
                    newPath = newPath[0:-1]
                confPath = resolveFilename(SCOPE_CONFIG, '')
                if confPath.endswith('/'):
                    confPath = confPath[0:-1]
                self.runlist = [('cd /'),
                                ('echo "Tworzenie archiwum %s/%s..."' % (newPath,BackupFile)),
                                ('tar -czvf %s/%s %s/lamedb* %s/*.tv %s/*.radio' % (newPath,BackupFile,confPath,confPath,confPath))
                                ]
                self.session.openWithCallback(self.doNothing ,j00zekConsole, title = "Tworzenie archiwum %s..." % BackupFile, cmdlist = self.runlist, endText = '\nKopia wykonana, naciśnij OK')
            return
        self.session.openWithCallback(boundFunction(SetDirPathCallBack), DirectorySelectorWidget, currDir='/', title='Wybierz katalog do zapisu archiwum listy kanałów')
        return
        
    def j00zekConsoleEndRun(self, ret =0):
        if ret == 0:
            #self.session.openWithCallback(self.j00zekConsoleEndRunClear ,MessageBox,"Clear channels list before updating?", MessageBox.TYPE_YESNO)
            if j00zekConfig.BouquetsClearLameDB.value != "norefresh":
                self.j00zekConsoleEndRunClear(True)
            else:
                self.j00zekConsoleEndRunClear(False)
        return

    def doNothing(self, ret = None):
        pass
        
    def j00zekConsoleEndRunClear(self, ret):
        if ret is True:
            self.ClearLameDB()
            self.BuildLameDB()
        self.reloadLAMEDB()
      
    def SaveSettings(self):
        for x in self["config"].list:
            x[1].save()
        configfile.save()
    
    def keyOK(self): #openpliPC - F2 emuluje green
        curIndex = self["config"].getCurrentIndex()
        currItem = self["config"].list[curIndex][1]
        if isinstance(currItem, ConfigDirectory):
            def SetDirPathCallBack(curIndex, newPath):
                if None != newPath:
                    self["config"].list[curIndex][1].value = newPath.replace('//','/')
                    self.runSetup()
            if self["config"].getCurrent()[1] == j00zekConfig.BouquetsOscamConfig:
                if os_path.isdir(j00zekConfig.BouquetsOscamConfig.value):
                    myCurrDir=j00zekConfig.BouquetsOscamConfig.value
                else:
                    myCurrDir='/'
                self.session.openWithCallback(boundFunction(SetDirPathCallBack, curIndex), DirectorySelectorWidget, currDir=myCurrDir, title='Wybierz katalog z konfiguracją OsCam-a')
            elif self["config"].getCurrent()[1] == j00zekConfig.m3ufile:
                if os_path.isdir(os_path.dirname(j00zekConfig.m3ufile.value)):
                    myCurrDir=os_path.dirname(j00zekConfig.m3ufile.value)
                else:
                    myCurrDir='/'
                self.session.openWithCallback(boundFunction(SetDirPathCallBack, curIndex), DirectorySelectorWidget, currDir=myCurrDir, title='Wybierz plik m3u', FileMode=True, searchpattern="m3u")
            elif self["config"].getCurrent()[1] == j00zekConfig.m3uURL:
                if os_path.isdir(os_path.dirname(j00zekConfig.m3uURL.value)):
                    myCurrDir=os_path.dirname(j00zekConfig.m3uURL.value)
                else:
                    myCurrDir='/'
                self.session.openWithCallback(boundFunction(SetDirPathCallBack, curIndex), DirectorySelectorWidget, currDir=myCurrDir, title='Wybierz plik url', FileMode=True, searchpattern="url")
        else:
            def choiceRet(ret):
                if ret:
                    if ret[1] == 'keyYellow': self.keyYellow()
                    if ret[1] == 'loadm3u': self.loadm3u()
                    if ret[1] == 'loadurl': self.loadm3u(fromURL=True)
                    if ret[1] == 'reloadurl': self.loadm3u(reload=True)
                    if ret[1] == 'keyBlue': self.keyBlue()
                    if ret[1] == 'keyRed': self.keyRed()
                    if ret[1] == 'keyGreen': self.keyGreen()
            self.SaveSettings()
            myChoiceList=[]
            if j00zekConfig.BouquetsEnabled.value : myChoiceList.append(('Pobierz z satelity', 'keyYellow'))
            if j00zekConfig.m3uEnabled.value and j00zekConfig.m3uMode.value == 'm3u': myChoiceList.append(("Aktualizuj z pliku .../%s" % os.path.basename(j00zekConfig.m3ufile.value), 'loadm3u'))
            if j00zekConfig.m3uEnabled.value and j00zekConfig.m3uMode.value == 'url':
                myChoiceList.append(("Pobierz z adresu http://.../%s" % os.path.basename(j00zekConfig.m3uURL.value), 'loadurl'))
                if os.path.exists(j00zekConfig.m3uURL.value.replace('.url','.m3u')): myChoiceList.append(("Aktualizuj z pobranego pliku .../%s" % os.path.basename(j00zekConfig.m3uURL.value.replace('.url','.m3u')), 'reloadurl'))
            if j00zekConfig.chlistEnabled.value : myChoiceList.append(('Pobierz z tunera', 'keyBlue'))
            myChoiceList.append(('Ładuj z archiwum listy', 'keyRed'))
            myChoiceList.append(('Utwórz archiwum listy', 'keyGreen'))
            self.session.openWithCallback(choiceRet, ChoiceBox, title = "Co chcesz zrobić?", list = myChoiceList) 
    
    def loadm3u(self, fromURL=False, reload=False):
        self.runlist = []
        if fromURL:
            if j00zekConfig.m3uURLkeep.value:
                tmpFileName = j00zekConfig.m3uURL.value.replace('.url','.m3u').replace('//','/')
            else:
                tmpFileName = '/tmp/%s' % os.path.basename(j00zekConfig.m3uURL.value.replace('.url','.m3u'))
            self.runlist.append("%s/components/pyCurl %s %s" % (PluginPath, j00zekConfig.m3uURL.value, tmpFileName))
        elif reload:
            tmpFileName = j00zekConfig.m3uURL.value.replace('.url','.m3u').replace('//','/')
        else:
            tmpFileName = j00zekConfig.m3ufile.value            
        self.runlist.append("%s/components/loadm3u %s %s %s %s %s %s %s" % (PluginPath,
                                                   tmpFileName,
                                                      j00zekConfig.FrameworkType.value,
                                                         j00zekConfig.m3uSplitMode.value,
                                                            j00zekConfig.m3uFilter.value,
                                                               j00zekConfig.m3uProxy.value,
                                                                  j00zekConfig.m3uAddIPTVmarker.value,
                                                                     j00zekConfig.m3uEPGmode.value ))
        if j00zekConfig.ClearBouquets.value:
            self.runlist.append("%s/components/ClearBouquets" % PluginPath)
        
        self.session.openWithCallback(self.loadm3uEndRun ,j00zekConsole, title = "Aktualizacja z m3u/URL", cmdlist = self.runlist)

    def loadm3uEndRun(self, ret = 0):
        self.reloadLAMEDB()
        
    def keyCancel(self):
        for x in self["config"].list:
            x[1].cancel()
        self.close()
        
    def keyLeft(self):
        ConfigListScreen.keyLeft(self)
        self.keyRightLeftActions()

    def keyRight(self):
        ConfigListScreen.keyRight(self)
        self.keyRightLeftActions()
            
    def keyRightLeftActions(self):
        if (self["config"].getCurrent()[1] == j00zekConfig.chlistEnabled or 
              self["config"].getCurrent()[1] == j00zekConfig.BouquetsEnabled or
              self["config"].getCurrent()[1] == j00zekConfig.Bouquets_caid or
              self["config"].getCurrent()[1] == j00zekConfig.Bouquets_Packet or
              self["config"].getCurrent()[1] == j00zekConfig.BouquetsNC or
              self["config"].getCurrent()[1] == j00zekConfig.BouquetsCP or
              self["config"].getCurrent()[1] == j00zekConfig.BouquetsClearLameDB or
              self["config"].getCurrent()[1] == j00zekConfig.BouquetsAction or
              self["config"].getCurrent()[1] == j00zekConfig.BouquetsOscam or
              self["config"].getCurrent()[1] == j00zekConfig.m3uEnabled or
              self["config"].getCurrent()[1] == j00zekConfig.m3uMode
              ):
            self.runSetup()
#### ####################################################################################################################################################
class DirectorySelectorWidget(Screen):
    if getDesktop(0).size().width() >= 1920:
        skin = """
          <screen name="DirectorySelectorWidget" position="center,center" size="1220,440" title="">
            <widget name="key_red"      position="10,10"  zPosition="2"  size="1200,35" valign="center"  halign="left"   font="Regular;24" transparent="1" foregroundColor="red" />
            <widget name="key_blue"     position="10,10"  zPosition="2"  size="1200,35" valign="center"  halign="center" font="Regular;24" transparent="1" foregroundColor="blue" />
            <widget name="key_green"    position="10,10"  zPosition="2"  size="1200,35" valign="center"  halign="right"  font="Regular;24" transparent="1" foregroundColor="green" />
            <widget name="key_yellow"   position="10,10"  zPosition="2"  size="1200,35" valign="center"  halign="center"  font="Regular;24" transparent="1" foregroundColor="yellow" />
            <widget name="curr_dir"     position="10,50"  zPosition="2"  size="1200,35" valign="center"  halign="left"   font="Regular;22" transparent="1" foregroundColor="white" />
            <widget name="filelist"     position="10,85"  zPosition="1"  size="1200,335" transparent="1" scrollbarMode="showOnDemand" />
          </screen>"""
    else:
        skin = """
          <screen name="DirectorySelectorWidget" position="center,center" size="620,440" title="">
            <widget name="key_red"      position="10,10"  zPosition="2"  size="600,35" valign="center"  halign="left"   font="Regular;22" transparent="1" foregroundColor="red" />
            <widget name="key_blue"     position="10,10"  zPosition="2"  size="600,35" valign="center"  halign="center" font="Regular;22" transparent="1" foregroundColor="blue" />
            <widget name="key_green"    position="10,10"  zPosition="2"  size="600,35" valign="center"  halign="right"  font="Regular;22" transparent="1" foregroundColor="green" />
            <widget name="key_yellow"   position="10,10"  zPosition="2"  size="600,35" valign="center"  halign="center"  font="Regular;22" transparent="1" foregroundColor="yellow" />
            <widget name="curr_dir"     position="10,50"  zPosition="2"  size="600,35" valign="center"  halign="left"   font="Regular;18" transparent="1" foregroundColor="white" />
            <widget name="filelist"     position="10,85"  zPosition="1"  size="580,335" transparent="1" scrollbarMode="showOnDemand" />
          </screen>"""
    def __init__(self, session, currDir, title="Select directory", FileMode=False, searchpattern=""):
        print("DirectorySelectorWidget.__init__ -------------------------------")
        Screen.__init__(self, session)
        # for the skin: first try MediaPlayerDirectoryBrowser, then FileBrowser, this allows individual skinning
        #self.skinName = ["MediaPlayerDirectoryBrowser", "FileBrowser" ]
        self["key_red"]    = Label(_("Cancel"))
        self["key_yellow"] = Label(_("Refresh"))
        #self["key_blue"]   = Label(_("New directory"))
        self["key_green"]  = Label(_("Select"))
        self["curr_dir"]   = Label(_(" "))
        self.filelist      = FileList(directory=currDir, matchingPattern=searchpattern, showFiles=FileMode)
        self.FileMode      = FileMode
        self["filelist"]   = self.filelist
        self["FilelistActions"] = ActionMap(["SetupActions", "ColorActions"],
            {
                "green" : self.use,
                "red"   : self.exit,
                "yellow": self.refresh,
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
        self["curr_dir"].setText(self.getCurrentDirectory())
        
    def getCurrentDirectory(self):
        currDir = self["filelist"].getCurrentDirectory()
        if currDir and os_path.isdir( currDir ):
            return currDir
        else:
            return "/"

    def use(self):
        if self.FileMode:
          selection = self["filelist"].getSelection()
          self.close( "%s/%s" % (self.filelist.getCurrentDirectory(),selection[0]) )
        else:
          self.close( self.getCurrentDirectory() )

    def exit(self):
        self.close(None)

    def ok(self):
        if self.filelist.canDescent():
            self.filelist.descent()
        self.currDirChanged()

    def refresh(self):
        self["filelist"].refresh()
