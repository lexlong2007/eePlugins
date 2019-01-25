# -*- coding: utf-8 -*-
from . import _
from Components.config import config
from enigma import eEnv
from os import path as os_path, mkdir as os_mkdir, remove as os_remove, listdir as os_listdir
from threading import Event
from Tools.Directories import resolveFilename, SCOPE_SKIN
from twisted.internet import defer
from twisted.web.client import getPage, downloadPage
from urllib import quote as urllib_quote
from xml.etree.cElementTree import fromstring as cet_fromstring

import time
import webRegex

class WeatherIconItem:

    def __init__(self, url = '', filename = '', index = -1, error = False):
        self.url = url
        self.filename = filename
        self.index = index
        self.error = error


class MSNWeatherItem:

    def __init__(self):
        self.temperature = ''
        self.skytext = ''
        self.humidity = ''
        self.winddisplay = ''
        self.observationtime = ''
        self.observationpoint = ''
        self.feelslike = ''
        self.skycode = ''
        self.date = ''
        self.day = ''
        self.low = ''
        self.high = ''
        self.skytextday = ''
        self.skycodeday = ''
        self.shortday = ''
        self.iconFilename = ''
        self.code = ''
        self.rainprecip = ''

class getWeather:
    ERROR = 0
    OK = 1

    def __init__(self):
        paths = (os_path.dirname(resolveFilename(SCOPE_SKIN, config.skin.primary_skin.value)) + '/weather_icons/'
                    ,'/etc/enigma2/weather_icons/',
                    eEnv.resolve('${libdir}/enigma2/python/Plugins/Extensions/MSNweather/icons/')
                )
        self.iconextension = '.png'
        for path in paths:
            if os_path.exists(path):
                self.iconpath = path
                break
        self.initialize(True)

    def EXCEPTIONDEBUG(self, myFUNC = '' , myText = '' ):
        from Plugins.Extensions.MSNweather.debug import printDEBUG
        printDEBUG( myFUNC , myText )
            
    def DEBUG(self, myFUNC = '' , myText = '' ):
        if config.plugins.WeatherPlugin.DebugGetWeatherBasic.value:
            from Plugins.Extensions.MSNweather.debug import printDEBUG
            printDEBUG( myFUNC , myText )

    def DEBUGxml(self, myFUNC = '' , myText = '' ):
        if config.plugins.WeatherPlugin.DebugGetWeatherXML.value:
            from Plugins.Extensions.MSNweather.debug import printDEBUG
            printDEBUG( myFUNC , myText )

    def DEBUGweb(self, myFUNC = '' , myText = '' ):
        if config.plugins.WeatherPlugin.DebugGetWeatherWEB.value:
            from Plugins.Extensions.MSNweather.debug import printDEBUG
            printDEBUG( myFUNC , myText )

    def DEBUGts(self, myFUNC = '' , myText = '' ):
        if config.plugins.WeatherPlugin.DebugGetWeatherTS.value:
            from Plugins.Extensions.MSNweather.debug import printDEBUG
            printDEBUG( myFUNC , myText )

    def DEBUGfull(self, myFUNC = '' , myText = '' ):
        if config.plugins.WeatherPlugin.DebugGetWeatherFULL.value:
            from Plugins.Extensions.MSNweather.debug import printDEBUG
            printDEBUG( myFUNC , myText )

    def initialize(self, full = False):
        self.city = ''
        self.degreetype = ''
        self.imagerelativeurl = ''
        self.url = ''
        self.weatherItems = {}
        self.thingSpeakItems = {}
        self.callback = None
        self.callbackShowIcon = None
        self.callbackAllIconsDownloaded = None
        if full:
            self.WebCurrentItems = {}
            self.WebhourlyItems = {}
            self.WebDailyItems = {}
        self.collectDataForHistogram = False
        return

    def cancel(self):
        self.DEBUG('cancel','>>>')
        self.callback = None
        self.callbackShowIcon = None
        return

    def returnDict(self, dictName): #weatherItems,thingSpeakItems,WebhourlyItems,WebDailyItems
        self.DEBUG('getWeather().returnDict(dictName=%s)' % dictName ,'>>>')
        if dictName is None:
            return {}
        elif dictName == 'weatherItems':
            return self.weatherItems
        elif dictName == 'thingSpeakItems':
            self.DEBUG('\t' ,'len(thingSpeakItems)=%s' % len(self.thingSpeakItems))
            return self.thingSpeakItems
        elif dictName == 'WebCurrentItems':
            return self.WebCurrentItems
        elif dictName == 'WebhourlyItems':
            return self.WebhourlyItems
        elif dictName == 'WebDailyItems':
            return self.WebDailyItems
        else:
            return {}
        
    def getWeatherData(self, degreetype, locationcode, city, weatherSearchFullName, thingSpeakChannelID, callback, callbackShowIcon, callbackAllIconsDownloaded = None, Histogram = False):
        self.DEBUG('getWeather().getWeatherData' ,'>>>')
        self.initialize()
        self.collectDataForHistogram = Histogram
        language = config.osd.language.value.replace('_', '-')
        if language == 'en-EN':
            language = 'en-US'
        elif language == 'no-NO':
            language = 'nn-NO'
        self.city = city
        self.callback = callback
        self.callbackShowIcon = callbackShowIcon
        self.callbackAllIconsDownloaded = callbackAllIconsDownloaded
        url = 'http://weather.service.msn.com/data.aspx?src=windows&weadegreetype=%s&culture=%s&wealocations=%s' % (degreetype, language, urllib_quote(locationcode))
        getPage(url).addCallback(self.xmlCallback).addErrback(self.xmlError)
        self.DEBUGxml('\t url_xml=' ,'%s' % url)
        if weatherSearchFullName != '':
            #url2 = 'http://www.msn.com/weather/we-city?culture=%s&form=PRWLAS&q=%s' % (language, urllib_quote(weatherSearchFullName))
            url2 = 'https://www.msn.com/%s/weather?culture=%s&form=PRWLAS&q=%s' % (language, language, urllib_quote(weatherSearchFullName))
            self.DEBUG('\t url_web="%s"' % url2)
            getPage(url2).addCallback(self.webCallback).addErrback(self.webError)
        if thingSpeakChannelID != '':
            url3 = 'https://thingspeak.com/channels/%s/feeds.xml?average=10&results=1' % thingSpeakChannelID
            self.DEBUG('\t url_thingSpeak=' ,'%s' % url3)
            getPage(url3).addCallback(self.thingSpeakCallback).addErrback(self.thingSpeakError)

    def getDefaultWeatherData(self, callback = None, callbackAllIconsDownloaded = None):
        self.DEBUG('getWeather().getDefaultWeatherData()')
        self.initialize()
        weatherPluginEntryCount = config.plugins.WeatherPlugin.entrycount.value
        if weatherPluginEntryCount >= 1:
            weatherPluginEntry = config.plugins.WeatherPlugin.Entry[0]
            self.getWeatherData(weatherPluginEntry.degreetype.value,
                                weatherPluginEntry.weatherlocationcode.value,
                                weatherPluginEntry.city.value,
                                weatherPluginEntry.weatherSearchFullName.value,
                                weatherPluginEntry.thingSpeakChannelID.value,
                                callback, None, callbackAllIconsDownloaded, True)
            return 1
        else:
            return 0

    def xmlError(self, error = None):
        errormessage = ''
        if error is not None:
            errormessage = str(error.getErrorMessage())
            self.EXCEPTIONDEBUG('getWeather().xmlError() >>> %s' % errormessage)
        if self.callback is not None:
            self.callback(self.ERROR, errormessage)
        self.DEBUG('getWeather().xmlError() <<<')
        return

    def errorIconDownload(self, error = None, item = None):
        item.error = True
        if os_path.exists(item.filename):
            os_remove(item.filename)

    def finishedIconDownload(self, result, item):
        if not item.error:
            self.showIcon(item.index, item.filename)

    def showIcon(self, index, filename):
        if self.callbackShowIcon is not None:
            self.callbackShowIcon(index, filename)
        return

    def finishedAllDownloadFiles(self, result):
        if self.callbackAllIconsDownloaded is not None:
            self.callbackAllIconsDownloaded()
        return

    def xmlCallback(self, xmlstring):
        self.DEBUGfull('getWeather().xmlCallback(%s)' % xmlstring.replace('/><','/>\n<'))
        IconDownloadList = []
        root = cet_fromstring(xmlstring)
        index = 0
        self.degreetype = 'C'
        errormessage = ''
        for childs in root:
            if childs.tag == 'weather':
                errormessage = childs.attrib.get('errormessage')
                if errormessage:
                    if self.callback is not None:
                        self.callback(self.ERROR, errormessage.encode('utf-8', 'ignore'))
                    break
                self.degreetype = childs.attrib.get('degreetype').encode('utf-8', 'ignore')
                self.imagerelativeurl = '%slaw/' % childs.attrib.get('imagerelativeurl').encode('utf-8', 'ignore')
                self.url = childs.attrib.get('url').encode('utf-8', 'ignore')
            for items in childs:
                if items.tag == 'current':
                    currentWeather = MSNWeatherItem()
                    currentWeather.temperature = items.attrib.get('temperature').encode('utf-8', 'ignore')
                    currentWeather.skytext = items.attrib.get('skytext').encode('utf-8', 'ignore')
                    currentWeather.humidity = items.attrib.get('humidity').encode('utf-8', 'ignore')
                    currentWeather.winddisplay = items.attrib.get('winddisplay').encode('utf-8', 'ignore')
                    currentWeather.observationtime = items.attrib.get('observationtime').encode('utf-8', 'ignore')
                    currentWeather.observationpoint = items.attrib.get('observationpoint').encode('utf-8', 'ignore')
                    currentWeather.feelslike = items.attrib.get('feelslike').encode('utf-8', 'ignore')
                    currentWeather.skycode = '%s%s' % (items.attrib.get('skycode').encode('utf-8', 'ignore'), self.iconextension)
                    currentWeather.code = items.attrib.get('skycode').encode('utf-8', 'ignore')
                    filename = '%s%s' % (self.iconpath, currentWeather.skycode)
                    currentWeather.iconFilename = filename
                    self.DEBUG('MSNWeather().xmlCallback() current: temp=%s, humidity=%s, wind=%s' % (currentWeather.temperature, currentWeather.humidity, currentWeather.winddisplay))
                    if not os_path.exists(filename):
                        url = '%s%s' % (self.imagerelativeurl, currentWeather.skycode)
                        IconDownloadList.append(WeatherIconItem(url=url, filename=filename, index=-1))
                    else:
                        self.showIcon(-1, filename)
                    self.weatherItems[str(-1)] = currentWeather

        if len(IconDownloadList) != 0:
            ds = defer.DeferredSemaphore(tokens=len(IconDownloadList))
            downloads = [ ds.run(download, item).addErrback(self.errorIconDownload, item).addCallback(self.finishedIconDownload, item) for item in IconDownloadList ]
            finished = defer.DeferredList(downloads).addErrback(self.xmlError).addCallback(self.finishedAllDownloadFiles)
        else:
            self.finishedAllDownloadFiles(None)
        self.DEBUG('getWeather().xmlCallback() <<<')
        return

    def thingSpeakCallback(self, xmlstring):
        self.DEBUGfull('getWeather().thingSpeakCallback %s' % xmlstring)
        try:
            root = cet_fromstring(xmlstring)
            for childs in root:
                #self.DEBUG('\titem= ' ,'%s' % childs.tag)
                if childs.tag in ('name','description'):
                    self.thingSpeakItems[childs.tag] = childs.text
                elif childs.tag.startswith('field'):
                    #self.DEBUG('\t' ,"childs.tag.startswith('field'):")
                    tmpName = '%sName' % childs.tag
                    self.thingSpeakItems[tmpName] = childs.text
                    tmpTXT = childs.text.lower().replace(' ','').replace('.','').replace(',','')
                    #self.DEBUG('\t tmpTXT = ' ,"'%s'" % tmpTXT)
                    if tmpTXT.find('pm') >= 0 and tmpTXT.find('25') >= 0:
                        #self.DEBUG('\t' ,'tmpTXT.find(pm) and tmpTXT.find(25):')
                        self.thingSpeakItems['PM2.5'] = childs.tag
                        self.thingSpeakItems['PM2.5Name'] = childs.text
                    elif tmpTXT.find('pm') >= 0 and tmpTXT.find('10') >= 0:
                        #self.DEBUG('\t' ,'tmpTXT.find(pm) and tmpTXT.find(10):')
                        self.thingSpeakItems['PM10'] = childs.tag
                        self.thingSpeakItems['PM10Name'] = childs.text
                    elif tmpTXT.find('pm') and tmpTXT.find('1'):
                        self.thingSpeakItems['PM1'] = childs.tag
                        self.thingSpeakItems['PM1Name'] = childs.text
                elif childs.tag == 'feeds':
                    for feeds in childs:
                        #self.DEBUG('\tfeeds= ' ,'%s' % feeds.tag)
                        if feeds.tag == 'feed':
                            for feed in feeds:
                                #self.DEBUG('\tfeed= ' ,'%s' % feed.tag)
                                if feed.tag == 'created-at':
                                    self.thingSpeakItems['ObservationTime'] = feed.text
                                elif feed.tag.startswith('field'):
                                    tmpName = '%sValue' % feed.tag
                                    self.thingSpeakItems[tmpName] = feed.text
                                    if feed.tag == self.thingSpeakItems.get('PM2.5', '?!?!?!?'):
                                        self.thingSpeakItems['PM2.5Value'] = feed.text
                                    elif feed.tag == self.thingSpeakItems.get('PM10', '?!?!?!?'):
                                        self.thingSpeakItems['PM10Value'] = feed.text
                                    elif feed.tag == self.thingSpeakItems.get('PM1', '?!?!?!?'):
                                        self.thingSpeakItems['PM1Value'] = feed.text
        except Exception as e:
            self.thingSpeakItems = {}
            self.thingSpeakItems['name'] = 'xml error'
            self.thingSpeakItems['description'] = str(e)
            EXCEPTIONDEBUG('getWeather().thingSpeakCallback EXCEPTIONDEBUG %s' % str(e))
        self.DEBUG('getWeather().thingSpeakCallback() <<<')
        
    def thingSpeakError(self, error = None):
        self.EXCEPTIONDEBUG('getWeather().thingSpeakError %s' % error)

    def webCallback(self, string):
        self.DEBUGfull('getWeather().webCallback %s' % string)
        reload(webRegex)
        self.WebCurrentItems, self.WebhourlyItems, self.WebDailyItems = webRegex.getWeather(string)
        self.DEBUGweb('getWeather().webCallback len(WebCurrentItems)= %s, len(WebhourlyItems)= %s, len(WebDailyItems)= %s' % ( \
                                                         len(self.WebCurrentItems),len(self.WebhourlyItems),len(self.WebDailyItems)))
        #final callback
        if self.collectDataForHistogram:
            myFile = eEnv.resolve('${libdir}/enigma2/python/Plugins/Extensions/MSNweather/histograms.data')
            currTime = int(time.time())
            data = self.WebCurrentItems.get('nowData', None)
            currData = self.weatherItems.get('-1', MSNWeatherItem())
            if data is not None:
                record = "%s|%s|%s=%s|%s=%s|%s=%s|%s=%s|currTemp=%s|skyCode=%s|observationtime=%s|iconFilename=%s" % (currTime, time.strftime("%d%H", time.localtime(currTime)),
                                                                 data[0][0], data[0][1].strip(),
                                                                 data[1][0], data[1][1].strip(),
                                                                 data[2][0], data[2][1].strip(),
                                                                 data[4][0], data[4][1].strip(),
                                                                 currData.temperature, currData.code,
                                                                 currData.observationtime, currData.iconFilename
                                     )
                self.DEBUGweb('getWeather().webCallback storing current data for histogram in %s' % myFile)
                self.DEBUGweb(record)
                data = []
                if os_path.exists(myFile):
                    with open(myFile, "r") as f:
                        for line in f:
                            if len(line.strip()) > 0:
                                if len(line.split('|')) > 2:
                                    try:
                                        storedTime = int(line.split('|')[0])
                                        if storedTime > (currTime - 2 * 86400):
                                            data.append(line.strip())
                                    except Exception: pass
                        f.close()
                data.append(record)
                with open(myFile, "w") as f:
                    f.write("\n".join(data))
                    f.close()
        
        config.plugins.WeatherPlugin.callbacksCount.value += 1
        if self.callback is not None:
            self.DEBUG('MSNWeather().webCallback() invoking callback')
            self.callback(self.OK, None)
        self.DEBUG('MSNWeather().webCallback() <<<')
        
    def webError(self, error = None):
        self.EXCEPTIONDEBUG('getWeather().webError %s' % error)

def download(item):
    self.DEBUG('download','>>>')
    return downloadPage(item.url, file(item.filename, 'wb'))