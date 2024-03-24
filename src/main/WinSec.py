import subprocess

def run_powershell_command(command):
    try:
        subprocess.run(["powershell", "-Command", command], check=True)
        print("Command executed successfully.")
    except subprocess.CalledProcessError:
        print("An error occurred while executing the command.")

def activate_rule(rule_id):
    if rule_id == 1:
        run_powershell_command("Add-MpPreference -AttackSurfaceReductionRules_Ids BE9BA2D9-53EA-4CDC-84E5-9B1EEEE46550 -AttackSurfaceReductionRules_Actions Enabled")
    elif rule_id == 2:
        run_powershell_command("Add-MpPreference -AttackSurfaceReductionRules_Ids 5BEB7EFE-FD9A-4556-801D-275E5FFC04CC -AttackSurfaceReductionRules_Actions Enabled")
    elif rule_id == 3:
        run_powershell_command("Add-MpPreference -AttackSurfaceReductionRules_Ids b2b3f03d-6a65-4f7b-a9c7-1c7ef74a9ba4 -AttackSurfaceReductionRules_Actions Enabled")
    elif rule_id == 4:
        run_powershell_command("Add-MpPreference -AttackSurfaceReductionRules_Ids 92E97FA1-2EDF-4476-BDD6-9DD0B4DDDC7B -AttackSurfaceReductionRules_Actions Enabled")

def display_menu():
    print("Select the rule to activate:")
    print("1 - Block executable content from email and webmail")
    print("2 - Block execution of potentially obfuscated scripts")
    print("3 - Block untrusted and unsigned processes that run from USB")
    print("4 - Block Win32 API calls in macros")

def main():
    display_menu()
    rule_choice = input("Enter your choice (1/2/3/4): ")

    if rule_choice in ['1', '2', '3', '4']:
        activate_rule(int(rule_choice))
        print("Rule activated successfully.")
    else:
        print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()