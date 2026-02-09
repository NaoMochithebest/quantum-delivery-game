import numpy as np
import re

class Auto_array:
    def __init__(self, solution):
        self.solution = solution

    def get_ndarray(self, fmt):
        pattern = fmt.replace('{', r'(\d+)').replace('}', '')
        regex = re.compile('^' + pattern + '$')
        parsed = []
        for var_name, val in self.solution.items():
            m = regex.match(var_name)
            if m:
                parsed.append((tuple(int(g) for g in m.groups()), int(val)))
        if not parsed:
            return np.array([]), []
        ndim = len(parsed[0][0])
        if ndim == 2:
            max_i = max(p[0][0] for p in parsed) + 1
            max_j = max(p[0][1] for p in parsed) + 1
            arr = np.zeros((max_i, max_j), dtype=int)
            for indices, val in parsed:
                arr[indices[0]][indices[1]] = val
            return arr, [list(range(max_i)), list(range(max_j))]
        max_idx = max(p[0][0] for p in parsed) + 1
        arr = np.zeros(max_idx, dtype=int)
        for indices, val in parsed:
            arr[indices[0]] = val
        return arr, [list(range(max_idx))]
