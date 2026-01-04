# CodePulse - Activity Monitor Configuration

This directory contains the official CodePulse project structure.

## 📂 Directory Organization

### `src/`
C++ source code for the activity monitor
- `main.cpp` - Main application entry point
- `sqlite3.c` / `sqlite3.h` - Embedded SQLite library
- `Makefile` - Build configuration

### `backend/`
Python Flask REST API and utilities
- `api_server.py` - Flask REST API server
- `generate_dashboard.py` - Dashboard HTML generator
- `pdf_generator.py` - PDF report generation
- `init_sample_data.py` - Test data initialization
- `quickstart.py` - Quick start utilities

### `frontend/`
Web-based dashboard
- `dashboard.html` - Single-page application with integrated CSS/JS

### `data/`
Generated files and database
- `activity.db` - SQLite database (auto-created)
- `*.pdf` - Generated PDF reports
- `*.png` - Generated charts

### `docs/`
Project documentation
- `ARCHITECTURE.md` - System design and architecture
- `INSTALLATION.md` - Detailed installation guide

### `.github/`
GitHub templates and workflows
- `ISSUE_TEMPLATE/` - Issue templates
- `pull_request_template.md` - PR template

## 🚀 Getting Started

1. **Quick Start**: See [SETUP.md](SETUP.md)
2. **Full Installation**: See [docs/INSTALLATION.md](docs/INSTALLATION.md)
3. **Architecture**: See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
4. **Contributing**: See [CONTRIBUTING.md](CONTRIBUTING.md)

## 📋 Project Files

- `README.md` - Project overview and features
- `requirements.txt` - Python dependencies
- `Dockerfile` - Docker image configuration
- `docker-compose.yml` - Local development with Docker
- `Procfile` - Render.com deployment
- `render.yaml` - Render configuration
- `.editorconfig` - Editor settings for consistency
- `.gitignore` - Git ignore patterns
- `LICENSE` - MIT License

---

**Welcome to CodePulse!** 🎉
