"""
Advanced Real-Time Backend Server
Handles WebSocket connections, ML predictions, AI explanations, and API endpoints
"""
from flask import Flask, render_template, jsonify, send_from_directory, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import os
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from monitor.collector import collect_metrics, get_detailed_metrics
from ml.predictor import SystemPredictor
from ml.anomaly import AnomalyDetector
from ai.explainer import AIExplainer
from ai.optimizer import SystemOptimizer
from ai.risk_predictor import RiskPredictor
from ai.report_generator import ReportGenerator
from ai.pdf_export import PDFExporter
import time
import threading

# Initialize Flask app
app = Flask(__name__, 
            static_folder='../frontend',
            template_folder='../frontend')
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Initialize components
predictor = SystemPredictor()
anomaly_detector = AnomalyDetector()
explainer = AIExplainer()
optimizer = SystemOptimizer(safe_mode=True)  # Safe mode by default
risk_predictor = RiskPredictor()
report_generator = ReportGenerator()
pdf_exporter = PDFExporter()

# Global state
is_streaming = False
stream_thread = None
metrics_history = []

# Known antivirus process name patterns (lowercase substrings)
ANTIVIRUS_KEYWORDS = [
    "msmpeng",      # Windows Defender
    "avast",        # Avast
    "avg",          # AVG
    "kaspersky",
    "mcafee",
    "nod32",
    "eset",
    "bitdefender",
    "quickheal",
    "defender",
    "securityhealthservice"
]


def is_antivirus_process(name: str) -> bool:
    """Heuristic check if a process looks like antivirus/security software"""
    if not name:
        return False
    lname = name.lower()
    return any(keyword in lname for keyword in ANTIVIRUS_KEYWORDS)

def risk_level(cpu, ram, disk):
    """Calculate risk level"""
    if cpu > 90 or ram > 90:
        return "CRITICAL"
    elif cpu > 75 or ram > 75:
        return "HIGH"
    elif cpu > 60 or ram > 60:
        return "MEDIUM"
    return "LOW"

