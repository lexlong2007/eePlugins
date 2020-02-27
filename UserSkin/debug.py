# -*- coding: utf-8 -*-
try:
    from inits import myDEBUG, myDEBUGfile, PluginName
except Exception:
    PluginName = 'debug'
    myDEBUG=True
    myDEBUGfile = '/tmp/%s.log' % PluginName

from datetime import datetime

append2file=False
def printDEBUG( myText  , myFUNC = '' ):
    global append2file
    if myDEBUG:
        try:
            print ("[%s%s] %s" % (PluginName,myFUNC,myText))
            if append2file == False:
                append2file = True
                f = open(myDEBUGfile, 'w')
            else:
                f = open(myDEBUGfile, 'a')
                f.write('%s\t%s\n' % (str(datetime.now()), myText))
            f.close
        except Exception:
            pass

printDBG=printDEBUG
str(datetime.now())
