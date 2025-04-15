import pandas as pd
import os

file_path = "../data_brute/disparites_h_f.xlsx"
output_folder = "../data_clean/"
output_file = os.path.join(output_folder, "disparites_h_f.csv")
xls = pd.ExcelFile(file_path)

df = pd.read_excel(xls, sheet_name="Figure 2")
df_csp=df.iloc[4:8,0:3]
df_csp.columns = ["catégorie socio-pro","Femmes","Hommes"]
df_csp.iloc[0,0]="Cadres"

df_variation = df.iloc[9:14,[0,2]]
mediane = df_variation.iloc[2,1]
df_variation["coefficient ajustement"] = 1+((df_variation.iloc[:,1]-mediane)/mediane)
df_tranche_age = df_variation.iloc[:,[0,2]]
df_tranche_age.columns = ["écart salaire par tranche d'âge","coefficient ajustement"]

# Initialisation de la liste des résultats
data = []

# Boucles sur chaque combinaison possible
for _, row_csp in df_csp.iterrows():
    for sexe in ["Femmes", "Hommes"]:
        salaire_base = row_csp[sexe]
        for _, row_age in df_tranche_age.iterrows():
            data.append({
                "catégorie socio-pro": row_csp["catégorie socio-pro"],
                "sexe": sexe[:-1],  # Enlève le 's' à la fin pour "Femme" / "Homme"
                "tranche d'âge": row_age["écart salaire par tranche d'âge"],
                "salaire_median": round(salaire_base * row_age["coefficient ajustement"], 2)
            })

# Création du DataFrame final
df_resultat = pd.DataFrame(data)

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

df_resultat.to_csv(output_file, index= False)
