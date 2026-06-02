# CodePulse - Live Activity Dashboard

CodePulse is an offline-first desktop application that tracks active coding time in editors (VS Code, PyCharm, and others), logs language usage, project folders, and focus streaks, and serves a local web dashboard. A Flask REST API provides live chart updates without requiring an internet connection for core monitoring.

## Features

- Real-time window tracking (active window and file extensions)
- Local SQLite database (no cloud dependency)
- Flask REST API with endpoints for statistics, projects, and languages
- Web dashboard with Chart.js visualizations (30-second refresh)
- Language and project analytics
- Focus streak tracking
- CORS enabled for local frontend integration
- PDF export for reports
- Responsive layout for mobile and desktop
- Optional deployment to Render.com

## Requirements

- C++17 or later (activity monitor)
- SQLite 3 (bundled in `src/`)
- Python 3.7 or later (API and dashboard)
- Flask and Flask-CORS (see `requirements.txt`)

## Quick Start

### 1. Install Python dependencies

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install flask flask-cors requests matplotlib
```

### 2. Initialize sample data (optional)

Use this step to test the dashboard without running the C++ monitor:

```bash
python backend/init_sample_data.py
```

### 3. Start the API server

```bash
python backend/api_server.py
```

Example output:

```
Starting CodePulse Flask API Server...
Dashboard: http://localhost:5000
API Stats: http://localhost:5000/api/stats
API Projects: http://localhost:5000/api/projects
API Languages: http://localhost:5000/api/languages

 * Running on http://localhost:5000
```

### 4. Open the dashboard

Open `http://localhost:5000` in a browser.

The dashboard refreshes every 30 seconds and shows:

- Last 7 days of activity (line chart)
- Today's language breakdown (doughnut chart)
- Top projects (ranked list)
- Summary statistics

## REST API Endpoints

All endpoints return JSON. CORS is enabled for local development.

### `GET /api/stats`

Activity for the last 7 days.

**Response:**

```json
{
  "success": true,
  "labels": ["2025-12-21", "2025-12-22", "..."],
  "data": [49.07, 40.9, "..."],
  "summary": {
    "total_minutes": 312.88,
    "total_sessions": 115,
    "languages": ["CSS", "Python", "C++"],
    "top_language": "Python"
  }
}
```

### `GET /api/languages`

Language distribution for today.

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

Health check for the API and database connection.

**Response:**

```json
{
  "status": "healthy",
  "database": "connected",
  "records": 456
}
```

### `GET /api/report/pdf`

Download a PDF report with charts and statistics.

**Usage:**

```bash
curl -o activity_report.pdf http://localhost:5000/api/report/pdf
```

**Response:** Binary PDF (`codepulse_report_<year>.pdf`) with 7-day activity, languages, projects, and summary stats.

## C++ Activity Monitor

Build and run the monitor to record activity into `data/activity.db`.

### Option 1: Makefile

```bash
cd src
make && ../build/activity_monitor
```

### Option 2: Manual build

```bash
cd src
g++ -std=c++17 -Wall -Wextra -O2 main.cpp sqlite3.c -o ../build/activity_monitor
../build/activity_monitor
```

## Project Structure

```
codepulse/
├── src/                    # C++ activity monitor
│   ├── main.cpp
│   ├── sqlite3.c
│   ├── sqlite3.h
│   └── Makefile
├── backend/                # Flask API and utilities
│   ├── api_server.py
│   ├── generate_dashboard.py
│   ├── pdf_generator.py
│   ├── init_sample_data.py
│   └── quickstart.py
├── frontend/
│   └── dashboard.html
├── data/
│   ├── activity.db
│   ├── daily_chart.png
│   └── codepulse_report_*.pdf
├── docs/
│   ├── ARCHITECTURE.md
│   └── INSTALLATION.md
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── Procfile
├── render.yaml
├── LICENSE
├── CONTRIBUTING.md
└── README.md
```

## Dashboard Behavior

- Charts refresh every 30 seconds
- Connection indicator: green when the API is reachable, red when offline
- Automatic retry on network errors
- Layout adapts to desktop, tablet, and mobile viewports

**Visualizations:**

1. **Activity timeline** — 7-day focus time (line chart)
2. **Language distribution** — today's breakdown (doughnut chart)
3. **Project summary** — top folders with duration and session counts

## Testing the API

### Python

