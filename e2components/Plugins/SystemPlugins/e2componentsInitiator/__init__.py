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
config.plugins.j00zekCC.rtType = ConfigSelection(default = "0", choices = [("0", _("Defined in skin")), ("1", _("don't move")), ("2", _("RUNNING")), ("3", _("SWIMMING"))])
config.plugins.j00zekCC.rtFontSize = ConfigSelection(default = "0", choices = [("0", _("if defined in skin")), ("0.1", _("+/- 10%%")), ("0.2", "+/- 20%%")])
config.plugins.j00zekCC.rtStartDelay = ConfigSelection(default = "0", choices =   [ ("0", _("Defined in skin")), ("1000", _("1s")), ("2000", _("2s")),
                                                                                   ("4000", _("4s")), ("6000", _("6s")), ("8000", _("8s")) ])
config.plugins.j00zekCC.rtStepTimeout = ConfigSelection(default = "0", choices = [ ("0", _("Defined in skin")), ("25", _("40 px/s")),
                                                                             ("50", _("20 px/s")), ("100", _("10 px/s")) ])
config.plugins.j00zekCC.rtRepeat = ConfigSelection(default = "0", choices = [ ("0", _("Defined in skin")), ("1", _("one time")),
                                                                             ("5", _("5 times")), ("100", _("never stop")) ])
#EventName
config.plugins.j00zekCC.enDescrType = ConfigSelection(default = "0", choices = [("0", _("Defined in skin")), ("1", _("Short")),
                                                                                ("2", _("Extended or Short")), ("3", _("Short and Extended")),
                                                                                ("4", _("Extended and short (if different)")) ])
config.plugins.j00zekCC.enTMDBratingFirst = ConfigYesNo(default = False)
#ConfigText(default = _("none")) #("", _(""))
