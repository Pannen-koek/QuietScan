import subprocess
import threading
import time

import unicodedata
import requests as re
import os
import json
import winreg
import ttkbootstrap as tb
import os
import datetime

api_key = os.getenv("API_Key_NQS")
unique_apps = set()
executing = False

# Save scan result into a .txt file
def save_scan_result_to_file(output):
    # Create a directory named "scan_history" if it doesn't exist
    if not os.path.exists("scan_history"):
        os.makedirs("scan_history")

    # Generate a unique filename based on the current date and time
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d  %H.%M.%S")
    filename = f"{timestamp} -- System Scan.txt"

    # Write the scan result to the file
    with open(os.path.join("scan_history", filename), "w") as file:
        file.write(output)


def remove_x64_suffix(app_name):
    x64_suffixes = [" (x64)", " (64-bit)", " x64", " 64-bit", " (64-bit symbols)", " (x64 en-US)"]
    for suffix in x64_suffixes:
        app_name = app_name.replace(suffix, "")
    return app_name


def sanitize_url(url):
    chars_to_remove = ["(", ")", "'", ","]
    for char in chars_to_remove:
        url = url.replace(char, "")
    url = url.replace(" ", "%20")
    return url


def enter_heading_text(textbox, text):
    textbox.config(state=tb.NORMAL)
    textbox.insert(tb.END, "\n" + "-" * 180 + "\n" + text + "\n" + "-" * 180 + "\n\n")
    textbox.see(tb.END)
    textbox.config(state=tb.DISABLED)
    time.sleep(2)


def enter_text(textbox, text):
    textbox.config(state=tb.NORMAL)
    textbox.insert(tb.END, text + "\n")
    textbox.see(tb.END)
    textbox.config(state=tb.DISABLED)


def new_scan(textbox):
    global executing
    if not executing:
        textbox.config(state=tb.NORMAL)
        textbox.delete("1.0", tb.END)
        enter_heading_text(textbox, "Starting new QuietScan")
        time.sleep(2)
        scanThread = threading.Thread(target=scan, args=(textbox,))
        scanThread.start()
        textbox.config(state=tb.DISABLED)


def scan(textbox):
    collect_unique_apps(textbox)
    get_cve(textbox)


def collect_unique_apps(textbox):
    global unique_apps
    global executing
    executing = True

    enter_heading_text(textbox, "Collecting unique applications on your machine")

    uninstall_regkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Uninstall")

    for i in range(0, winreg.QueryInfoKey(uninstall_regkey)[0]):
        try:
            subkey_name = winreg.EnumKey(uninstall_regkey, i)
            subkey_path = fr"Software\Microsoft\Windows\CurrentVersion\Uninstall\{subkey_name}"
            subkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, subkey_path)
            app_name, _ = winreg.QueryValueEx(subkey, "DisplayName")
            app_version, _ = winreg.QueryValueEx(subkey, "DisplayVersion")
            if app_name and app_version:
                app_name = remove_x64_suffix(app_name)
                if app_version in app_name:
                    app_name = app_name.replace(app_version, "").strip()
                unique_apps.add((app_name, app_version))
                enter_text(textbox, f"{app_name}: {app_version}")
        except FileNotFoundError:
            continue

    enter_heading_text(textbox, "Completed collecting unique applications on your machine")

def get_cve(textbox):
    global unique_apps
    global executing

    enter_heading_text(textbox, "Querying NIST Database for vulnerabilities")

    base_url = "https://services.nvd.nist.gov/rest/json/cves/2.0/?keywordExactMatch&keywordSearch="
    for app, _ in unique_apps:
        enter_text(textbox, f"Searching {app} for known vulnerabilities")
        formatted_app = sanitize_url(app)
        api_url = base_url + formatted_app
        try:
            response = re.get(api_url, headers={"apiKey":api_key})
            time.sleep(3)
            #enter_text(textbox, f"Response code: {response.status_code}")
            enter_text(textbox, f"Raw response for {app}:\n{response.text}")
            json_data = json.loads(response.text)
            vulndata = json_data.get('result', {}).get('CVE_Items', [])
            for item in vulndata:
                cve = item.get('cve', {})
                cve_id = cve.get('CVE_data_meta', {}).get('ID')
                description_data = cve.get('description', {}).get('description_data', [])
                descriptions = [desc.get('value') for desc in description_data if desc.get('lang') == 'en']
                if cve_id and descriptions:
                    enter_text(textbox, f"CVE Query for {cve_id}")
                    enter_text(textbox, f"CVE ID: {cve_id}")
                    enter_text(textbox, f"Description: {descriptions[0]}")
                    enter_text(textbox, "-" * 50)
        except Exception as e:
            enter_text(textbox, f"Found no CVEs for {app}: {e}")
    enter_heading_text(textbox, "Completed querying NIST Database for vulnerabilities")
    executing = False
