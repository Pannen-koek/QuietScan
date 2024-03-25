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

from tkinter import Scrollbar

api_key = os.getenv("API_Key_NQS")
unique_apps = set()
executing = False
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


def display_scan_history(frame, widget):
    # List all files in the scan_history folder
    scan_history_folder = os.path.join(CURRENT_DIR, "scan_history")
    if not os.path.exists(scan_history_folder):
        return []

    # Create buttons for each scan file
    scan_files = os.listdir(scan_history_folder)
    scan_buttons = []
    for filename in scan_files:
        formatted_filename = filename.replace(".txt", "")
        button = tb.Button(frame, text=formatted_filename,
                                         command=lambda file=filename: show_scan_result(file), width=50)

        widget.window_create(tb.END, window=button)
        widget.insert(tb.END, "\n\n")  # Add spacing between buttons

    return scan_buttons


def show_scan_result(filename):
    scan_history_folder = os.path.join(CURRENT_DIR, "scan_history")
    file_path = os.path.join(scan_history_folder, filename)
    with open(file_path, "r") as file:
        content = file.read()

    result_window = tb.Toplevel()
    result_window.title("Scan Result")

    text_widget = tb.Text(result_window, wrap=tb.WORD, width=160, height=40)
    scrollbar = Scrollbar(result_window, command=text_widget.yview)
    text_widget.config(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tb.RIGHT, fill=tb.Y)
    text_widget.pack(side=tb.LEFT, fill=tb.BOTH, expand=True)

    text_widget.insert(tb.END, content)
    text_widget.config(state=tb.DISABLED)


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


def new_scan(textbox, frame, widget, step1_checkbox, step2_checkbox):
    global executing
    if not executing:
        textbox.config(state=tb.NORMAL)
        textbox.delete("1.0", tb.END)
        enter_heading_text(textbox, "Starting new QuietScan")
        # time.sleep(2)
        scanThread = threading.Thread(target=scan, args=(textbox, frame, widget, step1_checkbox, step2_checkbox))
        scanThread.start()
        textbox.config(state=tb.DISABLED)


def scan(textbox, frame, widget, step1_checkbox, step2_checkbox):
    collect_unique_apps(textbox, step1_checkbox)
    get_cve(textbox, frame, widget, step2_checkbox)


def collect_unique_apps(textbox, checkbox):
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
    checkbox.invoke()

def get_cve(textbox, frame, widget, checkbox):
    global unique_apps
    global executing

    enter_heading_text(textbox, "Querying NIST Database for vulnerabilities")

    base_url = "https://services.nvd.nist.gov/rest/json/cves/2.0/?keywordExactMatch&keywordSearch="
    for app, _ in unique_apps:
        enter_text(textbox, f"\nSearching {app} for known vulnerabilities")
        formatted_app = sanitize_url(app)
        api_url = base_url + formatted_app
        try:
            response = re.get(api_url, headers={"apiKey":api_key})
            time.sleep(1)
            #enter_text(textbox, f"Response code: {response.status_code}")
            json_data = json.loads(response.text)
            total_results = json_data.get('totalResults')

            if total_results == 0:
                enter_text(textbox, f"Found no CVEs for {app}")
                continue
            else:
                vulndata = json_data.get('vulnerabilities', [])
                for item in vulndata:
                    cve = item.get('cve', {})
                    cveId = cve.get('id')
                    try:
                        cveYear = int(cveId.split("-")[1] if cveId else 0)
                    except ValueError:
                        continue
                    if cveYear < 2020:
                        continue
                    descriptions = [desc.get('value') for desc in cve.get('descriptions') if desc.get('lang') == 'en']
                    metrics = item.get('metrics', {}).get('cvssMetricV2', {})
                    baseSeverity = metrics.get('baseSeverity')
                    exploitabilityScore = metrics.get('exploitabilityScore')
                    impactScore = metrics.get('impactScore')
                    if cveId and descriptions:
                        enter_text(textbox, f"CVE Query for {cveId}")
                        enter_text(textbox, f"CVE ID: {cveId}")
                        enter_text(textbox, f"Description: {descriptions[0]}")
                        enter_text(textbox, f"Exploitability Score: {exploitabilityScore}")
                        enter_text(textbox, f"Impact Score: {impactScore}")
                        enter_text(textbox, "-" * 50)
        except Exception as e:
            enter_text(textbox, f"Found no CVEs for {app}: {e}")
    enter_heading_text(textbox, "Completed querying NIST Database for vulnerabilities")
    checkbox.invoke()
    save_scan_result_to_file(textbox.get("1.0", tb.END))
    # display_scan_history(frame, widget)
    executing = False
