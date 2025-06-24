import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import pandas as pd
import re
from openpyxl import load_workbook

def check_contents(file_path, output_text):
    valid_count = 0
    invalid_count = 0
    pattern = re.compile(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")
    invalid_links = []

    try:
        if file_path.endswith(('.csv', '.txt', '.xml', '.html')):
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
                for column in df.columns:
                    for index, value in df[column].iteritems():
                        if pattern.match(str(value)):
                            valid_count += 1
                        else:
                            invalid_count += 1
                            invalid_links.append(f"Invalid link in {column} at row {index + 1}: {value}")
            else:
                with open(file_path, 'r', encoding='utf-8') as fd:
                    for line_num, line in enumerate(fd, 1):
                        if pattern.match(line.strip()):
                            valid_count += 1
                        else:
                            invalid_count += 1
                            invalid_links.append(f"Invalid link at line {line_num}: {line.strip()}")

        elif file_path.endswith(('.xls', '.xlsx', '.xlsm', '.xlsb')):
            wb = load_workbook(filename=file_path, read_only=True, data_only=True)
            for sheet in wb.worksheets:
                for row in sheet.iter_rows():
                    for cell in row:
                        if pattern.match(str(cell.value)):
                            valid_count += 1
                        else:
                            invalid_count += 1
                            invalid_links.append(f"Invalid link in {sheet.title} at cell {cell.coordinate}: {cell.value}")

        output_text.insert(tk.END, f"Total valid links: {valid_count}\n")
        output_text.insert(tk.END, f"Total invalid links: {invalid_count}\n")
        if invalid_links:
            output_text.insert(tk.END, "Invalid links found:\n")
            for link in invalid_links:
                output_text.insert(tk.END, f"{link}\n")
        else:
            output_text.insert(tk.END, "No invalid links found.\n")
    except Exception as e:
        output_text.insert(tk.END, f"Error processing file: {e}\n")

def upload_file_gui(output_text):
    file_path = filedialog.askopenfilename(filetypes=[("All Files", "*.*")])
    if file_path:
        output_text.delete(1.0, tk.END)
        check_contents(file_path, output_text)
    else:
        messagebox.showwarning("No file selected", "Please select a file to validate.")

root = tk.Tk()
root.title("Link Validator")
root.geometry("600x400")

upload_file_btn = tk.Button(root, text="Upload File", command=lambda: upload_file_gui(output_text))
upload_file_btn.pack(pady=10)

output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=20)
output_text.pack(pady=10)

root.mainloop()