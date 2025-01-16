BUILD_EMULATOR = $(BUILD_DIR)/emulator
SRC_EMULATOR = $(SRC_DIR)/emulator

.PHONY: verilog_modules test_verilog_modules

$(BUILD_EMULATOR)/%_test: $(SRC_EMULATOR)/%_test.v
	mkdir -p $(dir $@)
	iverilog -o $@ $^

verilog_modules: $(patsubst $(SRC_EMULATOR)/%_test.v, $(BUILD_EMULATOR)/%_test, $(shell find $(SRC_EMULATOR) -name '*_test.v'))
	mkdir -p $(BUILD_EMULATOR)/io

test_verilog_modules: $(patsubst $(SRC_EMULATOR)/%_test.v, $(BUILD_EMULATOR)/%_test, $(shell find $(SRC_EMULATOR) -name '*_test.v'))
	$(foreach test_name, $^, echo "Executing $(test_name)" && ./$(test_name))

$(BUILD_EMULATOR)/module/libipc.so: $(SRC_EMULATOR)/module/ipc.cpp
	mkdir -p $(dir $@)
	g++ -shared -Wl,-soname,libipc.so -o $@ -fPIC $^

$(BUILD_EMULATOR)/module/ipc.py: $(SRC_EMULATOR)/module/ipc.py $(BUILD_EMULATOR)/module/libipc.so
	mkdir -p $(dir $@)
	cp -f $< $@

$(BUILD_EMULATOR)/module/ipc.o: $(SRC_EMULATOR)/module/ipc.cpp
	mkdir -p $(dir $@)
	g++ -o $@ $^
