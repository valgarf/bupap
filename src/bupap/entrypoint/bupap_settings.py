import sys

from bupap.config import settings


def main():
    argv = sys.argv[1:]
    if len(argv) != 1 or "--help" in argv or "-h" in argv:
        print(
            f"Usage: Calling `bupap-settings settings_key` will print the value of the settings key"
        )
        return
    try:
        print(settings[argv[0]])
    except KeyError:
        print(f"Unknown settings key {argv[0]}")


if __name__ == "__main__":
    main()
