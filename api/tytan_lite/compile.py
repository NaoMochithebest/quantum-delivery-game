"""Compile sympy Hamiltonian expression into QUBO dictionary."""

from sympy import expand, Symbol


class Compile:
    """
    Convert a sympy expression (Hamiltonian) to QUBO format.
    
    Usage:
        qubo, offset = Compile(H).get_qubo()
    """
    
    def __init__(self, expr):
        self.expr = expr
    
    def get_qubo(self):
        """
        Expand the expression and extract QUBO coefficients.
        
        For binary variables: q^2 = q, so diagonal terms include
        both quadratic self-terms and linear terms.
        
        Returns:
            qubo: dict of {(str, str): float} 
            offset: float (constant term)
        """
        expanded = expand(self.expr)
        
        qubo = {}
        offset = 0.0
        
        terms = expanded.as_ordered_terms()
        
        for term in terms:
            coeff_and_symbols = term.as_coeff_mul()
            coeff = float(coeff_and_symbols[0])
            syms = coeff_and_symbols[1]
            
            if len(syms) == 0:
                # Constant term
                offset += coeff
            elif len(syms) == 1:
                # Linear term: coeff * q_i  (since q_i^2 = q_i for binary)
                s = str(syms[0])
                # Check if it's actually q^2
                base, exp = syms[0].as_base_exp()
                if exp == 2:
                    # q^2 = q for binary, so treat as linear
                    s = str(base)
                    key = (s, s)
                    qubo[key] = qubo.get(key, 0) + coeff
                else:
                    key = (s, s)
                    qubo[key] = qubo.get(key, 0) + coeff
            elif len(syms) == 2:
                # Quadratic term: coeff * q_i * q_j
                s0_base, s0_exp = syms[0].as_base_exp()
                s1_base, s1_exp = syms[1].as_base_exp()
                
                # Handle cases like q_i^2 * q_j or q_i * q_j
                factors = []
                for s in syms:
                    base, exp = s.as_base_exp()
                    for _ in range(int(exp)):
                        factors.append(str(base))
                
                if len(factors) == 2:
                    a, b = sorted(factors)
                    if a == b:
                        # q_i^2 = q_i
                        key = (a, a)
                        qubo[key] = qubo.get(key, 0) + coeff
                    else:
                        key = (a, b)
                        qubo[key] = qubo.get(key, 0) + coeff
                elif len(factors) == 3:
                    # Higher order - shouldn't happen in QUBO, skip
                    pass
            else:
                # Higher order terms - for QUBO we only handle up to 2
                pass
        
        return qubo, offset
