################################################################################
#
# j00zekLabel with dynamic change of font size
#      by default mint font size is 3/4 of font size or 
#                       can be defined by minFontSize="32" parameter
################################################################################

from enigma import eWidget, eLabel, ePoint, eSize, gFont, \
    RT_HALIGN_LEFT, RT_HALIGN_CENTER, RT_HALIGN_RIGHT, RT_HALIGN_BLOCK, \
    RT_VALIGN_TOP, RT_VALIGN_CENTER, RT_VALIGN_BOTTOM, RT_WRAP

from Renderer import Renderer
from skin import parseColor, parseFont

DBG = False
try:
    if DBG: from Components.j00zekComponents import j00zekDEBUG
except Exception: DBG = False 

class j00zekLabel(Renderer):
    def __init__(self):
        Renderer.__init__(self)
        self.txText      = ""
        self.txtFlags    = 0
        self.txFontName  = "Regular"
        self.maxFontSize = 14
        self.minFontSize = 0
        self.txFont      = gFont(self.txFontName, self.maxFontSize)
        self.txLabel     = None
        self.soffset     = (0,0)
        self.W = self.H  = 0

    GUI_WIDGET = eWidget

    def postWidgetCreate(self, instance):
        for (attrib, value) in self.skinAttributes:
            if attrib == "size":
                x, y = value.split(',')
                self.W, self.H = int(x), int(y)
        self.instance.move(ePoint(0,0))
        self.instance.resize( eSize(self.W,self.H) )
        self.txLabel = eLabel(instance)

    def preWidgetRemove(self, instance):
        self.txLabel = None

    def applySkin(self, desktop, screen):
        def retValue(val, limit, default, Min=False):
            try:
                if Min:
                    x = min(limit, int(val))
                else:
                    x = max(limit, int(val))
            except:
                    x = default
            return x
            
        def setWrapFlag(attrib, value):
            if (attrib.lower() == "wrap" and value == "0") or \
               (attrib.lower() == "nowrap" and value != "0"):
                self.txtFlags &= ~RT_WRAP
            else:
                self.txtFlags |= RT_WRAP

        self.halign = valign = eLabel.alignLeft
        if self.skinAttributes:
            attribs = [ ]
            setWrapFlag("noWrap", "1") #wrap by default
            for (attrib, value) in self.skinAttributes:
                if attrib == "font":
                    self.txFont = parseFont(value, ((1,1),(1,1)))
                    self.maxFontSize = int(value.split(';')[1].strip())
                    self.txFontName = value.split(';')[0]
                    if self.minFontSize == 0:
                        self.minFontSize = int(self.maxFontSize  * 3 / 4)
                    if DBG: j00zekDEBUG("[j00zekLabel:applySkin] txfontName='%s', maxFontSize='%s', minFontSize='%s'" % (self.txFontName, self.maxFontSize, self.minFontSize)) 
                elif attrib == "minFontSize":
                    self.minFontSize = int(value.strip())
                    if DBG: j00zekDEBUG("[j00zekLabel:applySkin] minFontSize='%s'" % self.minFontSize)
                elif attrib == "foregroundColor":
                    self.txLabel.setForegroundColor(parseColor(value))
                elif attrib in ("shadowColor","borderColor"):    # fake for openpli-enigma2
                    self.txLabel.setShadowColor(parseColor(value))
                elif attrib == "shadowOffset":
                    x, y = value.split(',')
                    self.soffset = (int(x),int(y))
                    self.txLabel.setShadowOffset(ePoint(self.soffset))
                elif attrib == "borderWidth":            # fake for openpli-enigma2
                    self.soffset = (-int(value),-int(value))
                elif attrib == "valign" and value in ("top","center","bottom"):
                    valign = { "top": eLabel.alignTop, "center": eLabel.alignCenter, "bottom": eLabel.alignBottom }[value]
                    self.txtFlags |= { "top": RT_VALIGN_TOP, "center": RT_VALIGN_CENTER, "bottom": RT_VALIGN_BOTTOM }[value]
                elif attrib == "halign" and value in ("left","center","right","block"):
                    self.halign = { "left": eLabel.alignLeft, "center": eLabel.alignCenter, "right": eLabel.alignRight, "block": eLabel.alignBlock }[value]
                    self.txtFlags |= { "left": RT_HALIGN_LEFT, "center": RT_HALIGN_CENTER, "right": RT_HALIGN_RIGHT, "block": RT_HALIGN_BLOCK }[value]
                elif attrib == "noWrap":
                    setWrapFlag(attrib, value)
                else:
                    attribs.append((attrib,value))
                    if attrib == "backgroundColor":
                        self.txLabel.setBackgroundColor(parseColor(value))
                    elif attrib == "transparent":
                        self.txLabel.setTransparent(int(value))
                        
            self.skinAttributes = attribs
        ret = Renderer.applySkin(self, desktop, screen)
        
        self.txLabel.setFont(self.txFont)
        #if not (self.txtFlags & RT_WRAP):
        #    self.txLabel.setNoWrap(1)
        self.txLabel.setNoWrap(0)
        self.txLabel.setVAlign(valign)
        self.txLabel.setHAlign(self.halign)
        self.txLabel.move( ePoint(0,0) )
        self.txLabel.resize( eSize(self.W,self.H) )
        self.txLabel.setText("")
        return ret

    def doSuspend(self, suspended):
        if suspended:
            self.changed((self.CHANGED_CLEAR,))
        else:
            self.changed((self.CHANGED_DEFAULT,))

    def connect(self, source):
        Renderer.connect(self, source)

    def changed(self, what):
        if what[0] == self.CHANGED_CLEAR:
            self.txText = ""
            if self.instance:
                self.txLabel.setText("")
        else:
            if not self.txLabel is None:
                self.txText = self.source.text or ""
                self.txLabel.setText(self.txText)
                if self.txText != "":
                    self.setFontSize()

    def setFontSize(self):
        if DBG: j00zekDEBUG("[j00zekLabel:setFontSize] >>>")

        if not (self.txtFlags & RT_WRAP):
            self.txText = self.txText.replace("\xe0\x8a"," ").replace(chr(0x8A)," ").replace("\n"," ").replace("\r"," ")

        currSize = self.maxFontSize
        while currSize > self.minFontSize:
            currSize -= 1
            self.txLabel.setFont(parseFont("%s;%s" % (self.txFontName, currSize), ((1,1),(1,1))))
            text_size = self.txLabel.calculateSize()
            if DBG: j00zekDEBUG("[j00zekLabel:setFontSize] Size of text for font %s is %s/%s" % (currSize, text_size.height(), self.H))
            if text_size.height() <= self.H:
                break
