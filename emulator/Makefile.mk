BUILD_EMULATOR = $(BUILD_DIR)/emulator
SRC_EMULATOR = $(SRC_DIR)/emulator

.PHONY: test_verilog_modules

$(BUILD_EMULATOR)/%_test: $(SRC_EMULATOR)/%_test.v
	mkdir -p $(dir $@)
	iverilog -o $@ $^

test_verilog_modules: $(patsubst $(SRC_EMULATOR)/%_test.v, $(BUILD_EMULATOR)/%_test, $(shell find $(SRC_EMULATOR) -name '*_test.v'))
	$(foreach test_name, $^, echo "Executing $(test_name)" && ./$(test_name))
