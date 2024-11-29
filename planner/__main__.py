import argparse
import logging


from planner.asm import program_parser
from planner.sim import bin_parser
from planner.sim import io


def args_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action="store_true")
    subparsers = parser.add_subparsers(dest="source")

    asm_parser = subparsers.add_parser("asm", help="Parse Assembly")
    asm_parser.add_argument("asm_file")
    asm_parser.add_argument("-r", "--resolved", action="store_true")
    asm_parser.add_argument("-b", "--rom-binary",
                        action="store_true",
                        help="prints instruction as binary in ROM (metadata+program) format."
                        )

    bin_parser = subparsers.add_parser("bin", help="Parse Binary")
    bin_parser.add_argument("bin_file")
    return parser

def main():
    args = args_parser().parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    if args.source == "asm":
        asm = program_parser.AsmParser()
        with open(args.asm_file, "r") as f:
            for line in f.readlines():
                asm.parse_line(line)
        output = asm.get_str(resolved=args.resolved, rom_binary=args.rom_binary)
        print(output)
    if args.source == "bin":
        with open(args.bin_file, "r") as f:
            _bin = bin_parser.BinRunner(f.read())
            _bin.set_input_device(5, io.Numpad("id(5), range(0-9)"))
            _bin.set_output_device(6, io.IntegerOutput("Screen6"))
            while True:
                _bin.step()


if __name__ == '__main__':
    main()
