import os
import subprocess
import sys

def is_root():
    return os.geteuid() == 0

def run_command(cmd):
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"[!] Command failed: {cmd}")
    else:
        print("[+] Command executed successfully.")

def input_prompt(prompt):
    try:
        return input(prompt).strip()
    except KeyboardInterrupt:
        print("\n[!] Cancelled.")
        return None

def list_users():
    print("\n--- Users ---")
    with open("/etc/passwd") as f:
        for line in f:
            parts = line.split(":")
            uid = int(parts[2])
            if uid >= 1000 and uid < 65534:
                print(parts[0])
    print()

def menu():
    options = [
        "Exit",
        "Add User",
        "Modify User",
        "List Users",
        "Add Group",
        "Modify Group",
        "Add User to Group",
        "Delete Group",
        "Change User Password",
        "Enable User Account",
        "Disable User Account",
        "Delete User Account (with files)",
        "Delete User Account (keep files)",
    ]

    for i, opt in enumerate(options):
        print(f"{i}) {opt}")
    
    choice = input_prompt("Choose an option: ")
    return choice

def main():
    if not is_root():
        print("[!] This script must be run as root.")
        sys.exit(1)

    while True:
        choice = menu()
        if not choice:
            continue

        if choice == "0":
            print("Goodbye.")
            break

        elif choice == "1":
            username = input_prompt("Enter new username: ")
            if username:
                run_command(f"useradd {username}")

        elif choice == "2":
            old = input_prompt("Enter username to modify: ")
            new = input_prompt("Enter new username: ")
            if old and new:
                run_command(f"usermod -l {new} {old}")

        elif choice == "3":
            list_users()

        elif choice == "4":
            group = input_prompt("Enter new group name: ")
            if group:
                run_command(f"groupadd {group}")

        elif choice == "5":
            old = input_prompt("Enter group to modify: ")
            new = input_prompt("Enter new group name: ")
            if old and new:
                run_command(f"groupmod -n {new} {old}")

        elif choice == "6":
            user = input_prompt("Enter username: ")
            group = input_prompt("Enter group to add to: ")
            if user and group:
                run_command(f"usermod -aG {group} {user}")

        elif choice == "7":
            group = input_prompt("Enter group to delete: ")
            if group:
                run_command(f"groupdel {group}")

        elif choice == "8":
            user = input_prompt("Enter username to change password: ")
            if user:
                run_command(f"passwd {user}")

        elif choice == "9":
            user = input_prompt("Enter username to enable: ")
            if user:
                run_command(f"usermod -U {user}")

        elif choice == "10":
            user = input_prompt("Enter username to disable: ")
            if user:
                run_command(f"usermod -L {user}")

        elif choice == "11":
            user = input_prompt("Enter username to delete (with files): ")
            if user:
                run_command(f"userdel -r {user}")

        elif choice == "12":
            user = input_prompt("Enter username to delete (keep files): ")
            if user:
                run_command(f"userdel {user}")

        else:
            print("[!] Invalid option. Try again.")


if __name__ == "__main__":
    main()
