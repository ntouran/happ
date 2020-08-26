"""A subclass of the Dragon lattice physics plugin's interface that runs Hallam XS"""
from armi import runLog
from armi.reactor.flags import Flags

from terrapower.physics.neutronics.dragon import dragonInterface
from terrapower.physics.neutronics.dragon import dragonWriter
from terrapower.physics.neutronics.dragon import dragonExecutor
from terrapower.physics.neutronics.dragon.dragonFactory import dragonFactory

from .plugin import CONF_OPT_HALLAM_DRAGON
from . import unitCellConverter


class HallamLatticeInterface(dragonInterface.DragonInterface):
    """Runs lattice physics for 1-D Hallam cases."""

    name = "HallamLattice"

    def __init__(self, r, cs):
        """
        Register Hallam subclasses with the DRAGON factory

        We wait until the interface is instantiated to do this so we can be sure
        all settings are fully loaded at this point.
        """
        dragonInterface.DragonInterface.__init__(self, r, cs)
        _registerHallamDragonSubclasses()

    def selectObjsToRun(self):
        """
        Choose blocks that will be passed for DRAGON analysis.

        For starters we will hard-code the blueprint-derived basic fuel cell.
        """
        basicFuelDesign = self.o.r.blueprints.blockDesigns["basic fuel"]
        basicFuel = basicFuelDesign.construct(
            self.o.cs,
            self.o.r.blueprints,
            0,
            1,
            height=1,
            xsType="A",
            materialInput={},
        )
        return [basicFuel]


def _registerHallamDragonSubclasses():
    """
    Register 1-D Hallam code with the Dragon factory.

    Use baseline classes for most operations
    """
    dragonFactory.copyEntriesToKey(CONF_OPT_HALLAM_DRAGON)
    dragonFactory.setKey(CONF_OPT_HALLAM_DRAGON)
    dragonFactory.registerWriter(CONF_OPT_HALLAM_DRAGON, HallamDragonWriter)
    dragonFactory.registerExecuter(CONF_OPT_HALLAM_DRAGON, HallamDragonExecuter)


class HallamDragonWriter(dragonWriter.DragonWriterHomogenized):
    def _buildTemplateData(self):
        """Add 1-D geometry information to the template data."""
        templateData = dragonWriter.DragonWriterHomogenized._buildTemplateData(self)
        templateData["radii"] = self._makeRadii()
        templateData["geomsplits"] = self._makeGeomSplits()
        return templateData

    def _makeRadii(self):
        radii = []
        for obj in sorted(self.armiObjs):
            radii.append(obj.getDimension("od") / 2.0)
        return radii

    def _makeGeomSplits(self):
        """Say how many times to split each ring"""
        splits = [
            5 if obj.hasFlags([Flags.FUEL, Flags.MODERATOR]) else 1
            for obj in self.armiObjs
        ]
        return splits


class HallamDragonExecuter(dragonExecutor.DragonExecuter):
    """Transform the ARMI blocks to unit cells on their way into the 1-D writer."""

    def __init__(self, options: dragonExecutor.DragonOptions, block):
        dragonExecutor.DragonExecuter.__init__(self, options, block)
        self._transformToUnitCell()

    def _transformToUnitCell(self):
        """Replace this Executer's block with a 1-D converted form."""
        conv = unitCellConverter.HallamUnitCellConverter(self.block)
        self.block = conv.convert()

    def writeInput(self):
        """Write the input file with the children of this converted unit cell block."""
        inputWriter = dragonFactory.makeWriter(self.block, self.options)
        inputWriter.write()
