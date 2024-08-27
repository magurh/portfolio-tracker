import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from portfolio_tracker.loader import DataLoader
from portfolio_tracker.manager import PortfolioManager
from portfolio_tracker.config import type1_df_path, type2_df_path, type3_df_path

class PortfolioGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Portfolio Tracker")
        self.geometry("800x600")

        # Load data
        self.load_data()

        # Initialize PortfolioManager
        self.portfolio_manager = PortfolioManager(self.transactions)

        # Create widgets
        self.create_widgets()

    def load_data(self):
        # Use DataLoader to load data
        data_loader = DataLoader(type1_df_path, type2_df_path, type3_df_path)
        self.transactions = data_loader.load_transactions()

    def create_widgets(self):
        # Create a frame for the portfolio value
        self.value_frame = ttk.Frame(self)
        self.value_frame.pack(pady=20)
        
        # Portfolio value label
        self.value_label = ttk.Label(self.value_frame, text="Current Portfolio Value:")
        self.value_label.grid(row=0, column=0, padx=10, pady=10)

        self.portfolio_value = tk.StringVar()
        self.portfolio_value.set(f"${self.portfolio_manager.current_portfolio_value():,.2f}")
        self.value_display = ttk.Label(self.value_frame, textvariable=self.portfolio_value, font=("Arial", 18))
        self.value_display.grid(row=0, column=1, padx=10, pady=10)

        # Create a frame for the pie chart
        self.chart_frame = ttk.Frame(self)
        self.chart_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Draw pie chart
        self.draw_pie_chart()

    def draw_pie_chart(self):
        # Get stock percentages
        percentages = self.portfolio_manager.stock_percentage_of_portfolio()
        
        # Create a matplotlib figure
        fig = Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(111)

        # Create a pie chart
        labels = [f"{stock}: {percent:.2f}%" for stock, percent in percentages.items()]
        sizes = list(percentages.values())
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)

        # Equal aspect ratio ensures that pie is drawn as a circle.
        ax.axis('equal')

        # Embed the pie chart in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Run the application
if __name__ == "__main__":
    app = PortfolioGUI()
    app.mainloop()
