#!/bin/sh
from version import Version
PluginInfo='@j00zek %s' % Version

PluginName = 'IPTVplayersManager'
PluginGroup = 'Extensions'

#Plugin Paths
from Tools.Directories import resolveFilename, SCOPE_PLUGINS
PluginFolder = PluginName
PluginPath = resolveFilename(SCOPE_PLUGINS, '%s/%s' %(PluginGroup,PluginFolder))
PluginLanguageDomain = PluginName
PluginLanguagePath = resolveFilename(SCOPE_PLUGINS, '%s/%s/locale' % (PluginGroup,PluginFolder))
PluginsExtensionsPath = resolveFilename(SCOPE_PLUGINS, '%s' % PluginGroup)

#translation
from Components.Language import language
import gettext
from os import environ
    
def localeInit():
    lang = language.getLanguage()[:2]
    environ["LANGUAGE"] = lang
    gettext.bindtextdomain(PluginLanguageDomain, PluginLanguagePath)

def translate(txt):
    t = gettext.dgettext(PluginLanguageDomain, txt)
    if t == txt:
            t = gettext.gettext(txt)
    return t

localeInit()
language.addCallback(localeInit)


#some useful stuff
def ClearMemory(): #avoid GS running os.* (e.g. os.system) on tuners with small RAM
    with open("/proc/sys/vm/drop_caches", "w") as f: f.write("1\n")
