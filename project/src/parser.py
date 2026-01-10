import os

def parse_instance_file(file_path):
    """
    Universal parser for BPPLIB instances (Falkenauer, Scholl, Hard28).
    Returns a list of ONE instance (since Scholl/Hard files are single instances).
    """
    instances = []
    filename = os.path.basename(file_path)
    
    try:
        with open(file_path, 'r') as f:
            lines = [l.strip() for l in f.readlines() if l.strip()]
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return []

    if not lines:
        return []

    # Heuristic detection of format
    # Falkenauer (Binpack1-8 format) starts with Number of Problems (e.g. "20")
    # AND subsequent lines have strings like "u120_00".
    # Scholl/Hard28 starts with Num Items (e.g. "50") then Capacity ("1000").
    
    first_line_val = -1
    try:
        first_line_val = int(lines[0])
    except ValueError:
        pass # Might be string

    # Check if it's a Falkenauer Multi-Instance file
    is_multi_instance = False
    if len(lines) > 2:
        # Line 1 is a name?
        if not lines[1][0].isdigit(): 
            is_multi_instance = True
    
    if is_multi_instance:
        # Re-use the logic from before for binpack1.txt
        return parse_falkenauer_multi(lines)
    else:
        # Single Instance (Scholl / Hard28 / BPPLIB Single format)
        # Format:
        # Line 0: Num Items
        # Line 1: Capacity
        # Line 2+: Items
        
        try:
            num_items = int(lines[0])
            capacity = float(lines[1]) # Use float for safety
            
            items_list = []
            for i in range(2, len(lines)):
                items_list.append(float(lines[i]))
                
            items_dict = {i+1: size for i, size in enumerate(items_list)}
            
            # Best Known is NOT in the file for Scholl. 
            # We return None, caller must look it up.
            best_known = None 
            
            instances.append({
                "name": filename,
                "capacity": capacity,
                "num_items": num_items,
                "best_known": best_known,
                "items_dict": items_dict
            })
            
        except (ValueError, IndexError) as e:
            print(f"Error parsing single instance {filename}: {e}")
            
    return instances

def parse_falkenauer_multi(lines):
    instances = []
    num_problems = int(lines[0])
    current_line = 1
    
    for _ in range(num_problems):
        if current_line >= len(lines):
            break
        name = lines[current_line].strip()
        # Normalize Name for BPPLIB Excel Lookup
        # binpack files have "u120_00", but Excel has "Falkenauer_u120_00.txt"
        if not name.startswith("Falkenauer_"):
            name = f"Falkenauer_{name}.txt"
            
        current_line += 1
        
        parts = lines[current_line].split()
        capacity = float(parts[0])
        num_items = int(parts[1])
        best_known = int(parts[2])
        current_line += 1
        
        items_list = []
        for _ in range(num_items):
            items_list.append(float(lines[current_line]))
            current_line += 1
            
        items_dict = {i+1: size for i, size in enumerate(items_list)}
        
        instances.append({
            "name": name,
            "capacity": capacity,
            "num_items": num_items,
            "best_known": best_known,
            "items_dict": items_dict
        })
    return instances
