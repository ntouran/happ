"""
Hallam-specific components.
"""
from armi.reactor import parameters
from armi.reactor.components import basicShapes
from armi.reactor.components import ShapedComponent

SCALLOP_RADIUS = "sradius"


def getScallopedHexParamDefs():
    """
    Need to add a radius of the scallop to fully define beyond a hex.
    """
    pDefs = parameters.ParameterDefinitionCollection()
    with pDefs.createBuilder(
        location=parameters.ParamLocation.AVERAGE, saveToDB=True
    ) as pb:
        pb.defParam(SCALLOP_RADIUS, units="cm", description="Radius of scallop")


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
        ip=None,
        sradius=None,
        mult=None,
        modArea=None,
        op=None,
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
            components, ip=ip, sradius=sradius, mult=mult, op=op, modArea=modArea
        )

    def getComponentArea(self, cold=False):
        """The scallop radius represents a subtraction of 2 full circles"""
        area = basicShapes.Hexagon.getComponentArea(self, cold=cold)
        circleArea = math.pi * self.getDimension(SCALLOP_RADIUS, cold=cold) ** 2
        mult = self.getDimension("mult")
        return area - circleArea * 6 * mult
