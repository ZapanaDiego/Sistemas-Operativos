CC ?= gcc
CFLAGS ?= -std=c11 -O2 -Wall -Wextra -Werror -D_GNU_SOURCE -Iinclude
ASFLAGS ?= -Iinclude
LDFLAGS ?=

LIB_SRC = src/rtos.c src/sem.c src/pipe.c src/bus1553.c src/flight_sw.c src/trace.c src/scenario.c
LIB_OBJ = $(LIB_SRC:.c=.o) src/switch.o
BIN = entornoRTOS
TEST = test_signatures
TEST_CONTEXT = test_context
TEST_BUS = test_bus

all: $(BIN)

$(BIN): $(LIB_OBJ) src/main.o
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)

$(TEST): $(LIB_OBJ) tests/test_signatures.o
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)

$(TEST_CONTEXT): $(LIB_OBJ) tests/test_context.o
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)

$(TEST_BUS): $(LIB_OBJ) tests/test_bus.o
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)

%.o: %.c
	$(CC) $(CFLAGS) -c -o $@ $<

src/switch.o: src/switch.S
	$(CC) $(ASFLAGS) -c -o $@ $<

test: $(TEST) $(TEST_CONTEXT) $(TEST_BUS) $(BIN) out/disasm.txt
	@if grep -R "ucontext" include src; then echo "ucontext encontrado"; exit 1; fi
	./$(TEST)
	./$(TEST_BUS)
	./$(TEST_CONTEXT)
	./tests/test_determinism.sh

out/disasm.txt: $(BIN)
	mkdir -p out
	objdump -d -Mintel $(BIN) > out/disasm.txt

run-pip-off: $(BIN) out/disasm.txt
	mkdir -p out
	./$(BIN) --scenario s1 --out out/s1_pip_off.txt

run-pip-on: $(BIN) out/disasm.txt
	mkdir -p out
	./$(BIN) --scenario s2 --out out/s2_pip_on.txt

all-scenarios: $(BIN) out/disasm.txt
	mkdir -p out
	./$(BIN) --scenario s0 --out out/s0_pip_off.txt
	./$(BIN) --scenario s1 --out out/s1_pip_off.txt
	./$(BIN) --scenario s2 --out out/s2_pip_on.txt
	./$(BIN) --scenario s3 --out out/s3_control.txt

view: all-scenarios
	mkdir -p out
	cp viewer/viewer.html out/viewer.html
	@echo "Abre out/viewer.html en el navegador."

clean:
	rm -f $(LIB_OBJ) src/main.o tests/test_signatures.o tests/test_context.o tests/test_bus.o \
		$(BIN) $(TEST) $(TEST_CONTEXT) $(TEST_BUS) out/disasm.txt out/viewer.html \
		out/s0_data.js out/s1_data.js out/s2_data.js out/s3_data.js
