#
# j00zek 2018
#

from enigma import eTimer
from Components.Converter.Converter import Converter
from Components.Element import cached
from Components.Language import language
#from decimal import Decimal as dec
import math, datetime

DBG = True
if DBG: from Components.j00zekComponents import j00zekDEBUG

#simple and dirty translation
if language.getLanguage() == 'pl_PL':
    MoonPhasesDict = { 0: "N\xc3\xb3w", 1: "Sierp przybywaj\xc4\x85cy", 2: "I kwadra", 3: "Przybywaj\xc4\x85cy ksi\xc4\x99\xc5\xbcyc garbaty", 
                       4: "Pe\xc5\x82nia", 5: "Ubywaj\xc4\x85cy ksi\xc4\x99\xc5\xbcyc garbaty", 6: "III kwadra", 7: "Sierp ubywaj\xc4\x85cy"}
else:
    MoonPhasesDict = { 0: "New Moon", 1: "Waxing Crescent", 2: "First Quarter", 3: "Waxing Gibbous",
                       4: "Full Moon", 5: "Waning Gibbous", 6: "Last Quarter", 7: "Waning Crescent"}


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
        

    def currCyclePerc(self): 
        date = datetime.date.today()
        known_new_moon = datetime.date(2017,1,28)
        lunar_cycle = 29.530588853   # days per lunation
        phase_length = lunar_cycle/8 # days per phase
        days = (date - known_new_moon).days - 1 #we count from next day of newmoon
        days = math.fmod(days + phase_length/2, lunar_cycle)
        return days/lunar_cycle
    
    def currPhase(self, CyclePerc): 
        index = CyclePerc * 8 + 0.5
        index = math.floor(index)
        return MoonPhasesDict[int(index) & 7]
   
    def myRound(self, x, base=5):
        return int(base * round(float(x)/base))
        
    def currPhaseIcon(self, CyclePerc): 
        return self.myRound(CyclePerc * 100)
        
    def currPhaseLuma(self, CyclePerc):
        return (math.cos(((CyclePerc + .5) / .5 * math.pi)) + 1) * .5 * 100
      
    @cached
    def getText(self):
        CyclePerc = self.currCyclePerc()
        if self.type == self.PHASE:
            retTXT = self.currPhase(CyclePerc)
            if DBG: j00zekDEBUG("[j00zekMoon:getText] currentPhase: %s (%s)" % (retTXT, CyclePerc))
        elif self.type == self.ICON:
            retTXT = self.currPhaseIcon(CyclePerc)
            if DBG: j00zekDEBUG("[j00zekMoon:getText] phaseIcon: %s (%s)" % (retTXT, CyclePerc))
        elif self.type == self.LUMINATION:
            retTXT = self.currPhaseLuma(CyclePerc)
            retTXT = str(round(retTXT,1)) + '%'
            if DBG: j00zekDEBUG("[j00zekMoon:getText] moon Lumination: %s (%s)" % (retTXT, CyclePerc))
        else:
            if DBG: j00zekDEBUG("[j00zekMoon:getText] Unknown type requested")
            retTXT = "---"
        return str(retTXT)

    text = property(getText)
