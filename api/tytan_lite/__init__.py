"""
tytan_lite: Minimal subset of TYTAN SDK for QUBO/TSP solving.
Original TYTAN SDK: https://github.com/tytansdk/tytan (Apache-2.0 License)

This module provides only the 4 functions needed for TSP:
  - symbols_list: Create symbolic variable arrays
  - Compile: Convert Hamiltonian expression to QUBO matrix
  - sampler.SASampler: Simulated Annealing sampler
  - Auto_array: Decode results into ndarray
"""

from .symbols import symbols_list
from .compile import Compile
from .auto_array import Auto_array
from . import sampler

__all__ = ['symbols_list', 'Compile', 'Auto_array', 'sampler']
