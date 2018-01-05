# -*- coding: utf-8 -*-
from version import Version
Info='@j00zek %s' % Version

#stale
PluginName = 'J00zekBouquets'
PluginGroup = 'Extensions'

#Paths
from Tools.Directories import fileExists,resolveFilename, SCOPE_CURRENT_SKIN, SCOPE_PLUGINS
PluginFolder = PluginName
PluginPath = resolveFilename(SCOPE_PLUGINS, '%s/%s/' %(PluginGroup,PluginFolder))
SkinPath = resolveFilename(SCOPE_CURRENT_SKIN, '')
