"""
Takes a Hallam unit cell and converts it to concentric cylinders

The Hallam fuel/control/moderator unit cell is quite complex. This converts
it as input in full detail into a set of homogenized cylinders in advance
of running 1-D lattice physics calculations.

This is related to what the BlockConverter in ARMI does but that is actually 
pretty specific to Hex pin lattice assemblies. It may make sense to graduate
this implementation to the framework if it is more generic, and then label
that particular implementation as more specific. 

Fundamentally, what we want to do is to define a list of groups of components, 
each of which will become a circle. We'll start from the inside moving
out. For example, in Aronchick Figure 5, the Helium is the first 
region in the fuel cell is the center hole, which in our Hallam inputs is made 
of the ``center tube`` and the ``center hole`` components. So for the basic fuel
cell in 1D (Figure 6) we would have something like::

    rings = [
        (center hole, center tube), 
        (fuel, clad, coolant), 
        (process tube,), 
        (moderator coolant, moderator clad), 
        (moderator, more moderator clad),
    ]

But our hex global cases are conducive to making the 5/1 cell of figure 7. 
This has control/void in the middle with some surrounding graphite/na/ss, and
then has the equivalent of 5 basic fuel cells around it. 

"""
from dataclasses import dataclass
from typing import List

from armi.reactor.converters import blockConverters
from armi.reactor.components import Component
from armi.reactor import blocks
from armi.reactor import components


@dataclass
class RingSpec:
    """Data needed to define a ring in a ring-converted block."""

    components: List[Component]
    innerDiamCm: float = 0.0
    heightCm: float = 1.0
    fraction: float = 1.0


class HallamUnitCellConverter(blockConverters.BlockConverter):
    """Hallam-specific unit cell converter that grabs key components to make 1-D unit cells."""

    def __init__(self, sourceBlock, quiet=False):
        blockConverters.BlockConverter.__init__(self, sourceBlock, quiet=quiet)
        self.ringSpecs = []

        self.convertedBlock = blocks.ThRZBlock(
            name=sourceBlock.name + "-cyl", height=sourceBlock.getHeight()
        )
        self.convertedBlock.setLumpedFissionProducts(
            sourceBlock.getLumpedFissionProductCollection()
        )
        self._buildRingSpecs()

    def _buildRingSpecs(self):
        """
        Build ring specifications for Hallam fuel cell.

        Height and inner radius will be added during conversion.
        """
        sbn = self._sourceBlock.getComponentByName
        self.ringSpecs = [
            RingSpec(components=[sbn("center hole"),]),
            RingSpec(
                components=[
                    sbn("center tube"),
                    sbn("spacers"),
                    sbn("fuel"),
                    sbn("clad"),
                    sbn("bond"),
                    sbn("coolant"),
                ]
            ),
            RingSpec(components=[sbn("process tube")]),
            RingSpec(
                components=[sbn("moderator coolant annulus"), sbn("moderator clad")]
            ),
            RingSpec(components=[sbn("moderator"), sbn("moderator coolant gap")]),
        ]

    def convert(self):
        innerDiam = 0.0
        height = self._sourceBlock.getHeight()
        for ringSpec in self.ringSpecs:
            ringSpec.innerDiamCm = innerDiam
            ringSpec.heightCm = height
            ring = _makeRing(ringSpec)
            self.convertedBlock.add(ring)
            innerDiam = ring.getDimension("od")
        return self.convertedBlock


def _makeRing(ringSpec: RingSpec):
    """Given a ring specification, make a circle component representing it."""

    blender = blocks.Block(name="blender")
    for c in ringSpec.components:
        blender.add(components.UnshapedComponent.fromComponent(c))

    area = blender.getVolume() / ringSpec.heightCm * ringSpec.fraction

    tempInC = sum(c.temperatureInC for c in ringSpec.components) / len(
        ringSpec.components
    )

    outerDiamCm = blockConverters.getOuterDiamFromIDAndArea(ringSpec.innerDiamCm, area)
    ring = components.Circle(
        "convertedRing",
        "Custom",
        tempInC,
        tempInC,
        od=outerDiamCm,
        id=ringSpec.innerDiamCm,
        mult=1,
    )
    # here we lose a bit of identity of the constituents.
    # it would be a bit nicer if we could add components to components
    nDensities = blender.getNumberDensities()
    nDensities = {k: v * ringSpec.fraction for k, v in nDensities.items()}
    ring.setNumberDensities(nDensities)
    return ring
