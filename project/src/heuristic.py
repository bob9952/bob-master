import heapq

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

def counting_sort(item_order, items_dict, max_val):
    """
    Sorts items in DECREASING order using Counting Sort.
    item_order: List of item IDs.
    items_dict: Mapping of ID -> Size.
    max_val: Maximum item size.
    """
    # Create frequency array
    count = [[] for _ in range(int(max_val) + 1)]
    
    for item_id in item_order:
        size = int(items_dict[item_id])
        if size <= max_val:
            count[size].append(item_id)
            
    # Reconstruct sorted list (Decreasing)
    sorted_items = []
    for s in range(int(max_val), -1, -1):
        if count[s]:
            sorted_items.extend(count[s])
            
    return sorted_items

def first_fit_lookup(item_order, items_dict, bin_capacity):
    """
    Applies First-Fit using a Lookup Table (Map) logic similar to C++ FF++ implementation.
    The map associates an object weight to an index in the bin array.
    The index signifies the minimum index at which an object of the current weight could be placed the last time.
    """
    bins = []
    # Lookup table: maps item_size -> index of the first bin that MIGHT fit this size
    # This corresponds to `bin_map` in C++ implementation
    bin_map = {} 
    
    EPSILON = 1e-6 
    
    for item_id in item_order:
        item_size = items_dict[item_id]
        placed = False
        
        # Start search from the index stored in bin_map for this size, or 0
        start_idx = bin_map.get(item_size, 0)
        
        # Check existing bins starting from start_idx
        for j in range(start_idx, len(bins)):
            bin = bins[j]
            if bin['used'] + item_size <= bin_capacity + EPSILON:
                bin['used'] += item_size
                bin['items'].append((item_id, item_size))
                
                # Update map: next time, start searching for this size from THIS bin index
                # (because previous bins are full for this size)
                bin_map[item_size] = j
                
                placed = True
                break
        
        if not placed:
            # Create new bin
            new_bin_idx = len(bins)
            bins.append({'used': item_size, 'items': [(item_id, item_size)]})
            
            # Update map: new bin is the first candidate for this size now (if it wasn't placed before)
            # Actually, C++ sets bin_map[objects[i]] = num_open_bins++ when creating new bin
            bin_map[item_size] = new_bin_idx
            
    return bins

def best_fit_lookup(item_order, items_dict, bin_capacity):
    """
    Applies Best-Fit using a Lookup Table (Bucket Queue).
    (Algorithm 10 from Rieck's paper)
    Only works efficiently for INTEGER capacities.
    """
    if not float(bin_capacity).is_integer():
        # Fallback to standard Best Fit for float capacities
        return best_fit(item_order, items_dict, bin_capacity)

    capacity_int = int(bin_capacity)
    bins = []
    
    # Lookup table: index i stores a LIST of bin INDICES that have exactly i remaining capacity
    # capacity_lookup[rem] = [bin_idx1, bin_idx2, ...]
    capacity_lookup = [[] for _ in range(capacity_int + 1)]
    
    for item_id in item_order:
        item_size = items_dict[item_id]
        item_size_int = int(item_size) # Assume integer items
        
        best_bin_idx = -1
        
        # Search for smallest remaining capacity >= item_size
        # We look from item_size up to capacity
        for rem in range(item_size_int, capacity_int + 1):
            if capacity_lookup[rem]:
                # Found a bin with 'rem' space!
                # Take the last one (LIFO is fine and fast)
                best_bin_idx = capacity_lookup[rem].pop()
                break
        
        if best_bin_idx != -1:
            # Update bin
            bins[best_bin_idx]['used'] += item_size
            bins[best_bin_idx]['items'].append((item_id, item_size))
            
            # Re-insert into lookup with NEW remaining capacity
            new_rem = int(capacity_int - bins[best_bin_idx]['used'])
            capacity_lookup[new_rem].append(best_bin_idx)
            
        else:
            # Create new bin
            new_bin = {'used': item_size, 'items': [(item_id, item_size)]}
            bins.append(new_bin)
            
            # Insert into lookup
            new_rem = int(capacity_int - item_size)
            capacity_lookup[new_rem].append(len(bins) - 1)
            
    return bins

def max_rest_pq(item_order, items_dict, bin_capacity):
    """
    Applies Max-Rest using a Priority Queue (Heap).
    Faster implementation O(N log N) vs O(N^2).
    """
    bins = []
    # Heap stores (-remaining_capacity, bin_index)
    # Python heapq is min-heap, so we use negative to get max-heap behavior
    pq = []
    EPSILON = 1e-6
    
    for item_id in item_order:
        item_size = items_dict[item_id]
        placed = False
        
        if pq:
            # Check the bin with MAXIMUM remaining capacity (top of heap)
            neg_rem, idx = pq[0]
            remaining = -neg_rem
            
            if remaining >= item_size - EPSILON:
                # It fits! Remove from heap, update, and push back
                heapq.heappop(pq)
                
                bins[idx]['used'] += item_size
                bins[idx]['items'].append((item_id, item_size))
                
                new_rem = remaining - item_size
                heapq.heappush(pq, (-new_rem, idx))
                placed = True
        
        if not placed:
            # Create new bin
            new_bin = {'used': item_size, 'items': [(item_id, item_size)]}
            bins.append(new_bin)
            
            new_idx = len(bins) - 1
            rem = bin_capacity - item_size
            heapq.heappush(pq, (-rem, new_idx))
            
    return bins
