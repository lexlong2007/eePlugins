#import inspect
from os import path, system
from datetime import datetime

append2file=False
myDEBUG='/tmp/j00zekComponents.log'
imageType=None

def getImageType():
    return imageType

def isImageType(imgName = ''):
    global imageType
    #check using opkg
    if imageType is None:
        if path.exists('/etc/opkg/all-feed.conf'):
            with open('/etc/opkg/all-feed.conf', 'r') as file:
                fileContent = file.read()
                file.close()
                fileContent = fileContent.lower()
                if fileContent.find('VTi') > -1:
                    imageType = 'vti'
                elif fileContent.find('code.vuplus.com') > -1:
                    imageType = 'vuplus'
                elif fileContent.find('openpli-7') > -1:
                    imageType = 'openpli7'
                elif fileContent.find('openatv') > -1:
                    imageType = 'openatv'
                    if fileContent.find('/5.3/') > -1:
                        imageType += '5.3'
    #check using specifics
    if imageType is None:
        if path.exists('/usr/lib/enigma2/python/Plugins/SystemPlugins/VTIPanel/'):
            imageType = 'vti'
        elif path.exists('/usr/lib/enigma2/python/Plugins/Extensions/Infopanel/'):
            imageType = 'openatv'
        elif path.exists('/usr/lib/enigma2/python/Blackhole'):
            imageType = 'blackhole'
        elif path.exists('/etc/init.d/start_pkt.sh'):
            imageType = 'pkt'
        else:
            imageType = 'unknown'
    if imgName.lower() == imageType.lower() :
        return True
    else:
        return False

def j00zekDEBUG(myText = None, Append = True):
    global append2file, myDEBUG
    if myDEBUG is None:
        return
    if myText is None:
        return
    try:
        if append2file == False or Append == False:
            append2file = True
            f = open(myDEBUG, 'w')
        else:
            f = open(myDEBUG, 'a')
        f.write('%s\t%s\n' % (str(datetime.now()),myText))
        f.close()
        if path.getsize(myDEBUG) > 100000:
            system('sed -i -e 1,10d %s' % myDEBUG)
        #print(myText)
    except Exception, e:
        system('echo "Exception:%s" >> %s' %( str(e), myDEBUG ))
    return

def logMissing(myText = None, Append = True):
    global append2file, myDEBUG
    if myDEBUG is None:
        return
    if myText is None:
        return
    try:
        if append2file == False or Append == False:
            append2file = True
            f = open(myDEBUG, 'w')
        else:
            f = open(myDEBUG, 'a')
        f.write('%s\t%s\n' % (str(datetime.now()),myText))
        f.close()
        if path.getsize(myDEBUG) > 100000:
            system('sed -i -e 1,10d %s' % myDEBUG)
        #print(myText)
    except Exception, e:
        pass
    return

def isINETworking(addr = '8.8.8.8', port = 53):
    try:
        import socket
        if addr[:1].isdigit(): addr = socket.gethostbyname(addr)
        socket.setdefaulttimeout(0.5)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((addr, port))#connection with google dns service
        return True
    except Exception as e:
        pass
        #printDEBUG("%s" % str(e))
    #printDEBUG("Error no internet connection. > %s" % str(e))
    return False
  