import sys
from .cli import CLI


def main():
    cli = CLI()
    args = cli.parse_args()
    cli.exec_convert(args)


if __name__ == "__main__":
    main()
