import sys
import re

class SIExpression:
    def __init__(self, kg=0, m=0, s=0, A=0, K=0, mol=0, cd=0):
        self.kg = kg  # kilogram
        self.m = m    # meter
        self.s = s    # second
        self.A = A    # ampere
        self.K = K    # kelvin
        self.mol = mol  # mole
        self.cd = cd  # candela

    def __mul__(self, other):
        return SIExpression(
            self.kg + other.kg,
            self.m + other.m,
            self.s + other.s,
            self.A + other.A,
            self.K + other.K,
            self.mol + other.mol,
            self.cd + other.cd
        )

    def __eq__(self, other):
        return (
            self.kg == other.kg and
            self.m == other.m and
            self.s == other.s and
            self.A == other.A and
            self.K == other.K and
            self.mol == other.mol and
            self.cd == other.cd
        )

    def __str__(self):
        units = [
            ("kg", self.kg),
            ("m", self.m),
            ("s", self.s),
            ("A", self.A),
            ("K", self.K),
            ("mol", self.mol),
            ("cd", self.cd)
        ]
        return '*'.join([f"{unit}" if power == 1 else f"{unit}^{power}" for unit, power in units if power != 0]) or "1"

# Define a dictionary to map composed units to their SI expressions as SIExpression objects
unit_map = {
    "N": SIExpression(1, 1, -2),  # Newton: kg*m*s^-2
    "J": SIExpression(1, 2, -2),  # Joule: kg*m^2*s^-2
    "W": SIExpression(1, 2, -3),  # Watt: kg*m^2*s^-3
    "C": SIExpression(0, 0, 1, 1),  # Coulomb: A*s
    "V": SIExpression(1, 2, -3, -1),  # Volt: kg*m^2*s^-3*A^-1
    "ohm": SIExpression(1, 2, -3, -2),  # Ohm: kg*m^2*s^-3*A^-2
    "F": SIExpression(-1, -2, 4, 2),  # Farad: kg^-1*m^-2*s^4*A^2
    "H": SIExpression(1, 2, -2, -2),  # Henry: kg*m^2*s^-2*A^-2
    "T": SIExpression(1, 0, -2, -1),  # Tesla: kg*s^-2*A^-1
    "Wb": SIExpression(1, 2, -2, -1),  # Weber: kg*m^2*s^-2*A^-1
    "Hz": SIExpression(0, 0, -1),  # Hertz: s^-1
    "Pa": SIExpression(1, -1, -2),  # Pascal: kg*m^-1*s^-2
    "lx": SIExpression(0, -2, 0, 0, 0, 0, 1),  # Lux: m^-2*cd
    "S": SIExpression(-1, -2, 3, 2),  # Siemens: kg^-1*m^-2*s^3*A^2
    "m": SIExpression(0, 1),  # meter
    "s": SIExpression(0, 0, 1),  # second
    "kg": SIExpression(1),  # kilogram
    "A": SIExpression(0, 0, 0, 1),  # ampere
    "K": SIExpression(0, 0, 0, 0, 1),  # kelvin
    "mol": SIExpression(0, 0, 0, 0, 0, 1),  # mole
    "cd": SIExpression(0, 0, 0, 0, 0, 0, 1)  # candela
}

def parse_unit_with_power(unit_str):
    match = re.match(r"([a-zA-Z]+)(\^(-?\d+))?", unit_str)
    if match:
        unit = match.group(1)
        power = int(match.group(3)) if match.group(3) else 1
        return unit, power
    return unit_str, 1

def parse_and_convert(expression):
    # Split the expression by the multiplication operator
    units = expression.split('*')
    result_expression = SIExpression()

    for unit in units:
        unit_name, power = parse_unit_with_power(unit)
        if unit_name in unit_map:
            unit_si_expression = unit_map[unit_name]
            for _ in range(abs(power)):
                result_expression = result_expression * (unit_si_expression if power > 0 else SIExpression(
                    -unit_si_expression.kg, -unit_si_expression.m, -unit_si_expression.s, 
                    -unit_si_expression.A, -unit_si_expression.K, -unit_si_expression.mol, -unit_si_expression.cd
                ))
        else:
            print(f"Warning: Unit '{unit_name}' not found in the mapping.")

    # Print the result as a combined SI expression
    si_str = str(result_expression)
    match_found = False
    for key, value in unit_map.items():
        if result_expression == value:
            print(f"SI conversion of '{expression}': {si_str} = {key}")
            match_found = True
            break
    if not match_found:
        print(f"SI conversion of '{expression}': {si_str}")

# Take input from command line arguments
if len(sys.argv) > 1:
    input_expression = sys.argv[1]
    parse_and_convert(input_expression)
else:
    print("Please provide a units expression as a command line argument.")
