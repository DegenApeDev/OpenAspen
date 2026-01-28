"""
System monitoring utilities for Linux
Collects CPU, memory, disk, network, and process information
"""
import psutil
import platform
from typing import Dict, List, Any
from datetime import datetime


class SystemMonitor:
    """Collects and formats Linux system metrics"""
    
    @staticmethod
    def get_cpu_info() -> Dict[str, Any]:
        """Get CPU usage and information"""
        return {
            "usage_percent": psutil.cpu_percent(interval=1),
            "usage_per_cpu": psutil.cpu_percent(interval=1, percpu=True),
            "count_physical": psutil.cpu_count(logical=False),
            "count_logical": psutil.cpu_count(logical=True),
            "frequency_mhz": psutil.cpu_freq().current if psutil.cpu_freq() else None,
            "load_average": psutil.getloadavg() if hasattr(psutil, "getloadavg") else None,
        }
    
    @staticmethod
    def get_memory_info() -> Dict[str, Any]:
        """Get memory usage information"""
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        return {
            "total_gb": round(mem.total / (1024**3), 2),
            "available_gb": round(mem.available / (1024**3), 2),
            "used_gb": round(mem.used / (1024**3), 2),
            "percent_used": mem.percent,
            "swap_total_gb": round(swap.total / (1024**3), 2),
            "swap_used_gb": round(swap.used / (1024**3), 2),
            "swap_percent": swap.percent,
        }
    
    @staticmethod
    def get_disk_info() -> Dict[str, Any]:
        """Get disk usage information"""
        partitions = []
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                partitions.append({
                    "device": partition.device,
                    "mountpoint": partition.mountpoint,
                    "fstype": partition.fstype,
                    "total_gb": round(usage.total / (1024**3), 2),
                    "used_gb": round(usage.used / (1024**3), 2),
                    "free_gb": round(usage.free / (1024**3), 2),
                    "percent_used": usage.percent,
                })
            except PermissionError:
                continue
        
        disk_io = psutil.disk_io_counters()
        return {
            "partitions": partitions,
            "io_read_mb": round(disk_io.read_bytes / (1024**2), 2) if disk_io else None,
            "io_write_mb": round(disk_io.write_bytes / (1024**2), 2) if disk_io else None,
        }
    
    @staticmethod
    def get_network_info() -> Dict[str, Any]:
        """Get network statistics"""
        net_io = psutil.net_io_counters()
        connections = len(psutil.net_connections())
        
        return {
            "bytes_sent_mb": round(net_io.bytes_sent / (1024**2), 2),
            "bytes_recv_mb": round(net_io.bytes_recv / (1024**2), 2),
            "packets_sent": net_io.packets_sent,
            "packets_recv": net_io.packets_recv,
            "active_connections": connections,
        }
    
    @staticmethod
    def get_top_processes(limit: int = 10) -> List[Dict[str, Any]]:
        """Get top processes by CPU and memory usage"""
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status']):
            try:
                processes.append({
                    "pid": proc.info['pid'],
                    "name": proc.info['name'],
                    "cpu_percent": proc.info['cpu_percent'],
                    "memory_percent": round(proc.info['memory_percent'], 2),
                    "status": proc.info['status'],
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        # Sort by CPU usage
        processes.sort(key=lambda x: x['cpu_percent'] or 0, reverse=True)
        return processes[:limit]
    
    @staticmethod
    def get_system_info() -> Dict[str, Any]:
        """Get general system information"""
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        uptime = datetime.now() - boot_time
        
        return {
            "hostname": platform.node(),
            "os": platform.system(),
            "os_version": platform.release(),
            "architecture": platform.machine(),
            "boot_time": boot_time.strftime("%Y-%m-%d %H:%M:%S"),
            "uptime_hours": round(uptime.total_seconds() / 3600, 2),
            "users_logged_in": len(psutil.users()),
        }
    
    @classmethod
    def get_full_report(cls) -> Dict[str, Any]:
        """Get comprehensive system report"""
        return {
            "timestamp": datetime.now().isoformat(),
            "system": cls.get_system_info(),
            "cpu": cls.get_cpu_info(),
            "memory": cls.get_memory_info(),
            "disk": cls.get_disk_info(),
            "network": cls.get_network_info(),
            "top_processes": cls.get_top_processes(limit=10),
        }
    
    @classmethod
    def format_report_for_llm(cls) -> str:
        """Format system report in a human-readable way for LLM analysis"""
        report = cls.get_full_report()
        
        output = []
        output.append("=== LINUX SYSTEM HEALTH REPORT ===\n")
        
        # System Info
        sys = report['system']
        output.append(f"System: {sys['hostname']} ({sys['os']} {sys['os_version']})")
        output.append(f"Uptime: {sys['uptime_hours']} hours")
        output.append(f"Architecture: {sys['architecture']}\n")
        
        # CPU
        cpu = report['cpu']
        output.append(f"CPU Usage: {cpu['usage_percent']}%")
        output.append(f"CPU Cores: {cpu['count_physical']} physical, {cpu['count_logical']} logical")
        if cpu['load_average']:
            output.append(f"Load Average: {cpu['load_average']}\n")
        
        # Memory
        mem = report['memory']
        output.append(f"Memory: {mem['used_gb']}GB / {mem['total_gb']}GB ({mem['percent_used']}%)")
        output.append(f"Swap: {mem['swap_used_gb']}GB / {mem['swap_total_gb']}GB ({mem['swap_percent']}%)\n")
        
        # Disk
        disk = report['disk']
        output.append("Disk Usage:")
        for part in disk['partitions']:
            output.append(f"  {part['mountpoint']}: {part['used_gb']}GB / {part['total_gb']}GB ({part['percent_used']}%)")
        output.append("")
        
        # Network
        net = report['network']
        output.append(f"Network: Sent {net['bytes_sent_mb']}MB, Received {net['bytes_recv_mb']}MB")
        output.append(f"Active Connections: {net['active_connections']}\n")
        
        # Top Processes
        output.append("Top 10 Processes by CPU:")
        for i, proc in enumerate(report['top_processes'], 1):
            output.append(f"  {i}. {proc['name']} (PID {proc['pid']}): CPU {proc['cpu_percent']}%, MEM {proc['memory_percent']}%")
        
        return "\n".join(output)


async def monitor_system_health() -> str:
    """Async wrapper for system monitoring"""
    return SystemMonitor.format_report_for_llm()


async def get_cpu_status() -> Dict[str, Any]:
    """Get just CPU information"""
    return SystemMonitor.get_cpu_info()


async def get_memory_status() -> Dict[str, Any]:
    """Get just memory information"""
    return SystemMonitor.get_memory_info()


async def get_disk_status() -> Dict[str, Any]:
    """Get just disk information"""
    return SystemMonitor.get_disk_info()


async def check_system_alerts() -> Dict[str, Any]:
    """Check for system issues that need attention"""
    cpu = SystemMonitor.get_cpu_info()
    mem = SystemMonitor.get_memory_info()
    disk = SystemMonitor.get_disk_info()
    
    alerts = []
    
    # CPU alerts
    if cpu['usage_percent'] > 90:
        alerts.append({"level": "critical", "component": "CPU", "message": f"CPU usage at {cpu['usage_percent']}%"})
    elif cpu['usage_percent'] > 75:
        alerts.append({"level": "warning", "component": "CPU", "message": f"CPU usage at {cpu['usage_percent']}%"})
    
    # Memory alerts
    if mem['percent_used'] > 90:
        alerts.append({"level": "critical", "component": "Memory", "message": f"Memory usage at {mem['percent_used']}%"})
    elif mem['percent_used'] > 80:
        alerts.append({"level": "warning", "component": "Memory", "message": f"Memory usage at {mem['percent_used']}%"})
    
    # Disk alerts
    for part in disk['partitions']:
        if part['percent_used'] > 95:
            alerts.append({"level": "critical", "component": "Disk", "message": f"{part['mountpoint']} at {part['percent_used']}%"})
        elif part['percent_used'] > 85:
            alerts.append({"level": "warning", "component": "Disk", "message": f"{part['mountpoint']} at {part['percent_used']}%"})
    
    return {
        "alert_count": len(alerts),
        "alerts": alerts,
        "status": "critical" if any(a['level'] == 'critical' for a in alerts) else "warning" if alerts else "healthy"
    }
