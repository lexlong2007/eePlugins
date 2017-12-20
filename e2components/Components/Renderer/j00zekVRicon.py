# renderer for Video resolution icons @j00zek 2017
# purpose:
#       -smaller and more ellegant xml
#       -should work quicker as no multiple checks necessary

from Renderer import Renderer

from enigma import ePixmap, ePicLoad, eSize, iServiceInformation
from Tools.Directories import pathExists, SCOPE_SKIN_IMAGE, SCOPE_CURRENT_SKIN, resolveFilename

class j00zekVRicon(Renderer):
   
    def __init__(self):
        Renderer.__init__(self)
        #self.picload = ePicLoad()
        self.iconPath = resolveFilename(SCOPE_CURRENT_SKIN, 'icons')
        self.iconUHD = 'ico_uhd_on.png'
        self.iconHD = 'ico_hd_on_1080.png'
        self.iconHDready = 'ico_hd_on_720.png'
        self.icon960 = 'ico_hd_on_960.png'
        self.iconSD = 'ico_sd_on_576.png'

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
                        x = info.getInfo(iServiceInformation.sVideoWidth)
                        y = info.getInfo(iServiceInformation.sVideoHeight)
                        if x > 1920 and y > 1080:
                            tmpIcon = '%s/%s' % (self.iconPath, self.iconUHD) #UHD - 3840x2160
                        elif x > 1280 and y > 720:
                            tmpIcon = '%s/%s' % (self.iconPath, self.iconHD) #HD - 1920x1080
                        elif x == 960 and y == 540: 
                            tmpIcon = '%s/%s' % (self.iconPath, self.icon960) # 960x540
                        elif x > 720 and y > 576:
                            tmpIcon = '%s/%s' % (self.iconPath, self.iconHDready) #HDready - 1280x720
                        elif x > 0 and y > 0:
                            tmpIcon = '%s/%s' % (self.iconPath, self.iconSD) #SD - 720 x 576 / 768 x 576 / 720 x 480
                        
                        if tmpIcon != '' and pathExists(tmpIcon):
                            #print "Rendering icon '%s'" % tmpIcon
                            self.instance.setScale(1)
                            self.instance.setPixmapFromFile(tmpIcon)
                            self.instance.show()
                        else:
                            self.instance.hide()
                            print "Path for icon '%s' not found" % tmpIcon
                          
