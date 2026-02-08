"""Auto_array: decode QUBO results into numpy ndarray."""

import numpy as np
import re


class Auto_array:
    """
    Convert a solution dict to an ndarray based on variable name pattern.
    
    Usage:
        arr, subs = Auto_array(result[0][0]).get_ndarray('q{}_{}')
    """
    
    def __init__(self, solution):
        self.solution = solution
    
    def get_ndarray(self, fmt):
        """
        Parse variable names matching the format and build an ndarray.
        
        Args:
            fmt: format string like 'q{}_{}' 
            
        Returns:
            (ndarray, list_of_index_lists)
        """
        # Convert format to regex
        # 'q{}_{}' -> 'q(\d+)_(\d+)'
        pattern = fmt.replace('{', r'(\d+)').replace('}', '')
        regex = re.compile('^' + pattern + '$')
        
        # Parse all matching variables
        parsed = []
        for var_name, val in self.solution.items():
            m = regex.match(var_name)
            if m:
                indices = tuple(int(g) for g in m.groups())
                parsed.append((indices, int(val)))
        
        if not parsed:
            return np.array([]), []
        
        # Determine dimensions
        ndim = len(parsed[0][0])
        
        if ndim == 1:
            max_idx = max(p[0][0] for p in parsed) + 1
            arr = np.zeros(max_idx, dtype=int)
            for indices, val in parsed:
                arr[indices[0]] = val
            subs = [list(range(max_idx))]
        elif ndim == 2:
            max_i = max(p[0][0] for p in parsed) + 1
            max_j = max(p[0][1] for p in parsed) + 1
            arr = np.zeros((max_i, max_j), dtype=int)
            for indices, val in parsed:
                arr[indices[0]][indices[1]] = val
            subs = [list(range(max_i)), list(range(max_j))]
        else:
            raise ValueError("Only 1D and 2D arrays are supported")
        
        return arr, subs
