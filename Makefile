BUILD = build
SIMULATOR_FLAG := -DOPC_SIM_ENABLED
OPC_CFLAGS = -nostdlib -nodefaultlibs

.PHONY: clean prep all

all: prep $(BUILD)/greeting $(BUILD)/sim_greeting $(BUILD)/sample_rom_text.txt

clean:
	rm -f $(BUILD)/*

prep:
	mkdir -p $(BUILD)/

# simulator specific rules
$(BUILD)/sim_o: lib/sim.c
	gcc -c -o $@ $< $(SIMULATOR_FLAG) -I include/

$(BUILD)/sim_asm_o: lib/sim.asm
	nasm -f elf64 -o $@ $^

$(BUILD)/sim_logging_o: lib/logging.c
	gcc -c -o $@ $< $(SIMULATOR_FLAG) -I include/

$(BUILD)/logging_o: lib/logging.c
	gcc -c -o $@ $< $(OPC_CFLAGS) -I include/

$(BUILD)/sim_greeting: $(BUILD)/sim_o $(BUILD)/sim_asm_o $(BUILD)/greeting_o $(BUILD)/font_o $(BUILD)/sim_logging_o
	gcc -o $@ $^

$(BUILD)/greeting: linker.ld $(BUILD)/ourpc_asm_o $(BUILD)/greeting_o $(BUILD)/font_o $(BUILD)/logging_o
	ld -T linker.ld -o $@ $(BUILD)/ourpc_asm_o $(BUILD)/greeting_o $(BUILD)/font_o $(BUILD)/logging_o

# simulator agnostic rules
$(BUILD)/font_o: lib/font.c
	gcc -c -o $@ $(OPC_CFLAGS) $< -I include/

$(BUILD)/ourpc_asm_o: lib/ourpc.asm
	nasm -f elf64 -o $@ $^

$(BUILD)/greeting_o: greetings.c
	gcc -c -o $@ $(OPC_CFLAGS) $^ -I include/

# independent helper tools
$(BUILD)/text_to_led: text_to_led.c $(BUILD)/font_o
	gcc -o $@ $^ -I include/

$(BUILD)/sample_rom_text.txt: $(BUILD)/text_to_led
	$^ "Happy Diwali!" > $@
