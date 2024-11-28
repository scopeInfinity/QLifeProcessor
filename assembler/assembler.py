import argparse

from assembler import asm_parser

def args_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("asm")
    parser.add_argument("-r", "--resolved", action="store_true")
    parser.add_argument("-b", "--rom-binary",
                        action="store_true",
                        help="prints instruction as binary in ROM (metadata+program) format."
                        )
    return parser

def main():
    args = args_parser().parse_args()
    asm = asm_parser.AsmParser()
    with open(args.asm, "r") as f:
        for line in f.readlines():
            asm.parse_line(line)
    output = asm.get_str(resolved=args.resolved, rom_binary=args.rom_binary)
    print(output)

if __name__ == '__main__':
    main()
