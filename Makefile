SRC_DIR=.
BUILD_DIR=build
OUTPUT_DIR=output

.PHONY: clean test all run_ping_pong

all: $(patsubst programs/%.asm, $(OUTPUT_DIR)/programs/%.bin, $(shell find programs/ -name '*.asm'))

clean:
	rm -r $(BUILD_DIR)
	rm -r (OUTPUT_DIR)

include emulator/Makefile.mk

pytest:
	pytest -s --log-cli-level=INFO

test: pytest test_verilog_modules

$(OUTPUT_DIR)/programs/%.bin: programs/%.asm
	mkdir -p $(dir $@)
	python3 -m planner asm -b $^ > $@


run_ping_pong:
	python3 -m planner -v compile_and_execute ping_pong
