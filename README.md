# CodePulse - Live Activity Dashboard

CodePulse is a lightweight, offline-first C++ desktop app that monitors active coding time in any editor (VS Code, PyCharm, etc.), logs language usage, project folders, and focus streaks, and generates a real-time web dashboard — all without internet. Now featuring a **live Flask API** with auto-updating charts!

## ✨ Features

- ✅ **Real-time window tracking** - Detects active window and file extensions
- ✅ **Local SQLite database** - No cloud required, 100% offline
- ✅ **Flask REST API** - Four endpoints for real-time data
- ✅ **Live web dashboard** - Auto-updating Chart.js visualizations
- ✅ **Language breakdown** - Track coding time by language
- ✅ **Project analytics** - See which folders get the most attention
- ✅ **Focus streaks** - Build and maintain coding momentum
- ✅ **CORS enabled** - Easy frontend integration
- ✅ **PDF Export** - Generate professional reports with charts and statistics
- ✅ **Mobile responsive** - Works perfectly on phones and tablets
- ✅ **Render.com ready** - Deploy to cloud in minutes

## 📋 Requirements

- **C++ 17+** for the activity monitor
- **SQLite 3** (included)
- **Python 3.7+** for dashboard API
- **Flask & Flask-CORS** (auto-installed)

## 🚀 Quick Start

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

Or manually:
```bash
pip install flask flask-cors requests matplotlib
```

### 2. Initialize Sample Data (Optional)

To test with sample data (skip if you already have activity from the C++ monitor):

```bash
python backend/init_sample_data.py
```

### 3. Start the API Server

```bash
python backend/api_server.py
```

You'll see:
```
Starting CodePulse Flask API Server...
Dashboard: http://localhost:5000
API Stats: http://localhost:5000/api/stats
API Projects: http://localhost:5000/api/projects
API Languages: http://localhost:5000/api/languages

 * Running on http://localhost:5000
```

### 4. Open Your Browser

Visit **`http://localhost:5000`** to view your live dashboard!

The dashboard auto-updates every 30 seconds with:
- 📊 **Last 7 Days Activity** (line chart)
- 💬 **Today's Language Breakdown** (doughnut chart)
- 📁 **Top Projects** (ranked list)
- 📈 **Summary Statistics**

## 🔌 REST API Endpoints

All endpoints return JSON and support CORS.

### `GET /api/stats`

Last 7 days of activity data.

**Response:**
```json
{
  "success": true,
  "labels": ["2025-12-21", "2025-12-22", ...],
  "data": [49.07, 40.9, ...],
  "summary": {
    "total_minutes": 312.88,
    "total_sessions": 115,
    "languages": ["CSS", "Python", "C++"],
    "top_language": "Python"
  }
}
```

### `GET /api/languages`

Today's language distribution.

**Response:**
```json
{
  "success": true,
  "labels": ["Python", "JavaScript", "CSS"],
  "data": [120.5, 45.2, 30.1]
}
```

### `GET /api/projects`

Top 10 project folders by activity.

**Response:**
```json
{
  "success": true,
  "projects": [
    {
      "folder": "src/components",
      "duration_minutes": 125.5,
      "language": "Python",
      "session_count": 12
    }
  ]
}
```

### `GET /api/health`

Health check - verify API is running.