```python
import requests
response = requests.get('http://localhost:5000/api/stats')
data = response.json()
print(data['summary']['total_minutes'])
```

### curl

```bash
curl http://localhost:5000/api/stats
curl http://localhost:5000/api/languages
curl http://localhost:5000/api/projects
curl http://localhost:5000/api/health
```

### Browser

Open any endpoint URL directly, for example `http://localhost:5000/api/stats`.

## Troubleshooting

### Port 5000 in use

```bash
python -c "from api_server import app; app.run(port=8000)"
```

Then use `http://localhost:8000`.

### No data on the dashboard

1. Confirm `data/activity.db` exists
2. Run `python backend/init_sample_data.py`, or run the C++ monitor
3. Check `http://localhost:5000/api/health`

### Flask not installed

```bash
pip install flask flask-cors
```

### CORS errors

CORS is enabled in `api_server.py`. If errors persist, clear the browser cache, inspect the browser console (F12), and verify endpoints return JSON when opened directly.

### Charts not loading

Check the browser console (F12), confirm Chart.js loads from the CDN, and verify API responses are valid JSON.

## Legacy Static Dashboard

```bash
python backend/generate_dashboard.py
```

This generates `data/daily_chart.png` and `frontend/dashboard.html`. Open the HTML file locally:

```bash
start frontend/dashboard.html   # Windows
open frontend/dashboard.html    # macOS
xdg-open frontend/dashboard.html  # Linux
```

## PDF Reports

### Command line

```bash
python backend/pdf_generator.py
```

Creates `codepulse_report_YYYY.pdf` in the data directory.

### REST API

```bash
curl http://localhost:5000/api/report/pdf -o report.pdf
```

### Report contents

- 7-day activity chart
- Language distribution
- Top projects
- Summary statistics and daily metrics

### Custom export

```python
from pdf_generator import generate_report
generate_report(output_path='my_reports/report_dec_28.pdf')
```

```python
from datetime import datetime, timedelta
from pdf_generator import generate_report

start = datetime.now() - timedelta(days=30)
generate_report(start_date=start, days=30)
```

## Deployment

### Local network

In `api_server.py`, bind to all interfaces for LAN access:

```python
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

Access from another machine: `http://<host-ip>:5000`.

### Render.com

1. Create a Web Service at https://render.com and connect the repository.
2. Use Python 3, branch `main`, build command `pip install -r requirements.txt`, and the Procfile start command.
3. Deploy and open the assigned URL (for example `https://codepulse-ss.onrender.com`).

### Production WSGI

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 api_server:app
```

## Database

SQLite schema:

```sql
CREATE TABLE sessions(
    timestamp TEXT,
    file TEXT,
    language TEXT,
    duration_sec FLOAT
);
```

Timestamps are stored as Unix epoch seconds.

## Custom refresh interval

The embedded dashboard calls `setInterval(fetchAndUpdateDashboard, 30000)` (30 seconds). Change the interval in milliseconds in `api_server.py` as needed (for example `60000` for one minute).

## API integration example

```html
<div id="stats"></div>
<script>
fetch('http://localhost:5000/api/stats')
  .then(res => res.json())
  .then(data => {
    document.getElementById('stats').innerText =
      `Total focus: ${data.summary.total_minutes} minutes`;
  });
</script>
```

## Configuration

**Python version:** 3.7 or higher (`python --version`).

**Virtual environment (recommended):**

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
source .venv/bin/activate       # macOS / Linux
pip install -r requirements.txt
```

**Production:** set `debug=False` in `api_server.py` when not developing locally.

## Key files

| File | Purpose |
|------|---------|
| `backend/api_server.py` | Flask API and live dashboard |
| `backend/pdf_generator.py` | PDF report generation |
| `backend/generate_dashboard.py` | Static dashboard generator |
| `backend/init_sample_data.py` | Sample activity data |
| `requirements.txt` | Python dependencies |
| `Procfile` / `render.yaml` | Render deployment |
| `src/main.cpp` | C++ activity monitor |

## License

Open source; see `LICENSE` for terms.

## Support

1. Confirm the server is running (`python backend/api_server.py`)
2. Verify `data/activity.db` exists
3. Call `http://localhost:5000/api/health`
4. Review the browser console (F12) for errors
5. Reinstall dependencies if needed: `pip install -r requirements.txt --force-reinstall`

## Running locally

```bash
python backend/api_server.py
```

Open `http://localhost:5000` to view the dashboard.
