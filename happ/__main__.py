import sys
import os


def buildPath():
    """
    Add plugins/ and armi/ submodules, and the root to the path. 

    Notes
    -----
    This allows the plugins to be
    imported from the more informal `plugins/` directory if they are pulled in as
    submodules, rather than installed into the users formal Python environment.
    This should be done rather early, as it is intended to function //as if// the plugins
    themselves were in the pythonpath all along.

    """
    # prepend the expected ARMI framework location to the path so we don't accidentally
    # get another one if it is present.
    sys.path.insert(
        0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "armi"))
    )

    root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    base, pluginDirs, _ = next(os.walk(os.path.join(root, "plugins")))
    for pluginDir in pluginDirs:
        sys.path.append(os.path.join(base, pluginDir))

    sys.path.append(os.path.abspath(root))


buildPath()

import armi
from armi.cli import ArmiCLI
from happ import app

# if running this as an app, we must register the app
# (otherwise we may be running as a plugin and don't want to register it)
armi.configure(app.HallamApp())


def main():
    code = ArmiCLI().run()
    sys.exit(code)


if __name__ == "__main__":
    main()
