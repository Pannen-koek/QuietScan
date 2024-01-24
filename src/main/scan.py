import subprocess
import requests
import ttkbootstrap as tb


# Function to search for CVEs for a given application and version
def search_cve(application_name, version):
    base_url = "https://services.nvd.nist.gov/rest/json/cves/1.0"
    cpe = f"cpe:2.3:a:{application_name}:{version}"

    params = {
        'resultsPerPage': '10',  # adjust as needed
        'cpeMatchString': cpe
    }

    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code}"


def system_scan(textbox): # TODO implement threading
    # Define the command to list installed programs using wmic
    scan = 'wmic product get name,version'

    # Run the command
    result = subprocess.run(scan, capture_output=True, text=True, shell=True)

    if result.returncode == 0:
        output = result.stdout
        # Process each line of the output
        for line in output.splitlines():
            textbox.insert(tb.END, f"{line}" + '\n')

            # parts = line.strip().split()
            # if len(parts) >= 2:
            # app_name = parts[0]
            # app_version = parts[1]
            # cve_results = search_cve(app_name, app_version)
            # textbox.insert(tb.END, f"{app_name} {app_version}" + '\n')
    # else:
    # textbox.insert(tb.END, "Error:", result.stderr + '\n')