DBG=True
from datetime import datetime

append2file=False
def printDEBUG( myFUNC = '' , myText = '' ):
    if DBG:
        myDEBUGfile = '/tmp/WeatherPlugin.log'
        global append2file
        print ("[%s] %s" % (myFUNC,myText))
        try:
            if append2file == False:
                append2file = True
                f = open(myDEBUGfile, 'w')
            else:
                f = open(myDEBUGfile, 'a')
            f.write('[%s] %s%s\n' % (str(datetime.now()), myFUNC, myText))
            f.close
        except Exception as e:
            pass
