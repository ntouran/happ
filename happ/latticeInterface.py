import os

import numpy as np

from armi import runLog
from armi import interfaces
from armi.physics import neutronics


class HallamLatticeInterface(interfaces.Interface):
    name = "HallamLattice"

    def interactBOC(self, cycle=None):
        runLog.info("Making Hallam cross sections :o")

