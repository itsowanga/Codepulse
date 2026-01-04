#!/usr/bin/env python3
"""
CodePulse Dashboard Generator
Reads activity.db and generates visualizations
"""

import sqlite3
import json
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from collections import defaultdict
from flask import Flask, render_template_string, jsonify
import os
from config import get_db_path, DATA_DIR, FRONTEND_DIR

app = Flask(__name__)

# Connect to database
def get_db_connection():
    # Centralized database path
    conn = sqlite3.connect(get_db_path())
    conn.row_factory = sqlite3.Row
    return conn

# Get language distribution for a specific date
def get_language_distribution(conn, date):
    cursor = conn.cursor()
    query = """
    SELECT language, SUM(duration_sec) as total_duration 
    FROM sessions 
    WHERE date(CAST(timestamp AS INTEGER), 'unixepoch') = ? 
    GROUP BY language 
    ORDER BY total_duration DESC
    """
    cursor.execute(query, (date,))
    rows = cursor.fetchall()
    
    result = {}
    for row in rows:
        result[row['language'] if row['language'] else 'Other'] = row['total_duration']
    
    return result

# Get focus data over time (last 7 days)
@app.route('/stats', methods=['POST'])
def get_focus_over_time(conn, days=7):
    cursor = conn.cursor()
    dates = []
    focus_counts = []
    
    for i in range(days, -1, -1):
        date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
        query = """
        SELECT COUNT(*) as session_count, SUM(duration_sec) as total_duration
        FROM sessions 
        WHERE date(CAST(timestamp AS INTEGER), 'unixepoch') = ?
        """
        cursor.execute(query, (date,))
        row = cursor.fetchone()
        
        total_duration = row['total_duration'] if row['total_duration'] else 0
        # Convert to minutes for better readability
        dates.append(date)
        focus_counts.append(total_duration / 60.0)  # in minutes

    return jsonify(dates=dates, focus_counts=focus_counts)

