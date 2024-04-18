SRC_DIR=.
BUILD_DIR=build

.PHONY: clean

clean:
	rm -r $(BUILD_DIR)

include emulator/Makefile.mk
