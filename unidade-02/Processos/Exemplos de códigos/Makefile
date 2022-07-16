CC=gcc

FLAGS=-O3 -Wno-unused-result
LDFLAGS=

all: fork1 fork2 fork3

fork1: fork1.c
	$(CC) $(FLAGS) fork1.c -o fork1 $(LDFLAGS)

fork2: fork2.c
	$(CC) $(FLAGS) fork2.c -o fork2 $(LDFLAGS)

fork3: fork3.c
	$(CC) $(FLAGS) fork3.c -o fork3 $(LDFLAGS)

clean:
	rm -rf fork1 fork2 fork3
