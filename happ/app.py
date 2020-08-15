import armi
from armi.apps import App
from armi import materials

from terrapower.physics.neutronics.dragon import DragonPlugin

from happ.plugin import HallamPhysicsPlugin


class HallamApp(App):
    def __init__(self):
        # activate all built-in plugins
        App.__init__(self)

        # set app-specific material lookup order to prioritize the Hallam materials.
        # You want to set material namespace order here so it is active whenever
        # you have activated this particular app.
        materials.setMaterialNamespaceOrder(["happ.materials", "armi.materials"])

        # register our plugin with the plugin manager
        self._pm.register(HallamPhysicsPlugin)
        self._pm.register(DragonPlugin)

    @property
    def splashText(self):
        return "** Nick's Hallam App **"
