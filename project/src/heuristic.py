def first_fit(item_order, items_dict, bin_capacity):
    """
    Applies the First Fit heuristic to pack items in the given order.
    """
    bins = []
    EPSILON = 1e-6 
    
    for item_id in item_order:
        item_size = items_dict[item_id]
        placed = False
        
        for bin in bins:
            if bin['used'] + item_size <= bin_capacity + EPSILON:
                bin['used'] += item_size
                bin['items'].append((item_id, item_size))
                placed = True
                break
        
        if not placed:
            bins.append({'used': item_size, 'items': [(item_id, item_size)]})
            
    return bins

def next_fit(item_order, items_dict, bin_capacity):
    """
    Applies the Next Fit heuristic.
    Only checks the current (last open) bin.
    """
    bins = []
    EPSILON = 1e-6 
    
    # Start with one empty bin if there are items
    if not item_order:
        return []
        
    # Create first bin
    current_bin = {'used': 0.0, 'items': []}
    bins.append(current_bin)
    
    for item_id in item_order:
        item_size = items_dict[item_id]
        
        # Check only the last bin
        if current_bin['used'] + item_size <= bin_capacity + EPSILON:
            current_bin['used'] += item_size
            current_bin['items'].append((item_id, item_size))
        else:
            # Close current, open new
            current_bin = {'used': item_size, 'items': [(item_id, item_size)]}
            bins.append(current_bin)
            
    return bins

def best_fit(item_order, items_dict, bin_capacity):
    """
    Applies the Best Fit heuristic.
    Places item in the bin where it fits with the MINIMUM remaining space.
    """
    bins = []
    EPSILON = 1e-6 
    
    for item_id in item_order:
        item_size = items_dict[item_id]
        
        best_bin_idx = -1
        min_residual_space = float('inf')
        
        # Check all bins to find tightest fit
        for i, bin in enumerate(bins):
            residual = bin_capacity - bin['used']
            # If it fits...
            if residual >= item_size - EPSILON:
                # ...and is tighter than what we found so far
                if residual < min_residual_space:
                    min_residual_space = residual
                    best_bin_idx = i
        
        if best_bin_idx != -1:
            bins[best_bin_idx]['used'] += item_size
            bins[best_bin_idx]['items'].append((item_id, item_size))
        else:
            bins.append({'used': item_size, 'items': [(item_id, item_size)]})
            
    return bins

def max_rest(item_order, items_dict, bin_capacity):
    """
    Applies the Max-Rest (Worst-Fit) heuristic.
    Places item in the bin with the MAXIMUM remaining space (if it fits).
    """
    bins = []
    EPSILON = 1e-6 
    
    for item_id in item_order:
        item_size = items_dict[item_id]
        
        best_bin_idx = -1
        max_residual_space = -1.0
        
        # Check all bins to find the one with most room
        for i, bin in enumerate(bins):
            residual = bin_capacity - bin['used']
            
            # If it fits...
            if residual >= item_size - EPSILON:
                # ...and has more space than what we found so far
                if residual > max_residual_space:
                    max_residual_space = residual
                    best_bin_idx = i
        
        if best_bin_idx != -1:
            bins[best_bin_idx]['used'] += item_size
            bins[best_bin_idx]['items'].append((item_id, item_size))
        else:
            bins.append({'used': item_size, 'items': [(item_id, item_size)]})
            
    return bins
