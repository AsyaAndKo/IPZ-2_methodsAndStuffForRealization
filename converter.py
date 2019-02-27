import argparse


def xml2json(input_file: str, out_file: str):
    from xmltodict import parse
    from json import dump

    try:
        f = open(input_file, "rb")
        out = open(out_file, "w")
    except OSError as e:
        print(f"Can't open file {e}")
        return

    res: str = parse(f)
    dump(res, out, indent=4)


def json2xml(input_file: str, out_file: str):
    from xmltodict import unparse
    from json import load

    try:
        f = open(input_file, "r")
        out = open(out_file, "w")
    except OSError as e:
        print(f"Can't open file {e}")
        return

    res: str = unparse(load(f), pretty=True)
    out.write(res)


CONVERTERS: dict = {
    "json2xml": json2xml,
    "xml2json": xml2json
}


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description="Converts files")

    ap.add_argument("--list",
                    default=False,
                    action="store_const",
                    const=True,
                    help="List of available parsers")
    ap.add_argument("-c", "--converter",
                    type=str,
                    default=False,
                    help="Name of the converter")
    ap.add_argument("-i", "--in",
                    dest="in_file",
                    type=str,
                    default=False,
                    help="Path to the input file")
    ap.add_argument("-o", "--out",
                    dest="out_file",
                    type=str,
                    default=False,
                    help="Path to the output file")

    args = ap.parse_args()

    if args.list:
        print("Available converters:")
        for conv in CONVERTERS.keys():
            print(f"\t{conv}")
    elif args.converter and args.in_file and args.out_file:
        print(f"Converting from {args.in_file} to {args.out_file}")

        CONVERTERS[args.converter](args.in_file, args.out_file)

        print("Converted successfully")
    elif args.in_file and args.out_file:
        print("Trying to determine converter type from extension")
        fr = args.in_file.split(".")[-1]
        to = args.out_file.split(".")[-1]

        conv = CONVERTERS.get(fr + "2" + to)
        if conv is not None:
            print(f"Determined converter is {fr + '2' + to}")
            print(f"Converting from {args.in_file} to {args.out_file}")

            conv(args.in_file, args.out_file)

            print("Converted successfully")
        else:
            print(f"Can't determine converter type from files \
                {args.in_file} {args.out_file}")
