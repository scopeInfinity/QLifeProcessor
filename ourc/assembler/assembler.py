import argparse

import asm_parser
import unit
import util

def args_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("asm")
    parser.add_argument("-r", "--resolved", action="store_true")
    return parser

def main():
    args = args_parser().parse_args()
    asm = asm_parser.AsmParser.get_instance()
    with open(args.asm, "r") as f:
        for line in f.readlines():
            asm.parse_line(line)
    asm.append_boilerplate()

    asm.print(resolved=args.resolved)


if __name__ == '__main__':
    main()
