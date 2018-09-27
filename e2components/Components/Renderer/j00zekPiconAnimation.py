#######################################################################
#
#    Renderer for Enigma2
#    Coded by j00zek (c)2018
#
#    Uszanuj moja prace i nie kasuj/zmieniaj informacji kto jest autorem renderera
#    Please respect my work and don't delete/change name of the renderer author
#
#    This program is free software; you can redistribute it and/or
#    modify it under the terms of the GNU General Public License
#    as published by the Free Software Foundation; either version 2
#    of the License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#    
#    To use it do the following:
#       - download package of animated picons, for example from my opkg
#       - write them in the animatedPicons folder on mounted device or in /usr/share/enigma2/
#             NOTE:if you want to use any other folder, you need to specify it in widget definition. E.g. pixmaps="animatedPicons/Flara/"
#       - include J00zekPiconAnimation widget in the infobar skin definition.
#             E.g. <widget source="session.CurrentService" render="j00zekPiconAnimation" position="30,30" size="220,132" zPosition="5" transparent="1" alphatest="blend" />
#             NOTE:
#                  -  position="X,Y" should be the same like position of a picon in skin definition
#                  -  size="X,Y" should be the same like size of a picon in skin definition
#                  -  zPosition="Z" should be bigger than zPosition of a picon in skin definition, to display animation over the picon.
#
####################################################################### 
from Tools.LoadPixmap import LoadPixmap
from Components.Pixmap import Pixmap
from Renderer import Renderer
from enigma import ePixmap, eTimer
from Tools.Directories import fileExists, SCOPE_SKIN_IMAGE, SCOPE_CURRENT_SKIN, resolveFilename
from Components.config import config
from Components.Harddisk import harddiskmanager
import os

##### write log in /tmp folder #####
DBG = True
try:
    from Components.j00zekComponents import j00zekDEBUG
except Exception:
    def j00zekDEBUG(myText=None):
        if not myText is None:
            print(myText)
#####

searchPaths = ['/usr/share/enigma2/']

def initPiconPaths():
    if DBG: j00zekDEBUG('[j00zekPiconAnimation]:[initPiconPaths] >>>')
    for part in harddiskmanager.getMountedPartitions():
        addPiconPath(part.mountpoint)
    if os.path.exists("/proc/mounts"):
        with open("/proc/mounts", "r") as f:
            for line in f:
                if line.startswith('/dev/sd'):
                    mountpoint = line.split(' ')[1]
                    addPiconPath(mountpoint)

def addPiconPath(mountpoint):
    if DBG: j00zekDEBUG('[j00zekPiconAnimation]:[addPiconPath] >>> mountpoint=' + mountpoint)
    if mountpoint == '/':
        return
    global searchPaths
    try:
        if mountpoint not in searchPaths:
            if DBG: j00zekDEBUG('j00zekPiconAnimation]:[addPiconPath] mountpoint not in searchPaths')
            for pp in os.listdir(mountpoint):
                lpp = os.path.join(mountpoint, pp) + '/'
                if pp.find('picon') >= 0 and os.path.isdir(lpp): #any folder *picon*
                    for pf in os.listdir(lpp):
                        if pf.endswith('.png') and mountpoint not in searchPaths: #if containf *.png
                            if mountpoint.endswith('/'):
                                searchPaths.append(mountpoint)
                            else:
                                searchPaths.append(mountpoint + '/')
                            if DBG: j00zekDEBUG('[j00zekPiconAnimation]:[addPiconPath] mountpoint appended to searchPaths')
                            break
                    else:
                        continue
                    break
    except Exception, e:
        if DBG: j00zekDEBUG('[j00zekPiconAnimation]:[addPiconPath] Exception:' + str(e))

def onPartitionChange(why, part):
    if DBG: j00zekDEBUG('[j00zekPiconAnimation]:[onPartitionChange] >>>')
    global searchPaths
    if why == 'add' and part.mountpoint not in searchPaths:
        addPiconPath(part.mountpoint)
    elif why == 'remove' and part.mountpoint in searchPaths:
        searchPaths.remove(part.mountpoint)

