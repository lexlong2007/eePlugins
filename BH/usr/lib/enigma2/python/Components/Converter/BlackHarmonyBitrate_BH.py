# for crash & http://blackharmony.pl/ by areq 2015-12-13 http://areq.eu.org/

from enigma import eConsoleAppContainer, eTimer, iServiceInformation
from Components.Converter.Converter import Converter
from Components.Element import cached
import os

class BlackHarmonyBitrate_BH(Converter, object):

    def __init__(self, type):
        Converter.__init__(self, type)        
        self.clearValues()
        self.container = eConsoleAppContainer()
        self.container.appClosed.append(self.appClosed)
        self.container.dataAvail.append(self.dataAvail)
        self.timer = eTimer()
        self.timer.callback.append(self.start)
        self.runTimer = eTimer()
        self.runTimer.callback.append(self.runBitrate)

    @cached
    def getText(self):
        #print "bitrate class getText", self.vcur
        if self.vcur > 0:
            return '%d Kb/s' % self.vcur
        else:
            return ''

    text = property(getText)

    def doSuspend(self, suspended):
        #print "bitrate class doSuspend", suspended
        if suspended == 0:
            self.running = 1
            self.start()
        else:
            os.system('killall -9 bitrate > /dev/null 2>&1') #don't leave garbage (defunct process)
            #self.container.kill()
            self.clearValues()

    def start(self):
        if self.source.service and self.running == 1:
            self.runTimer.start(600, True)
        else:
            print "bitrate class start po else", self.source.service, self.running
        if self.running == 1:
            os.system('echo "self.timer.start(300, True)" >> /tmp/bitrate')
            #print "bitrate class setup timer"
            self.timer.start(300, True)

    def runBitrate(self):
        os.system('killall -9 bitrate > /dev/null 2>&1')
        if os.path.exists('/usr/lib/enigma2/python/Plugins/SystemPlugins/VTIPanel'):
            demux = 2
        else:
            adapter = 0
            demux = 0
        try:
            stream = self.source.service.stream()
            if stream:
                streamdata = stream.getStreamingData()
                if streamdata:
                    if 'demux' in streamdata:
                        demux = streamdata['demux']
                        if demux < 0: demux = 0
                    if 'adapter' in streamdata:
                        adapter = streamdata["adapter"]
                        if adapter < 0: adapter = 0
        except:
            pass
        info = self.source.service.info()
        vpid = info.getInfo(iServiceInformation.sVideoPID)
        apid = info.getInfo(iServiceInformation.sAudioPID)
        os.system('echo "bitrate %i %i %i %i" >> /tmp/bitrate' % ( adapter, demux, vpid, vpid ))
        if vpid >= 0 and apid >= 0:
            if os.path.exists('/usr/lib/enigma2/python/Plugins/SystemPlugins/VTIPanel'):
                cmd = 'bitrate %i %i %i' % ( demux, vpid, vpid )
            else:
                cmd = 'bitrate %i %i %i %i' % ( adapter, demux, vpid, vpid )
            print "bitrate class start", cmd
            self.running = 2
            self.container.execute(cmd)
    
    def clearValues(self):
        self.vmin = self.vmax = self.vavg = self.vcur = 0
        self.amin = self.amax = self.aavg = self.acur = 0
        self.remainingdata = ''
        self.datalines = []
        self.running = 0

    def appClosed(self, retval):
        self.clearValues()
        print "bitrate class bitrateStopped", retval

    def dataAvail(self, str):
        str = self.remainingdata + str
        newlines = str.split('\n')
        if len(newlines[-1]):
            self.remainingdata = newlines[-1]
            newlines = newlines[0:-1]
        else:
            self.remainingdata = ''
        for line in newlines:
            if len(line):
                self.datalines.append(line)

        if len(self.datalines) >= 2:
            try:
                self.vmin, self.vmax, self.vavg, self.vcur = [int(x) for x in self.datalines[0].split(' ')]
                self.amin, self.amax, self.aavg, self.acur = [int(x) for x in self.datalines[1].split(' ')]
            except:
                print "bitrate class dataAvail except"
            self.datalines = []
            #print "bitrate class new data"
            Converter.changed(self, (self.CHANGED_POLL,))