"""
Advanced Risk Prediction Engine
Uses ML and prompt engineering to predict system failure risks
"""
import pandas as pd
import numpy as np
from ai.prompt_engine import PromptEngine

class RiskPredictor:
    def __init__(self):
        self.prompt_engine = PromptEngine()
        self.risk_history = []
    
    def predict_risk(self, cpu, ram, disk, trend="stable"):
        """Predict system risk level with detailed analysis"""
        risk_score = self._calculate_risk_score(cpu, ram, disk)
        risk_level = self._get_risk_level(risk_score)
        crash_probability = self._calculate_crash_probability(cpu, ram, disk)
        time_to_failure = self._estimate_time_to_failure(cpu, ram, disk, risk_level)
        
        # Build AI prompt for risk prediction
        prompt = self.prompt_engine.risk_prediction_prompt(cpu, ram, disk, trend)
        
        # Generate AI-powered risk assessment
        assessment = self._generate_risk_assessment(
            cpu, ram, disk, risk_level, crash_probability, time_to_failure
        )
        
        return {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "crash_probability": crash_probability,
            "time_to_failure": time_to_failure,
            "assessment": assessment,
            "prompt_used": prompt  # For demonstration of prompt engineering
        }
    
    def _calculate_risk_score(self, cpu, ram, disk):
        """Calculate numerical risk score (0-100)"""
        # Weighted risk calculation
        cpu_risk = max(0, (cpu - 50) * 1.5) if cpu > 50 else 0
        ram_risk = max(0, (ram - 60) * 1.2) if ram > 60 else 0
        disk_risk = max(0, (disk - 70) * 0.8) if disk > 70 else 0
        
        # Critical thresholds
        if cpu > 95:
            cpu_risk = 100
        if ram > 95:
            ram_risk = 100
        if disk > 95:
            disk_risk = 100
        
        # Combined risk (weighted average)
        total_risk = (cpu_risk * 0.4 + ram_risk * 0.4 + disk_risk * 0.2)
        return min(100, max(0, total_risk))
    
    def _get_risk_level(self, risk_score):
        """Convert risk score to level"""
        if risk_score >= 80:
            return "CRITICAL"
        elif risk_score >= 60:
            return "HIGH"
        elif risk_score >= 40:
            return "MEDIUM"
        elif risk_score >= 20:
            return "LOW"
        else:
            return "MINIMAL"
    
    def _calculate_crash_probability(self, cpu, ram, disk):
        """Calculate probability of system crash (0-100%)"""
        probability = 0
        
        # CPU-based crash probability
        if cpu > 95:
            probability += 60
        elif cpu > 90:
            probability += 40
        elif cpu > 85:
            probability += 20
        
        # RAM-based crash probability
        if ram > 95:
            probability += 50
        elif ram > 90:
            probability += 30
        elif ram > 85:
            probability += 15
        
        # Combined critical state
        if cpu > 90 and ram > 90:
            probability = min(100, probability + 20)
        
        return min(100, probability)
    
    def _estimate_time_to_failure(self, cpu, ram, disk, risk_level):
        """Estimate time until potential system failure"""
        if risk_level == "CRITICAL":
            if cpu > 95 or ram > 95:
                return "Immediate (0-5 minutes)"
            else:
                return "Very Soon (5-15 minutes)"
        elif risk_level == "HIGH":
            return "Soon (15-30 minutes)"
        elif risk_level == "MEDIUM":
            return "Possible (30-60 minutes)"
        else:
            return "Not imminent"
    
    def _generate_risk_assessment(self, cpu, ram, disk, risk_level, crash_probability, time_to_failure):
        """Generate detailed risk assessment using AI reasoning"""
        assessment = f"""
RISK ASSESSMENT ANALYSIS
{'='*50}

Current System State:
- CPU Usage: {cpu:.1f}%
- RAM Usage: {ram:.1f}%
- Disk Usage: {disk:.1f}%

Risk Analysis:
- Overall Risk Level: {risk_level}
- Crash Probability: {crash_probability:.1f}%
- Estimated Time to Failure: {time_to_failure}

"""
        
        if risk_level == "CRITICAL":
            assessment += """
⚠️ CRITICAL RISK DETECTED ⚠️

The system is in a critical state and may experience:
- System freeze or crash
- Data loss risk
- Application failures
- Unresponsive interface

IMMEDIATE ACTIONS REQUIRED:
1. Close all non-essential applications immediately
2. Save all work in progress
3. Consider system restart
4. Monitor system closely

"""
        elif risk_level == "HIGH":
            assessment += """
⚠️ HIGH RISK WARNING

The system is under significant stress:
- Performance degradation likely
- Potential for system instability
- Applications may become slow

RECOMMENDED ACTIONS:
1. Close resource-intensive applications
2. Free up memory
3. Monitor system metrics
4. Prepare for potential issues

"""
        elif risk_level == "MEDIUM":
            assessment += """
ℹ️ MEDIUM RISK

System is experiencing elevated usage:
- Monitor system performance
- Consider closing unused applications
- System is stable but should be watched

"""
        else:
            assessment += """
✅ LOW RISK

System is operating normally:
- All metrics within safe ranges
- No immediate concerns
- Continue regular monitoring

"""
        
        # Add predictive insights
        if cpu > 85 or ram > 85:
            assessment += """
PREDICTIVE INSIGHT:
Based on current metrics, if usage continues to increase, the system
may reach critical levels within the next monitoring cycle. Proactive
optimization is recommended.

"""
        
        return assessment
    
    def track_risk_trend(self, risk_score):
        """Track risk over time to identify trends"""
        self.risk_history.append(risk_score)
        
        # Keep only last 50 records
        if len(self.risk_history) > 50:
            self.risk_history.pop(0)
        
        if len(self.risk_history) >= 5:
            recent_avg = np.mean(self.risk_history[-5:])
            overall_avg = np.mean(self.risk_history)
            
            if recent_avg > overall_avg * 1.2:
                return "INCREASING"
            elif recent_avg < overall_avg * 0.8:
                return "DECREASING"
            else:
                return "STABLE"
        
        return "INSUFFICIENT_DATA"

def predict_risk(cpu, ram, disk, trend="stable"):
    """Convenience function for risk prediction"""
    predictor = RiskPredictor()
    return predictor.predict_risk(cpu, ram, disk, trend)
