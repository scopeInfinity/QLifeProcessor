SRC_DIR=.
BUILD_DIR=build

.PHONY: clean test

clean:
	rm -r $(BUILD_DIR)

include emulator/Makefile.mk

pytest:
	pytest -s

test: pytest test_verilog_modules
