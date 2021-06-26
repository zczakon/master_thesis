import itertools
import numpy as np


def translate_to_lexicographic(generators: iter):
    pass


def ordered_forms(generators: iter, deg: int):
    if not 1 <= deg < len(generators):
        print('degree not allowed')
        return

    # generators=translate_to_lexicographic(generators)

    generators = list(itertools.combinations(generators, deg))
    unique = list(set(generators))
    return sorted(list(unique))


def extract_vector(element):  # of the form Chain(1:(0, 1, 0, 0))
    element = str(element)
    # vector=str((list(cochain.homology(generators=True).values())[1][1][1]))
    gen = element[9:len(element) - 2]
    gen = gen.replace(', ', '')
    gen = gen.replace('-', '')

    vector = [int(gen[i]) for i in range(len(gen))]
    return vector


# i have a list of tuples [(Vector space of dimension 1 over Rational Field, Chain(1:(1, 0, 0, 0))),
#                         (Vector space of dimension 1 over Rational Field, Chain(1:(0, 1, 0, 0))),
#                         (Vector space of dimension 1 over Rational Field, Chain(1:(0, 0, 0, 1)))]

def translate_to_forms(homology_gens: list, deg: int, generators: iter):
    """
    return list of lists which are wedge products of generating forms. list(x^y^z, y^z^w,...)
    """
    homology_gens = homology_gens[0]

    generating_forms = []
    for n in range(len(homology_gens)):
        # vector = extract part of a string
        vector = extract_vector(homology_gens[n][1])
        generating_forms.append([])
        for i in range(len(vector)):
            if vector[i] != 0:
                generating_forms[n].append(ordered_forms(generators, deg)[i])
    return generating_forms


def cohomology_deg(cohomology: dict, deg: int):
    li = [cohomology[key] for key in cohomology.keys() if key == deg]
    return li


def generate_cohomology(lie_algebra, deg):
    generators = list(lie_algebra.gens())

    if deg == 0 or deg >= len(generators):
        print('degree not allowed')
        return

    cochain = lie_algebra.chevalley_eilenberg_complex(dual=True)
    cohomology = cochain.homology(generators=True)
    cohomologies = [cohomology_deg(cohomology, n) for n in range(len(cohomology.keys()))]

    return translate_to_forms(cohomologies[deg], deg=deg, generators=generators)


def display(list_of_generators: iter):
    for i in range(len(list_of_generators)):
        tuple = (list_of_generators[i][0])
        string = str(tuple).replace(', ', '^')
        string = string.replace('(', '[')
        string = string.replace(')', ']')

        if len(string) == 5:  # forms of deg 1
            string = string.replace(',', '')
        print(string)
    pass

