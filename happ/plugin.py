from armi import plugins
from armi import interfaces
from armi.interfaces import STACK_ORDER as ORDER
from armi.reactor.assemblies import HexAssembly

from happ import latticeInterface

from happ.blocks import HallamBlock
from happ.components import ScallopedHex


class HallamPhysicsPlugin(plugins.ArmiPlugin):
    @staticmethod
    @plugins.HOOKIMPL
    def exposeInterfaces(cs):
        kernels = [
            interfaces.InterfaceInfo(
                ORDER.FLUX, latticeInterface.HallamLatticeInterface, {}
            )
        ]
        return kernels

    @staticmethod
    @plugins.HOOKIMPL
    def defineBlockTypes():
        """Register the Hallam block type with ARMI"""
        return [(ScallopedHex, HallamBlock)]

    @staticmethod
    @plugins.HOOKIMPL
    def defineAssemblyTypes():
        """Register the Hallam block type with Hex assemblies"""
        return [(HallamBlock, HexAssembly)]
