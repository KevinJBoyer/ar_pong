from apps.pong import Pong
from apps.setup import Setup
from system.system import System


def main():
    apps = [Pong]

    system = System()
    setup = Setup(system, apps=apps)
    system.run()


if __name__ == "__main__":
    main()
