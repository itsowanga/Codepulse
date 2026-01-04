# CodePulse Installation Guide

## Prerequisites

- **Operating System**: Windows 10+ (with Windows API support)
- **C++ Compiler**: MSVC, GCC, or Clang with C++17 support
- **Python**: 3.7 or higher
- **Build Tools**: Make (included with MinGW or download separately)

## Step 1: Clone the Repository

```bash
git clone https://github.com/itsowanga/codepulse.git
cd codepulse
```

## Step 2: Set Up Python Environment

### Option A: Using Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
.venv\Scripts\activate  # Windows
# or
source .venv/bin/activate  # macOS/Linux
```

### Option B: Using Conda

```bash
conda create -n codepulse python=3.9
conda activate codepulse
```

## Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- **flask** - Web framework for the API
- **flask-cors** - Cross-origin request handling
- **requests** - HTTP library for API calls
- **matplotlib** - Chart generation
- **reportlab** - PDF generation (if using pdf_generator.py)

## Step 4: Build the C++ Monitor

```bash
cd src
make clean
make
```

If you encounter build errors:
- **Windows**: Ensure you have MinGW or MSVC installed
- **Build Output**: Check build/activity_monitor.exe exists

### Compile Manually (if Make fails)

```bash
g++ -std=c++17 -O2 main.cpp sqlite3.c -o activity_monitor.exe -lWs2_32
```

## Step 5: Initialize Sample Data (Optional)

To test the dashboard with sample data:

```bash
cd backend
python init_sample_data.py
```

This populates the database with test activity records.

## Step 6: Start the API Server

```bash
cd backend
python api_server.py
```

You should see:
```
 * Running on http://localhost:5000
```

## Step 7: Open the Dashboard

1. Open `frontend/dashboard.html` in your web browser
   - Or navigate to `http://localhost:5000/dashboard.html`
2. You should see charts and activity data

## Step 8: Start the C++ Monitor (Production)

In a new terminal:

```bash
cd src
./build/activity_monitor.exe
```

Or on Windows:
```powershell
.\build\activity_monitor.exe
```

This will run in the background and continuously log your activity.

---

## Troubleshooting Installation

### Issue: "python not found"
**Solution**: 
- Install Python from [python.org](https://python.org)
- Add Python to PATH
- Use `python3` instead of `python` on some systems

### Issue: "pip install fails"
**Solution**:
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Issue: "make not found"
**Solution**:
- **Windows with MinGW**: MinGW includes make
- **Windows without MinGW**: Download from http://gnuwin32.sourceforge.net/packages/make.htm
- **Alternative**: Use manual compilation command above

### Issue: "C++ compilation errors"
**Solution**:
- Ensure C++17 is supported: `g++ --version`
- Update compiler: `choco install mingw` (if using Chocolatey)
- Check for conflicting versions

### Issue: "Port 5000 already in use"
**Solution**: Edit `backend/api_server.py` and change:
```python
app.run(host='0.0.0.0', port=5001)  # Change 5000 to 5001
```

### Issue: "Database not found"
**Solution**:
```bash
cd backend
python init_sample_data.py
```

---

## Uninstallation

### Windows

1. **Stop the C++ Monitor**: Close the running process
2. **Deactivate Python Environment**:
   ```bash
   deactivate
   ```
3. **Delete Project Folder**:
   ```powershell
   Remove-Item -Recurse -Force c:\path\to\codepulse
   ```

### macOS/Linux

```bash
deactivate  # Deactivate virtual environment
rm -rf ~/path/to/codepulse
```

---

## Next Steps

- Read [ARCHITECTURE.md](./ARCHITECTURE.md) to understand the project structure
- Check [README.md](../README.md) for features and usage
- See [CONTRIBUTING.md](../CONTRIBUTING.md) to contribute

---

## Getting Help

- **Issues**: Open a GitHub issue with details about your problem
- **Questions**: Start a discussion on GitHub
- **Documentation**: Check the docs/ folder for detailed guides

---

**Happy monitoring!** 🚀
