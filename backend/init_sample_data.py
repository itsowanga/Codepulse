#!/usr/bin/env python3
"""
Initialize sample data in activity.db for testing the dashboard
"""

import sqlite3
from datetime import datetime, timedelta
import random

def init_sample_data():
    """Create sample activity data for the last 7 days"""
    conn = sqlite3.connect('activity.db')
    cursor = conn.cursor()
    
    # Create table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions(
            timestamp TEXT,
            file TEXT,
            language TEXT,
            duration_sec FLOAT
        )
    """)
    
    # Clear existing data
    cursor.execute("DELETE FROM sessions")
    
    languages = ['C++', 'Python', 'JavaScript', 'SQL', 'CSS', 'Other']
    files = [
        'main.cpp',
        'utils.py',
        'app.js',
        'dashboard.html',
        'style.css',
        'database.sql',
        'config.json',
        'test.py',
        'module.cpp'
    ]
    
    # Generate sample data for the last 7 days
    base_time = datetime.now() - timedelta(days=7)
    
    for day_offset in range(8):
        current_date = base_time + timedelta(days=day_offset)
        
        # Generate 10-20 sessions per day
        sessions_per_day = random.randint(10, 20)
        
        for _ in range(sessions_per_day):
            # Random time during the day
            hour = random.randint(6, 23)
            minute = random.randint(0, 59)
            second = random.randint(0, 59)
            
            session_time = current_date.replace(hour=hour, minute=minute, second=second)
            timestamp = int(session_time.timestamp())
            
            file = random.choice(files)
            language = random.choice(languages)
            duration = random.randint(30, 300)  # 30 sec to 5 min per session
            
            cursor.execute(
                "INSERT INTO sessions (timestamp, file, language, duration_sec) VALUES (?, ?, ?, ?)",
                (timestamp, file, language, duration)
            )
    
    conn.commit()
    conn.close()
    print("Sample data initialized successfully!")

if __name__ == '__main__':
    init_sample_data()
