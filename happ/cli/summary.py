from armi.cli.entryPoint import EntryPoint
from armi.reactor.flags import Flags
from armi import materials
from armi.nucDirectory import nuclideBases as nb


class HallamTables(EntryPoint):
    """Make some input-checking tables to compare with old Hallam pubs."""

    name = "tables"
    settingsArgument = "required"

    def invoke(self):
        from armi import cases

        case = cases.Case(cs=self.cs)
        o = self._o = case.initializeOperator()

        core = self._o.r.core
        b = core.getFirstBlock(Flags.FUEL | Flags.INNER)
        self._makeMaterialTable(b)
        self._makeNumberDensityTable(b)
        print(b.getMaxArea())

        basicFuelDesign = o.r.blueprints.blockDesigns["basic fuel"]
        basicFuel = basicFuelDesign.construct(o.cs, o.r.blueprints, 0, 1, 10, "A", {})
        self._makeMaterialTable(basicFuel)
        self._makeNumberDensityTable(basicFuel)
        print(basicFuel.getMaxArea())

    def _makeMaterialTable(self, b):
        """
        Make a table that shows area fractions on a material basis.

        Can be compared with Aronchik Table 2.
        """
        matNames = getAllMaterials(b)

        densities = getMatDensities(b, matNames)
        areas = getAreaFracsByMaterial(b, matNames)

        for matName, area in sorted(areas.items()):
            print(f"{matName:20s} {densities[matName]:6.3f} {area:.6f}")

    def _makeNumberDensityTable(self, b):
        """
        Make a table of number densities by element. 

        C.f. Aronchick Table 3
        """
        elements = ("ZR", "C", "MO", "FE", "NI", "CR", "NA", "SN")
        ndens = b.getNumberDensities()
        totals = {}
        for el in elements:
            totalNumDens = 0.0
            eb = nb.byName[el]
            for nucBase in eb.getNaturalIsotopics():
                totalNumDens += ndens.pop(nucBase.name, 0.0)
            totals[el] = totalNumDens

        # grab the leftovers:
        for nucName, nd in sorted(ndens.items()):
            totals[nucName] = nd

        for name, ndens in totals.items():
            if not ndens:
                continue
            print(f"{name:6s} {ndens:10.5e}")


def getAreaFracsByMaterial(b, matNames):
    areas = {}
    total = 0.0
    for matName in matNames:
        comps = b.getComponentsOfMaterial(materialName=matName)
        area = sum([c.getArea() for c in comps])
        areas[matName] = area
        total += area

    for matName in areas:
        areas[matName] /= total

    return areas


def getMatDensities(b, matNames):
    """Get mass densities of a list of material names"""
    densities = {}
    for matName in matNames:
        comps = b.getComponentsOfMaterial(materialName=matName)
        densities[matName] = comps[0].material.density3(Tc=comps[0].p.temperatureInC)
    return densities


def getAllMaterials(obj):
    """
    Get set of all material names in composite

    Notes
    -----
    Uses names instead of objects to keep them unique.
    """
    mats = set()
    for child in obj.getChildren(deep=True):
        if hasattr(child, "material"):
            mats.add(child.material.name)
    return mats
