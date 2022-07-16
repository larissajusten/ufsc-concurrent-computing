CC=gcc

FLAGS=-O3 -Wno-unused-result
LDFLAGS=-lpthread

all: thread1 thread2

thread1: thread1.c
	$(CC) $(FLAGS) thread1.c -o thread1 $(LDFLAGS)

thread2: thread2.c
	$(CC) $(FLAGS) thread2.c -o thread2 $(LDFLAGS)

clean:
	rm -rf thread1 thread2
