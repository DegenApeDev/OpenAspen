#!/usr/bin/env python3
"""
Linux System Monitor powered by LM Studio
A practical example of using OpenAspen with local LLMs for system administration
"""
import asyncio
import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from openaspen.skills.system_monitor import (
    SystemMonitor,
    monitor_system_health,
    check_system_alerts,
)

# Set dummy OpenAI key for embeddings (not used in this example)
os.environ.setdefault("OPENAI_API_KEY", "sk-dummy-key")


class SystemHealthAnalyzer:
    """Uses LM Studio to analyze Linux system health"""
    
    def __init__(self, base_url: str = "http://localhost:1234/v1"):
        self.llm = ChatOpenAI(
            base_url=base_url,
            api_key="not-needed",
            model="local-model",
            temperature=0.3,  # Lower temperature for more focused analysis
        )
        
        self.system_prompt = """You are a Linux system administrator AI assistant.
Your job is to analyze system metrics and provide actionable insights.

When analyzing system health:
1. Identify any critical issues that need immediate attention
2. Suggest optimizations for performance
3. Warn about potential problems before they become critical
4. Be concise and practical - focus on actionable advice
5. Use clear severity levels: CRITICAL, WARNING, INFO

Keep responses focused and under 200 words unless detailed analysis is requested."""
    
    async def analyze_system(self, detailed: bool = False) -> str:
        """Analyze current system health using LLM"""
        
        # Get system report
        report = SystemMonitor.format_report_for_llm()
        
        # Get alerts
        alerts = await check_system_alerts()
        
        # Build prompt
        if detailed:
            prompt = f"""Analyze this Linux system and provide a detailed health assessment:

{report}

Current Alerts: {alerts['alert_count']} ({alerts['status']})
{chr(10).join([f"- [{a['level'].upper()}] {a['component']}: {a['message']}" for a in alerts['alerts']])}

Provide:
1. Overall health assessment
2. Critical issues (if any)
3. Performance optimization recommendations
4. Preventive maintenance suggestions"""
        else:
            prompt = f"""Quick system health check:

{report}

Alerts: {alerts['alert_count']} ({alerts['status']})

Provide a brief assessment (2-3 sentences) and any urgent actions needed."""
        
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=prompt)
        ]
        
        response = await self.llm.ainvoke(messages)
        return response.content
    
    async def diagnose_issue(self, issue_description: str) -> str:
        """Diagnose a specific system issue"""
        
        report = SystemMonitor.format_report_for_llm()
        
        prompt = f"""A user reports this issue: "{issue_description}"

Current system state:
{report}

Based on the system metrics, diagnose the likely cause and suggest solutions."""
        
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=prompt)
        ]
        
        response = await self.llm.ainvoke(messages)
        return response.content
    
    async def recommend_optimizations(self) -> str:
        """Get optimization recommendations"""
        
        cpu = SystemMonitor.get_cpu_info()
        mem = SystemMonitor.get_memory_info()
        disk = SystemMonitor.get_disk_info()
        processes = SystemMonitor.get_top_processes(limit=15)
        
        prompt = f"""Analyze these system metrics and recommend optimizations:

CPU Usage: {cpu['usage_percent']}%
Memory Usage: {mem['percent_used']}% ({mem['used_gb']}GB / {mem['total_gb']}GB)
Swap Usage: {mem['swap_percent']}%

Top Processes:
{chr(10).join([f"- {p['name']}: CPU {p['cpu_percent']}%, MEM {p['memory_percent']}%" for p in processes[:10]])}

Disk Usage:
{chr(10).join([f"- {p['mountpoint']}: {p['percent_used']}%" for p in disk['partitions']])}

Suggest specific optimizations to improve performance."""
        
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=prompt)
        ]
        
        response = await self.llm.ainvoke(messages)
        return response.content


async def main():
    print("=" * 70)
    print("  🐧 Linux System Monitor - Powered by LM Studio")
    print("=" * 70)
    print()
    
    # Check LM Studio connection
    print("🔍 Checking LM Studio connection...")
    try:
        analyzer = SystemHealthAnalyzer()
        print("✅ Connected to LM Studio at http://localhost:1234/v1\n")
    except Exception as e:
        print(f"❌ Failed to connect to LM Studio: {e}")
        print("\n💡 Make sure:")
        print("  1. LM Studio is running")
        print("  2. Local Server is started")
        print("  3. A model is loaded")
        return
    
    # Show raw metrics
    print("📊 Current System Metrics:")
    print("-" * 70)
    report = SystemMonitor.format_report_for_llm()
    print(report)
    print()
    
    # Check for alerts
    print("🚨 System Alerts:")
    print("-" * 70)
    alerts = await check_system_alerts()
    if alerts['alerts']:
        for alert in alerts['alerts']:
            emoji = "🔴" if alert['level'] == 'critical' else "⚠️"
            print(f"{emoji} [{alert['level'].upper()}] {alert['component']}: {alert['message']}")
    else:
        print("✅ No alerts - system is healthy")
    print()
    
    # AI Analysis
    print("🤖 AI Analysis (powered by your local LLM):")
    print("-" * 70)
    try:
        analysis = await analyzer.analyze_system(detailed=True)
        print(analysis)
        print()
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        print("Note: This requires LM Studio to be running with a model loaded")
        return
    
    # Optimization recommendations
    print("\n💡 Optimization Recommendations:")
    print("-" * 70)
    try:
        recommendations = await analyzer.recommend_optimizations()
        print(recommendations)
        print()
    except Exception as e:
        print(f"❌ Failed to get recommendations: {e}")
    
    # Interactive mode
    print("\n" + "=" * 70)
    print("✅ System monitoring complete!")
    print("\n💡 You can also use this for:")
    print("  - Continuous monitoring (run in a loop)")
    print("  - Alert notifications (integrate with your notification system)")
    print("  - Automated diagnostics (call diagnose_issue() with symptoms)")
    print("  - Performance trending (log metrics over time)")


async def demo_continuous_monitoring():
    """Demo: Continuous monitoring with periodic checks"""
    analyzer = SystemHealthAnalyzer()
    
    print("🔄 Starting continuous monitoring (Ctrl+C to stop)...\n")
    
    try:
        while True:
            print(f"\n⏰ Check at {SystemMonitor.get_system_info()['boot_time']}")
            print("-" * 50)
            
            # Quick health check
            analysis = await analyzer.analyze_system(detailed=False)
            print(analysis)
            
            # Check alerts
            alerts = await check_system_alerts()
            if alerts['alerts']:
                print(f"\n🚨 {alerts['alert_count']} active alerts!")
                for alert in alerts['alerts']:
                    print(f"  - [{alert['level']}] {alert['message']}")
            
            # Wait 30 seconds
            await asyncio.sleep(30)
            
    except KeyboardInterrupt:
        print("\n\n✅ Monitoring stopped")


if __name__ == "__main__":
    print()
    
    # Check if psutil is installed
    try:
        import psutil
    except ImportError:
        print("❌ Error: psutil is not installed")
        print("Install it with: pip install psutil")
        exit(1)
    
    # Run main demo
    asyncio.run(main())
    
    # Uncomment to run continuous monitoring instead:
    # asyncio.run(demo_continuous_monitoring())
