# CodePulse Architecture

## Overview

CodePulse is a modular activity monitoring system with three main components:

```
┌─────────────────────────────────────────────────────────┐
│         CodePulse Activity Monitor System               │
└─────────────────────────────────────────────────────────┘
         │
         ├──────────────────┬──────────────────┬──────────────────┐
         │                  │                  │                  │
         ▼                  ▼                  ▼                  ▼
    ┌────────┐         ┌────────┐        ┌────────┐         ┌────────┐
    │   C++  │         │SQLite  │        │ Flask  │         │Frontend│
    │ Monitor│────────▶│  DB    │◀──────▶│  API   │────────▶│ HTML5  │
    │        │         │        │        │        │         │        │
    └────────┘         └────────┘        └────────┘         └────────┘
       src/              data/           backend/           frontend/
```

## Components

### 1. C++ Activity Monitor (`src/`)

**Purpose**: Real-time window tracking and file extension detection

**Key Files**:
- `main.cpp` - Main application entry point with Windows API integration
- `sqlite3.c`, `sqlite3.h` - SQLite embedded library
- `Makefile` - Build configuration

**Functionality**:
- Monitors active window title and process
- Detects file extensions from window title
- Logs activity with timestamps
- Writes directly to SQLite database
- Runs as a background service

**Technologies**:
- Windows API (GetActiveWindow, GetWindowText)
- C++17
- SQLite embedded database

---

### 2. SQLite Database (`data/`)

**Purpose**: Persistent local storage with no network dependency

**Key Tables**:
- `activity` - Records of active coding sessions
  - `id` - Primary key
  - `timestamp` - When activity was logged
  - `window_title` - Active window title
  - `language` - Detected programming language
  - `project_folder` - Associated project folder
  - `duration` - Session duration in seconds

**Files**:
- `activity.db` - Main database file (auto-created)

**Advantages**:
- 100% offline operation
- No cloud dependency
- Full privacy - data stays on your machine
- Fast local queries
- Easily shareable database file

---

### 3. Flask REST API (`backend/`)

**Purpose**: Serve activity data and generate reports

**Key Files**:
- `api_server.py` - Main Flask application
- `generate_dashboard.py` - Dashboard HTML generation
- `pdf_generator.py` - PDF report generation
- `init_sample_data.py` - Test data initialization

**API Endpoints**:
- `GET /api/activity` - All activity records (with pagination)
- `GET /api/summary` - Daily summary statistics
- `GET /api/languages` - Language breakdown
- `GET /api/projects` - Project analytics
- `GET /api/chart-data` - Data for frontend charts
- `POST /api/export-pdf` - Generate PDF report

**Features**:
- CORS enabled for frontend integration
- Error handling and validation
- Auto-updating data feeds
- PDF generation with charts

**Technologies**:
- Flask web framework
- Flask-CORS for cross-origin requests
- Matplotlib for chart generation
- ReportLab for PDF generation

---

### 4. Web Dashboard (`frontend/`)

**Purpose**: Beautiful real-time visualization of activity data

**Key Files**:
- `dashboard.html` - Single-page application with embedded CSS and JavaScript

**Features**:
- Real-time updating charts
- Language usage breakdown
- Project focus analytics
- Focus streaks and streaks
- Mobile responsive design
- PDF report generation
- Time range filtering

**Technologies**:
- HTML5
- CSS3 (responsive design)
- Chart.js for visualizations
- Vanilla JavaScript (no frameworks)
- Mobile-first design

**Chart Types**:
- Line chart - Coding time over time
- Pie chart - Language distribution
- Bar chart - Project activity
- Statistics cards - Key metrics

---

## Data Flow

### Recording Activity

```
C++ Monitor
    │
    ├─ Every 5 minutes (configurable):
    │  1. Get active window title
    │  2. Extract language from file extension
    │  3. Detect project folder
    │  4. Insert record into SQLite
    │
    └─► SQLite Database (activity.db)
```

### Serving Data

