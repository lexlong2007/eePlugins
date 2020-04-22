#######################################################################
#
#  Coded by j00zek (c)2020
#
#  Uszanuj moja prace i nie kasuj/zmieniaj informacji kto jest autorem renderera
#  Please respect my work and don't delete/change name of the renderer author
#
#  Nie zgadzam sie na wykorzystywanie tego skryptu w projektach platnych jak np. Graterlia!!!
#
#  Prosze NIE dystrybuowac tego skryptu w formie archwum zip, czy tar.gz
#  Zgadzam sie jedynie na dystrybucje z repozytorium opkg
#
################################################################################
from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
######################################################################################
def sessionstart(session, **kwargs):
    try:
        #from Components.Sources.mySource import mySource
        #session.screen['mySource'] = mySource()
        from Components.Sources.StaticText import StaticText
        session.screen['j00zekStaticSource'] = StaticText()
        print "e2components config initiated"
    except Exception, e:
        print "Exception for e2components: %s" % str(e)

def Plugins(**kwargs):
    return [PluginDescriptor(where=[PluginDescriptor.WHERE_SESSIONSTART], fnc=sessionstart)]
