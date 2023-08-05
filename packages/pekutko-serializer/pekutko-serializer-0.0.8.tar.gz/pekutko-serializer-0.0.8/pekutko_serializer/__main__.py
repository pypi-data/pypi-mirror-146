import sys

sys.path.append(sys.path[0] + "/.")

# sys.path.append("..")

from serializer import create_serializer
# from cli.CLI import CLI

exit()
def main():
    cli = CLI()
    args = cli.parse_args()
    cli.exec_convert(args)



if __name__ == "__main__":
    main()