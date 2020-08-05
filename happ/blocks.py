"""
Define custom Blocks class for Hallam.

The Hallam blocks are basically hexagons, but rather than having any given
component on the outside, they have a mix of process tubes and graphite.
Thus, we need to customize how they figure out what their maximum area is. 
We will use the dimension of the moderators to derive the max area.
"""
import math

from armi.reactor import blocks
from armi.reactor.flags import Flags
from armi.utils import hexagon


class HallamBlock(blocks.HexBlock):
    """
    Hexagonal block with max area defined by scalloped moderator component.

    The side length of the large hex is exactly equal to the flat-to-flat pitch of the
    perfect hexagons of the moderators (including gap and sheath), which should be 16.102"
    nominally. Thus, the pitch of the large hex is sqrt(3)*s = sqrt(3)*(the pitch of the
    small hex).
    """

    def getMaxArea(self):
        modClad = self.getComponent(Flags.MODERATOR|Flags.CLAD, exact=True)
        gap = self.getComponent(Flags.MODERATOR|Flags.COOLANT|Flags.GAP, exact=True)
        modPitch = modClad.getPitchData()+gap.getDimension("widthOuter")
        return hexagon.area(math.sqrt(3)*modPitch)
