from mp_api.client import MPRester
from ase.visualize import view
from pymatgen.io.ase import AseAtomsAdaptor

with MPRester("yQ1u3WrfYKDCHDtpke7iPYVq86jKwhyx") as mpr:
    chemical_formula = input('Enter a molecule ')
    docs = mpr.materials.summary.search(
            formula=[chemical_formula], fields=["material_id"]
        )
    if len(docs) > 3:
        choice = input('There are more than 3 matching compounds, would you like to continue? (y/n) ')
        if choice == 'y':
            for compound in docs:
                structure = mpr.get_structure_by_material_id(compound.material_id)
                ase_structure = AseAtomsAdaptor.get_atoms(structure)
                view(ase_structure)
        else:
            for x in range(3):
                structure = mpr.get_structure_by_material_id(docs[x].material_id)
                ase_structure = AseAtomsAdaptor.get_atoms(structure)
                view(ase_structure)

    else:
        for compound in docs:
            structure = mpr.get_structure_by_material_id(compound.material_id)
            ase_structure = AseAtomsAdaptor.get_atoms(structure)
            view(ase_structure)
