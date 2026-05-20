# 🔥 AI-Based System Performance Analyzer

## Advanced Real-Time Operating System Performance Monitoring & Analysis System

A comprehensive, industry-grade system performance analyzer that combines real-time monitoring, machine learning predictions, AI-powered explanations, and automated optimization recommendations.

---

## ✨ Features

### 🖥️ **Real-Time System Monitoring**
- Continuous CPU, RAM, and Disk usage monitoring
- Per-process resource tracking
- Real-time metrics streaming via WebSocket
- Historical data collection and storage

### 🤖 **Machine Learning Engine**
- **CPU/RAM Usage Prediction** - Forecasts future resource usage
- **Anomaly Detection** - Identifies abnormal system behavior using Isolation Forest
- **Time Series Analysis** - Pattern recognition and trend analysis
- **Multiple ML Models** - Linear Regression, Random Forest, Isolation Forest

### 🧠 **AI-Powered Explanation Engine**
- **Prompt Engineering** - Advanced prompt templates for different analysis tasks
- **Root Cause Analysis** - Identifies why system is slow
- **Human-Friendly Explanations** - Converts technical metrics to simple language
- **Diagnostic Prompts** - Structured prompts for system diagnosis

### ⚠️ **Risk Assessment & Prediction**
- Real-time risk score calculation (0-100)
- Crash probability estimation
- Time-to-failure prediction
- Risk level classification (MINIMAL/LOW/MEDIUM/HIGH/CRITICAL)

### ⚙️ **Auto-Optimization Engine**
- Automatic process termination (safe mode)
- Memory optimization suggestions
- Cache clearing recommendations
- System optimization automation

### 📊 **Advanced Reporting**
- Comprehensive performance reports
- PDF export functionality
- Historical analysis
- Peak usage detection
- AI-generated insights

### 🌐 **Real-Time Web Dashboard**
- Beautiful, modern UI with live charts
- Real-time metric updates
- Interactive visualizations
- Process monitoring panel
- Risk assessment display

---

## 🛠️ Technologies Used

### **Programming Languages**
- **Python** - Core backend, ML, AI engine
- **HTML/CSS/JavaScript** - Frontend dashboard
- **SQL** - Data storage (SQLite/CSV)

### **Frameworks & Libraries**
- **Flask** - Web framework
- **Flask-SocketIO** - Real-time WebSocket communication
- **Chart.js** - Data visualization
- **scikit-learn** - Machine learning
- **pandas** - Data analysis
- **psutil** - System monitoring
- **ReportLab** - PDF generation

### **AI & ML Technologies**
- Linear Regression (CPU prediction)
- Random Forest (Enhanced prediction)
- Isolation Forest (Anomaly detection)
- Prompt Engineering (AI explanations)

---

## 📁 Project Structure

```
ai_system_analyzer/
│
├── monitor/
│   └── collector.py          # System metrics collection
│
├── ml/
│   ├── predictor.py          # ML prediction engine
│   └── anomaly.py            # Anomaly detection
│
├── ai/
│   ├── explainer.py          # AI explanation engine
│   ├── optimizer.py          # Auto-optimization
│   ├── prompt_engine.py      # Prompt engineering
│   ├── risk_predictor.py     # Risk assessment
│   ├── report_generator.py   # Report generation
│   └── pdf_export.py         # PDF export
│
├── backend/
│   └── server.py             # Flask server + WebSocket
│
├── frontend/
│   └── index.html            # Dashboard UI
│
├── data/
│   └── metrics.csv           # Historical data
│
├── models/                    # Trained ML models
├── reports/                   # Generated reports
│
├── main.py                    # Entry point
├── requirements.txt          # Dependencies
└── README.md                  # This file
```

---

## 🚀 Installation & Setup

### **Step 1: Clone/Download Project**
```bash
# Navigate to project directory
cd "AI Based System Performance Analyzer"
```

### **Step 2: Install Python Dependencies**
```bash
pip install -r requirements.txt
```

### **Step 3: Run the System**
```bash
python main.py
```

### **Step 4: Access Dashboard**
Open your web browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 📖 Usage Guide

### **Starting the System**
1. Run `python main.py` from the project root
2. Wait for "Starting Backend Server..." message
3. Open browser to `http://127.0.0.1:5000`
4. Dashboard will automatically start streaming metrics

### **Dashboard Features**
- **Real-Time Metrics** - CPU, RAM, Disk usage with live updates
- **ML Predictions** - See predicted future usage
- **Risk Assessment** - Monitor system risk levels
- **AI Explanations** - Understand why system is slow
- **Process List** - View top resource-consuming processes
- **Charts** - Visualize performance trends

### **API Endpoints**
- `GET /api/metrics` - Get current metrics
- `GET /api/report` - Generate performance report
- `GET /api/report/pdf` - Download PDF report
- `POST /api/predict` - Get ML predictions
- `POST /api/risk` - Risk assessment
- `POST /api/optimize` - System optimization

### **Generating Reports**
1. Click "Generate Performance Report" button in dashboard
2. Or use API: `GET http://127.0.0.1:5000/api/report`
3. For PDF: Click "Download PDF Report" or use `/api/report/pdf`

---

## 🎯 Key Features Explained

