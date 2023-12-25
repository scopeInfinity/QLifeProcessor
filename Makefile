clean:
	rm -f sim_greeting fake_entry.o

greeting:
	nasm -f elf64 fake_entry.asm
	gcc fake_entry.o greetings.c -I include

sim_greeting: fake_entry.asm greetings.c fake_sim.c lib/logging.c
	nasm -f elf64 fake_entry.asm
	gcc -o sim_greeting fake_entry.o greetings.c fake_sim.c lib/logging.c -I include/
