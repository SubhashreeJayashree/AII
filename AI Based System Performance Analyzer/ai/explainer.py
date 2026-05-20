"""
AI Explanation Engine
Generates human-like explanations using prompt engineering
"""
from ai.prompt_engine import PromptEngine, build_prompt

class AIExplainer:
    def __init__(self):
        self.prompt_engine = PromptEngine()
    
    def explain(self, cpu, ram, disk, processes, anomaly_info=None):
        """Generate AI explanation for current system state"""
        try:
            # Build explanation prompt
            prompt = build_prompt(
                "explain",
                cpu=cpu,
                ram=ram,
                disk=disk,
                processes=processes,
                anomaly_info=anomaly_info or "No anomalies detected"
            )
            
            # Simulate AI response (replace with real LLM API call)
            explanation = self._generate_response(cpu, ram, disk, processes, anomaly_info)
            
            return explanation
        except Exception as e:
            return f"System analysis error: {str(e)}"
    
    def _generate_response(self, cpu, ram, disk, processes, anomaly_info):
        """Generate response based on system state"""
        # This simulates an AI response
        # In production, replace with OpenAI API, local LLM, or other AI service
        
        top_process = processes[0] if processes else None
        process_name = top_process.get('name', 'Unknown') if top_process else 'Unknown'
        process_cpu = top_process.get('cpu_percent', 0) if top_process else 0
        
        explanations = []
        
        # CPU analysis
        if cpu > 90:
            explanations.append(f"⚠️ CRITICAL: CPU usage is extremely high at {cpu:.1f}%. Your system may freeze or become unresponsive.")
            if process_name != 'Unknown':
                explanations.append(f"The main culprit is {process_name}, consuming {process_cpu:.1f}% of CPU.")
        elif cpu > 75:
            explanations.append(f"⚠️ WARNING: CPU usage is high at {cpu:.1f}%. System performance may degrade.")
            if process_name != 'Unknown':
                explanations.append(f"{process_name} is the primary CPU consumer.")
        elif cpu > 50:
            explanations.append(f"ℹ️ CPU usage is moderate at {cpu:.1f}%. System is handling load normally.")
        else:
            explanations.append(f"✅ CPU usage is healthy at {cpu:.1f}%. System is running efficiently.")
        
        # RAM analysis
        if ram > 90:
            explanations.append(f"🚨 CRITICAL: RAM is almost exhausted at {ram:.1f}%. System may crash or become very slow.")
            explanations.append("Immediate action: Close unnecessary applications to free memory.")
        elif ram > 80:
            explanations.append(f"⚠️ WARNING: RAM usage is high at {ram:.1f}%. Consider closing background applications.")
        elif ram > 60:
            explanations.append(f"ℹ️ RAM usage is moderate at {ram:.1f}%. System has sufficient memory available.")
        else:
            explanations.append(f"✅ RAM usage is healthy at {ram:.1f}%. Plenty of memory available.")
        
        # Disk analysis
        if disk > 90:
            explanations.append(f"🚨 CRITICAL: Disk storage is almost full at {disk:.1f}%. Free up space immediately.")
        elif disk > 80:
            explanations.append(f"⚠️ WARNING: Disk storage is getting full at {disk:.1f}%. Consider cleaning up files.")
        
        # Overall assessment
        if cpu > 85 and ram > 80:
            explanations.append("\n🔴 SYSTEM OVERLOAD: Both CPU and RAM are critically high. System slowdown is imminent.")
        elif cpu > 75 or ram > 75:
            explanations.append("\n🟡 PERFORMANCE DEGRADATION: System is under stress. Monitor closely.")
        else:
            explanations.append("\n🟢 SYSTEM STABLE: All metrics are within normal ranges.")
        
        return " ".join(explanations)
    
    def generate_diagnostic(self, cpu, ram, disk, processes):
        """Generate detailed diagnostic explanation"""
        prompt = build_prompt("diagnostic", cpu=cpu, ram=ram, disk=disk, processes=processes)
        
        # Simulated diagnostic response
        response = f"""
DIAGNOSTIC ANALYSIS:

Root Cause Analysis:
- CPU Usage: {cpu:.1f}% {'(CRITICAL)' if cpu > 85 else '(NORMAL)' if cpu < 50 else '(HIGH)'}
- RAM Usage: {ram:.1f}% {'(CRITICAL)' if ram > 80 else '(NORMAL)' if ram < 60 else '(HIGH)'}
- Disk Usage: {disk:.1f}% {'(CRITICAL)' if disk > 90 else '(NORMAL)'}

Primary Issues:
"""
        
        if processes:
            top = processes[0]
            response += f"- Main process: {top.get('name', 'Unknown')} consuming {top.get('cpu_percent', 0):.1f}% CPU\n"
        
        return response
    
    def generate_optimization_suggestions(self, cpu, ram, disk, processes):
        """Generate optimization suggestions"""
        suggestions = []
        
        if cpu > 75:
            suggestions.append("1. Close CPU-intensive applications")
            if processes:
                top = processes[0]
                suggestions.append(f"   - Consider closing: {top.get('name', 'Unknown')}")
        
        if ram > 75:
            suggestions.append("2. Free up RAM by closing unused applications")
            suggestions.append("   - Close browser tabs you're not using")
            suggestions.append("   - Disable startup programs")
        
        if disk > 80:
            suggestions.append("3. Clean up disk space")
            suggestions.append("   - Delete temporary files")
            suggestions.append("   - Uninstall unused programs")
        
        if not suggestions:
            suggestions.append("System is optimized. No immediate actions needed.")
        
        return "\n".join(suggestions)

def explain(cpu, ram, disk, processes, anomaly_info=None):
    """Convenience function for explanation"""
    explainer = AIExplainer()
    return explainer.explain(cpu, ram, disk, processes, anomaly_info)
