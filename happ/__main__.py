import sys
from armi.cli import ArmiCLI


def main():
    code = ArmiCLI().run()
    sys.exit(code)


if __name__ == "__main__":
    main()
