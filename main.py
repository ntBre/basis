import json
import numpy as np


class Shell:
    def __init__(self, w, c, e):
        self.angular_momenta = w
        self.coefficients = [[float(x) for x in i] for i in c]
        self.exponents = [float(x) for x in e]

    def __repr__(self):
        return f"""Shell {{
    angular_momenta: {self.angular_momenta},
    coefficients: {self.coefficients},
    exponents: {self.exponents},
}}"""


class Element:
    def __init__(self, atom, shells=None):
        if shells is None:
            shells = []
        self.atom = atom
        self.shells = shells

    def __repr__(self):
        return f"""{self.atom}: {self.shells}"""


def load_basis_set(filename):
    """load a basis set from filename and return it as a list of
    Elements

    """
    ptable = {
        "1": "H",
        "8": "O",
        }
    with open(filename) as f:
        s = json.load(f)
    elts = s['elements']
    elements = []
    for elt in elts:
        # coefficients are 2D, one row for each angular_momenta, I think
        # this means you actually don't need angular_momenta since the
        # position in coefficients is the angular_momentum
        e = Element(ptable[elt])
        for shell in elts[elt]['electron_shells']:
            e.shells.append(Shell(
                shell['angular_momentum'],
                shell['coefficients'],
                shell['exponents'],
                ))
        elements.append(e)
    return elements


def S(a, b):
    return 0


def K(ax, bx, a, b: float) -> float:
    "ax, bx coordinates; a, b orbital exponents"
    Qx = ax - bx
    # alpha and beta
    q = a*b / (a + b)
    return np.exp(-q*Qx**2)


def E(i, j, t: int, ax, bx, a, b: float):
    Qx = ax - bx
    # alpha and beta
    q = a*b / (a + b)
    p = a + b
    if t < 0 or t > i+j:
        return 0.0
    elif i == j == t == 0:
        return K(ax, bx, a, b)
    elif i > 0:
        return 1/(2*p) * E(i-1, j, t-1) \
            - q*Qx/a * E(i-1, j, t) \
            + (t+1) * E(i-1, j, t+1)
    else:
        return 1/(2*p) * E(i, j-1, t-1) \
            - q*Qx/b * E(i, j-1, t) \
            + (t+1) * E(i, j-1, t+1)


elements = load_basis_set("sets/sto-3g.json")
print(elements)
