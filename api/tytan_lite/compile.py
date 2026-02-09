from sympy import expand

class Compile:
    def __init__(self, expr):
        self.expr = expr

    def get_qubo(self):
        expanded = expand(self.expr)
        qubo = {}
        offset = 0.0
        for term in expanded.as_ordered_terms():
            coeff_and_symbols = term.as_coeff_mul()
            coeff = float(coeff_and_symbols[0])
            syms = coeff_and_symbols[1]
            if len(syms) == 0:
                offset += coeff
            elif len(syms) == 1:
                base, exp = syms[0].as_base_exp()
                s = str(base) if exp == 2 else str(syms[0])
                key = (s, s)
                qubo[key] = qubo.get(key, 0) + coeff
            elif len(syms) == 2:
                factors = []
                for s in syms:
                    base, exp = s.as_base_exp()
                    for _ in range(int(exp)):
                        factors.append(str(base))
                if len(factors) == 2:
                    a, b = sorted(factors)
                    key = (a, a) if a == b else (a, b)
                    qubo[key] = qubo.get(key, 0) + coeff
        return qubo, offset
