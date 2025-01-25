SRC_DIR=.
BUILD_DIR=build
OUTPUT_DIR=output

.PHONY: clean test all run_verilog_io run_ping_pong all_programs_binary all_programs_resolved output_rom_binaries

all: all_programs_binary all_programs_resolved verilog_modules

clean:
	rm -rf $(BUILD_DIR)
	rm -rf $(OUTPUT_DIR)

include emulator/Makefile.mk

pytest:
	pytest -s --log-cli-level=INFO

test: pytest test_verilog_modules

all_programs_binary: $(patsubst programs/%.asm, $(OUTPUT_DIR)/programs/%.bin, $(shell find programs/ -name '*.asm'))

output_rom_binaries: $(OUTPUT_DIR)/programs/boot_sequence.bin $(OUTPUT_DIR)/programs/ping_pong.bin

$(OUTPUT_DIR)/programs/%.bin: programs/%.asm
	mkdir -p $(dir $@)
	python3 -m planner asm -b $^ > $@

all_programs_resolved: $(patsubst programs/%.asm, $(OUTPUT_DIR)/programs/%_resolved.asm, $(shell find programs/ -name '*.asm'))

$(OUTPUT_DIR)/programs/%_resolved.asm: programs/%.asm
	mkdir -p $(dir $@)
	python3 -m planner asm -r $^ > $@

run_ping_pong:
	python3 -m planner compile_and_execute ping_pong

run_verilog_io:
	python3 -m planner verilog_io