def stream_metrics():
    """Continuously stream system metrics via WebSocket"""
    global is_streaming, metrics_history
    
    # Try to load or train model
    if not predictor.is_trained:
        predictor.train_model()
        if not predictor.is_trained:
            predictor.load_model()
    
    # Train anomaly detector
    anomaly_detector.train_ml_model()
    
    while is_streaming:
        try:
            # Collect metrics
            cpu, ram, disk, top_processes = collect_metrics()
            
            # ML Prediction
            predicted_cpu = predictor.predict_cpu(cpu, ram, disk)
            predicted_ram = predictor.predict_ram(cpu, ram, disk)
            
            # Anomaly Detection
            anomaly_result = anomaly_detector.detect_ml_anomaly(cpu, ram, disk)
            
            # Risk Prediction
            trend = risk_predictor.track_risk_trend(risk_predictor._calculate_risk_score(cpu, ram, disk))
            risk_assessment = risk_predictor.predict_risk(cpu, ram, disk, trend)
            
            # AI Explanation
            anomaly_info = "No anomalies" if not anomaly_result['is_anomaly'] else str(anomaly_result['anomalies'])
            explanation = explainer.explain(cpu, ram, disk, top_processes, anomaly_info)
            
            # Optimization suggestions
            optimization_suggestions = explainer.generate_optimization_suggestions(cpu, ram, disk, top_processes)
            
            # Calculate risk level
            current_risk = risk_level(cpu, ram, disk)
            
            # Detect suspicious processes (non-system, high usage)
            suspicious = []
            for p in top_processes:
                name = (p.get("name") or "").lower()
                cpu_p = p.get("cpu_percent", 0) or 0
                ram_p = p.get("memory_percent", 0) or 0
                # Basic ignore list of known system/idle processes
                if name in ("system idle process", "system", "dwm.exe", "csrss.exe", "wininit.exe"):
                    continue
                if is_antivirus_process(name):
                    continue
                if cpu_p > 40 or ram_p > 30:
                    suspicious.append(
                        {
                            "name": p.get("name", "Unknown"),
                            "cpu_percent": round(cpu_p, 2),
                            "memory_percent": round(ram_p, 2),
                        }
                    )

            # Prepare data packet
            data = {
                "timestamp": time.strftime("%H:%M:%S"),
                "cpu": round(cpu, 2),
                "ram": round(ram, 2),
                "disk": round(disk, 2),
                "predicted_cpu": round(predicted_cpu, 2),
                "predicted_ram": round(predicted_ram, 2),
                "risk_level": current_risk,
                "risk_score": round(risk_assessment['risk_score'], 2),
                "crash_probability": round(risk_assessment['crash_probability'], 2),
                "time_to_failure": risk_assessment['time_to_failure'],
                "anomaly": anomaly_result['is_anomaly'],
                "anomaly_details": anomaly_result.get('anomalies', []),
                "risk_level_detailed": risk_assessment['risk_level'],
                "message": explanation,
                "optimization_suggestions": optimization_suggestions,
                "has_suspicious": len(suspicious) > 0,
                "suspicious_processes": suspicious,
                "top_processes": [
                    {
                        "name": p.get('name', 'Unknown'),
                        "cpu_percent": round(p.get('cpu_percent', 0), 2),
                        "memory_percent": round(p.get('memory_percent', 0), 2),
                        "pid": p.get('pid', 0),
                        "is_antivirus": is_antivirus_process(p.get('name', ''))
                    }
                    for p in top_processes
                ],
                "has_antivirus": any(is_antivirus_process(p.get('name', '')) for p in top_processes)
            }
            
            # Store in history (keep last 100)
            metrics_history.append({
                "time": data["timestamp"],
                "cpu": data["cpu"],
                "ram": data["ram"],
                "disk": data["disk"]
            })
            if len(metrics_history) > 100:
                metrics_history.pop(0)
            
            # Emit to all connected clients
            socketio.emit('update', data)
            
            # Sleep for 2 seconds
            time.sleep(2)
            
        except Exception as e:
            print(f"Error in stream_metrics: {e}")
            time.sleep(2)

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    print(f"Client connected: {request.sid}")
    emit('connected', {'message': 'Connected to AI System Performance Analyzer'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    print(f"Client disconnected: {request.sid}")

@socketio.on('start_stream')
def handle_start_stream():
    """Start metrics streaming"""
    global is_streaming, stream_thread
    
    if not is_streaming:
        is_streaming = True
        stream_thread = threading.Thread(target=stream_metrics, daemon=True)
        stream_thread.start()
        emit('stream_started', {'message': 'Metrics streaming started'})

@socketio.on('stop_stream')
def handle_stop_stream():
    """Stop metrics streaming"""
    global is_streaming
    is_streaming = False
    emit('stream_stopped', {'message': 'Metrics streaming stopped'})

@app.route('/')
def index():
    """Serve main dashboard"""
    return send_from_directory('../frontend', 'index.html')

@app.route('/api/metrics')
def get_metrics():
    """REST API endpoint for current metrics"""
    try:
        cpu, ram, disk, top_processes = collect_metrics()
        return jsonify({
            "cpu": cpu,
            "ram": ram,
            "disk": disk,
            "top_processes": top_processes
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/report')
def generate_report_api():
    """Generate and return performance report"""
    try:
        report = report_generator.generate_report()
        return jsonify({
            "success": True,
            "report": report
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/report/pdf')
def generate_pdf_report():
    """Generate PDF report and return download link"""
    try:
        report = report_generator.generate_report()
        result = pdf_exporter.export_report_to_pdf(report)
        
        if result["success"]:
            return jsonify({
                "success": True,
                "file_path": result["file_path"],
                "message": result["message"]
            })
        else:
            return jsonify({
                "success": False,
                "error": result.get("error", "Unknown error")
            }), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/optimize', methods=['POST'])
def optimize_system():
    """API endpoint for system optimization"""
    try:
        data = request.json or {}
        cpu = data.get('cpu', 0)
        ram = data.get('ram', 0)
        disk = data.get('disk', 0)
        processes = data.get('processes', [])
        
        result = optimizer.auto_optimize(cpu, ram, disk, processes)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/predict', methods=['POST'])
def predict_metrics():
    """API endpoint for ML prediction"""
    try:
        data = request.json or {}
        cpu = data.get('cpu', 0)
        ram = data.get('ram', 0)
        disk = data.get('disk', 0)
        
        predicted_cpu = predictor.predict_cpu(cpu, ram, disk)
        predicted_ram = predictor.predict_ram(cpu, ram, disk)
        
        return jsonify({
            "predicted_cpu": predicted_cpu,
            "predicted_ram": predicted_ram
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/risk', methods=['POST'])
def assess_risk():
    """API endpoint for risk assessment"""
    try:
        data = request.json or {}
        cpu = data.get('cpu', 0)
        ram = data.get('ram', 0)
        disk = data.get('disk', 0)
        trend = data.get('trend', 'stable')
        
        risk = risk_predictor.predict_risk(cpu, ram, disk, trend)
        return jsonify(risk)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/history')
def get_history():
    """Get metrics history"""
    return jsonify(metrics_history[-50:])  # Last 50 records

if __name__ == '__main__':
    print("="*70)
    print("AI-Based System Performance Analyzer - Backend Server")
    print("="*70)
    print("Starting server...")
    print("Dashboard available at: http://127.0.0.1:5000")
    print("API endpoints available at: http://127.0.0.1:5000/api/*")
    print("="*70)
    
    # Start streaming automatically
    is_streaming = True
    stream_thread = threading.Thread(target=stream_metrics, daemon=True)
    stream_thread.start()
    
    # Run server
    socketio.run(app, host='0.0.0.0', port=5000, debug=False, allow_unsafe_werkzeug=True)
