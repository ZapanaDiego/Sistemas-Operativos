CC ?= gcc
CFLAGS ?= -std=c11 -O2 -Wall -Wextra -Werror -D_GNU_SOURCE -Iinclude
LDFLAGS ?=

LIB_SRC = src/rtos.c src/sem.c src/pipe.c src/flight_sw.c src/trace.c src/scenario.c
LIB_OBJ = $(LIB_SRC:.c=.o)
BIN = entornoRTOS
TEST = test_signatures

all: $(BIN)

$(BIN): $(LIB_OBJ) src/main.o
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)

$(TEST): $(LIB_OBJ) tests/test_signatures.o
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)

%.o: %.c
	$(CC) $(CFLAGS) -c -o $@ $<

test: $(TEST)
	./$(TEST)

run-pip-off: $(BIN)
	mkdir -p out
	./$(BIN) --scenario s1 --out out/s1_pip_off.txt

run-pip-on: $(BIN)
	mkdir -p out
	./$(BIN) --scenario s2 --out out/s2_pip_on.txt

all-scenarios: $(BIN)
	mkdir -p out
	./$(BIN) --scenario s0 --out out/s0_pip_off.txt
	./$(BIN) --scenario s1 --out out/s1_pip_off.txt
	./$(BIN) --scenario s2 --out out/s2_pip_on.txt
	./$(BIN) --scenario s3 --out out/s3_control.txt

clean:
	rm -f $(LIB_OBJ) src/main.o tests/test_signatures.o $(BIN) $(TEST)
