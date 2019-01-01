from . import _
from Components.ActionMap import ActionMap
from datetime import datetime
from enigma import getDesktop, ePoint, eSize
from Components.config import config
from Components.Label import Label
from Components.Pixmap import Pixmap
from Components.Sources.StaticText import StaticText
from os import path
from Screens.Screen import Screen
from Tools.LoadPixmap import LoadPixmap
import time

class MSNweatherHistograms(Screen):

    def __init__(self, session, args = 0):
        self.session = session
        if getDesktop(0).size().width() < 1921:
            WindowWidth = 1200
            WindowHeight = 600
            FontSize = 24
            SpaceBetweenBars = 10
            fieldSize = 70
            offset = 50
            self.scaleSize = 100
        self.maxItems = int(1200 / (fieldSize + SpaceBetweenBars))
        self.skin = '<screen name="MSNweatherHistograms" position="center,center" size="%s,%s" title="What happened in last 24 hours?">\n' % (WindowWidth,WindowHeight)
        self.skin += '<widget name="MaxValue" position="0,150" size="220,25" font="Regular;20" halign="left" foregroundColor="lemon" />\n'
        i = 0
        while i < self.maxItems:
            posX = i * (fieldSize + SpaceBetweenBars)
            self.PressureBarPosY = offset + self.scaleSize
            self.skin += '<widget name="Header%s" position="%s,0" zPosition="5" size="%s,30" halign="center" font="Regular;24" transparent="1"/>\n' % (i, posX, fieldSize)
            self.skin += '<widget name="bar%s" position="%s,%s" zPosition="1" size="%s,3" alphatest="blend"/>\n' % (i, posX, self.PressureBarPosY, fieldSize)
            self.skin += '<widget render="Label" source="name%s" position="%s,%s" zPosition="5" size="%s,30" foregroundColor="lemon" halign="center" font="Regular;24" transparent="1"/>\n' % (i, posX, self.PressureBarPosY + 10, fieldSize)
            i += 1
        self.skin += '</screen>\n'
        #self.DEBUG(self.skin)

        Screen.__init__(self, session)
        self["setupActions"] = ActionMap(["SetupActions", "ColorActions"],
            {
                "cancel": self.cancel,
                "ok": self.keyOk,
            }, -2)
        
        self.setTitle(_("What happened with %s during last %s hours?") % ( _('pressure'),self.maxItems))
        self['MaxValue'] = StaticText()

        self.currTime = int(time.time())
        i = 0
        self.mapDict = {}
        while i < self.maxItems:
            hour = int(time.strftime("%d%H", time.localtime(self.currTime - (self.maxItems - 1 - i) * 3600)))
            self.mapDict[hour] = i
            self.DEBUG('self.mapDict[%s] = %s' % (hour,i))
            hour = str(hour)[2:]
            if hour < 10:
                self['Header%s' % i] = Label('0%s:00' % hour)
            else:
                self['Header%s' % i] = Label('%s:00' % hour)
            self['bar%s' % i] = Pixmap()
            self['name%s' % i] = StaticText()
            i += 1
            
        self.bar = LoadPixmap(cached=True, path= '/usr/lib/enigma2/python/Plugins/Extensions/MSNweather/icons/bar.png')
       
        self.onLayoutFinish.append(self.startRun)
    
    def DEBUG(self, myFUNC = '' , myText = '' ):
        if config.plugins.WeatherPlugin.DebugMSNweatherHistograms.value:
            from Plugins.Extensions.MSNweather.debug import printDEBUG
            printDEBUG( myFUNC , myText )

    def startRun(self):
        self.DEBUG('MSNweatherHistograms(Screen).startRun >>>')
        minPressure = 9999
        maxPressure = 99
        myData = []
        myFile = '/usr/lib/enigma2/python/Plugins/Extensions/MSNweather/histograms.data'
        if path.exists(myFile):
            with open(myFile, 'r') as f:
                for line in f:
                    if len(line.strip()) > 0:
                        myData.append(line.strip())
                        record = line.strip().split('|')
                        pressure = int(record[4].split('=')[1].replace('.00','').replace('mbar','').strip())
                        if minPressure > pressure: minPressure = pressure
                        if maxPressure < pressure: maxPressure = pressure
                f.close()
        diffPressure = maxPressure - minPressure
        stepPressure = int(self.scaleSize / diffPressure)
        self.DEBUG('\t\t minPressure=%s, maxPressure=%s, diffPressure=%s, stepPressure%s' % (minPressure, maxPressure, diffPressure, stepPressure))
        
        myDataCount = len(myData)
        if myDataCount > 0:
            i = 0
            while i < (myDataCount - 1):
                record = myData[i].split('|')
                #self.DEBUG('\t record="%s"' % (record))
                hour = int(record[1])
                pressure = str(record[4].split('=')[1].replace('.00','').replace('mbar','').strip())
                self.DEBUG('\t hour="%s", pressure="%s"' % (hour, pressure))
                index = self.mapDict.get(hour, -1)
                if index > -1:
                    #self.DEBUG('\t\t name%s="%s"' % (index, pressure))
                    self['name%s' % index].text = pressure
                    self['bar%s' % index].instance.resize(eSize(int(70), int(int(pressure) - minPressure + 30) ))
                    self['bar%s' % index].instance.setScale(0)
                    barX = self['bar%s' % index].instance.position().x()
                    self.DEBUG('\t\t barX=%s, self.PressureBarPosY=%s, newY=%s' % (barX, self.PressureBarPosY, int(self.PressureBarPosY - (int(pressure) - minPressure) * stepPressure)))
                    self['bar%s' % index].instance.move(ePoint(int(barX), int(self.PressureBarPosY - (int(pressure) - minPressure) * stepPressure)))
                    self['bar%s' % index].instance.setPixmap(self.bar)
                    self['bar%s' % index].show()
                i += 1

    def keyOk(self):
        self.close()

    def cancel(self):
        self.close()
