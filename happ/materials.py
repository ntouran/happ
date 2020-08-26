from armi import materials
from armi.materials import material
from armi.materials import graphite
from armi.utils.units import getTc


class UMo(materials.FuelMaterial):
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

    def applyInputParams(self, U235_wt_frac=None, *args, **kwargs):
        """Adjust uranium enrichment from input"""
        U235_wt_frac = 0.1 if U235_wt_frac is None else U235_wt_frac
        self.setMassFrac("U235", U235_wt_frac * 0.9)
        self.setMassFrac("U238", (1.0 - U235_wt_frac) * 0.9)
        materials.FuelMaterial.applyInputParams(self, *args, **kwargs)

    def linearExpansionPercent(self, Tk=None, Tc=None):
        r"""
        Get linear expansion dLL in percent.

        Aronchick expands fuel from 17.1 at 21.1°C to 16.64 g/cc at fuel operating
        temperature (476 °C), so this should be consistent with that endpoint.

        During ARMI's 3D thermal expansion, density is scaled by 1/(1+dLL)**3
        So we need

        .. math::

            \frac{17.1}{16.64} = (1+dLL(T_H))^3

        """
        tempC = getTc(Tc, Tk)
        return 100 * (tempC - 20.0) * 0.00913 / 476.0

    def heatCapacity(self, Tk=None, Tc=None):
        """Cp from Burkes in J/g-C"""
        Tc = getTc(Tc, Tk)
        return 0.137 + 5.12e-5 * Tc + 1.99e-8 * Tc ** 2


class SS304(materials.Material):
    """
    Stainless Steel 304 for Hallam

    Information from Aronchick
    """

    name = "SS304"

    def setDefaultMassFracs(self):
        """Set mass fracs and density from Table 2 in Aronchick"""
        self.setMassFrac("FE", 0.74)
        self.setMassFrac("CR", 0.18)
        self.setMassFrac("NI", 0.08)
        self.p.refDens = 7.90

    def linearExpansionPercent(self, Tk=None, Tc=None):
        r"""
        Get linear expansion dLL in percent.

        Aronchick expands steel from 7.9 at 21.1°C to 7.72 g/cc at operating temperature
        (assume 400 °C), so this should be consistent with that endpoint.

        Similar to UMo, we solve

        .. math::

            \frac{7.9}{7.72} = (1+dLL(T_H))^3

        """
        tempC = getTc(Tc, Tk)
        return 100 * (tempC - 20.0) * 0.007712 / 400.0


class Zircaloy2(materials.Material):
    """
    Zircaloy 2 for Hallam

    Information from Aronchick
    """

    name = "Zircaloy2"

    def setDefaultMassFracs(self):
        """Set mass fracs and density from Table 2 in Aronchick"""
        self.setMassFrac("ZR", 0.985)
        self.setMassFrac("SN", 0.015)
        self.p.refDens = 6.57

    def linearExpansionPercent(self, Tk=None, Tc=None):
        r"""
        Get linear expansion dLL in percent.

        .. math::

            \frac{6.57}{6.52} = (1+dLL(T_H))^3

        """
        tempC = getTc(Tc, Tk)
        return 100 * (tempC - 20.0) * 0.00255 / 400.0


class HastelloyX(materials.Material):
    """
    Control cladding for Hallam.

    Note that this material was NOT modeled in the original aronchick paper explicitly,
    but rather used specialized calculations.
    """

    name = "HastelloyX"

    def setDefaultMassFracs(self):
        """Info derived from haynes data sheet"""
        self.setMassFrac("NI", 0.51)  # 47, but lumping others in
        self.setMassFrac("CR", 0.22)
        self.setMassFrac("FE", 0.18)
        self.setMassFrac("MO", 0.09)
        self.p.refDens = 8.22

    def linearExpansionPercent(self, Tk=None, Tc=None):
        """
        Disable thermal expansion for this material for now

        It won't matter much for the paper
        """
        # returning 0 actually triggers an error in ARMI
        return 0.0001

    def linearExpansionFactor(self, Tc, T0):
        return 0.0001


class RareEarths(materials.Material):
    """
    Control material (Gd oxide, Sm oxide) for Hallam

    Note that this material was NOT modeled in the original aronchick paper explicitly,
    but rather used specialized calculations.
    """

    name = "RareEarths"

    def setDefaultMassFracs(self):
        """Made up numbers for starters"""
        self.setMassFrac("GD", 0.3)
        self.setMassFrac("SM", 0.3)
        self.setMassFrac("O", 0.4)
        self.p.refDens = 4.22

    def linearExpansionPercent(self, Tk=None, Tc=None):
        """
        Disable thermal expansion for this material for now

        It won't matter much for the paper
        """
        # returning 0 actually triggers an error in ARMI
        return 0.0001

    def linearExpansionFactor(self, Tc, T0):
        return 0.0001


class Graphite(graphite.Graphite):
    """
    Graphite with reduced density to match Table 2 in Aronchick.
    """

    name = "Graphite"

    def setDefaultMassFracs(self):
        """Reduce density to comply with paper"""
        graphite.Graphite.setDefaultMassFracs(self)
        self.p.refDens = 1.67


class Helium(material.Fluid):
    name = "Helium"

    def setDefaultMassFracs(self):
        """Helium"""
        self.setMassFrac("HE4", 1.0)
        self.p.refDens = 0.001
