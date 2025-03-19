import pandas as pd
import os

file_path = "../data_brute/part des 25 34 ans titulaire diplome sup.xlsx"
output_folder = "../data_clean/"
output_file = os.path.join(output_folder, "diplome_sup_clean.csv")
xls = pd.ExcelFile(file_path)
df = pd.read_excel(xls, sheet_name="Data")

df_clean = df.iloc[4:].reset_index(drop=True)
df_clean.columns = ["codegeo","lib_geo","année", "stat_diplome"]
df_clean["année"] = pd.to_numeric(df_clean["année"], errors= "coerce")
df_clean = df_clean.sort_values("année").groupby("codegeo").last().reset_index()

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

df_clean.to_csv(output_file, index= False)