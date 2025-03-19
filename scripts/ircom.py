import pandas as pd
import os

file_path = "../data_brute/ircom_communes_complet_revenus_2022.xlsx"
output_folder = "../data_clean/"
output_file = os.path.join(output_folder, "ircom.csv")
xls = pd.ExcelFile(file_path)
df = pd.read_excel(xls)

df_clean = df.iloc[6:-3,:6]
df_clean.columns = ["Departement","Commune","Lib Commune","Tranche RFR","Nombre foyers fiscaux","RFR"]
df_clean["RFR"] = df_clean["RFR"] * 1000


# Nettoyer et convertir en entier (remplace “n.c.” par NaN puis 0)
df_clean["Nombre foyers fiscaux"] = (
    pd.to_numeric(
        df_clean["Nombre foyers fiscaux"]
                 .astype(str)
                 .str.replace("\u00A0", "", regex=False)
                 .replace("n.c.", pd.NA),
        errors="coerce"
    )
    .fillna(0)
    .astype(int)
)


import pandas as pd
import os

# 📂 Charger le fichier Excel
file_path = "../data_brute/ircom_communes_complet_revenus_2022.xlsx"
output_folder = "../data_clean/"
output_file = os.path.join(output_folder, "ircom.csv")
xls = pd.ExcelFile(file_path)
df = pd.read_excel(xls)

# 🔹 Sélection des colonnes et nettoyage initial
df_clean = df.iloc[6:-3, :6]
df_clean.columns = ["Departement", "Commune", "Lib Commune", "Tranche RFR", "Nombre foyers fiscaux", "RFR"]
df_clean["RFR"] = df_clean["RFR"] * 1000

# 🔹 Nettoyer et convertir en entier (remplace “n.c.” par NaN puis 0)
for col in ["Nombre foyers fiscaux", "RFR"]:
    df_clean[col] = (
        pd.to_numeric(
            df_clean[col].astype(str).str.replace("\u00A0", "", regex=False).replace("n.c.", ""),
            errors="coerce"
        )
        .fillna(0)
    )

# 🔹 Fonction pour calculer médiane ou moyenne selon le cas
def compute_group_median(group):
    tranche = group[group["Tranche RFR"] != "Total"]
    total_row = group[group["Tranche RFR"] == "Total"]

    # Vérifier si une ligne "Total" est présente
    if not total_row.empty:
        total_row = total_row.iloc[0]
        total_foyers = total_row["Nombre foyers fiscaux"]
    else:
        total_foyers = 0

    if tranche.empty:
        # Cas où seule la ligne "Total" existe → moyenne simple
        if not total_row.empty and total_foyers != 0:
            return pd.Series({
                "Departement": total_row.get("Departement", None),
                "Commune": total_row.get("Commune", None),
                "Lib Commune": total_row.get("Lib Commune", None),
                "Nombre total de foyers fiscaux": total_foyers,
                "RFR": total_row["RFR"] / total_foyers
            })
        return pd.Series({"Departement": None, "Commune": None, "Lib Commune": None, "Nombre total de foyers fiscaux": None, "RFR": float("nan")})

    # 🔹 Sinon, interpolation de la médiane
    N = tranche["Nombre foyers fiscaux"].sum()
    half = N / 2
    cum = 0

    for _, row in tranche.iterrows():
        prev = cum
        cum += row["Nombre foyers fiscaux"]
        if cum >= half:
            if "à" in row["Tranche RFR"]:
                lo, hi = row["Tranche RFR"].split(" à ")
                lo, hi = float(lo.replace(" ", "")), float(hi.replace(" ", ""))
            else:
                lo = float(row["Tranche RFR"].split()[2].replace(" ", ""))
                hi = lo * 1.5
            return pd.Series({
                "Departement": row["Departement"],
                "Commune": row["Commune"],
                "Lib Commune": row["Lib Commune"],
                "Nombre total de foyers fiscaux": total_foyers,
                "RFR": lo + ((half - prev) / row["Nombre foyers fiscaux"]) * (hi - lo)
            })

# 🔹 Application sur tout le DataFrame
df_clean = (
    df_clean
    .sort_values(["Departement", "Commune"])
    .groupby(["Departement", "Commune"])
    .apply(compute_group_median)
    .reset_index(drop=True)  # Supprime les anciens index pour un affichage propre
)

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

df_clean.to_csv(output_file, index= False)