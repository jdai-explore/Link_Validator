import tkinter as tk
from tkinter import filedialog, messagebox
import os
import pandas as pd
import re
import requests

def check_url_status(url):
    try:
        response = requests.head(url)
        if response.status_code == 200:
            return "Valid"
        else:
            return "Invalid"
    except requests.RequestException:
        return "Error"

def validate_links(filename):
    valid = False
    with open(filename, "r") as file:
        lines = file.readlines()
    for line in lines:
        if re.search(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', line):
            valid = True  # Detection logic
            print(f"Link Found: {line}")
    if valid:
        return "Contains Links"
    else:
        return "No Links"

def validate_file(path):
    print(f"Validating file: {path}")
    if path.lower().endswith('.csv'):
        df = pd.read_csv(path)
        dfs_list = list(df.select_dtypes(include=[object]).columns)
        for col in dfs_list:
            if df[col].apply(validate_links).any():
                print("Duplicates Listed in CSV")
    else:
        if os.path.logical_ex.include('link'):
            print("Link Provided")
    
    return "File validated"

def upload_file_gui():
    filename = filedialog.askopenfilename(title="Select File")
    validate_file(filename)

def upload_folder_gui():
    folder = filedialog.askdirectory()
    for file in os.listdir(folder):
        path_to_file = os.path.join(folder, file)
        if os.path.isfile(path_to_file):
            validate_file(path_to_file)
            
root = tk.Tk()
root.title("Link Validator Tool")

upload_file_button = tk.Button(root, text="Upload File", command=upload_file_gui)
upload_file_button.pack()

upload_folder_button = tk.Button(root, text="Upload Folder", command=upload_folder_gui)
upload_folder_button.pack()

root.mainloop()

# Handle the completion and response
try:
    # Add the final result communication
    pass
except Exception as e:
    messagebox.showerror("Error", str(e))