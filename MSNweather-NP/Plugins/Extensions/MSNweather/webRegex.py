#!/usr/bin/python
# -*- coding: utf-8 -*- 
#######################################################################
#
#    download and analyzes wather data from MSN
#    Coded by j00zek (c)2018
#
#    Uszanuj moja prace i nie kasuj/zmieniaj informacji kto jest autorem skryptu
#    Please respect my work and don't delete/change name of the script author
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
#######################################################################

iconsMap={
    'lekkideszczzesniegiem' :   '6.png',
    "slabeopadydeszczu"     :   '9.png',
    'opadydeszczu'          :   '11.png',
    'deszcz'                :   '11.png',
    "niewielkieopadysniegu" :   '13.png', 
    'snieg'                 :   '16.png',
    "zachmurzeniecalkowite" :   '26.png',
    'zachmurzenieduze'      :   '27.png',
    'zachmurzeniemale'      :   '29.png',
    'czesciowoslonecznie'   :   '30.png',
    'bezchmurnie'           :   '31.png',
    'slonecznie'            :   '32.png',
    'przewaznieslonecznie'  :   '34.png',
    #'0'         :  '0.png', #
    #'1'         :  '1.png', #
    #'2'         :  '2.png', #
    #'3'         :  '3.png', #
    #'4'         :  '4.png', #
    #'5'         :  '5.png', #
    #'7'         :  '7.png', #
    #'8'         :  '8.png', #
    #'10'        : '10.png', #
    #'12'        : '12.png', #
    #'14'        : '14.png', #
    #'15'        : '15.png', #
    #'17'        : '17.png', #
    #'18'        : '18.png', #
    #'19'        : '19.png', #
    #'20'        : '20.png', #
    #'21'        : '21.png', #
    #'22'        : '22.png', #
    #'23'        : '23.png', #
    #'24'        : '24.png', #
    #'25'        : '25.png', #
    #'35'        : '35.png', #
    #'36'        : '36.png', #
    #'37'        : '37.png', #
    #'38'        : '38.png', #
    #'39'        : '39.png', #
    #'40'        : '40.png', #
    #'41'        : '41.png', #
    #'42'        : '42.png', #
    #'43'        : '43.png', #
    #'44'        : '44.png', #
    #'45'        : '45.png', #
    #'46'        : '46.png', #
    #'47'        : '47.png', #
    #'48'        : '48.png', #
    }

def plTOansi(text):
    text = text.replace(" ","").replace("ś","s").replace("ł","l").strip()
    text = text.replace("ę","e").replace("ć","c").replace("ó","o").strip()
    return text
  
import re
# instantiate the parser and fed it some HTML
def getWeather(webContent, DBGnow = False, DBGhourly = False, DBGdaily = False):
    webContent = webContent.replace('&#176;','°')
    def findInContent( WC, reFindString ):
        retTxt = ''
        FC = re.findall(reFindString, WC, re.S)
        if FC:
            for i in FC:
                retTxt += i
        return retTxt
    def getList( retList, WC, reFindString ):
        FC = re.findall(reFindString, WC, re.S)
        if FC:
            for i in FC:
                retList.append(i)
        return retList
    #now
    nowContent = findInContent(webContent, '<div class="weather-info">(.*?)</div>')
    nowDict = {}
    nowDict['title'] = getList([], nowContent, '<span>(.*?)</span>.*<ul>')
    nowDict['nowData']  = getList([], nowContent, '<li><span>(.*?)</span>(.*?)</li>')
    if DBGnow:
        print '---------------------------------- nowContent ----------------------\n'
        print nowContent
        print '---------------------------------- nowDict ----------------------\n'
        print nowDict
        print nowDict['title'][0]
    # >>>>> hourly <<<<<
    hourlyContent = findInContent(webContent, '<div class="dailydetails" >(.*?)</ul>')
    hourlyDict = {}
    hourlyDict['title'] = getList([], hourlyContent, '<h2 id="hourlymsg">[\n ]*(.*?)[\n ]*<span>(.*?)</span>[\n ]*<span>(.*?)</span>')
    id = 0
    Lines = getList([], hourlyContent, '<li>(.*?)</li>')
    for Line in Lines:
        #print Line
        hourlyDict['Record=%s' % id] = getList([], Line, 'class="time">(.*?)<.*alt="(.*?)".*src="(.*?)".*class="temp">(.*?)<.*class="precipicn"><span>(.*?)<')
        id += 1
    # >>>>> daily <<<<<
    dailyContent = findInContent(webContent, '<div class="dailymsg"(.*?)</ul>')
    dailyDict = {}
    dailyDict['title'] = 'Daily'
    id = 0
    Lines = getList([], dailyContent, '<li(.*?)</li>')
    for Line in Lines:
        if DBGdaily: print '---------------------------------- Line ----------------------\n' , Line
        dailyDict['Record=%s' % id] = getList([], Line, 'role="button" href="\?(.*?)".*<span>(.*?)<.*<span>(.*?)<.*src="(.*?)".*alt="(.*?)" .*data-icon="(.*?)".*daytemphigh">(.*?)<.*<p>(.*?)</p>.*<span>(.*?)<')
        try:
            weatherIconName = plTOansi(dailyDict['Record=%s' % id][0][4].lower())
            dailyDict['WeatherIcon4Record=%s' % id] = iconsMap.get(weatherIconName, '')
        except Exception:
            dailyDict['WeatherIcon4Record=%s' % id] = ''
        if DBGdaily:
            print "---------------------------------- dailyDict['Record=%s'] ----------------------\n"  % id, dailyDict['Record=%s' % id]
            print '!!! >>> WeatherIcon4Record%s="%s" > "%s"' % (id, weatherIconName, dailyDict['WeatherIcon4Record=%s' % id])
        id += 1
    
    return nowDict, hourlyDict, dailyDict
            
#for tests outside e2
if __name__ == '__main__':
    import os
    os.system('touch /tmp/aqwerty')
    import urllib2
    webContent = urllib2.urlopen('http://www.msn.com/weather/we-city?culture=pl-PL&form=PRWLAS&q=Warszawa%2C%20Polska').read()
    nowDict, hourlyDict, dailyDict = getWeather(webContent, False, False, True)
    #print '---------------------------------- webContent ----------------------'
    #print webContent
    #print '---------------------------------- nowDict -------------------------'
    #print nowDict
    #print '---------------------------------- hourlyDict ----------------------'
    #print hourlyDict
    #print '---------------------------------- dailyDict -----------------------'
    #print dailyDict