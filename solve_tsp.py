"""
TSP solver using QUBO + Simulated Annealing.
No sympy dependency — QUBO matrix is built numerically for speed.
"""
from http.server import BaseHTTPRequestHandler
import json
import numpy as np


def build_qubo_tsp(dist_matrix, constraint_weight=2.0, cost_weight=1.0):
    """
    Build QUBO matrix for TSP directly (no symbolic math).
    
    Variables: q[t*N + i] = 1 if city i is visited at step t
    Total variables: N*N
    
    Constraints:
      A) Each step visits exactly 1 city: sum_i q[t][i] = 1
      B) Each city visited exactly once:  sum_t q[t][i] = 1
    Cost:
      sum_t sum_ij dist[i][j] * q[t][i] * q[(t+1)%N][j]
    """
    N = len(dist_matrix)
    n_vars = N * N
    Q = np.zeros((n_vars, n_vars))
    
    def idx(t, i):
        return t * N + i
    
    A = constraint_weight
    
    # Constraint A: each step has exactly 1 city
    for t in range(N):
        for i in range(N):
            Q[idx(t,i), idx(t,i)] -= A          # linear: -A * q[t][i]
            for j in range(i+1, N):
                Q[idx(t,i), idx(t,j)] += 2 * A  # quadratic: 2A * q[t][i]*q[t][j]
    
    # Constraint B: each city visited exactly once
    for i in range(N):
        for t in range(N):
            Q[idx(t,i), idx(t,i)] -= A
            for s in range(t+1, N):
                Q[idx(t,i), idx(s,i)] += 2 * A
    
    # Cost: minimize tour distance (including return)
    C = cost_weight
    for t in range(N):
        next_t = (t + 1) % N
        for i in range(N):
            for j in range(N):
                if i != j:
                    a, b = idx(t, i), idx(next_t, j)
                    mi, ma = min(a, b), max(a, b)
                    Q[mi, ma] += C * dist_matrix[i][j]
    
    return Q


def simulated_annealing(Q, n_vars, shots, T_num, rng):
    """
    Run SA on QUBO matrix. Optimized with numpy vectorization.
    """
    T_start = 5.0
    T_end = 0.001
    cool = (T_end / T_start) ** (1.0 / T_num)
    
    # Pre-compute upper triangular + diagonal for fast delta calc
    # Q_full[i,j] = Q[min(i,j), max(i,j)] for off-diag, Q[i,i] for diag
    Q_sym = Q + Q.T - np.diag(np.diag(Q))  # full symmetric
    
    best_state = None
    best_energy = float('inf')
    
    for _ in range(shots):
        state = rng.randint(0, 2, n_vars).astype(np.float64)
        energy = state @ Q_sym @ state * 0.5 + np.diag(Q) @ state * 0.5
        # More accurate: use upper triangular
        energy = 0.0
        for i in range(n_vars):
            if state[i]:
                energy += Q[i,i]
                for j in range(i+1, n_vars):
                    if state[j]:
                        energy += Q[i,j]
        
        local_best = state.copy()
        local_best_e = energy
        
        T = T_start
        # Pre-generate random numbers for speed
        flips = rng.randint(0, n_vars, T_num)
        rands = rng.random(T_num)
        
        for step in range(T_num):
            flip = flips[step]
            old_val = state[flip]
            new_val = 1.0 - old_val
            diff = new_val - old_val
            
            # Delta = diff * (Q[flip,flip] + sum of Q[min,max] for active neighbors)
            # Use numpy dot for speed
            delta = diff * (Q[flip, flip] + Q_sym[flip] @ state - Q[flip, flip] * old_val)
            
            if delta < 0 or rands[step] < np.exp(-delta / max(T, 1e-10)):
                state[flip] = new_val
                energy += delta
                if energy < local_best_e:
                    local_best_e = energy
                    local_best = state.copy()
            
            T *= cool
        
        if local_best_e < best_energy:
            best_energy = local_best_e
            best_state = local_best.copy()
    
    return best_state.astype(int), best_energy


def decode_path(state, N):
    """Extract city visit order from flat state vector."""
    path = []
    for t in range(N):
        for i in range(N):
            if state[t * N + i] == 1:
                path.append(i)
                break
    return path


class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self._cors()
        self.end_headers()

    def do_POST(self):
        try:
            body = json.loads(self.rfile.read(int(self.headers.get('Content-Length', 0))))
            houses = body.get('houses', [])
            shots = body.get('shots', 100)
            T_num = body.get('T_num', 2000)

            N = len(houses)
            if N < 3:
                return self._json(400, {'error': '3軒以上必要'})

            # Distance matrix
            dist = np.zeros((N, N))
            for i in range(N):
                for j in range(N):
                    if i != j:
                        dx = houses[i]['x'] - houses[j]['x']
                        dy = houses[i]['y'] - houses[j]['y']
                        dist[i][j] = np.sqrt(dx*dx + dy*dy)
            
            # Normalize
            mx = np.max(dist)
            if mx > 0:
                dist /= mx

            # Build QUBO numerically (instant, no sympy)
            Q = build_qubo_tsp(dist, constraint_weight=2.0, cost_weight=0.5)

            # Simulated Annealing
            rng = np.random.RandomState()
            best_state, _ = simulated_annealing(Q, N*N, shots, T_num, rng)

            # Decode
            path = decode_path(best_state, N)
            if len(path) != N or len(set(path)) != N:
                path = list(range(N))

            self._json(200, {'path': path})
        except Exception as e:
            self._json(500, {'error': str(e)})

    def _cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def _json(self, code, data):
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self._cors()
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
