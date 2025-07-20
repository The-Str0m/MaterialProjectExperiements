from mp_api.client import MPRester
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import re

with MPRester("your-api-here") as mpr:
    chemical_formula = input("Enter an element or compound: ")
    count = len(re.findall(r'[A-Z]', chemical_formula))
    band_gaps = []
    density = []
    crystalstructure = []
    if count == 1 and not bool(re.search(r'\d', chemical_formula)):
        docs = mpr.materials.summary.search(
            formula=chemical_formula, fields=["band_gap", "density", "symmetry"]
        )
        for compound in docs:
            band_gaps.append(compound.band_gap)
            density.append(compound.density)
            crystalstructure.append(compound.symmetry.crystal_system.value)
    else:
        docs = mpr.materials.summary.search(
            formula=chemical_formula, fields=["band_gap", "density", "symmetry"]
        )
        for compound in docs:
            band_gaps.append(compound.band_gap)
            density.append(compound.density)
            crystalstructure.append(compound.symmetry.crystal_system.value)
    colour_map = {
        "Triclinic": "red",
        "Monoclinic": "orange",
        "Orthorhombic": "yellow",
        "Tetragonal": "green",
        "Trigonal": "blue",
        "Hexagonal": "indigo",
        "Cubic": "violet"
    }
    colours = [colour_map[c] for c in crystalstructure]
    fig, ax = plt.subplots()
    ax.scatter(density, band_gaps, c=colours)
    legend_handles = [Patch(color=color, label=system) for system, color in colour_map.items()]
    ax.legend(handles=legend_handles, title="Crystal System", loc="lower right", fontsize="small", title_fontsize="small", markerscale=0.7)
    ax.set_ylabel("Band Gaps (in eV)")
    ax.set_xlabel("Density (in g.cm-3)")
    ax.set_title("Band-Gap vs Density Graph")
    plt.show()
