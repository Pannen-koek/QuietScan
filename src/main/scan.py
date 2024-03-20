import subprocess
import unicodedata
import requests as re
import os 
import json
import winreg
import ttkbootstrap as tb


unique_apps = set()

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

def system_scan():
    global unique_apps
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
                # Use a tuple of (app_name, app_version) to maintain uniqueness
                unique_apps.add((app_name, app_version))
        except FileNotFoundError:
            continue

    # Convert set to list if you need to return or further manipulate the list of apps
    #unique_apps_list = list(unique_apps)
    #for app in unique_apps_list:
        #print(app)

def get_cve():
    global unique_apps
    base_url = "https://services.nvd.nist.gov/rest/json/cves/2.0/?keywordExactMatch&keywordSearch={}"
    
    for app, _ in unique_apps:
        formatted_app = sanitize_url(app)  # Sanitize app name
        api_url = base_url.format(formatted_app)  # Use sanitized app name in URL
        try:
            response = re.get(api_url)
            print(response.status_code)
            json_data = json.loads(response.text)
            vulndata = json_data.get('result', {}).get('CVE_Items', [])
            for item in vulndata:
                cve = item.get('cve', {})
                cve_id = cve.get('CVE_data_meta', {}).get('ID')
                description_data = cve.get('description', {}).get('description_data', [])
                descriptions = [desc.get('value') for desc in description_data if desc.get('lang') == 'en']
                if cve_id and descriptions:
                    print(f"CVE ID: {cve_id}")
                    print(f"Description: {descriptions[0]}")
                    print("-" * 50)
        except Exception as e:
            print(f"An error occurred while fetching CVEs for {app}: {e}")
system_scan()
get_cve()