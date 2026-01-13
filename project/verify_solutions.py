import os
import pandas as pd

def check_solutions():
    print("--- Loading Solutions.xlsx ---")
    solutions_path = "project/data/Solutions.xlsx"
    
    if not os.path.exists(solutions_path):
        print(f"Error: {solutions_path} not found.")
        return

    # Load all sheets
    try:
        xls = pd.read_excel(solutions_path, sheet_name=None, engine='openpyxl')
    except Exception as e:
        print(f"Error reading Excel: {e}")
        return

    # Flatten into a single dictionary
    sol_map = {}
    for sheet_name, df in xls.items():
        print(f"Processing sheet: {sheet_name} ({len(df)} rows)")
        if 'Name' in df.columns:
            for val in df['Name'].dropna():
                val_str = str(val).strip()
                sol_map[val_str] = True

    print(f"\nTotal unique solutions loaded: {len(sol_map)}")

    print("\n--- Checking Local Files against Solutions ---")
    data_dir = "project/data"
    
    # Walk data dir
    total_files = 0
    found_count = 0
    missing = []
    
    for root, dirs, files in os.walk(data_dir):
        for f in files:
            if not f.endswith(".txt"):
                continue
            
            total_files += 1
            
            # Check exact match
            if f in sol_map:
                found_count += 1
            else:
                # Check without extension or with different casing
                name_no_ext = os.path.splitext(f)[0]
                if name_no_ext in sol_map:
                    found_count += 1
                else:
                    missing.append(os.path.join(os.path.basename(root), f))

    print(f"Total Local Instance Files: {total_files}")
    print(f"Found in Excel: {found_count}")
    print(f"Missing: {len(missing)}")
    
    if missing:
        print("\nExamples of missing files (First 10):")
        for m in missing[:10]:
            print(f" - {m}")

if __name__ == "__main__":
    check_solutions()

