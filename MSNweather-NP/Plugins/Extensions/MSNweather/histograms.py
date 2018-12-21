from Components.ActionMap import ActionMap
from enigma import getDesktop
from Components.Label import Label
from Components.Sources.StaticText import StaticText
from Screens.Screen import Screen
from os import path

class MSNweatherHistograms(Screen):
    if getDesktop(0).size().width() >= 192:
        skin = """
  <screen name="MSNweatherHistograms" position="center,center" size="1200,500" title="What happened in last 24 hours?">
    <widget name="Title1" position="0,10" size="420,25" font="Regular;20" halign="center"/>
    <widget name="Title2" position="0,50" size="420,25" font="Regular;20" halign="center"/>
    <widget name="Title3" position="0,100" size="420,25" font="Regular;20" halign="center"/>
  </screen>
"""

    def __init__(self, session, args = 0):
        self.session = session
        Screen.__init__(self, session)
        self["setupActions"] = ActionMap(["SetupActions", "ColorActions"],
            {
                "cancel": self.cancel,
                "ok": self.keyOk,
            }, -2)
        self.setTitle(_("What happened in weather during last 24 hours?"))
        self['Title1'] = Label(_("Preassure"))
        self['Title2'] = Label(_("Wind"))
        self['Title3'] = Label(_("Temperatur"))

    def keyOk(self):
        self.close()

    def cancel(self):
        self.close()
