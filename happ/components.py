"""
Hallam-specific components.
"""

import math

from armi.reactor import parameters
from armi.reactor.components import basicShapes
from armi.reactor.components import ShapedComponent

SCALLOP_RADIUS = "sradius"
SCALLOP_OFFSET = "offset"

ONE_THIRD = 2.0 * math.pi / 3.0


def getScallopedHexParamDefs():
    """
    Need to add a radius of the scallop to fully define beyond a hex.
    """
    pDefs = parameters.ParameterDefinitionCollection()
    with pDefs.createBuilder(
        location=parameters.ParamLocation.AVERAGE, saveToDB=True
    ) as pb:
        pb.defParam(SCALLOP_RADIUS, units="cm", description="Radius of scallop")
        pb.defParam(
            SCALLOP_OFFSET,
            units="cm",
            description="Distance of prism off of line from scallop circle center",
        )
    return pDefs


class ScallopedHex(basicShapes.Hexagon):
    """
    A hexagon with circular scallops taken out of each corner.

    These represent the moderators in Hallam NPF.

    Notes
    -----
    Arguably the coolant outside them could be some kind of "annular" one of these
    with a thickness specified as well...hmm.
    """

    is3D = False
    pDefs = getScallopedHexParamDefs()

    def __init__(
        self,
        name,
        material,
        Tinput,
        Thot,
        ip=0.0,
        sradius=None,
        offset=None,
        mult=None,
        modArea=None,
        op=0.0,
        isotopics=None,
        mergeWith=None,
        components=None,
    ):
        ShapedComponent.__init__(
            self,
            name,
            material,
            Tinput,
            Thot,
            isotopics=isotopics,
            mergeWith=mergeWith,
            components=components,
        )

        self._linkAndStoreDimensions(
            components,
            ip=ip,
            sradius=sradius,
            offset=offset,
            mult=mult,
            op=op,
            modArea=modArea,
        )

    def getComponentArea(self, cold=False):
        """
        The scallop radius represents a subtraction of 6 thirds of circles.

        This is rather complicated because you must also know how far offset the hexagon
        is from the center of the circle that is being scalloped. This determines how much
        less than six thirds of a circle (2 circles) should be subtracted off of each
        corner. It takes some thinking, but it ends up being a trigonometry problem.

        We will call this slide dimension the *offset*.

        If an inner pitch is defined, then this makes a scalloped hex shell with
        constant thickness = (op-ip)/2. The second circle's radius is a simple sum of the
        original radius and the thickness.

        .. warning:: If you fail to adjust the radius and offset of the inner
            hex, you get area fractions that match Aronchick to 0.6% or less. If
            you include them you are off on SS304 by 20%. I believe Aronchick
            was wrong in this case. We can do sensitivity studies later.
        """
        area = basicShapes.Hexagon.getComponentArea(self, cold=cold)
        ip = self.getDimension("ip", cold=cold)
        mult = self.getDimension("mult")
        radius = self.getDimension(SCALLOP_RADIUS, cold=cold)
        offset = self.getDimension(SCALLOP_OFFSET, cold=cold)
        scallopArea = _computeScallopArea(radius, offset)

        area -= scallopArea * mult

        if ip:
            # recompute scallops different offset for "annular" scalloped hexes
            # inner hexagon itself is already subtracted off by the parent class
            op = self.getDimension("op", cold=cold)
            thickness = (op - ip) / 2.0
            # compute the scallops of the smaller inner hexagon
            # radius += thickness
            # offset += thickness
            scallopArea = _computeScallopArea(radius, offset)
            # addition here because overall formula is (hex1-scallop1) - (hex2-scallop2)
            # or equivalently (hex1 - hex2) - scallop1 + scallop2
            area += scallopArea * mult

        return area


def _computeScallopArea(radius, offset):
    """
    Compute how much area should be subtracted given a radius and offset in cm.

    You really need to draw the triangles here to see what's going on. 
    """
    circleArea = math.pi * radius ** 2
    angleInRadians = math.atan(offset / radius)
    # what fraction of 6/3 (2) circles is subtracted off?
    circleFraction = 2.0 * (ONE_THIRD - angleInRadians) / ONE_THIRD
    return circleFraction * circleArea