**Response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "records": 456
}
```

### `GET /api/report/pdf`

Download professional PDF report with charts and statistics.

**Usage:**
```bash
curl -o activity_report.pdf http://localhost:5000/api/report/pdf
```

**Response:**
- Binary PDF file
- Contains: 7-day chart, language breakdown, projects, stats
- Filename: `codepulse_report_<year>.pdf`

## 🖥️ Running the C++ Activity Monitor

Compile and run the desktop monitor to start tracking:

### Option 1: Using Makefile
```bash
cd src
make && ../build/activity_monitor
```

### Option 2: Manual Compilation
```bash
cd src
g++ -std=c++17 -Wall -Wextra -O2 main.cpp sqlite3.c -o ../build/activity_monitor
../build/activity_monitor
```

The monitor will automatically log your activity to `data/activity.db`.

## 📁 Project Structure

```
codepulse/
├── src/                    # C++ activity monitor
│   ├── main.cpp           # Main application
│   ├── sqlite3.c          # SQLite source
│   ├── sqlite3.h          # SQLite header
│   └── Makefile           # Build configuration
│
├── backend/               # Python Flask API & utilities
│   ├── api_server.py      # REST API server
│   ├── generate_dashboard.py  # Dashboard generation
│   ├── pdf_generator.py   # PDF export
│   ├── init_sample_data.py    # Test data
│   └── quickstart.py      # Quick utilities
│
├── frontend/              # Web dashboard
│   └── dashboard.html     # Single-page app
│
├── data/                  # Generated data and reports
│   ├── activity.db        # SQLite database
│   ├── daily_chart.png    # Generated chart
│   └── codepulse_report_*.pdf  # Exported reports
│
├── docs/                  # Documentation
│   ├── ARCHITECTURE.md    # System design
│   └── INSTALLATION.md    # Detailed setup
│
├── .github/               # Issue/PR templates
├── Dockerfile             # Container build
├── docker-compose.yml     # Local dev compose
├── requirements.txt       # Python dependencies
├── Procfile               # Render deployment
├── render.yaml            # Render config
├── LICENSE                # MIT license
├── CONTRIBUTING.md        # Contribution guidelines
└── README.md              # Project overview (this file)
```

## 🎨 Dashboard Features

### Live Auto-Updating

- Charts refresh every 30 seconds automatically
- Connection indicator: **Green** = connected, **Red** = offline
- Automatic reconnection on network failure
- Smooth animations and transitions

### Responsive Design

- Works on desktop, tablet, and mobile
- Adapts to different screen sizes
- Touch-friendly on mobile devices

### Three Visualization Types

1. **Activity Timeline (Line Chart)**
   - 7-day focus time trends
   - Interactive data points
   - Duration labels

2. **Language Distribution (Doughnut Chart)**
   - Today's breakdown by programming language
   - Color-coded for easy identification

3. **Project Summary (List)**
   - Top folders ranked by activity
   - Language tags and duration
   - Session count

## 🧪 Testing the API

### Using Python
```python
import requests
response = requests.get('http://localhost:5000/api/stats')
data = response.json()
print(data['summary']['total_minutes'])
```

### Using curl
```bash
curl http://localhost:5000/api/stats
curl http://localhost:5000/api/languages
curl http://localhost:5000/api/projects
curl http://localhost:5000/api/health
```

### From Browser
Simply visit any endpoint URL:
- `http://localhost:5000/api/stats`
- `http://localhost:5000/api/languages`
- `http://localhost:5000/api/projects`

## 🚨 Troubleshooting

### Port 5000 Already in Use

```bash
# Use a different port
python -c "from api_server import app; app.run(port=8000)"
```

Then access at `http://localhost:8000`

### No Data Showing

1. Verify `activity.db` exists in the project directory
2. Initialize sample data: `python init_sample_data.py`
3. Or run the C++ monitor to generate real data
4. Check health endpoint: `http://localhost:5000/api/health`

### Flask Not Installed

```bash
pip install flask flask-cors
```

### CORS Errors

CORS is enabled by default in `api_server.py`. If you still see errors:
- Clear browser cache (Ctrl+Shift+Delete)
- Check browser console (F12) for detailed errors
- Verify API endpoints return data directly

### Charts Not Loading

- Open browser console (F12) and check for JavaScript errors
- Verify Chart.js CDN is accessible
- Check that API endpoints return valid JSON
- Ensure JavaScript is enabled

## 📊 Legacy Dashboard

The original static dashboard is still available:

```bash
python generate_dashboard.py
```

This creates:
- `daily_chart.png` - Matplotlib visualization
- `dashboard.html` - Static HTML with embedded charts

View with:
```bash
start dashboard.html  # Windows
open dashboard.html   # macOS
xdg-open dashboard.html  # Linux
```

## 📄 PDF Report Export

Generate professional PDF reports of your coding activity:

### Quick Export

```bash
python pdf_generator.py
```

Creates: `codepulse_report_YYYY.pdf`

### Via REST API

```bash
curl http://localhost:5000/api/report/pdf > report.pdf
```

### PDF Report Contents

- 📊 7-day activity chart
- 💬 Language distribution
- 📁 Top projects breakdown
- 📈 Summary statistics
- 📅 Daily metrics
- 🎯 Key insights

### Export Options

**To file:**
```bash
python pdf_generator.py
```

**To specific path:**
```python
from pdf_generator import generate_report
generate_report(output_path='my_reports/report_dec_28.pdf')
```

**With custom date range:**
```python
from datetime import datetime, timedelta
from pdf_generator import generate_report

start = datetime.now() - timedelta(days=30)
generate_report(start_date=start, days=30)
```

### API Endpoint

**GET `/api/report/pdf`**

Returns PDF file directly, downloads to your device.

