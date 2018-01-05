# standard Picon.py modified by @j00zek to support any picon folder name
# the name can be defined in xml by puttin attri picontype="<foldername>"
# e.g. picontype="zzpicon"
import os, re, unicodedata
from Renderer import Renderer
from enigma import ePixmap, ePicLoad
from Tools.Alternatives import GetWithAlternative
from Tools.Directories import pathExists, SCOPE_SKIN_IMAGE, resolveFilename
try:
    from Tools.Directories import SCOPE_CURRENT_SKIN
except Exception:
    from Tools.Directories import SCOPE_ACTIVE_SKIN as SCOPE_CURRENT_SKIN

from Components.Harddisk import harddiskmanager
from ServiceReference import ServiceReference
from Components.config import config, ConfigBoolean
searchPaths = ['/usr/share/enigma2/']
lastPiconsDict = {}
piconType = 'picon'

def initPiconPaths():
    for part in harddiskmanager.getMountedPartitions():
        addPiconPath(part.mountpoint)

def addPiconPath(mountpoint):
    if mountpoint == '/':
        return
    global searchPaths
    try:
        if mountpoint not in searchPaths:
            for pp in os.listdir(mountpoint):
                lpp = os.path.join(mountpoint, pp) + '/'
                if pp.find('picon') >= 0 and os.path.isdir(lpp): #any folder *picon*
                    for pf in os.listdir(lpp):
                        if pf.endswith('.png') and mountpoint not in searchPaths: #if containf *.png
                            if mountpoint.endswith('/'):
                                searchPaths.append(mountpoint)
                            else:
                                searchPaths.append(mountpoint + '/')
                            break
    except Exception, e:
        pass

def onPartitionChange(why, part):
    global searchPaths
    if why == 'add' and part.mountpoint not in searchPaths:
        addPiconPath(part.mountpoint)
    elif why == 'remove' and part.mountpoint in searchPaths:
        searchPaths.remove(part.mountpoint)


def findPicon(serviceName):
    global lastPiconsPathsDict, piconType
    pngname = None
    piconTypeName='%s%s' % (piconType,serviceName)
    if piconTypeName in lastPiconsDict:
        pngname = lastPiconsDict[piconTypeName]
    else:
        for path in searchPaths:
            sPath = path + piconType + '/'
            if pathExists(sPath + serviceName + '.png'):
                pngname = sPath + serviceName + '.png'
                lastPiconsDict[piconTypeName] = pngname
                break
    return pngname


def getPiconName(serviceName):
    sname = '_'.join(GetWithAlternative(serviceName).split(':', 10)[:10])
    pngname = findPicon(sname)
    if not pngname:
        fields = sname.split('_', 3)
        if len(fields) > 2 and fields[2] != '2':
            fields[2] = '1'
        if len(fields) > 0 and fields[0] == '4097':
            fields[0] = '1'
        pngname = findPicon('_'.join(fields))
    if not pngname:
        name = ServiceReference(serviceName).getServiceName()
        name = unicodedata.normalize('NFKD', unicode(name, 'utf_8', errors='ignore')).encode('ASCII', 'ignore')
        name = re.sub('[^a-z0-9]', '', name.replace('&', 'and').replace('+', 'plus').replace('*', 'star').lower())
        if len(name) > 0:
            pngname = findPicon(name)
            if not pngname and len(name) > 2 and name.endswith('hd'):
                pngname = findPicon(name[:-2])
    return pngname


class j00zekPicons(Renderer):

    def __init__(self):
        Renderer.__init__(self)
        self.PicLoad = ePicLoad()
        self.PicLoad.PictureData.get().append(self.updatePicon)
        self.piconsize = (0, 0)
        self.pngname = ''
        return

    def addPath(self, value):
        if pathExists(value):
            if not value.endswith('/'):
                value += '/'
            if value not in searchPaths:
                searchPaths.append(value)

    def applySkin(self, desktop, parent):
        attribs = self.skinAttributes[:]
        for attrib, value in self.skinAttributes:
            if attrib == 'path':
                self.addPath(value)
                attribs.remove((attrib, value))
            elif attrib == 'size':
                self.piconsize = value
            elif attrib == 'picontype':
                global piconType
                piconType = value
                attribs.remove((attrib, value))

        self.skinAttributes = attribs
        return Renderer.applySkin(self, desktop, parent)

    GUI_WIDGET = ePixmap

    def postWidgetCreate(self, instance):
        self.changed((self.CHANGED_DEFAULT,))

    def updatePicon(self, picInfo = None):
        ptr = self.PicLoad.getData()
        if ptr is not None:
            self.instance.setPixmap(ptr.__deref__())
            self.instance.show()
        return

    def changed(self, what):
        if self.instance:
            pngname = ''
            try:
                if not what[0] is self.CHANGED_CLEAR:
                    pngname = getPiconName(self.source.text)
                    if pngname is None:
                        pngname = findPicon('picon_default')
                    elif not pathExists(pngname):
                        pngname = findPicon('picon_default')
                    if self.pngname != pngname:
                        if pngname:
                            self.instance.setScale(1)
                            self.instance.setPixmapFromFile(pngname)
                            self.instance.show()
                        else:
                            self.instance.hide()
                        self.pngname = pngname
            except Exception, e:
                pass


harddiskmanager.on_partition_list_change.append(onPartitionChange)
initPiconPaths()