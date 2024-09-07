import datadog
import subprocess
import time# Initialize Datadog API
datadog.initialize(api_key='XXX', app_key='XXX')
 
MONITOR_ID = XXX  # Replace with your monitor ID
CHECK_INTERVAL = 300  # Check every 5 minutes (300 seconds)
 
def get_monitor_status():
    try:
        # Get the current monitor status
        monitor = datadog.api.Monitor.get(MONITOR_ID)
        return monitor['overall_state']
    except Exception as e:
        print(f"Error fetching monitor status: {e}")
        return Nonedef run_self_heal_script():
    try:
        # Trigger self-heal.sh script
        subprocess.run(['/etc/datadog-agent/checks.d/selfheal.sh'], check=True)
        print("Self-heal script executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to run self-heal script: {e}")if __name__ == "__main__":
    while True:
        monitor_status = get_monitor_status()
        if monitor_status == "Warn":
            print("Monitor is in alert state. Triggering self-heal script...")
            run_self_heal_script()
        else:
            print(f"Monitor status: {monitor_status}. No action needed.")        time.sleep(CHECK_INTERVAL)  # Wait for the next poll
