import armi

from armi import materials

materials.setMaterialNamespaceOrder(["happ.materials", "armi.materials"])

from happ import app

armi.configure(app.HallamApp())
