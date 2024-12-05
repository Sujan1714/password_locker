import os
import json
import string
import secrets
from cryptography.fernet import Fernet

# File paths for storage
DATA_FILE = "passwords.json"
KEY_FILE = "key.key"


# Function to generate or load encryption key
def load_or_generate_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as file:
            file.write(key)
    else:
        with open(KEY_FILE, "rb") as file:
            key = file.read()
    return key


# Initialize encryption key
key = load_or_generate_key()
cipher = Fernet(key)


# Function to save data securely to a JSON file
def save_data(data):
    encrypted_data = cipher.encrypt(json.dumps(data).encode())
    with open(DATA_FILE, "wb") as file:
        file.write(encrypted_data)


# Function to load data securely from a JSON file
def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "rb") as file:
        encrypted_data = file.read()
    return json.loads(cipher.decrypt(encrypted_data).decode())


# Function to generate a strong password
def generate_password(length=12, include_special=True):
    characters = string.ascii_letters + string.digits
    if include_special:
        characters += string.punctuation
    return ''.join(secrets.choice(characters) for _ in range(length))


# Function to store a password
def store_password(platform, username, password):
    data = load_data()
    data[platform] = {"username": username, "password": password}
    save_data(data)
    print(f"Password for {platform} saved successfully!")


# Function to retrieve a password
def retrieve_password(platform):
    data = load_data()
    if platform in data:
        print(f"Platform: {platform}")
        print(f"Username: {data[platform]['username']}")
        print(f"Password: {data[platform]['password']}")
    else:
        print(f"No password found for platform: {platform}")


# Function to display all stored platforms
def list_platforms():
    data = load_data()
    if data:
        print("Stored platforms:")
        for platform in data:
            print(f"- {platform}")
    else:
        print("No passwords stored yet!")


# Main menu for the CLI application
def main():
    while True:
        print("\nPassword Locker")
        print("1. Store a new password")
        print("2. Retrieve a password")
        print("3. Generate a strong password")
        print("4. List all stored platforms")
        print("5. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            platform = input("Enter platform name: ").strip()
            username = input("Enter username: ").strip()
            password = input("Enter password (leave blank to auto-generate): ").strip()
            if not password:
                password = generate_password()
                print(f"Generated password: {password}")
            store_password(platform, username, password)

        elif choice == "2":
            platform = input("Enter platform name: ").strip()
            retrieve_password(platform)

        elif choice == "3":
            length = int(input("Enter desired password length (default 12): ") or 12)
            include_special = input("Include special characters? (yes/no): ").strip().lower() == "yes"
            password = generate_password(length, include_special)
            print(f"Generated password: {password}")

        elif choice == "4":
            list_platforms()

        elif choice == "5":
            print("Exiting Password Locker. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again!")


# Run the application
if __name__ == "__main__":
    main()
