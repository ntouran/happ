"""
The Hallam plugin with design-specific settings, shapes, code, etc.

This can be used in the standalone Hallam App or as part of a different app.
"""
from armi import plugins
from armi import interfaces
from armi import interfaces
from armi.reactor.assemblies import HexAssembly
from armi.settings import setting
from armi.physics.neutronics import settings as neutronicsSettings

from happ.blocks import HallamBlock
from happ import components
from happ.cli import summary
from happ.cli import makeXS


CONF_OPT_HALLAM_DRAGON = "Hallam-DRAGON"
ORDER = interfaces.STACK_ORDER.CROSS_SECTIONS


class HallamPhysicsPlugin(plugins.ArmiPlugin):
    """Plugin with Hallam specific hooks"""

    @staticmethod
    @plugins.HOOKIMPL
    def exposeInterfaces(cs):
        from happ.latticeInterface import HallamLatticeInterface

        if cs["xsKernel"] == CONF_OPT_HALLAM_DRAGON:
            klass = HallamLatticeInterface
            return [interfaces.InterfaceInfo(ORDER, klass, {})]

    @staticmethod
    @plugins.HOOKIMPL
    def defineBlockTypes():
        """Register the Hallam block type with ARMI"""
        return [(components.ScallopedHex, HallamBlock)]

    @staticmethod
    @plugins.HOOKIMPL
    def defineAssemblyTypes():
        """Register the Hallam block type with Hex assemblies"""
        return [(HallamBlock, HexAssembly)]

    @staticmethod
    @plugins.HOOKIMPL
    def definParameters():
        """Register the custom parameters"""
        return {components.ScallopedHex: components.getScallopedHexParamDefs()}

    @staticmethod
    @plugins.HOOKIMPL
    def defineEntryPoints():
        return [
            summary.HallamTables,
            # makeXS.MakeXSEntryPoint
        ]

    @staticmethod
    @plugins.HOOKIMPL
    def defineSettings():
        """Define settings for the Hallam plugin."""
        settings = [
            # add XS kernel option for the Hallam 1-D mode
            setting.Option(CONF_OPT_HALLAM_DRAGON, neutronicsSettings.CONF_XS_KERNEL),
        ]
        return settings
