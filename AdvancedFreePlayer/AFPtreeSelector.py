# -*- coding: utf-8 -*-
from __init__ import *
from __init__ import translate as _
from Cleaningfilenames import *
from cueSheetHelper import getCut, resetMoviePlayState

from Screens.Screen import Screen

from Screens.ChoiceBox import ChoiceBox
from Screens.InputBox import InputBox
from Screens.MessageBox import MessageBox

from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.Pixmap import Pixmap
from Components.Sources.StaticText import StaticText
from Components.config import *
from Tools.LoadPixmap import LoadPixmap
from os import path, remove, listdir, symlink, system, access, W_OK
import re

from enigma import eTimer

from skin import parseColor

from time import *
from j00zekFileList import FileList, EXTENSIONS
import json

class AdvancedFreePlayerStarter(Screen):

    def __init__(self, session, openmovie, movieTitle):
        #printDEBUG("AdvancedFreePlayerStarter >>>")
        self.sortDate = False
        self.openmovie = openmovie
        self.movieTitle = movieTitle
        self.opensubtitle = ''
        self.URLlinkName = ''
        self.rootID = myConfig.MultiFramework.value
        self.LastPlayedService = None
  
        if path.exists(ExtPluginsPath + '/DMnapi/DMnapi.pyo') or path.exists(ExtPluginsPath +'/DMnapi/DMnapi.pyc') or path.exists(ExtPluginsPath +'/DMnapi/DMnapi.py'):
            self.DmnapiInstalled = True
        else:
            self.DmnapiInstalled = False
            
        #self.skin  = LoadSkin("AdvancedFreePlayerStart")
        
        Screen.__init__(self, session)
        self.onShow.append(self.PlayMovie)

    def PlayMovie(self):
        self.onShow.remove(self.PlayMovie)
        if not self.openmovie == "":
            if not path.exists(self.openmovie + '.cuts'):
                self.SelectFramework()
            elif path.getsize(self.openmovie + '.cuts') == 0:
                self.SelectFramework()
            else:
                self.session.openWithCallback(self.ClearCuts, MessageBox, _("Do you want to resume this playback?"), timeout=10, default=True)

    def ClearCuts(self, ret):
        if ret == False:
            resetMoviePlayState(self.openmovie + '.cuts')
        self.SelectFramework()

    def SelectFramework(self):
        if myConfig.MultiFramework.value == "select":
            from Screens.ChoiceBox import ChoiceBox
            self.session.openWithCallback(self.SelectedFramework, ChoiceBox, title = _("Select Multiframework"), list = getChoicesList())
        else:
            if self.openmovie.endswith('.ts'):
                self.rootID = '1'
            else:
                self.rootID = myConfig.MultiFramework.value
            self.StartPlayer()

    def SelectedFramework(self, ret):
        if ret:
            self.rootID = ret[1]
            printDEBUG("Selected framework: " + ret[1])
        self.StartPlayer()
      
    def StartPlayer(self):
        self.lastOPLIsetting = None
        
        if not path.exists(self.opensubtitle) and not self.opensubtitle.startswith("http://"):
            self.opensubtitle = ""
        if path.exists(self.openmovie) or self.openmovie.startswith("http://"):
            if myConfig.SRTplayer.value =="system":
                try: 
                    self.lastOPLIsetting = config.subtitles.pango_autoturnon.value
                    config.subtitles.pango_autoturnon.value = True
                except:
                    pass
                self.session.openWithCallback(self.ExitPlayer,AdvancedFreePlayer,self.openmovie,'',self.rootID,self.LastPlayedService,self.URLlinkName,self.movieTitle)
                return
            else:
                try: 
                    self.lastOPLIsetting = config.subtitles.pango_autoturnon.value
                    config.subtitles.pango_autoturnon.value = False
                    printDEBUG("OpenPLI subtitles disabled")
                except:
                    printDEBUG("pango_autoturnon non existent, is it VTI?")

                self.session.openWithCallback(self.ExitPlayer,AdvancedFreePlayer,self.openmovie,self.opensubtitle,self.rootID,self.LastPlayedService,self.URLlinkName,self.movieTitle)
                return
        else:
            printDEBUG("StartPlayer>>> File %s does not exist :(" % self.openmovie)
     
    def ExitPlayer(self):
        if self.lastOPLIsetting is not None:
            config.subtitles.pango_autoturnon.value = self.lastOPLIsetting
        myConfig.PlayerOn.value = False
        self.close()
##################################################################### CLASS END #####################################################################

