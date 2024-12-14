import argparse
import logging


from planner.asm import program_parser
from planner.sim import bin_parser
from planner.sim import devices
from planner.sim.programs import ping_pong


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

    bin_parser = subparsers.add_parser("compile_and_execute")
    bin_parser.add_argument("program")
    return parser

def main():
    args = args_parser().parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    if args.source == "asm":
        asm = program_parser.AsmParser()
        with open(args.asm_file, "r") as f:
            asm.parse_lines(f.readlines())
        output = asm.get_str(resolved=args.resolved, rom_binary=args.rom_binary)
        print(output)
    if args.source == "bin":
        with open(args.bin_file, "r") as f:
            _bin = bin_parser.BinRunner(f.read())
            _bin.set_input_device(5, devices.Numpad("id(5), range(0-9)"))
            _bin.set_output_device(6, devices.IntegerOutput("Screen6", bits=16))
            while True:
                _bin.step()
    if args.source == "compile_and_execute":
        if args.program == "ping_pong":
            ping_pong.start()
        else:
            print(f"{args.program} not found")



if __name__ == '__main__':
    main()
