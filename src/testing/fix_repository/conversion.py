
from fix_repository.values import masse_kg

def convert_kg_to_g(a: float):
    return a * 100


masse_g = convert_kg_to_g(masse_kg)

assert masse_g*1000 == masse_kg       
    