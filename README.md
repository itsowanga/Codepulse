# CodePulse

CodePulse is a lightweight, offline-first C++ desktop app that monitors active coding time in any editor (VS Code, PyCharm, etc.), logs language usage, project folders, and focus streaks, and generates a daily/weekly productivity dashboard with charts — all without internet. Syncs to web only when connected. 

## Requirements
1. C++ 17 or higher installed
2. SQLite version 3

## Running the code

1. Open the project directory

### Option 1 - Using the Makefile to run the code.
'''cmd
    make run
'''

### Option 2 - Using manual compilation commands.
'''cmd
    gcc -Wall -Wextra -c sqlite3.c -o sqlite3.o
    g++ -std=c++11 -Wall -Wextra -c main.cpp -o main.o
    g++ -o sqlite_app main.o sqlite3.o
    ./sqlite_app
'''




