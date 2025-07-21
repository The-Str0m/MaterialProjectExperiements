from mp_api.client import MPRester
from pymatgen.core import Composition
from matminer.featurizers.composition import ElementProperty
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, r2_score


data = []
featurizer = ElementProperty.from_preset("magpie")
with MPRester("yQ1u3WrfYKDCHDtpke7iPYVq86jKwhyx") as mpr:
    docs = mpr.materials.summary.search(
        elements=['C'], fields=["band_gap", "density", "material_id", "formula_pretty"]
    )
    for element in docs:
        comp = Composition(element.formula_pretty)
        features = featurizer.featurize(comp)
        row = {
            "material_id": element.material_id,
            "formula":  element.formula_pretty,
            "band_gap": element.band_gap,
            "density": element.density
        }
        feature_labels = featurizer.feature_labels()
        for label, value in zip(feature_labels, features):
            row[label] = value
        data.append(row)

df = pd.DataFrame(data)
df = df.dropna(subset=["band_gap"])
df = df.drop_duplicates()
X = df.drop(columns=["band_gap", "material_id", "formula"])
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
y = df["band_gap"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=6942
)
model = XGBRegressor(
    n_estimators=100,
    learning_rate=0.1,
    max_depth=5,
    random_state=6942
)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print("MAE:", mae)
print("R² score:", r2)

#uses XBGRegressor, magpie featuriser preset, basic data clean-up
#MAE is 0.7211464745612793, R^2 is 0.6375072420632402
