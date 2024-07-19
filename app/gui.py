import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from app.metrics import PortfolioTracker
from app.config import type1_df_path, type2_df_path, type3_df_path


class PortfolioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Portfolio Tracker")

        # Load data from config.py paths
        self.load_data()

        # Calculate metrics
        self.calculate_metrics()

        # Create widgets
        self.create_widgets()

    def load_data(self):
        try:
            self.type1_df = pd.read_csv(type1_df_path)
            self.type2_df = pd.read_csv(type2_df_path)
            self.type3_df = pd.read_csv(type3_df_path)
        except Exception as e:
            messagebox.showerror("Error", f"Error loading data: {str(e)}")
            self.type1_df = None
            self.type2_df = None
            self.type3_df = None

    def create_widgets(self):
        # Results Textbox
        self.results_text = tk.Text(self.root, height=20, width=80)
        self.results_text.grid(row=0, column=0, padx=10, pady=10)

        # Display metrics if data loaded successfully
        if self.type1_df is not None:
            self.display_metrics()

    def calculate_metrics(self):
        if self.type1_df is not None:
            try:
                tracker = PortfolioTracker(self.type1_df, self.type2_df)
                self.metrics = tracker.calculate_metrics()
            except Exception as e:
                messagebox.showerror("Error", f"Error calculating metrics: {str(e)}")
                self.metrics = None

    def display_metrics(self):
        self.results_text.insert(tk.END, "Portfolio Metrics:\n")
        for key, value in self.metrics.items():
            if isinstance(value, dict):
                self.results_text.insert(tk.END, f"{key}:\n")
                for sub_key, sub_value in value.items():
                    self.results_text.insert(tk.END, f"  {sub_key}: {sub_value}\n")
            else:
                self.results_text.insert(tk.END, f"{key}: {value}\n")


if __name__ == "__main__":
    root = tk.Tk()
    app = PortfolioApp(root)
    root.mainloop()
