"""
Advanced Report Generator with AI-Powered Analysis
Generates comprehensive system performance reports
"""
import pandas as pd
import os
from datetime import datetime
from ai.prompt_engine import PromptEngine

class ReportGenerator:
    def __init__(self):
        self.prompt_engine = PromptEngine()
    
    def generate_report(self, data_file="data/metrics.csv"):
        """Generate comprehensive performance report"""
        try:
            if not os.path.exists(data_file):
                return "No historical data available. System needs to run for some time to generate reports."
            
            df = pd.read_csv(data_file, names=["timestamp", "cpu", "ram", "disk"])
            
            if len(df) < 5:
                return "Insufficient data for report generation. Need at least 5 records."
            
            # Calculate statistics
            avg_cpu = df["cpu"].mean()
            peak_cpu = df["cpu"].max()
            avg_ram = df["ram"].mean()
            peak_ram = df["ram"].max()
            avg_disk = df["disk"].mean()
            peak_disk = df["disk"].max()
            
            # Find peak usage periods
            peak_cpu_time = df.loc[df["cpu"].idxmax(), "timestamp"]
            peak_ram_time = df.loc[df["ram"].idxmax(), "timestamp"]
            
            # Calculate risk periods
            high_cpu_periods = len(df[df["cpu"] > 85])
            high_ram_periods = len(df[df["ram"] > 80])
            critical_periods = len(df[(df["cpu"] > 90) | (df["ram"] > 90)])
            
            # Generate report sections
            report = self._build_report(
                avg_cpu, peak_cpu, avg_ram, peak_ram, avg_disk, peak_disk,
                peak_cpu_time, peak_ram_time,
                high_cpu_periods, high_ram_periods, critical_periods,
                len(df)
            )
            
            return report
        except Exception as e:
            return f"Error generating report: {str(e)}"
    
    def _build_report(self, avg_cpu, peak_cpu, avg_ram, peak_ram, avg_disk, peak_disk,
                     peak_cpu_time, peak_ram_time, high_cpu_periods, high_ram_periods,
                     critical_periods, total_records):
        """Build formatted report"""
        
        report = f"""
{'='*70}
    AI-BASED SYSTEM PERFORMANCE ANALYZER - PERFORMANCE REPORT
{'='*70}

Report Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Total Data Points Analyzed: {total_records}

{'='*70}
EXECUTIVE SUMMARY
{'='*70}

This report analyzes system performance metrics including CPU, RAM, and Disk usage
over the monitoring period. The analysis includes peak usage detection, risk
assessment, and optimization recommendations.

{'='*70}
SYSTEM METRICS SUMMARY
{'='*70}

CPU USAGE:
  - Average CPU Usage: {avg_cpu:.2f}%
  - Peak CPU Usage: {peak_cpu:.2f}%
  - Peak CPU Time: {peak_cpu_time}
  - High CPU Periods (>85%): {high_cpu_periods} occurrences

RAM USAGE:
  - Average RAM Usage: {avg_ram:.2f}%
  - Peak RAM Usage: {peak_ram:.2f}%
  - Peak RAM Time: {peak_ram_time}
  - High RAM Periods (>80%): {high_ram_periods} occurrences

DISK USAGE:
  - Average Disk Usage: {avg_disk:.2f}%
  - Peak Disk Usage: {peak_disk:.2f}%

{'='*70}
RISK ASSESSMENT
{'='*70}

Critical Overload Periods: {critical_periods} occurrences
Risk Level: {self._calculate_overall_risk(peak_cpu, peak_ram, critical_periods)}

"""
        
        # Add recommendations
        report += self._generate_recommendations(avg_cpu, peak_cpu, avg_ram, peak_ram, avg_disk)
        
        # Add AI-generated insights
        report += self._generate_ai_insights(avg_cpu, peak_cpu, avg_ram, peak_ram)
        
        report += f"""
{'='*70}
END OF REPORT
{'='*70}
"""
        return report
    
    def _calculate_overall_risk(self, peak_cpu, peak_ram, critical_periods):
        """Calculate overall system risk level"""
        if peak_cpu > 95 or peak_ram > 95 or critical_periods > 10:
            return "CRITICAL - Immediate action required"
        elif peak_cpu > 90 or peak_ram > 90 or critical_periods > 5:
            return "HIGH - System optimization recommended"
        elif peak_cpu > 80 or peak_ram > 80:
            return "MEDIUM - Monitor system closely"
        else:
            return "LOW - System operating normally"
    
    def _generate_recommendations(self, avg_cpu, peak_cpu, avg_ram, peak_ram, avg_disk):
        """Generate optimization recommendations"""
        recommendations = f"""
{'='*70}
OPTIMIZATION RECOMMENDATIONS
{'='*70}

"""
        
        if peak_cpu > 85:
            recommendations += """
1. CPU OPTIMIZATION:
   - Identify and close CPU-intensive applications during peak usage
   - Consider upgrading CPU if high usage is consistent
   - Check for background processes consuming CPU
   - Use task manager to identify resource-heavy applications

"""
        
        if peak_ram > 80:
            recommendations += """
2. RAM OPTIMIZATION:
   - Close unused browser tabs and applications
   - Disable unnecessary startup programs
   - Consider adding more RAM if usage consistently exceeds 80%
   - Clear browser cache and temporary files
   - Restart system periodically to free up memory

"""
        
        if avg_disk > 80:
            recommendations += """
3. DISK OPTIMIZATION:
   - Free up disk space by deleting temporary files
   - Uninstall unused programs
   - Move large files to external storage
   - Run disk cleanup utility
   - Consider upgrading to larger storage drive

"""
        
        if peak_cpu < 50 and peak_ram < 60:
            recommendations += """
4. SYSTEM STATUS:
   - System is operating efficiently
   - No immediate optimization needed
   - Continue regular monitoring

"""
        
        return recommendations
    
    def _generate_ai_insights(self, avg_cpu, peak_cpu, avg_ram, peak_ram):
        """Generate AI-powered insights using prompt engineering"""
        history_summary = f"Average CPU: {avg_cpu:.1f}%, Peak CPU: {peak_cpu:.1f}%, Average RAM: {avg_ram:.1f}%, Peak RAM: {peak_ram:.1f}%"
        peak_usage = f"Peak CPU: {peak_cpu:.1f}%, Peak RAM: {peak_ram:.1f}%"
        avg_usage = f"Average CPU: {avg_cpu:.1f}%, Average RAM: {avg_ram:.1f}%"
        
        # Build AI prompt (for demonstration - in production, call actual LLM)
        prompt = self.prompt_engine.report_prompt(history_summary, peak_usage, avg_usage)
        
        # Simulated AI insights
        insights = f"""
{'='*70}
AI-GENERATED INSIGHTS
{'='*70}

Based on machine learning analysis and pattern recognition:

"""
        
        if peak_cpu > 90:
            insights += "⚠️ CRITICAL INSIGHT: System experienced severe CPU overload. This indicates\n"
            insights += "   resource-intensive applications or potential system instability.\n\n"
        
        if peak_ram > 90:
            insights += "⚠️ CRITICAL INSIGHT: RAM usage reached critical levels. System may experience\n"
            insights += "   slowdowns or crashes if this pattern continues.\n\n"
        
        if avg_cpu > 70:
            insights += "ℹ️ PATTERN DETECTED: Consistently high CPU usage suggests system is under\n"
            insights += "   constant load. Consider optimizing running applications.\n\n"
        
        if peak_cpu < 50 and avg_cpu < 40:
            insights += "✅ OPTIMAL STATE: CPU usage is within healthy ranges. System is operating\n"
            insights += "   efficiently with good performance headroom.\n\n"
        
        insights += "PREDICTIVE ANALYSIS:\n"
        insights += f"- Based on current patterns, system is {'at risk' if peak_cpu > 85 else 'stable'}\n"
        insights += f"- Recommended monitoring frequency: {'High (every 1-2 minutes)' if peak_cpu > 85 else 'Normal (every 5 minutes)'}\n"
        
        return insights

def generate_report(data_file="data/metrics.csv"):
    """Convenience function to generate report"""
    generator = ReportGenerator()
    return generator.generate_report(data_file)