### **1. Prompt Engineering**
The system uses advanced prompt engineering with multiple prompt types:
- **Diagnostic Prompts** - Root cause analysis
- **Prediction Prompts** - Risk assessment
- **Optimization Prompts** - Performance improvement suggestions
- **Report Prompts** - Comprehensive report generation
- **Explanation Prompts** - User-friendly explanations

### **2. Machine Learning**
- **Training**: Models train on historical data automatically
- **Prediction**: Forecasts CPU/RAM usage for next 5 minutes
- **Anomaly Detection**: ML-based detection of unusual patterns
- **Model Persistence**: Trained models saved for reuse

### **3. Real-Time Processing**
- WebSocket-based streaming (2-second intervals)
- Live dashboard updates
- No page refresh needed
- Efficient data transmission

### **4. Risk Prediction**
- Calculates risk score (0-100)
- Estimates crash probability
- Predicts time to failure
- Provides actionable recommendations

---

## 🎓 For Academic Projects

### **What Makes This Project Advanced?**

✅ **Multi-Language Implementation** - Python, HTML, CSS, JavaScript  
✅ **Real-Time Systems** - WebSocket streaming  
✅ **Machine Learning** - Multiple ML models  
✅ **AI Integration** - Prompt engineering, AI explanations  
✅ **Operating Systems** - Low-level system monitoring  
✅ **Web Technologies** - Full-stack web application  
✅ **Data Analytics** - Historical analysis, reporting  
✅ **Automation** - Auto-optimization engine  

### **Viva Questions & Answers**

**Q: What is prompt engineering in your project?**  
A: We use structured prompt templates to convert system metrics into natural language queries that generate human-friendly explanations. Different prompt types (diagnostic, prediction, optimization) are used for different analysis tasks.

**Q: How does ML prediction work?**  
A: We train Linear Regression and Random Forest models on historical CPU/RAM/Disk data. The models learn patterns and predict future usage based on current metrics.

**Q: What makes this real-time?**  
A: We use WebSocket connections to stream metrics every 2 seconds without page refresh. The backend continuously monitors the system and pushes updates to all connected clients.

**Q: How does anomaly detection work?**  
A: We use Isolation Forest algorithm to identify unusual patterns in system metrics. It learns normal behavior and flags deviations as anomalies.

---

## 🔧 Configuration

### **Safe Mode (Optimization)**
By default, auto-optimization runs in safe mode (no automatic process termination). To enable full optimization, modify `backend/server.py`:
```python
optimizer = SystemOptimizer(safe_mode=False)  # Enable full optimization
```

### **Monitoring Interval**
Adjust collection interval in `monitor/collector.py`:
```python
start_data_collection(interval=2)  # Change 2 to desired seconds
```

### **Model Training**
Models train automatically when sufficient data is available (minimum 10 records). To retrain:
```python
from ml.predictor import SystemPredictor
predictor = SystemPredictor()
predictor.train_model()
```

---

## 📊 Sample Output

### **Dashboard Display**
- Real-time CPU: 45.2%
- Real-time RAM: 62.8%
- Real-time Disk: 78.5%
- Predicted CPU (next 5 min): 48.5%
- Risk Level: LOW
- Crash Probability: 5%

### **AI Explanation Example**
"CPU usage is healthy at 45.2%. System is running efficiently. RAM usage is moderate at 62.8%. System has sufficient memory available. System is stable with no major risk."

### **Risk Assessment Example**
- Risk Score: 25/100
- Risk Level: LOW
- Crash Probability: 5%
- Time to Failure: Not imminent

---

## 🐛 Troubleshooting

### **Port Already in Use**
If port 5000 is busy, modify `backend/server.py`:
```python
socketio.run(app, port=5001)  # Change port
```

### **Permission Errors (Windows)**
Some processes may require admin privileges. Run as administrator if needed.

### **Missing Dependencies**
```bash
pip install --upgrade -r requirements.txt
```

### **Model Training Issues**
Ensure `data/metrics.csv` has at least 10 records. Let the system run for a few minutes to collect data.

---

## 📝 License

This project is created for educational and academic purposes.

---

## 👨‍💻 Development

### **Adding New Features**
1. Add new modules in respective directories
2. Import in `backend/server.py`
3. Add API endpoints if needed
4. Update frontend if UI changes required

### **Extending ML Models**
1. Add new model class in `ml/` directory
2. Train in `SystemPredictor` class
3. Integrate in prediction pipeline

### **Custom Prompts**
Add new prompt types in `ai/prompt_engine.py`:
```python
def custom_prompt(self, **kwargs):
    return f"Your custom prompt here..."
```

---

## 🎉 Conclusion

This is a complete, production-ready AI-based system performance analyzer with:
- ✅ Real-time monitoring
- ✅ Machine learning
- ✅ AI explanations
- ✅ Risk prediction
- ✅ Auto-optimization
- ✅ Advanced reporting
- ✅ Professional dashboard

**Perfect for final year projects, academic submissions, and portfolio demonstrations!**

---

## 📞 Support

For issues or questions, check:
1. Requirements installation
2. Port availability
3. System permissions
4. Data collection status

---

**Built with ❤️ for Advanced System Performance Analysis**
