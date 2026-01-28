#!/usr/bin/env python3
"""Quick test to see system metrics"""
import asyncio
from openaspen.skills.system_monitor import SystemMonitor, check_system_alerts

async def main():
    print("=" * 70)
    print("  System Metrics Test")
    print("=" * 70)
    print()
    
    # Get formatted report
    report = SystemMonitor.format_report_for_llm()
    print(report)
    print()
    
    # Check alerts
    print("\n" + "=" * 70)
    print("  System Alerts")
    print("=" * 70)
    alerts = await check_system_alerts()
    print(f"Status: {alerts['status'].upper()}")
    print(f"Alert Count: {alerts['alert_count']}")
    
    if alerts['alerts']:
        print("\nActive Alerts:")
        for alert in alerts['alerts']:
            print(f"  [{alert['level'].upper()}] {alert['component']}: {alert['message']}")
    else:
        print("\n✅ No alerts - system is healthy!")

if __name__ == "__main__":
    asyncio.run(main())
