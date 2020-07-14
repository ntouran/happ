import armi
from armi.apps import App

from happ.plugin import HallamPhysicsPlugin

class HallamApp(App):
    def __init__(self):
        # activate all built-in plugins
        App.__init__(self)

        # register our plugin with the plugin manager
        self._pm.register(HallamPhysicsPlugin)

    @property
    def splashText(self):
        return "** Nick's Hallam App **"
