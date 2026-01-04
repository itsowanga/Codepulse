CXX = g++
CC = gcc
CXXFLAGS = -std=c++17 -Wall -Wextra -O2
CFLAGS = -Wall -Wextra -O2
TARGET = ../build/activity_monitor
BUILD_DIR = ../build

# Separate object files
OBJS = main.o sqlite3.o

$(TARGET): $(BUILD_DIR) $(OBJS)
	$(CXX) -o $(TARGET) $(OBJS)

main.o: main.cpp
	$(CXX) $(CXXFLAGS) -c main.cpp -o main.o

sqlite3.o: sqlite3.c
	$(CC) $(CFLAGS) -c sqlite3.c -o sqlite3.o

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

run: $(TARGET)
	$(TARGET)

clean:
	rm -f $(TARGET) *.o
	rm -rf $(BUILD_DIR)

.PHONY: run clean