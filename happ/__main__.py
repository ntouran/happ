import sys
from armi.cli import ArmiCLI
import armi

from happ import app

# if running this as an app, we must register the app
# (otherwise we may be running as a plugin and don't want to register it)
armi.configure(app.HallamApp())


def main():
    code = ArmiCLI().run()
    sys.exit(code)


if __name__ == "__main__":
    main()
