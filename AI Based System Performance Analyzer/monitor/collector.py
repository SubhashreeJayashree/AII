"""
Advanced Real-Time System Metrics Collector
Collects CPU, RAM, Disk, and Process-level data
"""
import psutil
import time
import csv
import os
from datetime import datetime

def get_top_processes(limit=5):
    """Get top CPU-consuming processes"""
    processes = []
    try:
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status']):
            try:
                proc.info['cpu_percent'] = proc.info['cpu_percent'] or 0
                proc.info['memory_percent'] = proc.info['memory_percent'] or 0
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        processes = sorted(processes, key=lambda x: x['cpu_percent'], reverse=True)
        return processes[:limit]
    except Exception as e:
        return []

def get_detailed_metrics():
    """Collect comprehensive system metrics"""
    try:
        # CPU metrics
        cpu_percent = psutil.cpu_percent(interval=0.1)
        cpu_count = psutil.cpu_count()
        cpu_per_core = psutil.cpu_percent(interval=0.1, percpu=True)
        
        # Memory metrics
        mem = psutil.virtual_memory()
        ram_percent = mem.percent
        ram_used = mem.used / (1024**3)  # GB
        ram_total = mem.total / (1024**3)  # GB
        ram_available = mem.available / (1024**3)  # GB
        
        # Disk metrics
        disk = psutil.disk_usage('/')
        disk_percent = disk.percent
        disk_used = disk.used / (1024**3)  # GB
        disk_total = disk.total / (1024**3)  # GB
        
        # Network metrics (optional)
        net = psutil.net_io_counters()
        
        # Process metrics
        top_processes = get_top_processes(5)
        
        # System load (if available)
        try:
            load_avg = os.getloadavg() if hasattr(os, 'getloadavg') else None
        except:
            load_avg = None
        
        return {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'cpu': {
                'percent': cpu_percent,
                'count': cpu_count,
                'per_core': cpu_per_core
            },
            'ram': {
                'percent': ram_percent,
                'used_gb': round(ram_used, 2),
                'total_gb': round(ram_total, 2),
                'available_gb': round(ram_available, 2)
            },
            'disk': {
                'percent': disk_percent,
                'used_gb': round(disk_used, 2),
                'total_gb': round(disk_total, 2)
            },
            'processes': top_processes,
            'load_avg': load_avg
        }
    except Exception as e:
        print(f"Error collecting metrics: {e}")
        return None

def collect_metrics():
    """Simplified metrics collection for real-time streaming"""
    try:
        cpu = psutil.cpu_percent(interval=0.1)
        ram = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent
        top_processes = get_top_processes(5)
        
        return cpu, ram, disk, top_processes
    except Exception as e:
        print(f"Error in collect_metrics: {e}")
        return 0, 0, 0, []

def start_data_collection(output_file="data/metrics.csv", interval=2):
    """Continuously collect and store metrics to CSV"""
    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)
    
    # Check if file exists to write header
    file_exists = os.path.exists(output_file)
    
    with open(output_file, "a", newline="") as f:
        writer = csv.writer(f)
        
        if not file_exists:
            writer.writerow(["timestamp", "cpu", "ram", "disk"])
        
        while True:
            try:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cpu, ram, disk, _ = collect_metrics()
                writer.writerow([timestamp, cpu, ram, disk])
                f.flush()  # Ensure data is written immediately
                time.sleep(interval)
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error in data collection: {e}")
                time.sleep(interval)

if __name__ == "__main__":
    print("Starting system metrics collection...")
    start_data_collection()
