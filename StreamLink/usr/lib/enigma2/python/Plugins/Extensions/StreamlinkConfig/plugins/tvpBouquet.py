# -*- coding: utf-8 -*-
#
#   Based on Kodi plugin.video.pilot.wp by c0d34fun licensed under GNU GENERAL PUBLIC LICENSE. Version 2, June 1991
#   Coded by j00zek
#
# ADDED by j00zek

import sys
import os

def _generate_E2bouquet():
    def doLog(txt, append = 'a' ):
        print txt
        open("/tmp/wpBouquet.log", append).write(txt + '\n')
      
    doLog('', 'w')
    if file_name == '':
        doLog('Ustaw nazwę pliku docelowego!')
        return

    channelsList = (  "http://hbbtvlive.v3.tvp.pl/hbbtvlive/livestream.php?app_id=tvpbialystok",
                      "http://hbbtvlive.v3.tvp.pl/hbbtvlive/livestream.php?app_id=tvpbydgoszcz",
                      "http://hbbtvlive.v3.tvp.pl/hbbtvlive/livestream.php?app_id=tvpgdansk",
                      "http://hbbtvlive.v3.tvp.pl/hbbtvlive/livestream.php?app_id=tvpgorzow",
                      "http://hbbtvlive.v3.tvp.pl/hbbtvlive/livestream.php?app_id=tvpkatowice",
                      "http://hbbtvlive.v3.tvp.pl/hbbtvlive/livestream.php?app_id=tvpkielce",
                      "http://hbbtvlive.v3.tvp.pl/hbbtvlive/livestream.php?app_id=tvpkrakow",
                      "http://hbbtvlive.v3.tvp.pl/hbbtvlive/livestream.php?app_id=tvplublin",
                      "http://hbbtvlive.v3.tvp.pl/hbbtvlive/livestream.php?app_id=tvplodz",
                      "http://hbbtvlive.v3.tvp.pl/hbbtvlive/livestream.php?app_id=tvpolsztyn",
                      "http://hbbtvlive.v3.tvp.pl/hbbtvlive/livestream.php?app_id=tvpopole",
                      "http://hbbtvlive.v3.tvp.pl/hbbtvlive/livestream.php?app_id=tvppoznan",
                      "http://hbbtvlive.v3.tvp.pl/hbbtvlive/livestream.php?app_id=tvprzeszow",
                      "http://hbbtvlive.v3.tvp.pl/hbbtvlive/livestream.php?app_id=tvpszczecin",
                      "http://hbbtvlive.v3.tvp.pl/hbbtvlive/livestream.php?app_id=tvpwroclaw",
                      "http://hbbtvlive.v3.tvp.pl/hbbtvlive/livestream.php?app_id=tvpwarszawa" )

    #generate bouquet
    from channelsMappings import name2serviceDict, name2service4wpDict, name2nameDict
    from datetime import date

    doLog('Generuje bukiet dla %s ...' % frameWork)
    open("/tmp/wpBouquet.log", "a").write('Generuje bukiet dla %s ...\n' % frameWork)
    data = '#NAME TVP Regionalne aktualizacja %s\n' % date.today().strftime("%d-%m-%Y")
    for item in channelsList:
        #print item
            title = item.split('=')[1].strip().replace('tvpb','TVP B').replace('tvpg','TVP G').replace('tvpk','TVP K').replace('tvpl','TVP L').replace('tvpo','TVP O').replace('tvpp','TVP P').replace('tvpr','TVP R').replace('tvps','TVP S').replace('tvpw','TVP W')
            lcaseTitle = title.lower().replace(' ','')
            standardReference = '%s:0:1:0:0:0:0:0:0:0' % frameWork
            #mapowanie bezpośrednie zdefiniowane dla wp
            ServiceID = name2service4wpDict.get(title , standardReference)
            if ServiceID.startswith(standardReference):
                ServiceID = name2serviceDict.get(name2nameDict.get(lcaseTitle, lcaseTitle) , standardReference)
            #mapowanie po zbalezionych kanalach w bukietach
                if ServiceID.startswith(standardReference):
                    doLog("\t- Brak mapowania referencji kanału  %s (%s) dla EPG" % (title, lcaseTitle))
            if not ServiceID.startswith(frameWork):
                ServiceIDlist = ServiceID.split(':')
                ServiceIDlist[0] = frameWork
                ServiceID = ':'.join(ServiceIDlist)
            data += '#SERVICE %s:%s%s:%s\n' % (ServiceID, streamlinkURL, item.replace(':','%3a') , title)
            data += '#DESCRIPTION %s\n' % (title)

    with open(file_name, 'w') as f:
        f.write(data.encode('utf-8'))
        f.close()

    doLog('Wygenerowano bukiet do pliku %s' % file_name)
    f = open('/etc/enigma2/bouquets.tv','r').read()
    if not os.path.basename(file_name) in f:
        doLog('Dodano bukiet do listy')
        if not f.endswith('\n'):
            f += '\n'
        f += '#SERVICE 1:7:1:0:0:0:0:0:0:0:FROM BOUQUET "%s" ORDER BY bouquet\n' % os.path.basename(file_name)
        open('/etc/enigma2/bouquets.tv','w').write(f)

if __name__ == '__main__':
    if len(sys.argv) >=5:
        file_name = sys.argv[1]
        #print 'filename' , file_name
        #print path + file_name
        streamlinkURL = 'http%%3a//127.0.0.1%%3a%s/' % sys.argv[4]
        frameWork = sys.argv[5]
        #print frameWork
        _generate_E2bouquet()
