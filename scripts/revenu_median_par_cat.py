import pandas as pd
import os

# 📂 Définition des chemins
input_file = "../data_brute/revenus médian par catégorie socio pro.xlsx"
output_folder = "../data_clean/"
output_file = os.path.join(output_folder, "revenus_median_par_cat.csv")

# ✅ Charger le fichier Excel
xls = pd.ExcelFile(input_file)
df = pd.read_excel(xls, sheet_name="Données")

# ✅ Nettoyage des données
df_modified = df.iloc[:, [0, -1]]  # Garder uniquement la première et la dernière colonne
df_modified = df_modified.iloc[3:8].reset_index(drop=True)  # Garder uniquement les lignes 4 à 8
df_modified.columns = ["CSP", "Revenu Médian 2022"]  # Renommer les colonnes
df_modified.iloc[4, 0] = "Ouvriers"  # Modifier la ligne correspondante

# 📂 Vérifier que le dossier de sortie existe
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# ✅ Sauvegarde des données nettoyées en CSV
df_modified.to_csv(output_file, index=False)

print(f"✅ Données nettoyées enregistrées dans : {output_file}")
