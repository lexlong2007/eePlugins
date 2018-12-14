from datetime import datetime

def printDEBUG( myFUNC = '' , myText = '' ):
    try:
        from Components.config import config
        if config.plugins.WeatherPlugin.DebugEnabled.value:
            myDEBUGfile = '/tmp/MSNweather.log'
            print ("[%s] %s" % (myFUNC,myText))
            if myFUNC == 'INIT':
                f = open(myDEBUGfile, 'w')
            else:
                f = open(myDEBUGfile, 'a')
            f.write('[%s] %s%s\n' % (str(datetime.now()), myFUNC, myText))
            f.close
    except Exception:
        pass
