from Plugins.Plugin import PluginDescriptor
from . import mygettext as _
from StreamlinkConfiguration import StreamlinkConfiguration

def main(session, **kwargs):
    if menuid == "vtimain" or menuid == "system":
        return [(_("Streamlink Configuration"), main, "StreamlinkConfiguration", 40)]
    return []

def Plugins(path, **kwargs):
    #return [PluginDescriptor(name=_("Streamlink Configuration"), where = PluginDescriptor.WHERE_PLUGINMENU, fnc = main, needsRestart = False)]
    return [PluginDescriptor(name=_("Streamlink Configuration"), where = PluginDescriptor.WHERE_MENU, fnc = main, needsRestart = False)]
