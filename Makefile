SRC_DIR=.
BUILD_DIR=build
OUTPUT_DIR=output

.PHONY: clean test all

all: $(patsubst programs/%.asm, $(OUTPUT_DIR)/programs/%.bin, $(shell find programs/ -name '*.asm'))

clean:
	rm -r $(BUILD_DIR)
	rm -r (OUTPUT_DIR)

include emulator/Makefile.mk

pytest:
	pytest -s --log-cli-level=DEBUG

test: pytest test_verilog_modules

$(OUTPUT_DIR)/programs/%.bin: programs/%.asm
	mkdir -p $(dir $@)
	python3 -m planner asm -b $^ > $@

