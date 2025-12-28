#!/usr/bin/env python3
"""
CodePulse Flask API Server
Provides REST API endpoints for real-time dashboard updates
"""

import sqlite3
import json
from datetime import datetime, timedelta
from collections import defaultdict, Counter
from flask import Flask, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

# Database connection
def get_db_connection():
    """Create a database connection"""
    db_path = os.path.join(os.path.dirname(__file__), 'activity.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

# ============================================================================
# API ENDPOINT 1: /api/stats - Last 7 days of statistics
# ============================================================================
@app.route('/api/stats', methods=['GET'])
def api_stats():
    """
    Returns stats for the last 7 days
    
    Returns:
    {
        "labels": ["2024-12-21", "2024-12-22", ...],
        "data": [45.5, 67.3, ...],  // minutes
        "summary": {
            "total_minutes": 412.5,
            "total_sessions": 28,
            "languages": ["python", "javascript", "cpp"],
            "top_language": "python"
        }
    }
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        labels = []
        data = []
        total_minutes = 0
        all_languages = []
        session_count = 0
        
        # Get last 7 days of data
        for i in range(7, -1, -1):
            date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            labels.append(date)
            
            # Query total duration for this date
            # Timestamps are Unix timestamps (seconds since epoch)
            query = """
            SELECT COUNT(*) as count, SUM(duration_sec) as total_duration
            FROM sessions 
            WHERE date(CAST(timestamp AS INTEGER), 'unixepoch') = ?
            """
            cursor.execute(query, (date,))
            row = cursor.fetchone()
            
            duration_minutes = 0
            count = 0
            if row:
                duration_minutes = (row['total_duration'] or 0) / 60.0
                count = row['count'] or 0
                total_minutes += duration_minutes
                session_count += count
            
            data.append(round(duration_minutes, 2))
            
            # Get languages used on this date
            query = """
            SELECT DISTINCT language FROM sessions
            WHERE date(CAST(timestamp AS INTEGER), 'unixepoch') = ? AND language IS NOT NULL
            """
            cursor.execute(query, (date,))
            for row in cursor.fetchall():
                all_languages.append(row['language'])
        
        # Get top language across all 7 days
        top_language = Counter(all_languages).most_common(1)[0][0] if all_languages else "N/A"
        unique_languages = list(set(all_languages))
        
        conn.close()
        
        return jsonify({
            "success": True,
            "labels": labels,
            "data": data,
            "summary": {
                "total_minutes": round(total_minutes, 2),
                "total_sessions": session_count,
                "languages": unique_languages,
                "top_language": top_language
            }
        })
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# ============================================================================
# API ENDPOINT 2: /api/projects - Top project folders
# ============================================================================
@app.route('/api/projects', methods=['GET'])
def api_projects():
    """
    Returns top project folders based on activity time
    
    Returns:
    {
        "success": true,
        "projects": [
            {"folder": "src/components", "duration_minutes": 125.5, "language": "python"},
            ...
        ]
    }
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Extract folder path from file path and get total duration per folder
        query = """
        SELECT 
            SUBSTR(file, 1, INSTR(file, '/') - 1) as folder,
            language,
            SUM(duration_sec) as total_duration,
            COUNT(*) as session_count
        FROM sessions
        WHERE file IS NOT NULL AND TRIM(file) != ''
        GROUP BY folder, language
        ORDER BY total_duration DESC
        LIMIT 10
        """
        
        cursor.execute(query)
        rows = cursor.fetchall()
        
        projects = []
        for row in rows:
            folder = row['folder'] if row['folder'] else "root"
            duration_minutes = round((row['total_duration'] or 0) / 60.0, 2)
            
            projects.append({
                "folder": folder,
                "duration_minutes": duration_minutes,
                "language": row['language'] or "Unknown",
                "session_count": row['session_count']
            })
        
        conn.close()
        
        return jsonify({
            "success": True,
            "projects": projects
        })
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# ============================================================================
# API ENDPOINT 3: /api/languages - Language distribution (today)
# ============================================================================
@app.route('/api/languages', methods=['GET'])
def api_languages():
    """
    Returns language distribution for today
    
    Returns:
    {
        "success": true,
        "labels": ["python", "javascript", "cpp"],
        "data": [120.5, 45.2, 30.1]  // minutes
    }
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        today = datetime.now().strftime('%Y-%m-%d')
        
        query = """
        SELECT language, SUM(duration_sec) as total_duration
        FROM sessions
        WHERE date(CAST(timestamp AS INTEGER), 'unixepoch') = ? AND language IS NOT NULL
        GROUP BY language
        ORDER BY total_duration DESC
        """
        
        cursor.execute(query, (today,))
        rows = cursor.fetchall()
        
        labels = []
        data = []
        
        for row in rows:
            labels.append(row['language'])
            data.append(round((row['total_duration'] or 0) / 60.0, 2))
        
        conn.close()
        
        return jsonify({
            "success": True,
            "labels": labels,
            "data": data
        })
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# ============================================================================
# Health check endpoint
# ============================================================================
@app.route('/api/health', methods=['GET'])
def health_check():
    """Simple health check endpoint"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM sessions")
        count = cursor.fetchone()[0]
        conn.close()
        
        return jsonify({
            "status": "healthy",
            "database": "connected",
            "records": count
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

# ============================================================================
# Serve dashboard frontend
# ============================================================================
@app.route('/', methods=['GET'])
def index():
    """Serve the main dashboard"""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>CodePulse - Live Dashboard</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js@3.9.1/dist/chart.min.js"></script>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 40px 20px;
            }
            
            .container {
                max-width: 1400px;
                margin: 0 auto;
            }
            
            header {
                text-align: center;
                color: white;
                margin-bottom: 40px;
            }
            
            header h1 {
                font-size: 2.5em;
                margin-bottom: 10px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }
            
            header p {
                font-size: 1.1em;
                opacity: 0.9;
                margin-bottom: 15px;
            }
            
            .status-indicator {
                display: inline-block;
                width: 12px;
                height: 12px;
                border-radius: 50%;
                background-color: #4CAF50;
                margin-right: 8px;
                animation: pulse 2s infinite;
            }
            
            .status-indicator.offline {
                background-color: #f44336;
                animation: none;
            }
            
            @keyframes pulse {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.5; }
            }
            
            .dashboard {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 30px;
                margin-bottom: 30px;
            }
            
            @media (max-width: 1024px) {
                .dashboard {
                    grid-template-columns: 1fr;
                }
            }
            
            .card {
                background: white;
                border-radius: 15px;
                padding: 30px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                transition: transform 0.3s ease, box-shadow 0.3s ease;
            }
            
            .card:hover {
                transform: translateY(-5px);
                box-shadow: 0 15px 50px rgba(0,0,0,0.3);
            }
            
            .card h2 {
                color: #333;
                margin-bottom: 20px;
                font-size: 1.5em;
                border-bottom: 3px solid #667eea;
                padding-bottom: 10px;
            }
            
            .chart-container {
                position: relative;
                height: 300px;
                margin-bottom: 20px;
            }
            
            .card.full-width {
                grid-column: 1 / -1;
            }
            
            .stats {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
            }
            
            .stat-box {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 25px;
                border-radius: 10px;
                text-align: center;
                transition: transform 0.3s ease;
            }
            
            .stat-box:hover {
                transform: scale(1.05);
            }
            
            .stat-box h3 {
                font-size: 0.9em;
                opacity: 0.9;
                margin-bottom: 10px;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
            
            .stat-box .value {
                font-size: 2.5em;
                font-weight: bold;
                margin-bottom: 5px;
            }
            
            .stat-box .unit {
                font-size: 0.8em;
                opacity: 0.8;
            }
            
            .projects-list {
                list-style: none;
            }
            
            .project-item {
                padding: 15px;
                background: #f9f9f9;
                border-left: 4px solid #667eea;
                margin-bottom: 10px;
                border-radius: 5px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            
            .project-item:hover {
                background: #f0f0f0;
            }
            
            .project-name {
                font-weight: 600;
                color: #333;
            }
            
            .project-stats {
                display: flex;
                gap: 15px;
                align-items: center;
            }
            
            .project-lang {
                background: #667eea;
                color: white;
                padding: 4px 10px;
                border-radius: 4px;
                font-size: 0.85em;
            }
            
            .project-time {
                color: #666;
                font-weight: 500;
            }
            
            footer {
                text-align: center;
                color: white;
                margin-top: 40px;
                opacity: 0.8;
                font-size: 0.9em;
            }
            
            .refresh-info {
                text-align: center;
                color: white;
                font-size: 0.9em;
                opacity: 0.8;
            }
            
            .loading {
                text-align: center;
                color: white;
                padding: 20px;
            }
            
            .spinner {
                border: 3px solid rgba(255,255,255,0.3);
                border-radius: 50%;
                border-top: 3px solid white;
                width: 30px;
                height: 30px;
                animation: spin 1s linear infinite;
                margin: 0 auto 10px;
            }
            
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <h1>💻 CodePulse Dashboard</h1>
                <p>
                    <span class="status-indicator" id="statusIndicator"></span>
                    <span id="statusText">Loading...</span>
                </p>
                <div class="refresh-info">
                    Auto-updating every 30 seconds
                </div>
            </header>
            
            <div class="dashboard">
                <div class="card">
                    <h2>📊 Last 7 Days Activity</h2>
                    <div class="chart-container">
                        <canvas id="statsChart"></canvas>
                    </div>
                </div>
                
                <div class="card">
                    <h2>💬 Language Distribution (Today)</h2>
                    <div class="chart-container">
                        <canvas id="languagesChart"></canvas>
                    </div>
                </div>
                
                <div class="card full-width">
                    <h2>📈 Summary Statistics</h2>
                    <div class="stats">
                        <div class="stat-box">
                            <h3>Total Focus Time</h3>
                            <div class="value" id="totalMinutes">-</div>
                            <div class="unit">minutes (7 days)</div>
                        </div>
                        <div class="stat-box">
                            <h3>Total Sessions</h3>
                            <div class="value" id="totalSessions">-</div>
                            <div class="unit">coding sessions</div>
                        </div>
                        <div class="stat-box">
                            <h3>Languages Used</h3>
                            <div class="value" id="languageCount">-</div>
                            <div class="unit">programming languages</div>
                        </div>
                        <div class="stat-box">
                            <h3>Top Language</h3>
                            <div class="value" id="topLanguage">-</div>
                            <div class="unit">most active</div>
                        </div>
                    </div>
                </div>
                
                <div class="card full-width">
                    <h2>📁 Top Projects</h2>
                    <ul class="projects-list" id="projectsList">
                        <li style="text-align: center; color: #999;">Loading projects...</li>
                    </ul>
                </div>
            </div>
            
            <footer>
                <p>🚀 CodePulse - Real-time Coding Activity Tracker | Last updated: <span id="lastUpdate">-</span></p>
            </footer>
        </div>
        
        <script>
            let statsChart = null;
            let languagesChart = null;
            
            async function fetchAndUpdateDashboard() {
                try {
                    // Update status
                    setStatus(true);
                    
                    // Fetch stats data
                    const statsResponse = await fetch('/api/stats');
                    const statsData = await statsResponse.json();
                    
                    if (!statsData.success) throw new Error('Failed to fetch stats');
                    
                    // Fetch languages data
                    const langResponse = await fetch('/api/languages');
                    const langData = await langResponse.json();
                    
                    if (!langData.success) throw new Error('Failed to fetch languages');
                    
                    // Fetch projects data
                    const projectsResponse = await fetch('/api/projects');
                    const projectsData = await projectsResponse.json();
                    
                    if (!projectsData.success) throw new Error('Failed to fetch projects');
                    
                    // Update charts
                    updateStatsChart(statsData.labels, statsData.data);
                    updateLanguagesChart(langData.labels, langData.data);
                    
                    // Update stats boxes
                    document.getElementById('totalMinutes').textContent = 
                        statsData.summary.total_minutes.toFixed(1);
                    document.getElementById('totalSessions').textContent = 
                        statsData.summary.total_sessions;
                    document.getElementById('languageCount').textContent = 
                        statsData.summary.languages.length;
                    document.getElementById('topLanguage').textContent = 
                        statsData.summary.top_language;
                    
                    // Update projects list
                    updateProjectsList(projectsData.projects);
                    
                    // Update last update time
                    const now = new Date();
                    document.getElementById('lastUpdate').textContent = 
                        now.toLocaleTimeString();
                    
                } catch (error) {
                    console.error('Error fetching dashboard data:', error);
                    setStatus(false);
                }
            }
            
            function setStatus(online) {
                const indicator = document.getElementById('statusIndicator');
                const text = document.getElementById('statusText');
                
                if (online) {
                    indicator.classList.remove('offline');
                    text.textContent = 'Connected - Data updated';
                } else {
                    indicator.classList.add('offline');
                    text.textContent = 'Disconnected - Retrying...';
                }
            }
            
            function updateStatsChart(labels, data) {
                const ctx = document.getElementById('statsChart').getContext('2d');
                
                if (statsChart) {
                    statsChart.data.labels = labels;
                    statsChart.data.datasets[0].data = data;
                    statsChart.update();
                } else {
                    statsChart = new Chart(ctx, {
                        type: 'line',
                        data: {
                            labels: labels,
                            datasets: [{
                                label: 'Focus Time (minutes)',
                                data: data,
                                borderColor: '#667eea',
                                backgroundColor: 'rgba(102, 126, 234, 0.1)',
                                borderWidth: 3,
                                fill: true,
                                pointRadius: 6,
                                pointBackgroundColor: '#667eea',
                                pointBorderColor: '#fff',
                                pointBorderWidth: 2,
                                tension: 0.4
                            }]
                        },
                        options: {
                            responsive: true,
                            maintainAspectRatio: false,
                            plugins: {
                                legend: { display: true }
                            },
                            scales: {
                                y: {
                                    beginAtZero: true,
                                    ticks: {
                                        callback: function(value) {
                                            return value.toFixed(0) + ' min';
                                        }
                                    }
                                }
                            }
                        }
                    });
                }
            }
            
            function updateLanguagesChart(labels, data) {
                const ctx = document.getElementById('languagesChart').getContext('2d');
                
                const colors = [
                    '#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', 
                    '#98D8C8', '#F7B731', '#5F27CD', '#00D2D3'
                ];
                
                if (languagesChart) {
                    languagesChart.data.labels = labels;
                    languagesChart.data.datasets[0].data = data;
                    languagesChart.update();
                } else {
                    languagesChart = new Chart(ctx, {
                        type: 'doughnut',
                        data: {
                            labels: labels,
                            datasets: [{
                                data: data,
                                backgroundColor: colors.slice(0, labels.length),
                                borderColor: '#fff',
                                borderWidth: 2
                            }]
                        },
                        options: {
                            responsive: true,
                            maintainAspectRatio: false,
                            plugins: {
                                legend: {
                                    position: 'bottom'
                                }
                            }
                        }
                    });
                }
            }
            
            function updateProjectsList(projects) {
                const list = document.getElementById('projectsList');
                
                if (projects.length === 0) {
                    list.innerHTML = '<li style="text-align: center; color: #999;">No projects found</li>';
                    return;
                }
                
                list.innerHTML = projects.map(project => `
                    <li class="project-item">
                        <div class="project-name">📁 ${project.folder}</div>
                        <div class="project-stats">
                            <span class="project-lang">${project.language}</span>
                            <span class="project-time">${project.duration_minutes.toFixed(1)} min</span>
                        </div>
                    </li>
                `).join('');
            }
            
            // Initial load
            fetchAndUpdateDashboard();
            
            // Auto-refresh every 30 seconds
            setInterval(fetchAndUpdateDashboard, 30000);
        </script>
    </body>
    </html>
    """

if __name__ == '__main__':
    # Check if activity.db exists
    if not os.path.exists('activity.db'):
        print("Warning: activity.db not found!")
        print("Please run init_sample_data.py first to create sample data")
    
    print("Starting CodePulse Flask API Server...")
    print("Dashboard: http://localhost:5000")
    print("API Stats: http://localhost:5000/api/stats")
    print("API Projects: http://localhost:5000/api/projects")
    print("API Languages: http://localhost:5000/api/languages")
    print("\nPress Ctrl+C to stop the server")
    
    # Determine environment
    is_production = os.environ.get('RENDER') == 'true'
    port = int(os.environ.get('PORT', 5000))
    debug = not is_production
    
    app.run(debug=debug, host='0.0.0.0', port=port)
