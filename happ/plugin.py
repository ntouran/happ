from armi import plugins
from armi import interfaces
from armi.interfaces import STACK_ORDER as ORDER

from happ import latticeInterface


class HallamPhysicsPlugin(plugins.ArmiPlugin):
    @staticmethod
    @plugins.HOOKIMPL
    def exposeInterfaces(cs):
        kernels = [
            interfaces.InterfaceInfo(ORDER.FLUX, latticeInterface.HallamLatticeInterface, {}),
        ]
        return kernels
