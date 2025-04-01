"""
EVA & GUARANI EGOS - Health Check System
Version: 8.0
Author: EVA & GUARANI
Last Updated: 2025-03-30
"""

import os
import sys
import logging
import json
import time
import psutil
import requests
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [HEALTH-CHECK] %(message)s',
    handlers=[
        logging.FileHandler("health_checks.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("HEALTH-CHECK")

@dataclass
class HealthStatus:
    """Health status data structure"""
    status: str  # "healthy", "degraded", "unhealthy"
    details: Dict
    timestamp: float
    subsystem: str
    metrics: Dict
    ethical_validation: bool

class QuantumHealthCheck:
    """Comprehensive health check system for EVA & GUARANI"""
    
    def __init__(self, base_path: Optional[Path] = None):
        self.base_path = base_path or Path(os.getcwd())
        self.last_check: Dict[str, HealthStatus] = {}
        self.anomaly_threshold = 0.2  # 20% deviation threshold
        self.check_interval = 60  # seconds
        self.ethical_framework_active = True
        
    def liveness_check(self) -> HealthStatus:
        """Basic liveness check"""
        try:
            # Check system resources
            cpu = psutil.cpu_percent()
            memory = psutil.virtual_memory().percent
            disk = psutil.disk_usage('/').percent
            
            status = "healthy"
            if cpu > 90 or memory > 90 or disk > 90:
                status = "degraded"
                
            return HealthStatus(
                status=status,
                details={
                    "cpu_usage": cpu,
                    "memory_usage": memory,
                    "disk_usage": disk
                },
                timestamp=time.time(),
                subsystem="BIOS-Q",
                metrics={"response_time": 0.001},
                ethical_validation=True
            )
        except Exception as e:
            logger.error(f"Liveness check failed: {e}")
            return self._create_unhealthy_status("liveness", str(e))
            
    def local_health_check(self) -> HealthStatus:
        """Local system health check"""
        try:
            checks = {
                "disk_writable": self._check_disk_writable(),
                "critical_processes": self._check_critical_processes(),
                "support_processes": self._check_support_processes(),
                "log_system": self._check_logging_system()
            }
            
            status = "healthy"
            failed = [k for k, v in checks.items() if not v]
            if failed:
                status = "degraded" if len(failed) < 2 else "unhealthy"
                
            return HealthStatus(
                status=status,
                details={"checks": checks, "failed": failed},
                timestamp=time.time(),
                subsystem="BIOS-Q",
                metrics={"failed_checks": len(failed)},
                ethical_validation=True
            )
        except Exception as e:
            logger.error(f"Local health check failed: {e}")
            return self._create_unhealthy_status("local", str(e))
            
    def dependency_health_check(self) -> HealthStatus:
        """Check system dependencies"""
        try:
            dependencies = {
                "ETHIK": self._check_subsystem("ETHIK"),
                "CRONOS": self._check_subsystem("CRONOS"),
                "ATLAS": self._check_subsystem("ATLAS"),
                "NEXUS": self._check_subsystem("NEXUS"),
                "MASTER": self._check_subsystem("MASTER")
            }
            
            failed = [k for k, v in dependencies.items() if not v]
            status = "healthy"
            if failed:
                status = "degraded" if len(failed) < 3 else "unhealthy"
                
            return HealthStatus(
                status=status,
                details={"dependencies": dependencies, "failed": failed},
                timestamp=time.time(),
                subsystem="BIOS-Q",
                metrics={"failed_dependencies": len(failed)},
                ethical_validation=True
            )
        except Exception as e:
            logger.error(f"Dependency health check failed: {e}")
            return self._create_unhealthy_status("dependency", str(e))
            
    def anomaly_detection(self) -> HealthStatus:
        """Detect system anomalies"""
        try:
            metrics = self._collect_system_metrics()
            anomalies = self._detect_anomalies(metrics)
            
            status = "healthy"
            if anomalies:
                status = "degraded" if len(anomalies) < 3 else "unhealthy"
                
            return HealthStatus(
                status=status,
                details={"anomalies": anomalies, "metrics": metrics},
                timestamp=time.time(),
                subsystem="BIOS-Q",
                metrics={"anomaly_count": len(anomalies)},
                ethical_validation=True
            )
        except Exception as e:
            logger.error(f"Anomaly detection failed: {e}")
            return self._create_unhealthy_status("anomaly", str(e))
    
    def _check_disk_writable(self) -> bool:
        """Check if disk is writable"""
        try:
            test_file = self.base_path / "health_check_test.tmp"
            test_file.write_text("test")
            test_file.unlink()
            return True
        except:
            return False
            
    def _check_critical_processes(self) -> bool:
        """Check critical system processes"""
        required_processes = ["init_bios_q.py", "context_boot_sequence.py"]
        running_processes = [p.name() for p in psutil.process_iter(['name'])]
        return all(proc in running_processes for proc in required_processes)
        
    def _check_support_processes(self) -> bool:
        """Check support processes"""
        support_processes = ["monitoring_daemon", "credential_manager"]
        running_processes = [p.name() for p in psutil.process_iter(['name'])]
        return any(proc in running_processes for proc in support_processes)
        
    def _check_logging_system(self) -> bool:
        """Check logging system"""
        try:
            logger.info("Health check logging test")
            return True
        except:
            return False
            
    def _check_subsystem(self, subsystem: str) -> bool:
        """Check subsystem health"""
        subsystem_path = self.base_path / subsystem
        return subsystem_path.exists() and any(subsystem_path.iterdir())
        
    def _collect_system_metrics(self) -> Dict:
        """Collect system metrics"""
        return {
            "cpu": psutil.cpu_percent(interval=1),
            "memory": psutil.virtual_memory().percent,
            "disk": psutil.disk_usage('/').percent,
            "network": len(psutil.net_connections()),
            "processes": len(psutil.pids())
        }
        
    def _detect_anomalies(self, metrics: Dict) -> List[str]:
        """Detect system anomalies"""
        anomalies = []
        baseline = {
            "cpu": 50,
            "memory": 70,
            "disk": 80,
            "network": 1000,
            "processes": 100
        }
        
        for metric, value in metrics.items():
            if abs(value - baseline[metric]) / baseline[metric] > self.anomaly_threshold:
                anomalies.append(f"{metric} deviation: {value} vs {baseline[metric]}")
                
        return anomalies
        
    def _create_unhealthy_status(self, check_type: str, error: str) -> HealthStatus:
        """Create unhealthy status"""
        return HealthStatus(
            status="unhealthy",
            details={"error": error, "check_type": check_type},
            timestamp=time.time(),
            subsystem="BIOS-Q",
            metrics={"error_count": 1},
            ethical_validation=True
        )
        
    def run_all_checks(self) -> Dict[str, HealthStatus]:
        """Run all health checks"""
        checks = {
            "liveness": self.liveness_check(),
            "local": self.local_health_check(),
            "dependency": self.dependency_health_check(),
            "anomaly": self.anomaly_detection()
        }
        
        self.last_check = checks
        return checks
        
    def get_system_status(self) -> Tuple[str, Dict]:
        """Get overall system status"""
        if not self.last_check:
            self.run_all_checks()
            
        statuses = [check.status for check in self.last_check.values()]
        if any(status == "unhealthy" for status in statuses):
            return "unhealthy", self.last_check
        elif any(status == "degraded" for status in statuses):
            return "degraded", self.last_check
        return "healthy", self.last_check

if __name__ == "__main__":
    health_checker = QuantumHealthCheck()
    status, details = health_checker.get_system_status()
    print(f"System Status: {status}")
    print(json.dumps(details, default=lambda x: x.__dict__, indent=2)) 