class AdvancedFreePlayerStart(Screen):

    def __init__(self, session):
        #printDEBUG("AdvancedFreePlayerStart >>>")
        self.openmovie = ''
        self.opensubtitle = ''
        self.URLlinkName = ''
        self.movietxt = _('Movie: ')
        self.subtitletxt = _('Subtitle: ')
        self.rootID = myConfig.MultiFramework.value
        self.LastPlayedService = None
        self.LastFolderSelected = None
        self.movieTitle = ''
        self.gettingDataFromWEB = False
        self.ShowDelay = 100
  
        self.skin  = LoadSkin("AdvancedFreePlayerStart")
        
        Screen.__init__(self, session)
        self["info"] = Label()
        self["myPath"] = Label(myConfig.FileListLastFolder.value)
        
        self["filemovie"] = Label(self.movietxt)
        self["filesubtitle"] = Label(self.subtitletxt)
        if myConfig.KeyOK.value == "playmovie":
            self["filemovie"].hide()
            self["filesubtitle"].hide()
            
        self["key_red"] = StaticText()
        from PlayWithdmnapi import KeyMapInfo #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        self["Description"] = Label(KeyMapInfo)
        self["Cover"] = Pixmap()
        
        if path.exists(ExtPluginsPath + '/DMnapi/DMnapi.pyo') or path.exists(ExtPluginsPath +'/DMnapi/DMnapi.pyc') or path.exists(ExtPluginsPath +'/DMnapi/DMnapi.py'):
            self.DmnapiInstalled = True
            self["key_green"] = StaticText(_("DMnapi"))
        else:
            self.DmnapiInstalled = False
            self["key_green"] = StaticText(_("Install DMnapi"))
            
        self["key_yellow"] = StaticText(_("Config"))
        if myConfig.FileListSort.value == 'date':
            self["key_blue"] = StaticText(_("Sort by date"))
            self.sortDate = True
        else:
            self["key_blue"] = StaticText(_("Sort by name"))
            self.sortDate = False
        self["info"].setText(PluginName + ' ' + PluginInfo)
        
        self.matchingPattern = ""
        for myExtension in EXTENSIONS:
            print myExtension, EXTENSIONS[myExtension]
            if EXTENSIONS[myExtension] == "movie":
                self.matchingPattern += "|" + myExtension
            elif myConfig.ShowMusicFiles.value == True and  EXTENSIONS[myExtension] == "music":
                self.matchingPattern += "|" + myExtension
            elif myConfig.ShowPicturesFiles.value == True and  EXTENSIONS[myExtension] == "picture":
                self.matchingPattern += "|" + myExtension
            elif myConfig.TextFilesOnFileList.value == True and  EXTENSIONS[myExtension] == "text":
                self.matchingPattern += "|" + myExtension
        self.matchingPattern = self.matchingPattern[1:]
        print   self.matchingPattern
        self.filelist = FileList(myConfig.FileListLastFolder.value, matchingPattern = "(?i)^.*\.(" + self.matchingPattern + ")(?!\.(cuts|ap$|meta$|sc$|wget$))",sortDate=self.sortDate)
            
        self["filelist"] = self.filelist
        self["actions"] = ActionMap(["AdvancedFreePlayerSelector"],
            {
                "selectFile": self.selectFile,
                "ExitPlayer": self.ExitPlayer,
                "lineUp": self.lineUp,
                "lineDown": self.lineDown,
                "pageUp": self.pageUp,
                "pageDown": self.pageDown,
                "PlayMovie": self.PlayMovie,
                "runDMnapi": self.runDMnapi,
                "runConfig": self.runConfig,
                "setSort": self.setSort,
                "playORdelete": self.playORdelete,
            },-2)
        self.setTitle(PluginName + ' ' + PluginInfo)
        if myConfig.StopService.value == True:
            self.LastPlayedService = self.session.nav.getCurrentlyPlayingServiceReference()
            self.session.nav.stopService()
        
        self.onLayoutFinish.append(self.__onLayoutFinish)
        self.GetCoverTimer = eTimer()

    def __onLayoutFinish(self):
        self.GetCoverTimer.callback.append(self.__refreshFilelist)
        self.GetCoverTimer.start(50, True)
    
    def __refreshFilelist(self):
        self.GetCoverTimer.callback.remove(self.__refreshFilelist)
        self.GetCoverTimer.callback.append(self.GetCoverTimerCB)
        self["filelist"].changeDir(myConfig.FileListLastFolder.value)
        self["filelist"].refresh()
    
    def buttonsNames(self):
        selection = self["filelist"].getSelection()
        if selection is not None and selection[1] == True and self["filelist"].getSelectedIndex() == 0:
            self["key_red"].setText("")
        elif self.openmovie == '':
            self["key_red"].setText(_("Delete"))
        elif selection is not None and selection[1] == True and self["filelist"].getSelectedIndex() > 0:
            self["key_red"].setText(_("Delete"))
        elif selection is not None and not selection[0] in self.openmovie : # selected different file than chosen movie
            self["key_red"].setText(_("Delete"))
        else:
            self["key_red"].setText(_("Play"))
      
    def pageUp(self):
        if self["filelist"].getSelectedIndex() == 0:
            self["filelist"].moveToIndex(len(self["filelist"].getFileList())-1)
        else:
            self["filelist"].pageUp()
        self.buttonsNames()
        self.GetCoverTimer.start(self.ShowDelay,False)


    def pageDown(self):
        if self["filelist"].getSelectedIndex() == (len(self["filelist"].getFileList())-1):
            self["filelist"].moveToIndex(0)
        else:
            self["filelist"].pageDown()
        self.buttonsNames()
        self.GetCoverTimer.start(self.ShowDelay,False)

    def lineUp(self):
        if self["filelist"].getSelectedIndex() == 0:
            self["filelist"].moveToIndex(len(self["filelist"].getFileList())-1)
        else:
            self["filelist"].up()
        self.buttonsNames()
        self.GetCoverTimer.start(self.ShowDelay,False)

    def lineDown(self):
        if self["filelist"].getSelectedIndex() == (len(self["filelist"].getFileList())-1):
            self["filelist"].moveToIndex(0)
        else:
            self["filelist"].down()
        self.buttonsNames()
        self.GetCoverTimer.start(self.ShowDelay,False)

    def playORdelete(self):
        if self["key_red"].getText() == _("Play"):
            self.PlayMovie()
            return
        def deleteRet(ret):
            selection = self["filelist"].getSelection()
            if myConfig.MoveToTrash == True:
                print 'mv -f %s/%s* %s/' % (self.filelist.getCurrentDirectory(),selection[0][:-4], myConfig.TrashFolder.value)
            else:
                print 'rm -rf %s/%s*' % (self.filelist.getCurrentDirectory(),selection[0][:-4])
            print ret
            if ret:
                selection = self["filelist"].getSelection()
                if selection[1] == True: # isDir
                    printDEBUG('Deleting folder %s' % selection[0])
                    system('rm -rf "%s"' % selection[0])
                else:
                    if selection[0][-4:].lower() in ('.srt','.txt','.url'):
                        ClearMemory()
                        if myConfig.MoveToTrash == True:
                            printDEBUG('Moving file "%s/%s" to %s/' % (self.filelist.getCurrentDirectory(),selection[0], myConfig.TrashFolder.value))
                            system('mv -f "%s/%s" %s/' % (self.filelist.getCurrentDirectory(),selection[0], myConfig.TrashFolder.value))
                        else:
                            printDEBUG('Deleting file "%s/%s"' % (self.filelist.getCurrentDirectory(),selection[0]))
                            system('rm -rf "%s/%s"' % (self.filelist.getCurrentDirectory(),selection[0]))
                    else:
                        ClearMemory()
                        if myConfig.MoveToTrash == True:
                            printDEBUG('Moving files "%s/%s" to %s/' % (self.filelist.getCurrentDirectory(),selection[0][:-4], myConfig.TrashFolder.value))
                            system('mv -f "%s/%s" %s/' % (self.filelist.getCurrentDirectory(),selection[0][:-4], myConfig.TrashFolder.value))
                        else:
                            printDEBUG('Deleting files "%s/%s"*' % (self.filelist.getCurrentDirectory(),selection[0][:-4]))
                            system('rm -rf "%s/%s"*' % (self.filelist.getCurrentDirectory(),selection[0][:-4]))
            self["filelist"].refresh()
            return
        
        selection = self["filelist"].getSelection()
        if selection[1] == True: # isDir
            self.session.openWithCallback(deleteRet, MessageBox, _("Delete '%s' folder?") % selection[0], timeout=10, default=False)
        elif selection[0][-4:].lower() in ('.srt','.txt'):
            self.session.openWithCallback(deleteRet, MessageBox, _("Delete subtitles for '%s' movie?") % selection[0][:-4], timeout=10, default=False)
        elif selection[0][-4:].lower() in ('.url'):
            self.session.openWithCallback(deleteRet, MessageBox, _("Delete link for '%s' movie?") % selection[0][:-4], timeout=10, default=False)
        else:
            self.session.openWithCallback(deleteRet, MessageBox, _("Delete '%s' movie?") % selection[0][:-4], timeout=10, default=False)
      
    def PlayMovie(self):
        if not self.openmovie == "":
            if myConfig.StoreLastFolder == True:
                myConfig.FileListLastFolder.value =  self["myPath"].getText()
                myConfig.FileListLastFolder.save()
            print self["myPath"].getText()
            self.lastPosition, Length = getCut(self.openmovie + '.cuts') #returns in mins
            if self.lastPosition < 1:
                self.SelectFramework()
            else:
                self.session.openWithCallback(self.ClearCuts, MessageBox, _("Do you want to resume this playback?"), timeout=10, default=True)

    def ClearCuts(self, ret):
        if ret == False:
            resetMoviePlayState(self.openmovie + '.cuts')
            self.lastPosition = 0
        self.SelectFramework()

    def SelectFramework(self):
        if myConfig.MultiFramework.value == "select":
            from Screens.ChoiceBox import ChoiceBox
            self.session.openWithCallback(self.SelectedFramework, ChoiceBox, title = _("Select Multiframework"), list = getChoicesList())
        else:
            if self.openmovie.endswith('.ts'):
                self.rootID = '1'
            elif self.openmovie.endswith('.flac') or self.openmovie.endswith('.fla'):
                self.rootID = '4099'
            else:
                self.rootID = myConfig.MultiFramework.value
            self.StartPlayer()

    def SelectedFramework(self, ret):
        if ret:
            self.rootID = ret[1]
            printDEBUG("Selected framework: " + ret[1])
        self.StartPlayer()
      
    def StartPlayer(self):
        lastOPLIsetting = None
        
        def EndPlayer():
            if lastOPLIsetting is not None:
                config.subtitles.pango_autoturnon.value = lastOPLIsetting
            self["filelist"].refresh()
            self.openmovie = ''
            self.opensubtitle = ''

        if not path.exists(self.opensubtitle) and not self.opensubtitle.startswith("http://"):
            self.opensubtitle = ""
            
        if path.exists(self.openmovie) or self.openmovie.startswith("http://"):
            if myConfig.SRTplayer.value =="system":
                printDEBUG("PlayWithSystem title:'%s' filename:'%s'" %(self.movieTitle,self.openmovie))
                from PlayWithSystem import AdvancedFreePlayer
            else:
                try: 
                    lastOPLIsetting = config.subtitles.pango_autoturnon.value
                    config.subtitles.pango_autoturnon.value = False
                    printDEBUG("OpenPLI subtitles disabled")
                except:
                    printDEBUG("pango_autoturnon non existent, is it VTI?")
                if myConfig.SRTplayer.value =="plugin-SubsSupport":
                    printDEBUG("PlayWithsubsupport title:'%s' filename:'%s'" %(self.movieTitle,self.openmovie))
                    from PlayWithsubsupport import AdvancedFreePlayer
                else:
                    printDEBUG("PlayWithdmnapi title:'%s' filename:'%s'" %(self.movieTitle,self.openmovie))
                    from PlayWithdmnapi import AdvancedFreePlayer
            #initiate player
            self.session.openWithCallback(EndPlayer,AdvancedFreePlayer,self.openmovie,self.opensubtitle,
                                            self.rootID,self.LastPlayedService,self.URLlinkName,
                                            self.movieTitle, self.lastPosition * 90 * 1000 * 60)
            return
        else:
            printDEBUG("StartPlayer>>> File %s does not exist :(" % self.openmovie)

    def runConfig(self):
        from AFPconfig import AdvancedFreePlayerConfig
        self.session.open(AdvancedFreePlayerConfig)
        return

    def setSort(self):
        if self.sortDate:
            #print "sortDate=False"
            self["filelist"].sortDateDisable()
            self.sortDate=False
            self["key_blue"].setText(_("Sort by name"))
        else:
            #print "sortDate=True"
            self["filelist"].sortDateEnable()
            self.sortDate=True
            self["key_blue"].setText(_("Sort by date"))
        self["filelist"].refresh()

    def selectFile(self):
        selection = self["filelist"].getSelection()
        if selection[1] == True: # isDir
            if selection[0] is not None and self.filelist.getCurrentDirectory() is not None and \
                    len(selection[0]) > len(self.filelist.getCurrentDirectory()) or self.LastFolderSelected == None:
                self.LastFolderSelected = selection[0]
                self["filelist"].changeDir(selection[0], "FakeFolderName")
            else:
                print "Folder Down"
                self["filelist"].changeDir(selection[0], self.LastFolderSelected)
            
            d = self.filelist.getCurrentDirectory()
            if d is None:
                d=""
            elif not d.endswith('/'):
                d +='/'
            #self.title = d
            self["myPath"].setText(d)
        else:
            d = self.filelist.getCurrentDirectory()
            if d is None:
                d=""
            elif not d.endswith('/'):
                d +='/'
            f = self.filelist.getFilename()
            printDEBUG("self.selectFile>> " + d + f)
            temp = self.getExtension(f)
            #print temp
            if temp == ".url":
                self.opensubtitle = ''
                self.openmovie = ''
                with open(d + f,'r') as UrlContent:
                    for data in UrlContent:
                        print data
                        if data.find('movieURL=') > -1: #find instead of startswith to avoid BOM issues ;)
                            self.openmovie = data.split('=')[1].strip()
                            self.URLlinkName = d + f
                        elif data.find('srtURL=') > -1:
                            self.opensubtitle = data.split('=')[1].strip()
                if self["filemovie"].getText() != (self.movietxt + self.openmovie):
                    self["filemovie"].setText(self.movietxt + self.openmovie)
                    self["filesubtitle"].setText(self.subtitletxt + self.opensubtitle)
                elif myConfig.KeyOK.value == 'play':
                    self.PlayMovie()
                    return
                else:
                    self.openmovie = ''
                    self["filemovie"].setText(self.movietxt)
                    self.opensubtitle = ''
                    self["filesubtitle"].setText(self.subtitletxt + self.opensubtitle)
            elif temp == ".srt" or temp == ".txt":
                #if self.DmnapiInstalled == True:
                if self.opensubtitle == (d + f): #clear subtitles selection
                    self["filesubtitle"].setText(self.subtitletxt)
                    self.opensubtitle = ''
                else:
                    self["filesubtitle"].setText(self.subtitletxt + f)
                    self.opensubtitle = d + f
            else:
                if self.openmovie == (d + f):
                    if myConfig.KeyOK.value == 'play':
                        self.PlayMovie()
                        return
                    else:
                        self.openmovie = ''
                        self["filemovie"].setText(self.movietxt)
                else:
                    self.openmovie = d + f
                    self.URLlinkName = ''
                    if myConfig.KeyOK.value == "playmovie":
                        self.setSubtitles(d + f)
                        self.PlayMovie()
                        return
                    self["filemovie"].setText(self.movietxt + f)
                
                #if self.DmnapiInstalled == True:
                self.setSubtitles(d + f)
        self.buttonsNames()
        
    def setSubtitles(self, movieNameWithPath = ''):
        if movieNameWithPath == '':
            self["filesubtitle"].setText(self.subtitletxt)
            self.opensubtitle = ''
        elif path.exists( movieNameWithPath[:-4] + ".srt"):
            self["filesubtitle"].setText(movieNameWithPath[:-4] + ".srt")
            self.opensubtitle = movieNameWithPath[:-4] + ".srt"
        elif path.exists( movieNameWithPath[:-4] + ".txt"):
            self["filesubtitle"].setText(movieNameWithPath[:-4] + ".txt")
            self.opensubtitle = movieNameWithPath[:-4] + ".txt"
        else:
            self["filesubtitle"].setText(self.subtitletxt)
            self.opensubtitle = ''
      
    def getExtension(self, MovieNameWithExtension):
        return path.splitext( path.basename(MovieNameWithExtension) )[1]
      
    def SetLocalDescriptionAndCover(self, MovieNameWithPath):
        FoundCover = False
        FoundDescr = False
        if MovieNameWithPath == '':
            self["Description"].setText('')
            return FoundCover, FoundDescr
        
        temp = getNameWithoutExtension(MovieNameWithPath)
        WebCoverFile='/tmp/%s.AFP.jpg' % getNameWithoutExtension(self.filelist.getFilename())
        ### COVER ###
        if path.exists(temp + '.jpg'):
            self["Cover"].instance.setScale(1)
            self["Cover"].instance.setPixmap(LoadPixmap(path=temp + '.jpg'))
            self["Cover"].show()
            FoundCover = True
        elif path.exists(WebCoverFile) and myConfig.PermanentCoversDescriptons.value == False:
            self["Cover"].instance.setScale(1)
            self["Cover"].instance.setPixmap(LoadPixmap(path=WebCoverFile))
            self["Cover"].show()
            FoundCover = True
        else:
            self["Cover"].hide()
        WebDescrFile='/tmp/%s.AFP.txt' % getNameWithoutExtension(self.filelist.getFilename())
        ### DESCRIPTION from EIT ###
        if path.exists(temp + '.eit'):
            def parseMJD(MJD):
                # Parse 16 bit unsigned int containing Modified Julian Date,
                # as per DVB-SI spec
                # returning year,month,day
                YY = int( (MJD - 15078.2) / 365.25 )
                MM = int( (MJD - 14956.1 - int(YY*365.25) ) / 30.6001 )
                D  = MJD - 14956 - int(YY*365.25) - int(MM * 30.6001)
                K=0
                if MM == 14 or MM == 15: K=1
                return "%02d/%02d/%02d" % ( (1900 + YY+K), (MM-1-K*12), D)

            def unBCD(byte):
                return (byte>>4)*10 + (byte & 0xf)

            import struct

            with open(temp + '.eit','r') as descrTXT:
                data = descrTXT.read() #[19:].replace('\00','\n')
                ### Below is based on EMC handlers, thanks to author!!!
                e = struct.unpack(">HHBBBBBBH", data[0:12])
                myDescr = _('Recorded: %s %02d:%02d:%02d\n') % (parseMJD(e[1]), unBCD(e[2]), unBCD(e[3]), unBCD(e[4]) )
                myDescr += _('Lenght: %02d:%02d:%02d\n\n') % (unBCD(e[5]), unBCD(e[6]), unBCD(e[7]) )
                extended_event_descriptor = []
                EETtxt = ''
                pos = 12
                while pos < len(data):
                    rec = ord(data[pos])
                    length = ord(data[pos+1]) + 2
                    if rec == 0x4E:
                    #special way to handle CR/LF charater
                        for i in range (pos+8,pos+length):
                            if str(ord(data[i]))=="138":
                                extended_event_descriptor.append("\n")
                            else:
                                if data[i]== '\x10' or data[i]== '\x00' or  data[i]== '\x02':
                                    pass
                                else:
                                    extended_event_descriptor.append(data[i])
                    pos += length

                    # Very bad but there can be both encodings
                    # User files can be in cp1252
                    # Is there no other way?
                EETtxt = "".join(extended_event_descriptor)
                if EETtxt:
                    try:
                        EETtxt.decode('utf-8')
                    except UnicodeDecodeError:
                        try:
                            EETtxt = EETtxt.decode("cp1250").encode("utf-8")
                        except UnicodeDecodeError:
                            # do nothing, otherwise cyrillic wont properly displayed
                            #extended_event_descriptor = extended_event_descriptor.decode("iso-8859-1").encode("utf-8")
                            pass
                
                self["Description"].setText(myDescr + ConvertChars(EETtxt) )
                FoundDescr = True
        ### DESCRIPTION from TXT ###
        elif path.exists(temp + '.txt'):
            with open(temp + '.txt','r') as descrTXT:
                myDescr = descrTXT.read()
                if len(myDescr) < 4 or myDescr[0] == "{" or myDescr[0] =="[" or myDescr[1] == ":" or myDescr[2] == ":":
                    self["Description"].setText('')
                else:
                    self["Description"].setText(myDescr)
                    FoundDescr = True
        elif path.exists(WebDescrFile) and myConfig.PermanentCoversDescriptons.value == False:
            with open(WebDescrFile,'r') as descrTXT:
                myDescr = descrTXT.read()
                if len(myDescr) < 4 or myDescr[0] == "{" or myDescr[0] =="[" or myDescr[1] == ":" or myDescr[2] == ":":
                    self["Description"].setText('')
                else:
                    self["Description"].setText(myDescr)
                    FoundDescr = True
        else:
            self["Description"].setText('')
            FoundDescr = False
        #print "Na koniec SetLocalDescriptionAndCover wartosci FoundCover=", FoundCover ,", FoundDescr=", FoundDescr
        return FoundCover, FoundDescr
    
    def ExitPlayer(self):
        if self.LastPlayedService:
            self.session.nav.playService(self.LastPlayedService)
        self.openmovie = None
        self.opensubtitle = None
        self.URLlinkName = None
        self.movietxt = None
        self.subtitletxt = None
        self.rootID = None
        self.LastPlayedService = None
        self.LastFolderSelected= None
        self.movieTitle = None
        self["Description"].setText('')
        ClearMemory() #just in case for nbox, where we have limited RAM
        system('(rm -rf /tmp/*.AFP.*;mkdir -p %s) &' % myConfig.TrashFolder.value)
        myConfig.PlayerOn.value = False
        configfile.save()
        self.close()
        
    def GetCoverTimerCB(self, AlternateMovieName = ''):
        self.GetCoverTimer.stop()
        #first we check if file selected, if no, cleaning everything
        if self["filelist"].getSelection()[1] == True: # isDir
            self["Cover"].hide()
            self["Description"].setText('')
            return
        extension = self.getExtension(self.filelist.getFilename())[1:]
        if not EXTENSIONS.has_key(extension) or EXTENSIONS[extension] != "movie":
            self["Cover"].hide()
            self["Description"].setText('')
            return
            
        ClearMemory() #just in case for nbox, where we have limited RAM
           
        ### LOCAL Descriptions and Covers###
        if AlternateMovieName == '':
            FoundCover, FoundDescr = self.SetLocalDescriptionAndCover(self.filelist.getCurrentDirectory() + self.filelist.getFilename())
            myMovie, movieYear =cleanFile(self.filelist.getFilename())
            self.movieTitle = myMovie
            if (FoundCover and FoundDescr) or myConfig.AutoDownloadCoversDescriptions.value == False: #no need to download data if both found locally ;)
                return
        else:
            myMovie, movieYear =cleanFile(myMovie=AlternateMovieName)
            self.movieTitle = myMovie
        
        if myConfig.AutoDownloadCoversDescriptions.value == False:
            return
        #print "Status covera i opisu:" , FoundCover,FoundDescr
        try:
            from twisted.web.client import getPage
            from twisted.web.client import downloadPage
            from twisted.web import client, error as weberror
            #from twisted.internet import defer, reactor
            #from urllib import urlencode
        except:
            printDEBUG("Error importing twisted. Something wrong with the image?")
            self["Description"].setText(_("Error importing twisted package. Seems something wrong with the image. :("))
            return
        # checking if network connection is working
        try:
            import socket
            socket.setdefaulttimeout(0.5)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(('8.8.8.8', 53))#connection with google dns service
        except:
            printDEBUG("Error no internet connection.")
            self["Description"].setText(_("No internet connection. :("))
            return
            
        def WebCover(ret):
            print "[AdvancedFreePlayer] WebCover >>>"
            self.gettingDataFromWEB = False
            self["Cover"].instance.setScale(1)
            self["Cover"].instance.setPixmap(LoadPixmap(path=WebCoverFile))
            self["Cover"].show()
            return
        def dataError(error = ''):
            printDEBUG("Error downloading data %s" % str(error))
            self.gettingDataFromWEB = False
            return
            
        def readTmBD(data, movieYear, isMovie):
            #print 'readTmBD'
            f = open('/tmp/TmBD.AFP.webdata', 'w')
            f.write(data)
            f.close
            if isMovie == True:
                try: 
                    list = json.loads(data)
                except:
                    self.gettingDataFromWEB = False
                    return
                data=None # some cleanup, just in case
                if 'total_results' in list:
                    coverPath=''
                    overview=''
                    release_date=''
                    id=''
                    otitle=''
                    original_language=''
                    title=''
                    popularity=''
                    vote_average=''
                    for myItem in list['results']:
                        coverPath=myItem['poster_path'].encode('ascii','ignore')
                        overview=myItem['overview']
                        release_date=myItem['release_date']
                        id=myItem['id']
                        otitle=myItem['original_title']
                        original_language=myItem['original_language']
                        title=myItem['title']
                        popularity='{:.2f}'.format(myItem['popularity'])
                        vote_average='{:.2f}'.format(myItem['vote_average'])
                        if movieYear != '':
                            printDEBUG("filtering movies list by release year %s" % movieYear)
                            if movieYear in release_date:
                                printDEBUG("filtered movies list by release year %s" % movieYear)
                                break
                    if coverPath != '':
                        coverUrl = "http://image.tmdb.org/t/p/%s%s" % (myConfig.coverfind_themoviedb_coversize.value, coverPath)
                        coverUrl = coverUrl.replace('\/','/')
                    Pelny_opis=overview + '\n\n' + _('Released: ') + release_date + '\n' + \
                                                _('Original title: ') + otitle +'\n' + _('Original language: ') + \
                                                original_language +'\n' + _('Popularity: ') + popularity + '\n' + \
                                                _('Score: ') + vote_average + '\n'
                    printDEBUG("========== Dane filmu %s ==========\nPlakat: %s,\n%s\n====================" %(title, coverUrl,Pelny_opis))
                    printDEBUG(WebDescrFile)
                    if not path.exists(WebDescrFile) and Pelny_opis.strip() != '':
                        with open(WebDescrFile, 'w') as WDF:
                            WDF.write(Pelny_opis)
                            WDF.close()
                    if FoundDescr == False:
                        printDEBUG("FoundDescr == False")
                        with open(WebDescrFile,'r') as descrTXT:
                            myDescr = descrTXT.read()
                            self["Description"].setText(myDescr)
                    if FoundCover == False: #no need to download cover, if we have it. ;)
                        downloadPage(coverUrl,WebCoverFile).addCallback(WebCover).addErrback(dataError)
                
                else:
                    self.gettingDataFromWEB = False
                    return
            else:
                list = re.findall('<seriesid>(.*?)</seriesid>.*?<language>(.*?)</language>.*?<SeriesName>(.*?)</SeriesName>.*?<Overview>(.*?)</Overview>.*?<FirstAired>(.*?)</FirstAired>.*?<Network>(.*?)</Network>', data, re.S)
                if list is not None and len(list)>0:
                    #print">>>>>>>>>>>>>>>>>>>>>>>>>",list
                    idx = 0
                    if movieYear != '':
                        printDEBUG("filtering series list by release year %s" % movieYear)
                        for coverPath,overview,release_date,id,otitle,original_language,title,popularity,vote_average in list:
                            if movieYear in release_date:
                                break
                            else:
                                idx += 1
                                
                    seriesid, original_language, SeriesName, overview, FirstAired, Network = list[idx]
                    coverUrl = "http://www.thetvdb.com/banners/_cache/posters/%s-1.jpg" % str(seriesid)
                    if FoundDescr == False:
                        printDEBUG("FoundDescr == False1")
                        self["Description"].setText(overview + '\n\n' + _('Released: ') + FirstAired + '\n' + _('Original title: ') + SeriesName +'\n' + _('Original language: ') + \
                                                    original_language +'\n' + _('Network: ') + Network + '\n')
                        with open(WebDescrFile, 'w') as WDF:
                            WDF.write(self["Description"].getText() )
                            WDF.close()
                    if FoundCover == False: #no need to download cover, if we have it. ;)
                        downloadPage(coverUrl,WebCoverFile).addCallback(WebCover).addErrback(dataError)
                else:
                    self.gettingDataFromWEB = False
                    return
        
        #start >>>
        myMovie=DecodeNationalLetters(myMovie).replace(' ','%20').replace('&', '%26')
        if myConfig.PermanentCoversDescriptons.value == True:
            WebCoverFile='%s/%s.jpg' % (self.filelist.getCurrentDirectory(), getNameWithoutExtension(self.filelist.getFilename()) )
            WebDescrFile='%s/%s.txt' % (self.filelist.getCurrentDirectory(), getNameWithoutExtension(self.filelist.getFilename()) )
        else:
            WebCoverFile='/tmp/%s.AFP.jpg' % getNameWithoutExtension(self.filelist.getFilename())
            WebDescrFile='/tmp/%s.AFP.txt' % getNameWithoutExtension(self.filelist.getFilename())
            
        if re.search('[Ss][0-9]+[Ee][0-9]+', myMovie):
            seriesName=re.sub('[Ss][0-9]+[Ee][0-9]+.*','', myMovie, flags=re.I)
            url = "http://thetvdb.com/api/GetSeries.php?seriesname=%s&language=%s" % (seriesName.replace('.','%20').replace(' ','%20'),myConfig.coverfind_language.value)
            isMovie = False
        else:
            url = "http://api.themoviedb.org/3/search/movie?api_key=8789cfd3fbab7dccf1269c3d7d867aff&query=%s&language=%s" % (myMovie,myConfig.coverfind_language.value)
            isMovie = True
        if self.gettingDataFromWEB == True:
            printDEBUG("[GetFromTMDBbyName] getPage running, skip '%s'this time" % url) #DEBUG
        else:
            printDEBUG("[GetFromTMDBbyName] url: " + url) #DEBUG
            self.gettingDataFromWEB = True
            getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(readTmBD,movieYear,isMovie).addErrback(dataError)
        
