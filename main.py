from apps.pong import Pong
from system import System


def main():
    apps = [Pong()]
    system = System(apps)
    system.run()


if __name__ == "__main__":
    main()
