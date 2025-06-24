import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import pandas as pd
from urllib.parse import urlparse
from openpyxl import load_workbook
from bs4 import BeautifulSoup
import threading
import csv
import os
from datetime import datetime

class LinkValidator:
    """Handles URL validation and file processing logic"""
    
    @staticmethod
    def is_valid_url(url):
        """Validate a URL using urllib.parse for more accurate checking"""
        try:
            result = urlparse(str(url).strip())
            return all([result.scheme in ('http', 'https'), 
                       result.netloc,
                       len(result.netloc.split('.')) > 1])
        except:
            return False

    @staticmethod
    def process_csv(file_path, progress_callback=None):
        """Process CSV files with progress reporting"""
        results = {'valid': 0, 'invalid': 0, 'invalid_links': []}
        try:
            df = pd.read_csv(file_path)
            total = len(df) * len(df.columns)
            processed = 0
            
            for column in df.columns:
                for index, value in df[column].items():
                    if pd.notna(value):
                        if LinkValidator.is_valid_url(value):
                            results['valid'] += 1
                        else:
                            results['invalid'] += 1
                            results['invalid_links'].append(
                                f"Invalid link in column '{column}', row {index + 2}: {value}"
                            )
                    processed += 1
                    if progress_callback and processed % 100 == 0:
                        progress_callback(processed/total)
        
        except Exception as e:
            raise Exception(f"CSV processing error: {str(e)}")
        return results

    @staticmethod
    def process_excel(file_path, progress_callback=None):
        """Process Excel files with progress reporting"""
        results = {'valid': 0, 'invalid': 0, 'invalid_links': []}
        try:
            wb = load_workbook(filename=file_path, read_only=True, data_only=True)
            sheets = wb.sheetnames
            total = sum(ws.max_row * ws.max_column for ws in wb.worksheets)
            processed = 0
            
            for sheet_name in sheets:
                ws = wb[sheet_name]
                for row in ws.iter_rows():
                    for cell in row:
                        if cell.value and str(cell.value).strip():
                            if LinkValidator.is_valid_url(cell.value):
                                results['valid'] += 1
                            else:
                                results['invalid'] += 1
                                results['invalid_links'].append(
                                    f"Invalid link in sheet '{sheet_name}', cell {cell.coordinate}: {cell.value}"
                                )
                        processed += 1
                        if progress_callback and processed % 100 == 0:
                            progress_callback(processed/total)
        
        except Exception as e:
            raise Exception(f"Excel processing error: {str(e)}")
        return results

    @staticmethod
    def process_text(file_path, progress_callback=None):
        """Process plain text files line by line"""
        results = {'valid': 0, 'invalid': 0, 'invalid_links': []}
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                total = len(lines)
                
                for i, line in enumerate(lines):
                    line = line.strip()
                    if line:
                        if LinkValidator.is_valid_url(line):
                            results['valid'] += 1
                        else:
                            results['invalid'] += 1
                            results['invalid_links'].append(
                                f"Invalid link at line {i + 1}: {line}"
                            )
                    if progress_callback and i % 100 == 0:
                        progress_callback(i/total)
        
        except Exception as e:
            raise Exception(f"Text file processing error: {str(e)}")
        return results

    @staticmethod
    def process_html(file_path, progress_callback=None):
        """Process HTML files extracting URLs from href and src attributes"""
        results = {'valid': 0, 'invalid': 0, 'invalid_links': []}
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')
                elements = soup.find_all(['a', 'img', 'link', 'script'])
                total = len(elements)
                
                for i, element in enumerate(elements):
                    url = element.get('href') or element.get('src')
                    if url:
                        if LinkValidator.is_valid_url(url):
                            results['valid'] += 1
                        else:
                            results['invalid'] += 1
                            results['invalid_links'].append(
                                f"Invalid link in element {element.name}: {url}"
                            )
                    if progress_callback and i % 100 == 0:
                        progress_callback(i/total)
        
        except Exception as e:
            raise Exception(f"HTML processing error: {str(e)}")
        return results


