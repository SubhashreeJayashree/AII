"""
Auto Optimization Engine
Automatically optimizes system performance
"""
import psutil
import os
import signal
import platform

class SystemOptimizer:
    def __init__(self, safe_mode=True):
        self.safe_mode = safe_mode
        self.protected_processes = [
            'System', 'svchost.exe', 'explorer.exe', 
            'winlogon.exe', 'csrss.exe', 'lsass.exe'
        ]
    
    def can_optimize(self, cpu, ram, disk):
        """Check if optimization is needed"""
        return cpu > 85 or ram > 80 or disk > 90
    
    def optimize_cpu(self, processes, threshold=50):
        """Kill processes consuming high CPU"""
        if self.safe_mode:
            return {"action": "safe_mode", "message": "Safe mode enabled. Manual optimization recommended."}
        
        killed = []
        try:
            for proc in processes:
                if proc.get('cpu_percent', 0) > threshold:
                    proc_name = proc.get('name', '')
                    if proc_name not in self.protected_processes:
                        try:
                            pid = proc.get('pid')
                            if pid:
                                os.kill(pid, signal.SIGTERM)
                                killed.append(proc_name)
                        except (ProcessLookupError, PermissionError, psutil.NoSuchProcess):
                            pass
        except Exception as e:
            return {"error": str(e)}
        
        return {
            "action": "killed",
            "processes": killed,
            "message": f"Terminated {len(killed)} high CPU processes"
        }
    
    def optimize_ram(self):
        """Suggest RAM optimization (safe operations only)"""
        suggestions = []
        
        try:
            # Get memory info
            mem = psutil.virtual_memory()
            
            if mem.percent > 80:
                suggestions.append("High RAM usage detected.")
                suggestions.append("Recommendations:")
                suggestions.append("- Close unused browser tabs")
                suggestions.append("- Close background applications")
                suggestions.append("- Restart system if RAM usage persists")
        except Exception as e:
            return {"error": str(e)}
        
        return {
            "action": "suggestions",
            "suggestions": suggestions
        }
    
    def clear_cache(self):
        """Clear system cache (platform-specific)"""
        if self.safe_mode:
            return {"action": "safe_mode", "message": "Cache clearing disabled in safe mode"}
        
        try:
            system = platform.system()
            if system == "Windows":
                # Windows cache clearing commands
                os.system("ipconfig /flushdns")
                return {"action": "cache_cleared", "message": "DNS cache cleared"}
            elif system == "Linux":
                # Linux cache clearing
                os.system("sync && echo 3 > /proc/sys/vm/drop_caches")
                return {"action": "cache_cleared", "message": "System cache cleared"}
            else:
                return {"action": "not_supported", "message": f"Cache clearing not supported on {system}"}
        except Exception as e:
            return {"error": str(e)}
    
    def auto_optimize(self, cpu, ram, disk, processes):
        """Automatic optimization based on metrics"""
        results = []
        
        if cpu > 85:
            result = self.optimize_cpu(processes)
            results.append(result)
        
        if ram > 80:
            result = self.optimize_ram()
            results.append(result)
        
        if disk > 90:
            results.append({
                "action": "disk_warning",
                "message": "Disk space critically low. Manual cleanup required."
            })
        
        return {
            "optimized": len(results) > 0,
            "results": results
        }
    
    def get_optimization_status(self):
        """Get current optimization status"""
        return {
            "safe_mode": self.safe_mode,
            "protected_processes": self.protected_processes
        }

def kill_process(name):
    """Legacy function for backward compatibility"""
    optimizer = SystemOptimizer(safe_mode=True)
    return optimizer.optimize_cpu([{"name": name, "cpu_percent": 100}])