##################################################################### SUBTITLES >>>>>>>>>>
    def runDMnapi(self):
        if self.DmnapiInstalled == True:
            self.DMnapi()
            self["filelist"].refresh()
        else:
            def doNothing():
                pass
            def goUpdate(ret):
                if ret is True:
                    runlist = []
                    runlist.append( ('chmod 755 %sUpdate*.sh' % PluginPath) )
                    runlist.append( ('cp -a %sUpdateDMnapi.sh /tmp/AFPUpdate.sh' % PluginPath) ) #to have clear path of updating this script too ;)
                    runlist.append( ('/tmp/AFPUpdate.sh %s "%s"' % (config.plugins.AdvancedFreePlayer.Version.value,PluginInfo)) )
                    from AFPconfig import AdvancedFreePlayerConsole
                    self.session.openWithCallback(doNothing, AdvancedFreePlayerConsole, title = _("Installing DMnapi plugin"), cmdlist = runlist)
                    return
            self.session.openWithCallback(goUpdate, MessageBox,_("Do you want to install DMnapi plugin?"),  type = MessageBox.TYPE_YESNO, timeout = 10, default = False)
        return

    def DMnapi(self):
        if not self["filelist"].canDescent():
            f = self.filelist.getFilename()
            temp = f[-4:]
            if temp != ".srt" and temp != ".txt":
                curSelFile = self["filelist"].getCurrentDirectory() + self["filelist"].getFilename()
                try:
                    from Plugins.Extensions.DMnapi.DMnapi import DMnapi
                    self.session.openWithCallback(self.dmnapiCallback, DMnapi, curSelFile)
                except:
                    printDEBUG("Exception loading DMnapi!!!")
            else:
                self.session.open(MessageBox,_("Please select movie files !\n\n"),MessageBox.TYPE_INFO)
                return

    def dmnapiCallback(self, answer=False):
        self["filelist"].refresh()
        
    def createSummary(self):
        return AdvancedFreePlayerStartLCD
##################################################################### LCD Screens <<<<<<<<<<<<<<<<<<<<<<<<<<<<<
class AdvancedFreePlayerStartLCD(Screen):
    skin = LoadSkin('AdvancedFreePlayerStartLCD')
                

##################################################################### CLASS ENDS <<<<<<<<<<<<<<<<<<<<<<<<<<<<<
