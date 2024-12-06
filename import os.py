import os
import json
import string
import secrets
from tkinter import *
from tkinter import messagebox
from cryptography.fernet import Fernet

# File paths
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


# Function to save data securely
def save_data(data):
    encrypted_data = cipher.encrypt(json.dumps(data).encode())
    with open(DATA_FILE, "wb") as file:
        file.write(encrypted_data)


# Function to load data securely
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
    if not platform or not username or not password:
        messagebox.showwarning("Missing Information", "All fields are required!")
        return
    data = load_data()
    data[platform] = {"username": username, "password": password}
    save_data(data)
    messagebox.showinfo("Success", f"Password for {platform} saved successfully!")


# Function to retrieve a password
def retrieve_password(platform):
    data = load_data()
    if platform in data:
        username = data[platform]["username"]
        password = data[platform]["password"]
        messagebox.showinfo("Password Retrieved", f"Platform: {platform}\nUsername: {username}\nPassword: {password}")
    else:
        messagebox.showwarning("Not Found", f"No password found for platform: {platform}")


# GUI Application
def main():
    # Create main window
    root = Tk()
    root.title("Password Locker")
    root.geometry("400x500")
    root.resizable(False, False)

    # Title Label
    Label(root, text="Password Locker", font=("Arial", 16, "bold")).pack(pady=10)

    # Store Password Frame
    store_frame = Frame(root)
    store_frame.pack(pady=10, fill=X, padx=20)

    Label(store_frame, text="Platform:").grid(row=0, column=0, sticky=W, pady=5)
    platform_entry = Entry(store_frame, width=30)
    platform_entry.grid(row=0, column=1, pady=5)

    Label(store_frame, text="Username:").grid(row=1, column=0, sticky=W, pady=5)
    username_entry = Entry(store_frame, width=30)
    username_entry.grid(row=1, column=1, pady=5)

    Label(store_frame, text="Password:").grid(row=2, column=0, sticky=W, pady=5)
    password_entry = Entry(store_frame, width=30)
    password_entry.grid(row=2, column=1, pady=5)

    def save_password():
        platform = platform_entry.get().strip()
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        if not password:
            password = generate_password()
            password_entry.insert(0, password)
            messagebox.showinfo("Generated Password", f"Generated password: {password}")
        store_password(platform, username, password)

    Button(store_frame, text="Save Password", command=save_password).grid(row=3, column=1, pady=10, sticky=E)

    # Retrieve Password Frame
    retrieve_frame = Frame(root)
    retrieve_frame.pack(pady=20, fill=X, padx=20)

    Label(retrieve_frame, text="Platform to Retrieve:").grid(row=0, column=0, sticky=W, pady=5)
    retrieve_entry = Entry(retrieve_frame, width=30)
    retrieve_entry.grid(row=0, column=1, pady=5)

    def retrieve():
        platform = retrieve_entry.get().strip()
        retrieve_password(platform)

    Button(retrieve_frame, text="Retrieve Password", command=retrieve).grid(row=1, column=1, pady=10, sticky=E)

    # Password Generation Frame
    gen_frame = Frame(root)
    gen_frame.pack(pady=20, fill=X, padx=20)

    Label(gen_frame, text="Password Length:").grid(row=0, column=0, sticky=W, pady=5)
    length_entry = Entry(gen_frame, width=5)
    length_entry.grid(row=0, column=1, sticky=W, pady=5)

    include_special = BooleanVar(value=True)
    Checkbutton(gen_frame, text="Include Special Characters", variable=include_special).grid(row=1, column=0, columnspan=2, sticky=W)

    def generate():
        length = int(length_entry.get() or 12)
        include = include_special.get()
        password = generate_password(length, include)
        messagebox.showinfo("Generated Password", f"Generated password: {password}")

    Button(gen_frame, text="Generate Password", command=generate).grid(row=2, column=1, pady=10, sticky=E)

    # Run the main loop
    root.mainloop()


if __name__ == "__main__":
    main()
