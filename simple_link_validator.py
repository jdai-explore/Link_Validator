"""
Simplified Link Validator - Minimal dependencies version
Use this if the main version has import issues
"""

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import pandas as pd
from urllib.parse import urlparse
import threading
import csv
import os
from datetime import datetime

class SimpleLinkValidator:
    """Simplified URL validation and file processing"""
    
    def __init__(self):
        self.processing_cancelled = False
    
    def is_valid_url(self, url):
        """Simple URL validation"""
        try:
            if pd.isna(url) or not str(url).strip():
                return False
                
            url_str = str(url).strip()
            result = urlparse(url_str)
            
            # Must have scheme and netloc
            if not result.scheme or not result.netloc:
                return False
                
            # Accept http/https schemes
            if result.scheme not in ('http', 'https'):
                return False
                
            # Basic netloc validation
            netloc = result.netloc.lower()
            if not netloc or netloc.startswith('.') or netloc.endswith('.'):
                return False
                
            return True
            
        except Exception:
            return False

    def process_csv(self, file_path, progress_callback=None):
        """Process CSV files"""
        results = {'valid': 0, 'invalid': 0, 'invalid_links': []}
        
        try:
            df = pd.read_csv(file_path)
            total = len(df) * len(df.columns)
            processed = 0
            
            for column in df.columns:
                if self.processing_cancelled:
                    break
                    
                for index, value in df[column].items():
                    if pd.notna(value):
                        url_str = str(value).strip()
                        if url_str:
                            if self.is_valid_url(url_str):
                                results['valid'] += 1
                            else:
                                results['invalid'] += 1
                                results['invalid_links'].append(
                                    f"Invalid link in column '{column}', row {index + 2}: {url_str[:50]}{'...' if len(url_str) > 50 else ''}"
                                )
                    processed += 1
                    if progress_callback and processed % 100 == 0:
                        progress_callback(processed/total)
        
        except Exception as e:
            raise Exception(f"CSV processing error: {str(e)}")
        
        return results

    def process_text(self, file_path, progress_callback=None):
        """Process text files"""
        results = {'valid': 0, 'invalid': 0, 'invalid_links': []}
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            
            total = len(lines)
            
            for i, line in enumerate(lines):
                if self.processing_cancelled:
                    break
                    
                line_str = line.strip()
                if line_str:
                    if self.is_valid_url(line_str):
                        results['valid'] += 1
                    else:
                        results['invalid'] += 1
                        results['invalid_links'].append(
                            f"Invalid link at line {i + 1}: {line_str[:50]}{'...' if len(line_str) > 50 else ''}"
                        )
                if progress_callback and i % 100 == 0:
                    progress_callback(i/total)
        
        except Exception as e:
            raise Exception(f"Text file processing error: {str(e)}")
        
        return results


