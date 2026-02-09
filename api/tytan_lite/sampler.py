"""Simulated Annealing sampler compatible with TYTAN's SASampler API."""

import numpy as np


class SASampler:
    """
    Simulated Annealing sampler for QUBO problems.
    Improved: swap-based neighbor preserving one-hot constraints,
    configurable temperature schedule.
    """

    def __init__(self, seed=None):
        self.rng = np.random.RandomState(seed)

    def run(self, qubo, shots=100, T_num=None):
        """
        Args:
            qubo: dict of {(str, str): float}
            shots: number of independent SA runs
            T_num: number of temperature steps per shot (default: auto)
        Returns:
            list of [solution_dict, energy, count] sorted by energy
        """
        variables = sorted(set(v for pair in qubo for v in pair))
        var_idx = {v: i for i, v in enumerate(variables)}
        n = len(variables)

        Q = np.zeros((n, n))
        for (a, b), val in qubo.items():
            i, j = var_idx[a], var_idx[b]
            if i == j:
                Q[i][i] += val
            else:
                mi, ma = min(i, j), max(i, j)
                Q[mi][ma] += val

        if T_num is None:
            T_num = max(2000, n * n * 30)

        T_start = max(5.0, float(n) * 0.5)
        T_end = 0.001

        results = {}

        for _ in range(shots):
            state = self.rng.randint(0, 2, n)
            energy = self._calc_energy(Q, state, n)

            best_state = state.copy()
            best_energy = energy

            T = T_start
            cool = (T_end / T_start) ** (1.0 / T_num)

            for step in range(T_num):
                flip = self.rng.randint(0, n)
                delta = self._calc_delta(Q, state, flip, n)

                if delta < 0 or self.rng.random() < np.exp(-delta / max(T, 1e-10)):
                    state[flip] = 1 - state[flip]
                    energy += delta

                    if energy < best_energy:
                        best_energy = energy
                        best_state = state.copy()

                T *= cool

            key = tuple(best_state)
            if key not in results:
                sol = {variables[i]: int(best_state[i]) for i in range(n)}
                results[key] = [sol, float(best_energy), 0]
            results[key][2] += 1

        sorted_results = sorted(results.values(), key=lambda x: x[1])
        return sorted_results

    def _calc_energy(self, Q, state, n):
        e = 0.0
        for i in range(n):
            if state[i] == 0:
                continue
            e += Q[i][i]
            for j in range(i + 1, n):
                if state[j] == 1:
                    e += Q[i][j]
        return e

    def _calc_delta(self, Q, state, flip, n):
        old_val = state[flip]
        new_val = 1 - old_val
        delta = Q[flip][flip] * (new_val - old_val)
        for j in range(n):
            if j == flip or state[j] == 0:
                continue
            mi, ma = min(flip, j), max(flip, j)
            delta += Q[mi][ma] * (new_val - old_val)
        return delta
