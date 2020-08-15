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
from armi.reactor.converters import blockConverters


class HallamUnitCellConverter(blockConverters.BlockConverter):
    def convert(self):
        pass
