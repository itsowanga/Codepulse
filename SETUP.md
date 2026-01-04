# Quick Setup Guide

Get CodePulse running in 5 minutes!

## ⚡ Fast Track

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Initialize sample data
python backend/init_sample_data.py

# 3. Start the API
python backend/api_server.py

# 4. Open dashboard
# Open frontend/dashboard.html in your browser
```

Navigate to `http://localhost:5000` and you're done! 🎉

## 📚 Full Setup

For detailed instructions, see [INSTALLATION.md](docs/INSTALLATION.md)

## 📁 Project Structure

```
codepulse/
├── src/              # C++ activity monitor
├── backend/          # Python Flask API
├── frontend/         # Web dashboard
├── data/             # Generated files & database
├── docs/             # Documentation
├── requirements.txt  # Python dependencies
└── README.md         # Project overview
```

## 🚀 What's Next?

- 📖 Read the [README](README.md) for features
- 🏗️  Check [ARCHITECTURE.md](docs/ARCHITECTURE.md) to understand the system
- 🤝 Want to contribute? See [CONTRIBUTING.md](CONTRIBUTING.md)

## 🆘 Troubleshooting

**API won't start?**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Port 5000 in use?**
Edit `backend/api_server.py` and change the port number.

**More issues?** Check [INSTALLATION.md](docs/INSTALLATION.md#troubleshooting-installation)

---

Happy coding! 💻
