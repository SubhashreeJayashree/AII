# 🚀 Quick Start Guide

## Installation (3 Steps)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the System
```bash
python main.py
```

### Step 3: Open Dashboard
Open your browser and go to:
```
http://127.0.0.1:5000
```

That's it! The system will start monitoring automatically.

---

## What You'll See

1. **Real-Time Metrics** - CPU, RAM, Disk usage updating every 2 seconds
2. **ML Predictions** - Forecasted future usage
3. **Risk Assessment** - System risk levels and crash probability
4. **AI Explanations** - Human-friendly explanations of system state
5. **Process List** - Top resource-consuming applications
6. **Live Charts** - Visual performance trends

---

## Features Available

### Dashboard Buttons
- **Generate Performance Report** - Creates text report
- **Download PDF Report** - Exports PDF to `reports/` folder
- **Refresh Metrics** - Restarts data streaming

### Automatic Features
- ✅ Real-time monitoring (starts automatically)
- ✅ ML model training (trains when enough data collected)
- ✅ Anomaly detection (runs continuously)
- ✅ Risk assessment (updates in real-time)
- ✅ Data logging (saves to `data/metrics.csv`)

---

## Troubleshooting

### Port 5000 Already in Use?
Edit `backend/server.py` line 200+ and change:
```python
socketio.run(app, port=5001)  # Use different port
```

### Missing Packages?
```bash
pip install --upgrade -r requirements.txt
```

### No Data Showing?
Wait 10-20 seconds for initial data collection. The system needs a few cycles to start showing metrics.

---

## File Locations

- **Data**: `data/metrics.csv`
- **Models**: `models/` (auto-created)
- **Reports**: `reports/` (auto-created)
- **Dashboard**: `frontend/index.html`

---

## Next Steps

1. Let the system run for 5-10 minutes to collect data
2. ML models will train automatically
3. Generate reports to see historical analysis
4. Check PDF reports in `reports/` folder

---

**Enjoy your AI-Based System Performance Analyzer! 🎉**
