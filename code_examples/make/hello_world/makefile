# The compiler to use
CC=g++

# Compiler flags
CFLAGS=-c -Wall

# Name of executable output
EXECUTABLE=hello

all: clean $(EXECUTABLE)

$(EXECUTABLE): main.o robot.o
	$(CC) main.o robot.o -o $(EXECUTABLE)

main.o: main.cpp
	$(CC) $(CFLAGS) main.cpp

robot.o: lib/robot.cpp
	$(CC) $(CFLAGS) lib/robot.cpp

clean:
	rm -f *.o $(EXECUTABLE)