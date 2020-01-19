from version import Version
Info='@j00zek %s' % Version

########################### Tlumaczenia ###########################################
from Tools.Directories import resolveFilename, SCOPE_PLUGINS
from Components.Language import language
import gettext
from os import environ

PluginLanguagePath = resolveFilename(SCOPE_PLUGINS, 'SystemPlugins/e2componentsInitiator/locale')
    
def localeInit():
    lang = language.getLanguage()[:2]
    environ["LANGUAGE"] = lang
    gettext.bindtextdomain("e2cInitiator", PluginLanguagePath)

def mygettext(txt):
    t = gettext.dgettext("e2cInitiator", txt)
    if t == txt:
        t = gettext.gettext(txt)
    return t

localeInit()
language.addCallback(localeInit)
_ = mygettext

########################### KONFIGURACJA ###########################################
from Components.config import config, ConfigSubsection, ConfigDirectory, ConfigSelection, ConfigYesNo

MinFontChoices = [("0", _("Defined in skin")), ("1", _("same as max font")),
                  ("0.75", _("75%% of defined font")), ("0,67", _("67%% of defined font")),
                  ("0,5", _("50%% of defined font")) ]
#############################################################################################

config.plugins.j00zekCC = ConfigSubsection()

config.plugins.j00zekCC.PiconAnimation_UserPath = ConfigDirectory(default = _('not set'))  
config.plugins.j00zekCC.AlternateUserIconsPath = ConfigDirectory(default = _('not set'))
#j00zekLabel
config.plugins.j00zekCC.j00zekLabelSN = ConfigSelection(default = "0", choices = MinFontChoices )
config.plugins.j00zekCC.j00zekLabelEN = ConfigSelection(default = "0", choices = MinFontChoices )
#runningText
config.plugins.j00zekCC.rtType = ConfigSelection(default = "0", choices = [("0", _("Defined in skin")), ("0", _("NONE")),
                                                                           ("1", _("RUNNING")), ("2", _("SWIMMING")), ("3", _("AUTO"))])
config.plugins.j00zekCC.rtSpeed = ConfigSelection(default = "0", choices = [ ("0", _("Defined in skin")), ("25", _("40 px/s")),

                                                                             ("50", _("20 px/s")), ("100", _("10 px/s")) ])
config.plugins.j00zekCC.rtFontSize = ConfigSelection(default = "0", choices = [("0", _("Defined in skin")), ("0.1", _("+/- 10%%")), ("0.2", "+/- 20%%")])
config.plugins.j00zekCC.rtInitialDelay = ConfigSelection(default = "0", choices =   [ ("0", _("Defined in skin")), ("1", _("1")), ("2", _("2")), ("3", _("3")) ])
#EventName
config.plugins.j00zekCC.enDescrType = ConfigSelection(default = "0", choices = [("0", _("Defined in skin")), ("1", _("SHORT_DESCRIPTION")),
                                                                                ("2", _("EXTENDED_DESCRIPTION")), ("3", _("FULL_DESCRIPTION")) ])
#ConfigYesNo(default = False) #ConfigText(default = _("none")) #("", _(""))