```
User opens dashboard.html
    │
    ├─ Browser loads HTML/CSS/JS
    ├─ JavaScript makes API requests
    │
    └─► Flask API Server
        │
        ├─ Query SQLite database
        ├─ Calculate summaries
        ├─ Generate chart data
        │
        └─► Return JSON response
            │
            ├─ Chart.js renders visualizations
            └─ Dashboard updates in real-time
```

### Report Generation

```
User clicks "Export PDF"
    │
    └─► Flask /api/export-pdf endpoint
        │
        ├─ Query activity data
        ├─ Generate charts with Matplotlib
        ├─ Create PDF with ReportLab
        │
        └─► Download codepulse_report_[date].pdf
```

---

## Directory Structure

```
codepulse/
├── src/                    # C++ activity monitor
│   ├── main.cpp           # Main application
│   ├── sqlite3.c          # SQLite source
│   ├── sqlite3.h          # SQLite header
│   └── Makefile           # Build configuration
│
├── backend/               # Python Flask API
│   ├── api_server.py      # Main REST API
│   ├── generate_dashboard.py  # Dashboard generation
│   ├── pdf_generator.py   # PDF export
│   ├── init_sample_data.py    # Test data
│   └── quickstart.py      # Quick start guide
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
│   └── ARCHITECTURE.md    # This file
│
├── README.md              # Project overview
├── LICENSE                # MIT license
├── CONTRIBUTING.md        # Contribution guidelines
├── requirements.txt       # Python dependencies
├── Procfile              # Render.com deployment
└── render.yaml           # Render configuration
```

---

## Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Monitor** | C++17 + Windows API | Real-time tracking |
| **Database** | SQLite 3 | Local data storage |
| **Backend** | Python 3.7+ + Flask | REST API |
| **Frontend** | HTML5 + CSS3 + JavaScript | Web dashboard |
| **Charts** | Chart.js | Visualizations |
| **Reports** | ReportLab + Matplotlib | PDF generation |
| **Deployment** | Render.com / Docker | Cloud hosting |

---

## Development Workflow

### Local Development

1. **Start the C++ Monitor** (background):
   ```bash
   cd src
   make && ./monitor
   ```

2. **Start the Flask API** (new terminal):
   ```bash
   cd backend
   python api_server.py
   ```

3. **Open the Dashboard**:
   - Navigate to `frontend/dashboard.html` in your browser
   - Or access at `http://localhost:5000` if serving from Flask

### Building and Deploying

- **Local Build**: `cd src && make`
- **Cloud Deploy**: Push to GitHub, Render auto-deploys via `Procfile`
- **Docker**: Build from `Dockerfile` (create if needed)

---

## Performance Considerations

- **C++ Monitor**: Minimal CPU usage (~1-2%), runs every 5 minutes
- **SQLite**: Fast local queries, no network latency
- **Flask API**: Efficient JSON serialization, caching support
- **Frontend**: Client-side rendering, minimal bandwidth
- **Charts**: Cached data, incremental updates

---

## Security & Privacy

✅ **100% Offline**: No internet required, data stays local
✅ **Private**: No telemetry or external API calls
✅ **Local Database**: Full control over your data
✅ **Shareable**: Export database or reports at your discretion
✅ **CORS Enabled**: Safe cross-origin requests on localhost

---

## Future Enhancements

- [ ] Multi-user support
- [ ] Cloud sync option (optional)
- [ ] Advanced analytics (focus patterns, productivity scores)
- [ ] Integration with calendar/meetings
- [ ] Browser extension for web activity tracking
- [ ] Real-time notifications for focus streaks
- [ ] Machine learning insights
- [ ] Cross-platform support (macOS, Linux)

---

## Troubleshooting

### Monitor Not Recording
- Check if C++ executable is running
- Verify database file exists in `data/activity.db`
- Review logs for permission issues

### API Returns Empty Data
- Run `python init_sample_data.py` to populate test data
- Check database file path in `api_server.py`

### Dashboard Not Updating
- Check browser console for errors
- Verify Flask server is running on port 5000
- Clear browser cache and refresh

---

**Last Updated**: January 2025
**Maintainer**: Owanga
