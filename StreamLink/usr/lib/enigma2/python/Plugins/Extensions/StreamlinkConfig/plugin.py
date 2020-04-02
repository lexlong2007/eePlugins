from Plugins.Plugin import PluginDescriptor
from . import mygettext as _

def main(session, **kwargs):
    from StreamlinkConfiguration import StreamlinkConfiguration
    session.open(StreamlinkConfiguration)

def Plugins(path, **kwargs):
    return [PluginDescriptor(name=_("Streamlink Configuration"), where = PluginDescriptor.WHERE_PLUGINMENU, fnc = main, needsRestart = False)]
