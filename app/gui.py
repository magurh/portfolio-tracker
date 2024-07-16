import tkinter as tk
from tkinter import ttk
import pandas as pd
from data_fetching import fetch_stock_price, fetch_crypto_price, fetch_exchange_rate
from metrics import calculate_portfolio_metrics

from app.config import type1_PATH, type2_PATH, type3_PATH

# Load CSV data (replace with actual file paths)
type1_df = pd.read_csv(type1_PATH)
type2_df = pd.read_csv(type2_PATH)
type3_df = pd.read_csv(type3_PATH)

# Function to update the dashboard with metrics
def update_dashboard():
    metrics = calculate_portfolio_metrics(type1_df, type2_df, type3_df)

    account_value_gbp.set(f"{metrics['account_value_gbp']:.2f} GBP")
    account_value_usd.set(f"{metrics['account_value_usd']:.2f} USD")
    unrealized_gains.set(f"{metrics['unrealized_gains']:.2f} GBP")
    realized_gains.set(f"{metrics['realized_gains']:.2f} GBP")
    day_change.set(f"{metrics['day_change']:.2f} GBP")
    dividend_income.set(f"{metrics['dividend_income']:.2f} GBP")
    total_commissions.set(f"{metrics['total_commissions']:.2f} GBP")

    # Update individual metrics
    update_individual_metrics(stock_frame, metrics['stock_metrics'])
    update_individual_metrics(index_fund_frame, metrics['index_fund_metrics'])
    update_individual_metrics(crypto_frame, metrics['crypto_metrics'])

def update_individual_metrics(frame, metrics):
    for widget in frame.winfo_children():
        widget.destroy()
    tk.Label(frame, text=f"Account Value: {metrics['account_value']:.2f} GBP").pack()
    tk.Label(frame, text=f"Unrealized Gains: {metrics['unrealized_gains']:.2f} GBP").pack()
    tk.Label(frame, text=f"Realized Gains: {metrics['realized_gains']:.2f} GBP").pack()
    tk.Label(frame, text=f"Dividend Income: {metrics['dividend_income']:.2f} GBP").pack()
    tk.Label(frame, text=f"Total Commissions: {metrics['total_commissions']:.2f} GBP").pack()

# Setup the main application window
app = tk.Tk()
app.title("Portfolio Tracker")

# Setup the notebook (tabs)
notebook = ttk.Notebook(app)
notebook.pack(expand=True, fill='both')

# Dashboard tab
dashboard_tab = ttk.Frame(notebook)
notebook.add(dashboard_tab, text='Dashboard')

# Stock tab
stock_tab = ttk.Frame(notebook)
notebook.add(stock_tab, text='Stocks')

# Index Fund tab
index_fund_tab = ttk.Frame(notebook)
notebook.add(index_fund_tab, text='Index Funds')

# Crypto tab
crypto_tab = ttk.Frame(notebook)
notebook.add(crypto_tab, text='Crypto')

# Dashboard contents
account_value_gbp = tk.StringVar()
account_value_usd = tk.StringVar()
unrealized_gains = tk.StringVar()
realized_gains = tk.StringVar()
day_change = tk.StringVar()
dividend_income = tk.StringVar()
total_commissions = tk.StringVar()

tk.Label(dashboard_tab, text="Account Value (GBP):").grid(row=0, column=0, sticky='e')
tk.Label(dashboard_tab, textvariable=account_value_gbp).grid(row=0, column=1, sticky='w')

tk.Label(dashboard_tab, text="Account Value (USD):").grid(row=1, column=0, sticky='e')
tk.Label(dashboard_tab, textvariable=account_value_usd).grid(row=1, column=1, sticky='w')

tk.Label(dashboard_tab, text="Unrealized Gains:").grid(row=2, column=0, sticky='e')
tk.Label(dashboard_tab, textvariable=unrealized_gains).grid(row=2, column=1, sticky='w')

tk.Label(dashboard_tab, text="Realized Gains:").grid(row=3, column=0, sticky='e')
tk.Label(dashboard_tab, textvariable=realized_gains).grid(row=3, column=1, sticky='w')

tk.Label(dashboard_tab, text="Day Change:").grid(row=4, column=0, sticky='e')
tk.Label(dashboard_tab, textvariable=day_change).grid(row=4, column=1, sticky='w')

tk.Label(dashboard_tab, text="Dividend Income:").grid(row=5, column=0, sticky='e')
tk.Label(dashboard_tab, textvariable=dividend_income).grid(row=5, column=1, sticky='w')

tk.Label(dashboard_tab, text="Total Commissions:").grid(row=6, column=0, sticky='e')
tk.Label(dashboard_tab, textvariable=total_commissions).grid(row=6, column=1, sticky='w')

# Individual metrics frames
stock_frame = ttk.Frame(stock_tab)
stock_frame.pack(fill='both', expand=True)

index_fund_frame = ttk.Frame(index_fund_tab)
index_fund_frame.pack(fill='both', expand=True)

crypto_frame = ttk.Frame(crypto_tab)
crypto_frame.pack(fill='both', expand=True)

# Initial update of the dashboard
update_dashboard()

# Run the application
app.mainloop()
