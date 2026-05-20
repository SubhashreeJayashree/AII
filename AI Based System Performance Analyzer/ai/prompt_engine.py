"""
Advanced Prompt Engineering System
Multiple prompt templates for different AI tasks
"""
from datetime import datetime

class PromptEngine:
    def __init__(self):
        self.system_role = "You are an expert operating system performance analyst and system optimization specialist."
    
    def diagnostic_prompt(self, cpu, ram, disk, processes):
        """Generate diagnostic prompt for root cause analysis"""
        proc_list = "\n".join([
            f"- {p.get('name', 'Unknown')}: CPU {p.get('cpu_percent', 0):.1f}%, RAM {p.get('memory_percent', 0):.1f}%"
            for p in processes[:5]
        ])
        
        prompt = f"""
{self.system_role}

SYSTEM PERFORMANCE DIAGNOSTIC TASK

Current System Metrics:
- CPU Usage: {cpu:.1f}%
- RAM Usage: {ram:.1f}%
- Disk Usage: {disk:.1f}%

Top Running Processes:
{proc_list}

Analysis Required:
1. Identify the root cause of any performance issues
2. Determine which processes are causing slowdowns
3. Explain the relationship between metrics
4. Assess system stability

Provide a clear, technical explanation in simple language.
"""
        return prompt
    
    def prediction_prompt(self, cpu, ram, disk, prediction_value):
        """Generate prediction prompt for risk assessment"""
        prompt = f"""
{self.system_role}

SYSTEM PERFORMANCE PREDICTION TASK

Current Metrics:
- CPU: {cpu:.1f}%
- RAM: {ram:.1f}%
- Disk: {disk:.1f}%

ML Prediction (Next 5 minutes):
- Predicted CPU: {prediction_value:.1f}%

Risk Assessment Required:
1. Will the system crash or freeze soon?
2. What is the risk level? (LOW/MEDIUM/HIGH/CRITICAL)
3. How long until potential system failure?
4. What are the warning signs?

Provide risk assessment with confidence level.
"""
        return prompt
    
    def optimization_prompt(self, cpu, ram, disk, processes):
        """Generate optimization prompt for performance improvement"""
        proc_list = ", ".join([p.get('name', 'Unknown') for p in processes[:5]])
        
        prompt = f"""
{self.system_role}

SYSTEM OPTIMIZATION TASK

Current Performance:
- CPU: {cpu:.1f}%
- RAM: {ram:.1f}%
- Disk: {disk:.1f}%

Active Processes: {proc_list}

Optimization Required:
1. Suggest immediate actions to improve performance
2. Recommend which processes to close/terminate
3. Provide step-by-step optimization plan
4. Estimate performance improvement after optimization

Give actionable, safe recommendations.
"""
        return prompt
    
    def report_prompt(self, history_summary, peak_usage, avg_usage):
        """Generate report generation prompt"""
        prompt = f"""
{self.system_role}

SYSTEM PERFORMANCE REPORT GENERATION

Historical Data Summary:
{history_summary}

Peak Usage Periods:
{peak_usage}

Average Usage:
{avg_usage}

Report Requirements:
1. Executive summary of system performance
2. Identify peak usage periods and patterns
3. Highlight risk periods and anomalies
4. Provide optimization recommendations
5. Predict future performance trends

Generate a professional, comprehensive performance report.
"""
        return prompt
    
    def risk_prediction_prompt(self, cpu, ram, disk, trend):
        """Generate risk prediction prompt"""
        prompt = f"""
{self.system_role}

SYSTEM RISK PREDICTION TASK

Current State:
- CPU: {cpu:.1f}%
- RAM: {ram:.1f}%
- Disk: {disk:.1f}%

Usage Trend: {trend}

Prediction Required:
1. Predict system crash probability (0-100%)
2. Estimate time to failure (if at risk)
3. Identify critical thresholds being approached
4. Recommend preventive actions

Provide risk score and urgency level.
"""
        return prompt
    
    def explain_prompt(self, cpu, ram, disk, processes, anomaly_info):
        """Generate user-friendly explanation prompt"""
        proc_list = "\n".join([
            f"- {p.get('name', 'Unknown')} (CPU: {p.get('cpu_percent', 0):.1f}%)"
            for p in processes[:3]
        ])
        
        prompt = f"""
{self.system_role}

USER-FRIENDLY EXPLANATION TASK

System Status:
- CPU: {cpu:.1f}%
- RAM: {ram:.1f}%
- Disk: {disk:.1f}%

Top Processes:
{proc_list}

Anomaly Detection:
{anomaly_info}

Task:
Explain the current system performance in simple, non-technical language.
- Why is the system slow/fast?
- What is causing the current state?
- What should the user do?

Use friendly, conversational tone. Avoid technical jargon.
"""
        return prompt

def build_prompt(prompt_type, **kwargs):
    """Factory function to build prompts"""
    engine = PromptEngine()
    
    if prompt_type == "diagnostic":
        return engine.diagnostic_prompt(
            kwargs.get('cpu', 0),
            kwargs.get('ram', 0),
            kwargs.get('disk', 0),
            kwargs.get('processes', [])
        )
    elif prompt_type == "prediction":
        return engine.prediction_prompt(
            kwargs.get('cpu', 0),
            kwargs.get('ram', 0),
            kwargs.get('disk', 0),
            kwargs.get('prediction', 0)
        )
    elif prompt_type == "optimization":
        return engine.optimization_prompt(
            kwargs.get('cpu', 0),
            kwargs.get('ram', 0),
            kwargs.get('disk', 0),
            kwargs.get('processes', [])
        )
    elif prompt_type == "explain":
        return engine.explain_prompt(
            kwargs.get('cpu', 0),
            kwargs.get('ram', 0),
            kwargs.get('disk', 0),
            kwargs.get('processes', []),
            kwargs.get('anomaly_info', 'No anomalies detected')
        )
    
    return ""
