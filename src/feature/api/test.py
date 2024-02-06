import subprocess
import requests


def system_scan():
    scan = 'wmic product get name,version'
    
    result = subprocess.run(scan, capture_output=True, text=True, shell=True)
    
    if result.returncode == 0:
        output = result.stdout
        for line in output.splitlines():
            parts = line.strip().split()
            if len(parts) >= 2:
                app_name = parts[0]
                app_version = parts[1]
               # cve_results = search_cve(app_name, app_version)
                print(f"{app_name} {app_version}")
                
system_scan()