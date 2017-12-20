from Renderer import Renderer

from enigma import ePixmap, ePicLoad, eSize

class j00zekPixmap(Renderer):
    def __init__(self):
        Renderer.__init__(self)
        self.size = (0, 0)
        self.resize = 1

    def applySkin(self, desktop, parent):
        attribs = self.skinAttributes[:]
        for attrib, value in self.skinAttributes:
            if attrib == 'resize':
                self.addPath(value)
                self.resize = int(value)
                attribs.remove((attrib, value))
            elif attrib == 'size':
                self.size = value

        self.skinAttributes = attribs
        return Renderer.applySkin(self, desktop, parent)

    GUI_WIDGET = ePixmap

    def postWidgetCreate(self, instance):
        self.changed((self.CHANGED_DEFAULT,))

    def changed(self, what):
        if what[0] != self.CHANGED_CLEAR:
            if self.source and hasattr(self.source, "pixmap"):
                if self.instance:
                    self.instance.setScale(self.resize)
                    #self.instance.setPixmapFromFile(self.source.pixmap)
                    self.instance.setPixmap(self.source.pixmap)
                    if self.resize == 1:
                        self.instance.resize(eSize(self.size))

