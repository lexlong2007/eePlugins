#
# j00zek 2018 base on 
#  moonphase.py - Calculate Lunar Phase
#  Author: Sean B. Palmer, inamidst.com
#  Cf. http://en.wikipedia.org/wiki/Lunar_phase#Lunar_phase_calculation
#  calculations from https://gist.github.com/miklb/ed145757971096565723
#

from enigma import eTimer
from Components.Converter.Converter import Converter
from Components.Element import cached
from decimal import Decimal as dec
import math, datetime

DBG = False
if DBG: from Components.j00zekComponents import j00zekDEBUG

class j00zekMoon(Converter, object):
    PHASE = 0
    ICON = 1
    LUMINATION = 2
    
    def __init__(self, arg):
        Converter.__init__(self, arg)
        if DBG: j00zekDEBUG('[j00zekMoon:__init__] >>> arg="%s"' % arg)
        if arg in ('faza', 'phase'):
            self.type = self.PHASE
        elif arg in ('obraz', 'icon'):
            self.type = self.ICON
        elif arg in ('lumination', 'oswietlenie'):
            self.type = self.LUMINATION
        else:
            self.type = 'unknown'
        

    def position(self, now=None): 
        days_in_second = 86400
        if now is None: 
            now = datetime.datetime.now()
        diff = now - datetime.datetime(2001, 1, 1)
        days = dec(diff.days) + (dec(diff.seconds) / dec(days_in_second))
        lunarCycle = dec("0.20439731") + (days * dec("0.03386319269"))
        return lunarCycle % dec(1)

    def currPhase(self, pos): 
        index = (pos * dec(8)) + dec("0.5")
        index = math.floor(index)
#        return {
#            0: "New Moon", 
#            1: "Waxing Crescent", 
#            2: "First Quarter", 
#            3: "Waxing Gibbous", 
#            4: "Full Moon", 
#            5: "Waning Gibbous", 
#            6: "Last Quarter", 
#            7: "Waning Crescent"
#        }[int(index) & 7]
        return {
            0: "N\xc3\xb3w", 
            1: "Sierp przybywaj\xc4\x85cy", 
            2: "I kwadra", 
            3: "Przybywaj\xc4\x85cy ksi\xc4\x99\xc5\xbcyc garbaty", 
            4: "Pe\xc5\x82nia", 
            5: "Ubywaj\xc4\x85cy ksi\xc4\x99\xc5\xbcyc garbaty", 
            6: "III kwadra", 
            7: "Sierp ubywaj\xc4\x85cy"
        }[int(index) & 7]
   
    def myRound(self, x, base=5):
        return int(base * round(float(x)/base))
        
    def currPhaseIcon(self, pos): 
        phase = 0
        lunarCycle = float(pos) * 100
        if lunarCycle > 50:
            phase = 100 - lunarCycle
        else:
            phase = lunarCycle * 2
        return phase
        
    @cached
    def getText(self):
        pos = self.position()
        roundedpos = round(float(pos), 3)
        if self.type == self.PHASE:
            retTXT = self.currPhase(pos)
            if DBG: j00zekDEBUG("[j00zekMoon:getText] currentPhase: %s (%s)" % (retTXT, roundedpos))
        elif self.type == self.ICON:
            retTXT = self.currPhaseIcon(pos)
            retTXT = str(self.myRound(retTXT))
            if DBG: j00zekDEBUG("[j00zekMoon:getText] phaseIcon: %s" % (retTXT))
        elif self.type == self.LUMINATION:
            retTXT = self.currPhaseIcon(pos)
            retTXT = str(round(retTXT,1)) + ' %'
            if DBG: j00zekDEBUG("[j00zekMoon:getText] moonLumination: %s" % (retTXT))
        else:
            if DBG: j00zekDEBUG("[j00zekMoon:getText] Unknown type requested")
            retTXT = "---"
        return retTXT

    text = property(getText)