class LinkValidatorApp:
    """Main application GUI"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Link Validator")
        self.root.geometry("800x600")
        self.results = None
        self.create_widgets()
        self.center_window()

    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def create_widgets(self):
        """Create all GUI widgets"""
        # Main frame
        main_frame = tk.Frame(self.root, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_frame = tk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(header_frame, text="Link Validator", font=('Arial', 16, 'bold')).pack(side=tk.LEFT)
        
        # Button frame
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        self.upload_btn = tk.Button(
            button_frame, 
            text="Upload File", 
            command=self.start_file_processing,
            width=15
        )
        self.upload_btn.pack(side=tk.LEFT, padx=5)
        
        self.export_btn = tk.Button(
            button_frame, 
            text="Export Results", 
            command=self.export_results,
            state=tk.DISABLED,
            width=15
        )
        self.export_btn.pack(side=tk.LEFT, padx=5)
        
        # Progress bar
        self.progress = ttk.Progressbar(
            main_frame, 
            orient=tk.HORIZONTAL, 
            length=100, 
            mode='determinate'
        )
        self.progress.pack(fill=tk.X, pady=5)
        self.progress_label = tk.Label(main_frame, text="")
        self.progress_label.pack()
        
        # Results display
        self.output_text = scrolledtext.ScrolledText(
            main_frame, 
            wrap=tk.WORD, 
            width=90, 
            height=25,
            font=('Consolas', 10)
        )
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_bar = tk.Label(
            main_frame, 
            text="Ready", 
            bd=1, 
            relief=tk.SUNKEN, 
            anchor=tk.W
        )
        self.status_bar.pack(fill=tk.X, pady=(5, 0))

    def start_file_processing(self):
        """Start file processing in a separate thread"""
        file_path = filedialog.askopenfilename(
            filetypes=[
                ("All Supported Files", "*.csv;*.xls;*.xlsx;*.txt;*.html;*.xml"),
                ("CSV Files", "*.csv"),
                ("Excel Files", "*.xls;*.xlsx"),
                ("Text Files", "*.txt"),
                ("HTML Files", "*.html"),
                ("XML Files", "*.xml"),
                ("All Files", "*.*")
            ]
        )
        
        if not file_path:
            return
            
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, f"Processing file: {file_path}\n")
        self.output_text.see(tk.END)
        self.update_status(f"Processing {os.path.basename(file_path)}...")
        
        # Disable buttons during processing
        self.upload_btn.config(state=tk.DISABLED)
        self.export_btn.config(state=tk.DISABLED)
        self.progress['value'] = 0
        self.progress_label.config(text="0%")
        
        # Start processing in a separate thread
        threading.Thread(
            target=self.process_file,
            args=(file_path,),
            daemon=True
        ).start()

    def process_file(self, file_path):
        """Process the selected file"""
        try:
            # Determine file type and process accordingly
            if file_path.endswith('.csv'):
                results = LinkValidator.process_csv(
                    file_path, 
                    self.update_progress
                )
            elif file_path.endswith(('.xls', '.xlsx')):
                results = LinkValidator.process_excel(
                    file_path, 
                    self.update_progress
                )
            elif file_path.endswith('.html'):
                results = LinkValidator.process_html(
                    file_path, 
                    self.update_progress
                )
            elif file_path.endswith('.txt'):
                results = LinkValidator.process_text(
                    file_path, 
                    self.update_progress
                )
            else:
                raise Exception("Unsupported file format")
            
            self.results = results
            self.display_results(results)
            self.update_status("Processing completed successfully")
            self.export_btn.config(state=tk.NORMAL)
            
        except Exception as e:
            self.output_text.insert(tk.END, f"\nError: {str(e)}\n")
            self.update_status(f"Error: {str(e)}")
        
        finally:
            self.upload_btn.config(state=tk.NORMAL)
            self.progress['value'] = 100
            self.progress_label.config(text="100%")

    def update_progress(self, progress):
        """Update progress bar from worker thread"""
        percent = int(progress * 100)
        self.root.after(0, lambda: self.progress.config(value=percent))
        self.root.after(0, lambda: self.progress_label.config(text=f"{percent}%"))

    def display_results(self, results):
        """Display validation results in the text widget"""
        self.output_text.insert(tk.END, "\n=== Validation Results ===\n")
        self.output_text.insert(tk.END, f"Total valid links: {results['valid']}\n")
        self.output_text.insert(tk.END, f"Total invalid links: {results['invalid']}\n\n")
        
        if results['invalid_links']:
            self.output_text.insert(tk.END, "=== Invalid Links Found ===\n")
            for link in results['invalid_links']:
                self.output_text.insert(tk.END, f"{link}\n")
        else:
            self.output_text.insert(tk.END, "No invalid links found.\n")
        
        self.output_text.see(tk.END)

    def export_results(self):
        """Export results to a CSV file"""
        if not self.results:
            messagebox.showwarning("No Results", "No results to export")
            return
            
        default_filename = f"link_validation_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        save_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")],
            initialfile=default_filename
        )
        
        if not save_path:
            return
            
        try:
            with open(save_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["Status", "Location", "URL"])
                
                # Write valid count
                writer.writerow(["Valid", "Summary", str(self.results['valid'])])
                
                # Write invalid entries
                for entry in self.results['invalid_links']:
                    # Parse the entry to extract location and URL
                    parts = entry.split(": ")
                    if len(parts) >= 2:
                        location = parts[0]
                        url = ": ".join(parts[1:])
                        writer.writerow(["Invalid", location, url])
                
            messagebox.showinfo("Success", f"Results exported to {save_path}")
            self.update_status(f"Results exported to {os.path.basename(save_path)}")
            
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export results: {str(e)}")
            self.update_status(f"Export failed: {str(e)}")

    def update_status(self, message):
        """Update the status bar"""
        self.status_bar.config(text=message)


if __name__ == "__main__":
    root = tk.Tk()
    app = LinkValidatorApp(root)
    root.mainloop()