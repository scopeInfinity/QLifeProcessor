BUILD_EMULATOR = $(BUILD_DIR)/emulator
SRC_EMULATOR = $(SRC_DIR)/emulator

.PHONY: verilog_modules test_verilog_modules verilog_data_prerequisites verilog_simulate

$(BUILD_EMULATOR)/%_test: $(SRC_EMULATOR)/%_test.v $(SRC_EMULATOR)/%.v
	mkdir -p $(dir $@)
	iverilog -o $@ $<

verilog_modules: $(BUILD_EMULATOR)/executable_chipset $(patsubst $(SRC_EMULATOR)/%_test.v, $(BUILD_EMULATOR)/%_test, $(shell find $(SRC_EMULATOR) -name '*_test.v'))
	mkdir -p $(BUILD_EMULATOR)/io

verilog_data_prerequisites: output_rom_binaries

test_verilog_modules: $(patsubst $(SRC_EMULATOR)/%_test.v, $(BUILD_EMULATOR)/%_test, $(shell find $(SRC_EMULATOR) -name '*_test.v'))
	$(MAKE) verilog_data_prerequisites
	$(foreach test_name, $^, echo "Executing $(test_name)" && ./$(test_name))

$(BUILD_EMULATOR)/executable_chipset: $(SRC_EMULATOR)/executable_chipset.v
	$(MAKE) verilog_data_prerequisites
	mkdir -p $(dir $@)
	iverilog -o $@ $^

verilog_simulate: $(BUILD_EMULATOR)/executable_chipset
	./$^ | $(MAKE) run_verilog_io
