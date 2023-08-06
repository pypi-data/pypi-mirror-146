import argparse


def main():
    parser = argparse.ArgumentParser(prog='guinstall',
                                     description='Easy installation for gui_scripter apps')

    parser.add_argument('-requirements', action='store_const', const=True,
                        default=False, dest='requirements',
                        help="Greet Message from Geeks For Geeks.")

    args = parser.parse_args()

    if args.requirements:
        print("requirements arg added !")
