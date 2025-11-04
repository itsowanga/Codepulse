CXX = g++
CC = gcc
CXXFLAGS = -std=c++11 -Wall -Wextra
CFLAGS = -Wall -Wextra
TARGET = sqlite_app

# Separate object files
OBJS = main.o sqlite3.o

$(TARGET): $(OBJS)
	$(CXX) -o $(TARGET) $(OBJS)

main.o: main.cpp
	$(CXX) $(CXXFLAGS) -c main.cpp -o main.o

sqlite3.o: sqlite3.c
	$(CC) $(CFLAGS) -c sqlite3.c -o sqlite3.o

run: $(TARGET)
	./$(TARGET)

clean:
	rm -f $(TARGET) *.o *.db

.PHONY: run clean