```bash
curl -o activity_report.pdf http://localhost:5000/api/report/pdf
```

Response:
- Content-Type: `application/pdf`
- File: Professional PDF with charts and data

### Use Cases

- 📋 Weekly/monthly reports for portfolio
- 💼 Share progress with team/manager
- 📊 Analyze coding patterns
- 🎯 Track productivity goals
- 📑 Archive activity history

## 🌐 Deployment

### Local Network Access

Modify `api_server.py` to listen on all interfaces:

```python
# In api_server.py, bottom of file
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)  # Listen on all IPs
```

Then access from another machine: `http://<your-computer-ip>:5000`

### Render.com Cloud Deployment

Deploy to Render.com free tier in 5 minutes:

#### Step 1: Connect Repository
1. Go to https://render.com
2. Sign up with GitHub
3. Create "New Web Service"
4. Select `itsowanga/Codepulse` repository

#### Step 2: Configure Service

| Setting | Value |
|---------|-------|
| Name | codepulse-api |
| Environment | Python 3 |
| Region | US East (or closest) |
| Branch | main |
| Build Command | `pip install -r requirements.txt` |
| Start Command | Leave blank (uses Procfile) |
| Plan | Free |

#### Step 3: Deploy
- Click "Create Web Service"
- Wait 2-3 minutes for build
- Service goes live automatically

#### Step 4: Access Dashboard
Visit your assigned URL:
```
https://codepulse-ss.onrender.com
```

(Render assigns a unique URL)

#### Test on Phone
1. Open phone browser
2. Visit Render URL
3. See responsive dashboard
4. Charts update live

### Production Deployment

Use a production WSGI server:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 api_server:app
```

Or with Render.com Pro plan for persistent storage and custom domain.

## 💾 Database

The app uses SQLite with a simple schema:

```sql
CREATE TABLE sessions(
    timestamp TEXT,      -- Unix timestamp
    file TEXT,           -- File path worked on
    language TEXT,       -- Programming language
    duration_sec FLOAT   -- Session duration in seconds
)
```

All timestamps are Unix epoch (seconds since 1970-01-01).

## 🔧 Advanced: Custom Refresh Rate

To change the dashboard update interval (default: 30 seconds), edit `api_server.py`:

```javascript
// Find this line (around line 600)
setInterval(fetchAndUpdateDashboard, 30000);

// Change 30000 to desired milliseconds
// 10000 = 10 seconds, 60000 = 1 minute, etc.
```

## 📝 API Integration Example

Create your own dashboard by fetching the API:

```html
<div id="stats"></div>

<script>
fetch('http://localhost:5000/api/stats')
  .then(res => res.json())
  .then(data => {
    document.getElementById('stats').innerText = 
      `Total Focus: ${data.summary.total_minutes} minutes`;
  });
</script>
```

## 🎯 Common Use Cases

### Track Daily Coding Time
Monitor your productivity trends across the week.

### Identify Most-Used Languages
See which languages you spend the most time on.

### Analyze Project Focus
Find out which projects get the most attention.

### Export Data
Fetch API data and export to CSV or JSON for analysis.

## ⚙️ Configuration

### Python Version
Requires Python 3.7 or higher. Check with:
```bash
python --version
```

### Virtual Environment (Recommended)
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

### Flask Debug Mode
Edit `api_server.py` last line to disable debug in production:
```python
app.run(debug=False, host='localhost', port=5000)  # Production
```

## 📄 Files

- **api_server.py** - Flask REST API with integrated live dashboard
- **pdf_generator.py** - PDF report generator with charts
- **generate_dashboard.py** - Legacy static dashboard generator
- **init_sample_data.py** - Generates 8 days of sample activity
- **requirements.txt** - Python package dependencies
- **Procfile** - Render.com deployment configuration
- **render.yaml** - Render service configuration
- **main.cpp** - C++ activity monitor
- **Makefile** - Build configuration
- **sqlite3.c/h** - SQLite3 library

## 📜 License

Open source - modify and extend as needed!

## ❓ Support

Having issues? Try:

1. **Check if server is running** - See output from `python api_server.py`
2. **Verify database exists** - `ls activity.db`
3. **Check API health** - Visit `http://localhost:5000/api/health`
4. **Review browser console** - Press F12 and check for errors
5. **Reinstall dependencies** - `pip install -r requirements.txt --force-reinstall`

## 🎉 You're Ready!

Your CodePulse dashboard is ready to deploy. Simply:

```bash
python api_server.py
```

Then visit `http://localhost:5000` and watch your coding activity come to life! 📊✨
