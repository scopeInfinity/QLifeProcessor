import argparse
import logging

from emulator.module.rom import ROM

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def args_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("rom", help="ROM file as text binary")
    parser.add_argument("--print_rom", action="store_true")
    return parser

def main():
    args = args_parser().parse_args()
    with open(args.rom, "r") as rom_f:
        rom = ROM(rom_f.read())
        if args.print_rom:
            rom.print()

if __name__ == '__main__':
    main()
