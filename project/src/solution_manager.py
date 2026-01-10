import os
import pandas as pd

class SolutionManager:
    def __init__(self, excel_path="data/Solutions.xlsx"):
        self.solutions = {}
        
        # Check if file exists, if not, try relative to project root or absolute
        if not os.path.exists(excel_path):
            # Try looking one level up if running from project/
            alt_path = os.path.join("..", excel_path)
            if os.path.exists(alt_path):
                excel_path = alt_path
            else:
                # Try finding it in project/data if running from root
                root_path = os.path.join("project", "data", "Solutions.xlsx")
                if os.path.exists(root_path):
                    excel_path = root_path
                else:
                    print(f"Warning: Solution file not found at {excel_path}. Optimization lookup will fail.")
                    return

        self.load_solutions_from_excel(excel_path)

    def load_solutions_from_excel(self, file_path):
        """
        Loads solutions from the official BPPLIB Excel file.
        Reads all sheets.
        """
        try:
            # Read all sheets
            xls = pd.read_excel(file_path, sheet_name=None, engine='openpyxl')
            
            for sheet_name, df in xls.items():
                # Expected columns: Name, Best LB, Best UB, Status
                if 'Name' in df.columns and 'Best UB' in df.columns:
                    for index, row in df.iterrows():
                        name = str(row['Name']).strip()
                        best_ub = row['Best UB']
                        
                        # Handle potential NaN or non-integer values
                        try:
                            best_ub = int(best_ub)
                            self.solutions[name] = best_ub
                        except (ValueError, TypeError):
                            continue
                            
            print(f"Successfully loaded {len(self.solutions)} optimal solutions from Excel.")
            
        except Exception as e:
            print(f"Error loading solutions from Excel: {e}")

    def get_optimal(self, instance_name):
        # Clean name (remove extension if needed, though excel usually has .txt)
        if instance_name in self.solutions:
            return self.solutions[instance_name]
        
        # Try finding with .txt appended
        if not instance_name.endswith('.txt'):
            name_with_ext = instance_name + '.txt'
            if name_with_ext in self.solutions:
                return self.solutions[name_with_ext]
                
        return None
