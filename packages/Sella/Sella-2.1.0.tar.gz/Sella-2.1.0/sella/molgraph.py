from ase import Atoms
from ase.data import covalent_radii

import numpy as np

class MolGraph:
    def __init__(self, atoms: Atoms, max_bonds: int = 20) -> None:
        self.atoms = atoms
        self.rcov = covalent_radii[self.atoms.numbers]
        self.nbonds = np.zeros(self.natoms, dtype=np.int32)
        self.labels = -np.ones(self.natoms, dtype=np.int32)
        self.c10y = -np.ones((self.natoms, max_bonds), dtype=np.int32)

    @property
    def natoms(self) -> int:
        return len(self.atoms)

    @property
    def nfrags(self) -> int:
        "Calculates the number of molecular fragments."
        # Index of -1 means that the atom doesn't belong to any fragment
        n = (self.labels == -1).sum()
        fragset = set(self.labels)
        fragset.discard(-1)
        return n + len(fragset)
