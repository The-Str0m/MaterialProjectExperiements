from mp_api.client import MPRester
import re
import pandas as pd

with MPRester("your-api-key") as mpr:
    chemical_formula = input("Enter an element or compound: ")
    count = len(re.findall(r'[A-Z]', chemical_formula))
    formulas = []
    band_gaps = []
    id = []
    if count == 1 and not bool(re.search(r'\d', chemical_formula)):
        docs = mpr.materials.summary.search(
            elements=[chemical_formula], fields=["formula_pretty", "band_gap", "material_id"]
        )
        for compound in docs:
            formulas.append(compound.formula_pretty)
            band_gaps.append(compound.band_gap)
            id.append(compound.material_id)
    else:
        docs = mpr.materials.summary.search(
            formula=chemical_formula, fields=["formula_pretty", "band_gap", "material_id"]
        )
        for compound in docs:
            formulas.append(compound.formula_pretty)
            band_gaps.append(compound.band_gap)
            id.append(compound.material_id)
    df = pd.DataFrame({
        'Chemical Formula': formulas,
        'Band Gap': band_gaps,
        "Material Ids": id
    })
    df.to_csv('materials.csv', index=True)