class j00zekPiconAnimation(Renderer):
    __module__ = __name__

    def __init__(self):
        Renderer.__init__(self)
        self.pixmaps = 'animatedPicons'
        self.pixdelay = 50
        self.doAnim = False
        self.animCounter = 0
        self.count = 0
        self.slideIcon = 0
        self.pixstep = 1
        self.pics = []
        self.animTimer = eTimer()
        self.animTimer.callback.append(self.timerEvent)
        self.what = ['CHANGED_DEFAULT','CHANGED_ALL','CHANGED_CLEAR','CHANGED_SPECIFIC','CHANGED_POLL']

    def applySkin(self, desktop, parent):
        if DBG: j00zekDEBUG('[j00zekPiconAnimation]:[applySkin] >>>')
        #Load attribs
        attribs = []
        for attrib, value in self.skinAttributes:
            if attrib == 'pixmaps':
                self.pixmaps = value
            elif attrib == 'pixdelay':
                self.pixdelay = int(value)
                if self.pixdelay < 50:
                    self.pixdelay = 50
            else:
                attribs.append((attrib, value))

        self.skinAttributes = attribs
        #Load animation into memory
        for path in searchPaths:
            if os.path.exists(os.path.join(path, self.pixmaps)):
                self.pixmaps = os.path.join(path, self.pixmaps)
                pngfiles = [f for f in os.listdir(self.pixmaps) if (os.path.isfile(os.path.join(self.pixmaps, f)) and f.endswith(".png"))]
                pngfiles.sort()
                for x in pngfiles:
                    if DBG: j00zekDEBUG('[j00zekPiconAnimation] read image %s' % os.path.join(self.pixmaps, x))
                    self.pics.append(LoadPixmap(os.path.join(self.pixmaps, x)))
                if len(self.pics) > 1:
                    self.count = len(self.pics)
                    self.doAnim = True
                break
        if DBG: j00zekDEBUG('[j00zekPiconAnimation]:[applySkin] Loaded pics=%s, path=%s, pixdelay=%s, step=%s' % (self.count,self.pixmaps,self.pixdelay,self.pixstep))
        return Renderer.applySkin(self, desktop, parent)

    GUI_WIDGET = ePixmap

    def postWidgetCreate(self, instance):
        if DBG: j00zekDEBUG('[j00zekPiconAnimation]:[postWidgetCreate] >>>')
#self.changed((self.CHANGED_DEFAULT,))
        return

    def preWidgetRemove(self, instance):
        if DBG: j00zekDEBUG('[j00zekPiconAnimation]:[preWidgetRemove] >>>')
        if not self.animTimer is None:
            self.animTimer.stop()
            self.animTimer.callback.remove(self.timerEvent)
            self.animTimer = None

    def connect(self, source):
        Renderer.connect(self, source)

    def doSuspend(self, suspended):
        if DBG: j00zekDEBUG('[j00zekPiconAnimation]:[doSuspend] >>> suspended=%s' % suspended)
        if suspended:
        	self.changed((self.CHANGED_CLEAR,))
        else:
        	self.changed((self.CHANGED_DEFAULT,))
            
    def changed(self, what):
        if DBG: j00zekDEBUG('[j00zekPiconAnimation]:[changed] >>>')
        if self.instance:
            if DBG: j00zekDEBUG('\t\t what[0]=%s(%s), self.doAnim=%s' % (self.what[int(what[0])], what[0], self.doAnim))
            if what[0] == self.CHANGED_CLEAR:
                if not self.animTimer is None: self.animTimer.stop()
                self.instance.hide()
                self.slideIcon = 0
                self.doAnim = True
            elif self.doAnim == True:
                self.doAnim = False
                self.slideIcon = 0
                self.instance.show()
                self.animTimer.start(self.pixdelay, True)

    def timerEvent(self):
        if DBG: j00zekDEBUG('[j00zekPiconAnimation]:[timerEvent] >>> self.slideIcon=%s' % self.slideIcon)
        self.animTimer.stop()
        if self.slideIcon < self.count:
            self.instance.setPixmap(self.pics[self.slideIcon])
            self.slideIcon = self.slideIcon + self.pixstep
            if self.slideIcon > self.count: self.slideIcon = self.count
            self.animTimer.start(self.pixdelay, True)
        elif self.slideIcon == self.count: #Note last frame does NOT exists
            if DBG: j00zekDEBUG('\t\t stop animation')
            self.instance.hide()
            self.doAnim = True
            self.animCounter = self.animCounter + 1
        if DBG: j00zekDEBUG('[j00zekPiconAnimation]:[timerEvent] <<<')

harddiskmanager.on_partition_list_change.append(onPartitionChange)
initPiconPaths()