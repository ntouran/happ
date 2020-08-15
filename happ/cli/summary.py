import tabulate

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
        self.o = case.initializeOperator()

        self._compareVolumeFractions()
        self._compareNumberDensities()

        self.o = None

    def _compareVolumeFractions(self):
        """Make table(s) to comparing our unit cell vol fracs to Aronchick's Table 2"""
        bFiveOne, basicFuel = self._getUnitCells()
        aronchickBasicFracs = (0.044491, 0.007841, 0.11066, 0.01209, 0.82200, 0.002910)
        aronchickFiveOneFracs = (0.037076, 0.007183, 0.10492, 0.01167, 0.82200, 0.01715)

        matNames = ("UMo", "SS304", "Sodium", "Zircaloy2", "Graphite", "Void")
        header = ["Material", "Aronchick", "ARMI", "diff (%)"]
        fracs = getAreaFracsByMaterial(basicFuel, matNames)
        print("Unit Cell Comparison for Basic Fuel Cell")
        table = []
        for mat, ref in zip(matNames, aronchickBasicFracs):
            table.append((mat, ref, fracs[mat], 100 * (fracs[mat] - ref) / ref))
        print(tabulate.tabulate(table, headers=header))
        print(basicFuel.getMaxArea())

        print("\nUnit Cell Comparison for 5/1 Fuel Cell")
        fracs = getAreaFracsByMaterial(bFiveOne, matNames)
        table = []
        for mat, ref in zip(matNames, aronchickFiveOneFracs):
            table.append((mat, ref, fracs[mat], 100 * (fracs[mat] - ref) / ref))
        print(tabulate.tabulate(table, headers=header))
        print(bFiveOne.getMaxArea())

        print(getMatDensities(basicFuel, matNames))

    def _compareNumberDensities(self):
        bFiveOne, basicFuel = self._getUnitCells()
        self._makeNumberDensityTable(bFiveOne)
        self._makeNumberDensityTable(basicFuel)

    def _getUnitCells(self):
        core = self.o.r.core
        bFiveOne = core.getFirstBlock(Flags.FUEL | Flags.INNER)
        basicFuelDesign = self.o.r.blueprints.blockDesigns["basic fuel"]
        basicFuel = basicFuelDesign.construct(
            self.o.cs, self.o.r.blueprints, 0, 1, 10, "A", {}
        )
        return bFiveOne, basicFuel

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
