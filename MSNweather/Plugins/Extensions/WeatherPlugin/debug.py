DBG=True
myDEBUGfile = '/tmp/WeatherPlugin.log'

append2file=False
def printDEBUG( myFUNC = '' , myText = '' ):
    global append2file
    if DBG:
        print ("[%s] %s" % (myFUNC,myText))
        try:
            if append2file == False:
                append2file = True
                f = open(myDEBUGfile, 'w')
            else:
                f = open(myDEBUGfile, 'a')
            f.write('[%s] %s\n' %(myFUNC,myText))
            f.close
        except Exception:
            pass
