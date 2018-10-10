#######################################################################
#
#    Renderer for Enigma2
#    Coded by j00zek (c)2018
#
#    Uszanuj moja prace i nie kasuj/zmieniaj informacji kto jest autorem renderera
#    Please respect my work and don't delete/change name of the renderer author
#
#    Nie zgadzam sie na wykorzystywanie tego renderera w projektach platnych jak np. Graterlia!!!
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

from Renderer import Renderer

from enigma import ePixmap, ePicLoad, eSize, iServiceInformation
from Tools.Directories import pathExists, SCOPE_SKIN_IMAGE, SCOPE_CURRENT_SKIN, resolveFilename

DBG = False
try:
    if DBG: from Components.j00zekComponents import j00zekDEBUG
except Exception:
    DBG = False
    
class j00zekFEicon(Renderer):
   
    def __init__(self):
        Renderer.__init__(self)
        #self.picload = ePicLoad()
        self.iconPath = resolveFilename(SCOPE_CURRENT_SKIN, 'icons')
        self.currIcon = ''

    def applySkin(self, desktop, parent):
        attribs = self.skinAttributes[:]
        for attrib, value in self.skinAttributes:
            if attrib == 'iconspath':
                if value[:1] == '/':
                    self.iconPath = value
                else:
                    self.iconPath = resolveFilename(SCOPE_CURRENT_SKIN, value)
                attribs.remove((attrib, value))

        self.skinAttributes = attribs
        return Renderer.applySkin(self, desktop, parent)

    GUI_WIDGET = ePixmap

    def postWidgetCreate(self, instance):
        self.changed((self.CHANGED_DEFAULT,))

    def changed(self, what):
        if what[0] != self.CHANGED_CLEAR:
            if self.source:
                if self.instance:
                    service = self.source.service
                    info = service and service.info()
                    if info:
                        tmpIcon = ''
                        tpdata = info.getInfoObject(iServiceInformation.sTransponderData)
                        if tpdata:
                            if not service.streamed() is None:
                                tmpIcon = 'ico_iptv.png'
                            else:
                                if tpdata.get('system', 0) is 0:
                                    tmpIcon = 'ico_%s.png' % tpdata.get('tuner_type', '').lower()
                                else:
                                    tmpIcon = 'ico_%s2.png' % tpdata.get('tuner_type', '').lower()
                        if pathExists('%s/%s' %(self.iconPath, tmpIcon)):
                            tmpIcon ='%s/%s' %(self.iconPath, tmpIcon)
                        elif pathExists('%s/%s' %(self.iconPath, tmpIcon.replace('-','_'))):
                            tmpIcon ='%s/%s' %(self.iconPath, tmpIcon.replace('-','_'))
                        if tmpIcon == '':
                            self.instance.hide()
                            if DBG: j00zekDEBUG("[j00zekFEicon:changed] Path for icon '%s' not found" % tmpIcon)
                        elif tmpIcon != self.currIcon:
                            if DBG: j00zekDEBUG("[j00zekFEicon:changed] displaying icon '%s'" % tmpIcon)
                            self.currIcon = tmpIcon
                            self.instance.setScale(1)
                            self.instance.setPixmapFromFile(tmpIcon)
                            self.instance.show()
