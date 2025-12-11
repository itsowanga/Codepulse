# CodePulse

CodePulse is a lightweight, offline-first C++ desktop app that monitors active coding time in any editor (VS Code, PyCharm, etc.), logs language usage, project folders, and focus streaks, and generates a daily/weekly productivity dashboard with charts — all without internet. Syncs to web only when connected. 

## Requirements
1. C++ 17 or higher installed
2. SQLite version 3
3. Python 3.7+ (for dashboard generation)
4. matplotlib and chart.js (included in HTML dashboard)

## Running the Activity Monitor

1. Open the project directory

### Option 1 - Using the Makefile to run the code.
```cmd
    make run
```

### Option 2 - Using manual compilation commands.
```cmd
    gcc -Wall -Wextra -c sqlite3.c -o sqlite3.o
    g++ -std=c++11 -Wall -Wextra -c main.cpp -o main.o
    g++ -o sqlite_app main.o sqlite3.o
    ./sqlite_app
```

## Generating the Dashboard

CodePulse includes Python scripts to visualize your coding activity:

### Initialize Sample Data (First Time)
```bash
python init_sample_data.py
```
This creates sample activity data for the last 7 days (useful for testing the dashboard).

### Generate Dashboard
```bash
python generate_dashboard.py
```

This script will:
- Query `activity.db` for your coding sessions
- Generate `daily_chart.png` with:
  - **Bar Chart**: Code activity by language (C++, Python, JavaScript, etc.)
  - **Line Chart**: Focus time over the last 7 days
- Generate `dashboard.html` with interactive charts using Chart.js
- Display summary statistics (total focus time, languages used, top language, average daily focus)

### View Dashboard
Open `dashboard.html` in your browser to see your coding analytics:
```bash
start dashboard.html  # Windows
open dashboard.html   # macOS
xdg-open dashboard.html  # Linux
```

## Project Structure
```
.
├── main.cpp              # Activity monitor (C++)
├── sqlite3.c/h           # SQLite library
├── activity.db           # Activity database (auto-created)
├── generate_dashboard.py # Dashboard generation script
├── init_sample_data.py   # Sample data initializer
├── dashboard.html        # Interactive web dashboard
└── daily_chart.png       # Static visualization (generated)
```

## Features
- ✅ Real-time window tracking (language detection from file extension)
- ✅ Local SQLite database (no cloud required)
- ✅ Daily productivity stats via CLI (`./sqlite_app stats`)
- ✅ Beautiful interactive dashboard with charts
- ✅ Language-based activity breakdown
- ✅ Focus streak tracking
- ✅ Focus time trends over time




