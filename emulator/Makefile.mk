BUILD_EMULATOR = $(BUILD_DIR)/emulator
SRC_EMULATOR = $(SRC_DIR)/emulator

$(BUILD_EMULATOR)/%_test: $(SRC_EMULATOR)/%_test.v
	mkdir -p $(dir $@)
	iverilog -o $@ $^

run_test_emulator: $(patsubst $(SRC_EMULATOR)/%_test.v, $(BUILD_EMULATOR)/%_test, $(shell find $(SRC_EMULATOR) -name '*_test.v'))
	$(foreach test_name, $^, echo "Executing $(test_name)" && ./$(test_name))
