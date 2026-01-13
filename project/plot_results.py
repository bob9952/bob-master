import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

def generate_plots():
    # Setup paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    results_dir = os.path.join(script_dir, "results")
    excel_path = os.path.join(results_dir, "experiment_results.xlsx")
    plots_dir = os.path.join(results_dir, "plots")
    
    if not os.path.exists(plots_dir):
        os.makedirs(plots_dir)
        
    if not os.path.exists(excel_path):
        print(f"Error: {excel_path} not found. Run experiments first.")
        return

    # Load Data
    df = pd.read_excel(excel_path)
    
    # Calculate Gaps for all heuristics relative to Optimal
    # Note: Some heuristics might not have gaps calculated in CSV, so we compute them now
    # We assume 'Optimal' column exists.
    
    heuristics = ['FF', 'FFD', 'FFD+', 'FFL', 'BF', 'BFD', 'BFL', 'NF', 'NFD', 'NFD+', 'MR', 'MRD', 'MR+', 'MRD+', 'GA']
    
    # Compute Gaps
    for h in heuristics:
        if h in df.columns:
            # If optimal is missing (0 or NaN), we can't compute gap properly, handle carefully
            # But our script ensures optimal is populated.
            df[f'Gap_{h}'] = df[h] - df['Optimal']
    
    # Categories
    categories = df['Category'].unique()
    
    print(f"Generating plots for categories: {categories}")
    
    # --- PLOT 1: Average Gap Comparison (Bar Chart) ---
    plt.figure(figsize=(12, 6))
    
    gap_data = []
    labels = []
    
    for cat in categories:
        cat_df = df[df['Category'] == cat]
        means = []
        for h in heuristics:
            if f'Gap_{h}' in cat_df.columns:
                means.append(cat_df[f'Gap_{h}'].mean())
            else:
                means.append(0)
        gap_data.append(means)
        labels.append(cat)
        
    x = np.arange(len(heuristics))
    width = 0.25
    
    fig, ax = plt.subplots(figsize=(14, 7))
    
    # We expect 3 categories: Easy, Medium, Hard. 
    # Adjust width offset dynamically
    for i, cat in enumerate(labels):
        offset = (i - len(labels)/2) * width + (width/2)
        ax.bar(x + offset, gap_data[i], width, label=cat)

    ax.set_ylabel('Average Gap from Optimal (Bins)')
    ax.set_title('Heuristic Performance: Solution Quality (Lower is Better)')
    ax.set_xticks(x)
    ax.set_xticklabels(heuristics)
    ax.legend()
    ax.grid(True, axis='y', linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, "comparison_gap.png"))
    print("Saved comparison_gap.png")
    
    # --- PLOT 2: Average Time Comparison (Log Scale) ---
    # Time columns: FF_Time, FFD_Time, etc.
    
    time_data = []
    
    for cat in categories:
        cat_df = df[df['Category'] == cat]
        means = []
        for h in heuristics:
            col_name = f"{h}_Time"
            if col_name in cat_df.columns:
                means.append(cat_df[col_name].mean())
            else:
                means.append(0)
        time_data.append(means)
        
    fig, ax = plt.subplots(figsize=(14, 7))
    
    for i, cat in enumerate(labels):
        offset = (i - len(labels)/2) * width + (width/2)
        ax.bar(x + offset, time_data[i], width, label=cat)

    ax.set_ylabel('Average Time (seconds) - Log Scale')
    ax.set_title('Heuristic Performance: Computational Time (Lower is Better)')
    ax.set_xticks(x)
    ax.set_xticklabels(heuristics)
    ax.set_yscale('log') # Log scale because GA is much slower
    ax.legend()
    ax.grid(True, axis='y', linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    plt.savefig(os.path.join(plots_dir, "comparison_time.png"))
    print("Saved comparison_time.png")

if __name__ == "__main__":
    generate_plots()

