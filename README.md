Pre-requisite:

yum install python3
pip3 install datadog


Create a bash script on each Itential IAP server that datadog will trigger. 

/etc/datadog-agent/checks.d/selfheal.sh


#!/bin/bash
sudo systemctl restart automation-platform.service




In the datadog directory make a trigger 
/etc/datadog-agent/conf.d/selfheal.d/selfheal.yml

init_config:
instances:
  - name: "Self Heal Trigger"
    command: "/etc/datadog-agent/checks.d/selfheal.sh"





Login to Datadog and create both an API Key and APPLICATION KEY
https://app.datadoghq.com/organization-settings/api-keys
https://app.datadoghq.com/organization-settings/application-keys




Setup crontab to check every 5 minutes

crontab -e

*/5 * * * * python3 /etc/datadog-agent/selfheal.py

Contents of /etc/datadog-agent/selfheal.py

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
