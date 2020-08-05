from armi.cli.entryPoint import EntryPoint
from armi.reactor.flags import Flags
from armi import materials


class HallamTables(EntryPoint):
    """Make some input-checking tables to compare with old Hallam pubs."""
    name="tables"
    settingsArgument='required'


    def invoke(self):
        from armi import cases
        case = cases.Case(cs=self.cs)
        self._o = case.initializeOperator()
        
        self._makeMaterialTable()

    def _makeMaterialTable(self):
        """Make a table that shows area fractions on a material basis.

        Can be compared with Aronchik Table 2.
        """
        core = self._o.r.core
        b = core.getFirstBlock(Flags.FUEL|Flags.INNER)
        matNames = getAllMaterials(b)
        areas = {}
        total = 0.0
        densities = {}
        for matName in matNames:
            comps = b.getComponentsOfMaterial(materialName=matName)
            area = sum([c.getArea() for c in comps])
            areas[matName]=area
            densities[matName]=comps[0].material.density3(Tc=comps[0].p.temperatureInC)
            total+=area

        for matName, area in sorted(areas.items()):
            print(f"{matName:20s} {densities[matName]:4.2f} {area/total:.6f}")

def getAllMaterials(obj):
    """
    Get set of all material names in composite

    Notes
    -----
    Uses names instead of objects to keep them unique.
    """
    mats=set()
    for child in obj.getChildren(deep=True):
        if hasattr(child,'material'):
            mats.add(child.material.name)
    return mats
