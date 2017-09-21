from Plugins.Plugin import PluginDescriptor

def sessionstart(session, **kwargs):
    from Components.Sources.BlackHarmonyMSNWeather import BlackHarmonyMSNWeather
    session.screen['BlackHarmonyMSNWeather'] = BlackHarmonyMSNWeather()


def Plugins(**kwargs):
    return [PluginDescriptor(where=[PluginDescriptor.WHERE_SESSIONSTART], fnc=sessionstart)]