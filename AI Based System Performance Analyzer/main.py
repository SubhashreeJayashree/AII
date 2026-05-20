"""
Main Entry Point for AI-Based System Performance Analyzer
Run this file to start the complete system
"""
import os
import sys
import time
import threading

# Ensure required directories exist
os.makedirs("data", exist_ok=True)
os.makedirs("models", exist_ok=True)
os.makedirs("reports", exist_ok=True)

def print_banner():
    """Print welcome banner (ASCII-safe for Windows consoles)"""
    banner = """
====================================================================
                 AI-BASED SYSTEM PERFORMANCE ANALYZER
              Advanced Real-Time Monitoring & Analysis
====================================================================

Features:
  - Real-Time System Monitoring (CPU, RAM, Disk)
  - Machine Learning Prediction Engine
  - Anomaly Detection (ML-based)
  - AI-Powered Explanation Engine
  - Risk Assessment & Prediction
  - Auto-Optimization Suggestions
  - Performance Report Generation
  - PDF Export Functionality
  - Advanced Prompt Engineering
  - Web-Based Real-Time Dashboard

Technologies:
  - Python (Backend, ML, AI)
  - Flask + Socket.IO (Real-Time Server)
  - HTML + CSS + JavaScript (Frontend)
  - Chart.js (Visualization)
  - scikit-learn (Machine Learning)
  - ReportLab (PDF Generation)

"""
    print(banner)

def start_data_collection():
    """Start background data collection"""
    from monitor.collector import start_data_collection
    print("Starting background data collection...")
    collection_thread = threading.Thread(
        target=start_data_collection,
        args=("data/metrics.csv", 2),
        daemon=True
    )
    collection_thread.start()
    print("Data collection started")

def main():
    """Main function"""
    print_banner()
    
    # Check if required packages are installed
    try:
        import psutil
        import flask
        import flask_socketio
        import pandas
        import sklearn
        import reportlab
    except ImportError as e:
        print(f"\n❌ Error: Required package not installed: {e}")
        print("\nPlease install requirements:")
        print("pip install -r requirements.txt")
        sys.exit(1)
    
    # Start data collection in background
    start_data_collection()
    
    # Give it a moment to start collecting
    time.sleep(1)
    
    # Start the backend server
    print("\n" + "="*70)
    print("Starting Backend Server...")
    print("="*70)
    print("\nDashboard will be available at: http://127.0.0.1:5000")
    print("Press Ctrl+C to stop the server\n")
    
    # Import and run server
    from backend.server import app, socketio
    
    try:
        socketio.run(app, host='0.0.0.0', port=5000, debug=False, allow_unsafe_werkzeug=True)
    except KeyboardInterrupt:
        print("\n\nShutting down server...")
        print("Thank you for using AI-Based System Performance Analyzer!")

if __name__ == "__main__":
    main()
