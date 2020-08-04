from armi import materials
from armi.utils.units import getTc

class UMo(materials.Material):
    """
    U-10Mo metallic fuel for Hallam

    There is a good modern reference for this material in [Burkes]_. 

    .. [Burkes] Thermophysical Properties of U-10Mo Alloy INL/EXT-10-19373
        https://inldigitallibrary.inl.gov/sites/sti/sti/4702554.pdf (2010)

    """
    name = "UMo"
    enrichedNuclide = "U235"
    def setDefaultMassFracs(self):
        """Set mass fracs and density from Table 2 in Aronchick"""
        self.setMassFrac("MO", 0.1)
        self.setMassFrac("MO", 0.1)
        self.setMassFrac("U235", 0.036 * 0.9)
        self.setMassFrac("U238", (1.0 - 0.036) * 0.9)
        self.p.refDens = 17.1


    def applyInputParams( self, U235_wt_frac=None, *args, **kwargs)
        """Adjust uranium enrichment from input"""
        U235_wt_frac = 0.1 if U235_wt_frac is None else U235_wt_frac
        self.setMassFrac("U235", U235_wt_frac * 0.9)
        self.setMassFrac("U238", (1.0 - U235_wt_frac) * 0.9)
        material.FuelMaterial.applyInputParams(self, *args, **kwargs)

    def linearExpansionPercent(self, Tk=None, Tc=None):
        r"""
        Get linear expansion dLL in percent.

        Aronchick expands fuel from 17.1 at 21.1°C to 16.64 g/cc at fuel operating
        temperature (476 °C), so this should be consistent with that endpoint.

        During ARMI's 2D thermal expansion, density is scaled by 1/(1+dLL)**2.
        So we need

        .. math::

            \frac{17.1}{16.64} = (1+dLL(T_H))^2

        """
        tempC = getTc(Tc, Tk)
        return (tempC-20.) * 0.1372/476.0

    def heatCapacity(self, Tk=None, Tc=None):
        """Cp from Burkes in J/g-C"""
        Tc = getTc(Tc, Tk)
        return 0.137+5.12e-5*Tc+1.99e-8*Tc**2
