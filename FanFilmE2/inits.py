# -*- coding: utf-8 -*-
from version import Version
pluginInfo='@j00zek %s' % Version

#stale
PluginName = 'FanFilmE2'
PluginGroup = 'Extensions'

#Plugin Paths
from Tools.Directories import resolveFilename, SCOPE_PLUGINS
PluginFolder = PluginName
PluginPath = resolveFilename(SCOPE_PLUGINS, '%s/%s/' %(PluginGroup,PluginFolder))

##################################################### CONFIGs #####################################################
from Components.config import *
config.plugins.FanFilmE2 = ConfigSubsection()
myConfig = config.plugins.FanFilmE2
myConfig.separator = NoSave(ConfigNothing())
myConfig.PrintDEBUG = ConfigYesNo(default = True)

#### >>> DEBUGGING <<< ####
from datetime import datetime
myDEBUG=True
myDEBUGfile = '/tmp/%s.log' % PluginName

append2file=False
def printDEBUG( myFUNC = '', myText ='' ):
    global append2file
    if myDEBUG:
        if myFUNC != '':
            print ("[%s:%s] %s" % (PluginName,myFUNC,myText))
        else:
            print ("[%s] %s" % (PluginName,myText))
        try:
            if append2file == False:
                append2file = True
                f = open(myDEBUGfile, 'w')
                f.write('\xef\xbb\xbf')
            else:
                f = open(myDEBUGfile, 'a')
            if myFUNC != '' and myText != '':
                f.write('%s %s\t%s\n' %(str(datetime.now()), myFUNC, myText))
            elif myFUNC != '' or myText != '':
                f.write('%s \t%s%s\n' %(str(datetime.now()), myFUNC, myText))
              
            f.close
        except:
            pass

printDBG=printDEBUG
