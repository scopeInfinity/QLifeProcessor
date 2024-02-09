BUILD = build
OUTPUT = output
SIMULATOR_FLAG := -DOPC_SIM_ENABLED
OPC_CFLAGS = -nostdlib -nodefaultlibs -no-pie -m32 -ffixed-r8 -ffixed-r9  -ffixed-r10 -ffixed-r11 -ffixed-r12 -ffixed-r13 -ffixed-r14 -ffixed-r15

.PHONY: clean prep all artifacts

all: prep $(BUILD)/greeting artifacts

clean:
	rm -f $(BUILD)/*

prep:
	mkdir -p $(BUILD)/
	mkdir -p $(OUTPUT)/

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
	ld -T linker.ld -m elf_i386 -o $@ $(BUILD)/ourpc_asm_o $(BUILD)/greeting_o $(BUILD)/font_o $(BUILD)/logging_o

# simulator agnostic rules
$(BUILD)/font_o: lib/font.c
	gcc -c -o $@ $(OPC_CFLAGS) $< -I include/

$(BUILD)/ourpc_asm_o: lib/ourpc.asm
	nasm -f elf32 -o $@ $^

$(BUILD)/greeting_o: greetings.c
	gcc -c -o $@ $(OPC_CFLAGS) $^ -I include/

# independent helper tools
$(BUILD)/text_to_led: text_to_led.c lib/font.c
	gcc -o $@ $^ -I include/

# generate artifacts

artifacts: $(OUTPUT)/sample_rom_text.txt $(OUTPUT)/objdump_ins_greetings.txt $(OUTPUT)/translated_ins.txt

$(OUTPUT)/sample_rom_text.txt: $(BUILD)/text_to_led
	$^ "Happy Diwali!" > $@

$(OUTPUT)/objdump_ins_greetings.txt: $(BUILD)/greeting
	objdump -D -M i386 -j .text $^ | cut -c2-4,29- > $@

# $(OUTPUT)/objdump_ins_greetings.txt: $(BUILD)/greeting
# 	objdump -d -M i386  -j .text $^ | grep bad && exit 1
# 	objdump -d -M i386  -j .text $^ | cut -c2-4,28- | sed -E 's/\s*(<|#).*//g' | grep -E '^[0-9a-f ]{2}[0-9a-f]\s' > $@

$(OUTPUT)/translated_ins.txt: fcompiler/translator.py $(OUTPUT)/objdump_ins_greetings.txt
	python3 $< $(OUTPUT)/objdump_ins_greetings.txt > $@