# Generate bar chart for language distribution
def generate_language_chart(conn, date):
    lang_data = get_language_distribution(conn, date)
    
    if not lang_data:
        print(f"No data for {date}, using today's data")
        date = datetime.now().strftime('%Y-%m-%d')
        lang_data = get_language_distribution(conn, date)
    
    if not lang_data:
        print("No activity data found in database")
        return False
    
    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Subplot 1: Language Distribution (Bar Chart)
    languages = list(lang_data.keys())
    durations = list(lang_data.values())
    
    # Convert to minutes for readability
    durations_minutes = [d / 60.0 for d in durations]
    
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']
    bar_colors = colors[:len(languages)] + colors * (len(languages) // len(colors) + 1)
    
    ax1.bar(languages, durations_minutes, color=bar_colors[:len(languages)], edgecolor='black', linewidth=1.5)
    ax1.set_ylabel('Duration (minutes)', fontsize=12, fontweight='bold')
    ax1.set_xlabel('Language', fontsize=12, fontweight='bold')
    ax1.set_title(f'Code Activity by Language - {date}', fontsize=14, fontweight='bold')
    ax1.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Add value labels on bars
    for i, (lang, duration) in enumerate(zip(languages, durations_minutes)):
        ax1.text(i, duration + 1, f'{duration:.1f}m', ha='center', va='bottom', fontweight='bold')
    
    # Subplot 2: Focus Over Time (Line Chart - Last 7 days)
    dates, focus_counts = get_focus_over_time(conn, days=7)
    
    ax2.plot(dates, focus_counts, marker='o', linewidth=2.5, markersize=8, color='#45B7D1', label='Total Focus Time')
    ax2.fill_between(range(len(dates)), focus_counts, alpha=0.3, color='#45B7D1')
    ax2.set_ylabel('Focus Time (minutes)', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Date', fontsize=12, fontweight='bold')
    ax2.set_title('Focus Over Time (Last 7 Days)', fontsize=14, fontweight='bold')
    ax2.grid(alpha=0.3, linestyle='--')
    ax2.tick_params(axis='x', rotation=45)
    
    # Add value labels on points
    for i, (date, duration) in enumerate(zip(dates, focus_counts)):
        ax2.text(i, duration + 2, f'{duration:.0f}m', ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    # Save chart to data/ directory
    os.makedirs(str(DATA_DIR), exist_ok=True)
    plt.savefig(os.path.join(str(DATA_DIR), 'daily_chart.png'), dpi=150, bbox_inches='tight')
    print("Generated daily_chart.png")
    return True

# Generate HTML dashboard
def generate_html_dashboard(conn, date):
    lang_data = get_language_distribution(conn, date)
    dates, focus_counts = get_focus_over_time(conn, days=7)
    
    # Prepare data for charts
    languages_json = json.dumps(list(lang_data.keys()))
    durations_json = json.dumps([d / 60.0 for d in lang_data.values()])
    dates_json = json.dumps(dates)
    focus_json = json.dumps(focus_counts)
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CodePulse Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@3.9.1/dist/chart.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 40px 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        header {{
            text-align: center;
            color: white;
            margin-bottom: 40px;
        }}
        
        header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        
        header p {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        
        .dashboard {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin-bottom: 30px;
        }}
        
        @media (max-width: 768px) {{
            .dashboard {{
                grid-template-columns: 1fr;
            }}
        }}
        
        .card {{
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}
        
        .card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 15px 50px rgba(0,0,0,0.3);
        }}
        
        .card h2 {{
            color: #333;
            margin-bottom: 20px;
            font-size: 1.5em;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }}
        
        .chart-container {{
            position: relative;
            height: 350px;
            margin-bottom: 20px;
        }}
        
        .stats {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }}
        
        .stat-box {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }}
        
        .stat-box h3 {{
            font-size: 0.9em;
            opacity: 0.9;
            margin-bottom: 10px;
        }}
        
        .stat-box .value {{
            font-size: 2em;
            font-weight: bold;
        }}
        
        footer {{
            text-align: center;
            color: white;
            margin-top: 40px;
            opacity: 0.8;
            font-size: 0.9em;
        }}
        
        .full-width {{
            grid-column: 1 / -1;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>💻 CodePulse Dashboard</h1>
            <p>Your coding activity at a glance</p>
        </header>
        
        <div class="dashboard">
            <div class="card">
                <h2>📊 Language Distribution</h2>
                <div class="chart-container">
                    <canvas id="languageChart"></canvas>
                </div>
            </div>
            
            <div class="card">
                <h2>⏱️ Focus Over Time</h2>
                <div class="chart-container">
                    <canvas id="focusChart"></canvas>
                </div>
            </div>
            
            <div class="card full-width">
                <h2>📈 Summary Statistics</h2>
                <div class="stats">
                    <div class="stat-box">
                        <h3>Total Focus Time Today</h3>
                        <div class="value">{sum(lang_data.values()) / 60:.1f} min</div>
                    </div>
                    <div class="stat-box">
                        <h3>Languages Used</h3>
                        <div class="value">{len(lang_data)}</div>
                    </div>
                    <div class="stat-box">
                        <h3>Top Language</h3>
                        <div class="value">{max(lang_data, key=lang_data.get) if lang_data else 'N/A'}</div>
                    </div>
                    <div class="stat-box">
                        <h3>Average Daily Focus</h3>
                        <div class="value">{sum(focus_counts) / len(focus_counts):.0f} min</div>
                    </div>
                </div>
            </div>
        </div>
        
        <footer>
            <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | CodePulse Activity Tracker</p>
        </footer>
    </div>
    
    <script>
        // Language Distribution Chart
        const languageCtx = document.getElementById('languageChart').getContext('2d');
        new Chart(languageCtx, {{
            type: 'bar',
            data: {{
                labels: {languages_json},
                datasets: [{{
                    label: 'Duration (minutes)',
                    data: {durations_json},
                    backgroundColor: [
                        '#FF6B6B',
                        '#4ECDC4',
                        '#45B7D1',
                        '#FFA07A',
                        '#98D8C8',
                        '#F7B731',
                        '#5F27CD'
                    ],
                    borderColor: '#333',
                    borderWidth: 2,
                    borderRadius: 8
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{
                        display: false
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        ticks: {{
                            callback: function(value) {{
                                return value.toFixed(0) + ' min';
                            }},
                            font: {{
                                size: 11
                            }}
                        }}
                    }},
                    x: {{
                        ticks: {{
                            font: {{
                                size: 11
                            }}
                        }}
                    }}
                }}
            }}
        }});
        
        // Focus Over Time Chart
        const focusCtx = document.getElementById('focusChart').getContext('2d');
        new Chart(focusCtx, {{
            type: 'line',
            data: {{
                labels: {dates_json},
                datasets: [{{
                    label: 'Focus Time (minutes)',
                    data: {focus_json},
                    borderColor: '#45B7D1',
                    backgroundColor: 'rgba(69, 183, 209, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    pointRadius: 6,
                    pointBackgroundColor: '#45B7D1',
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                    tension: 0.4
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    legend: {{
                        display: true,
                        position: 'top'
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        ticks: {{
                            callback: function(value) {{
                                return value.toFixed(0) + ' min';
                            }},
                            font: {{
                                size: 11
                            }}
                        }}
                    }},
                    x: {{
                        ticks: {{
                            font: {{
                                size: 11
                            }}
                        }}
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>
"""
    
    # Write dashboard to frontend/ directory
    os.makedirs(str(FRONTEND_DIR), exist_ok=True)
    with open(os.path.join(str(FRONTEND_DIR), 'dashboard.html'), 'w', encoding='utf-8') as f:
        f.write(html_content)
    print("Generated dashboard.html")

def main():
    try:
        conn = get_db_connection()
        
        # Get today's date
        today = datetime.now().strftime('%Y-%m-%d')
        
        print("CodePulse Dashboard Generator")
        print(f"Date: {today}\n")
        
        # Generate charts
        if generate_language_chart(conn, today):
            generate_html_dashboard(conn, today)
            print("\nDashboard generated successfully!")
            print(f"Files created: daily_chart.png, dashboard.html")
        else:
            print("No activity data to visualize")
        
        conn.close()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