class SimpleLinkValidatorApp:
    """Simplified GUI application"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Link Validator")
        self.root.geometry("800x600")
        
        self.results = None
        self.validator = SimpleLinkValidator()
        self.processing_thread = None
        
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
        """Create simplified GUI"""
        # Main frame
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(main_frame, text="Simple Link Validator", font=('Arial', 16, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Buttons
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        self.upload_btn = tk.Button(button_frame, text="Upload File", command=self.upload_file, width=15)
        self.upload_btn.pack(side=tk.LEFT, padx=5)
        
        self.export_btn = tk.Button(button_frame, text="Export Results", command=self.export_results, 
                                   state=tk.DISABLED, width=15)
        self.export_btn.pack(side=tk.LEFT, padx=5)
        
        self.clear_btn = tk.Button(button_frame, text="Clear", command=self.clear_results, width=15)
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, orient=tk.HORIZONTAL, length=100, mode='determinate')
        self.progress.pack(fill=tk.X, pady=10)
        
        self.progress_label = tk.Label(main_frame, text="Ready")
        self.progress_label.pack()
        
        # Results display
        self.output_text = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, width=90, height=25, 
                                                    font=('Consolas', 10))
        self.output_text.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Status bar
        self.status_bar = tk.Label(main_frame, text="Ready to process files", 
                                  bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(fill=tk.X, pady=(10, 0))

    def upload_file(self):
        """Upload and process file with better error handling"""
        try:
            print("Upload button clicked")  # Debug
            
            file_path = filedialog.askopenfilename(
                title="Select file to validate links",
                filetypes=[
                    ("Text Files", "*.txt"),
                    ("CSV Files", "*.csv"),
                    ("All Files", "*.*")
                ]
            )
            
            print(f"Selected file: {file_path}")  # Debug
            
            if not file_path:
                print("No file selected")  # Debug
                return
            
            # Check if file exists
            if not os.path.exists(file_path):
                messagebox.showerror("Error", "File not found!")
                return
            
            # Clear previous results
            self.clear_results()
            
            # Show file info
            file_size = os.path.getsize(file_path)
            self.output_text.insert(tk.END, f"Processing: {os.path.basename(file_path)}\n")
            self.output_text.insert(tk.END, f"Size: {file_size:,} bytes\n\n")
            
            self.status_bar.config(text="Processing file...")
            self.upload_btn.config(state=tk.DISABLED)
            self.progress['value'] = 0
            
            # Start processing in thread
            self.processing_thread = threading.Thread(target=self.process_file, args=(file_path,), daemon=True)
            self.processing_thread.start()
            
            print("Processing thread started")  # Debug
            
        except Exception as e:
            print(f"Error in upload_file: {e}")  # Debug
            messagebox.showerror("Error", f"Failed to process file: {str(e)}")
            self.upload_btn.config(state=tk.NORMAL)

    def process_file(self, file_path):
        """Process the file in background thread"""
        try:
            print(f"Starting to process: {file_path}")  # Debug
            
            # Determine file type
            if file_path.endswith('.csv'):
                results = self.validator.process_csv(file_path, self.update_progress)
            elif file_path.endswith('.txt'):
                results = self.validator.process_text(file_path, self.update_progress)
            else:
                # Try as text file
                results = self.validator.process_text(file_path, self.update_progress)
            
            print(f"Processing complete: {results}")  # Debug
            
            # Update UI in main thread
            self.root.after(0, lambda: self.display_results(results))
            self.root.after(0, lambda: self.upload_btn.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.export_btn.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.status_bar.config(text="Processing complete"))
            
        except Exception as e:
            print(f"Error in process_file: {e}")  # Debug
            error_msg = f"Error processing file: {str(e)}"
            self.root.after(0, lambda: self.output_text.insert(tk.END, f"\nERROR: {error_msg}\n"))
            self.root.after(0, lambda: self.upload_btn.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.status_bar.config(text=f"Error: {str(e)}"))

    def update_progress(self, progress):
        """Update progress bar"""
        try:
            percent = int(progress * 100)
            self.root.after(0, lambda: self.progress.config(value=percent))
            self.root.after(0, lambda: self.progress_label.config(text=f"Processing... {percent}%"))
        except Exception as e:
            print(f"Progress update error: {e}")

    def display_results(self, results):
        """Display validation results"""
        try:
            total_links = results['valid'] + results['invalid']
            
            self.output_text.insert(tk.END, "="*50 + "\n")
            self.output_text.insert(tk.END, "VALIDATION RESULTS\n")
            self.output_text.insert(tk.END, "="*50 + "\n\n")
            self.output_text.insert(tk.END, f"Total links found: {total_links}\n")
            self.output_text.insert(tk.END, f"Valid links: {results['valid']}\n")
            self.output_text.insert(tk.END, f"Invalid links: {results['invalid']}\n\n")
            
            if results['invalid_links']:
                self.output_text.insert(tk.END, "INVALID LINKS:\n")
                self.output_text.insert(tk.END, "-" * 30 + "\n")
                for i, link in enumerate(results['invalid_links'][:50], 1):  # Show first 50
                    self.output_text.insert(tk.END, f"{i}. {link}\n")
                
                if len(results['invalid_links']) > 50:
                    remaining = len(results['invalid_links']) - 50
                    self.output_text.insert(tk.END, f"\n... and {remaining} more (use Export to see all)\n")
            else:
                self.output_text.insert(tk.END, "No invalid links found!\n")
            
            self.output_text.see(tk.END)
            self.results = results
            
        except Exception as e:
            print(f"Error displaying results: {e}")

    def export_results(self):
        """Export results to CSV"""
        try:
            if not self.results:
                messagebox.showwarning("No Results", "No results to export")
                return
            
            save_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV Files", "*.csv")],
                initialfile=f"link_validation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            )
            
            if not save_path:
                return
            
            with open(save_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["Status", "Location", "URL"])
                writer.writerow(["SUMMARY", f"Valid: {self.results['valid']}", f"Invalid: {self.results['invalid']}"])
                
                for entry in self.results['invalid_links']:
                    parts = entry.split(": ", 1)
                    if len(parts) >= 2:
                        writer.writerow(["Invalid", parts[0], parts[1]])
            
            messagebox.showinfo("Success", f"Results exported to {save_path}")
            
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export: {str(e)}")

    def clear_results(self):
        """Clear all results"""
        self.output_text.delete(1.0, tk.END)
        self.results = None
        self.export_btn.config(state=tk.DISABLED)
        self.progress['value'] = 0
        self.progress_label.config(text="Ready")


def main():
    """Main function with error handling"""
    try:
        print("Starting Simple Link Validator...")
        root = tk.Tk()
        app = SimpleLinkValidatorApp(root)
        print("GUI created successfully")
        root.mainloop()
    except Exception as e:
        print(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()