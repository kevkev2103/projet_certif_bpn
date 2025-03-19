import pandas as pd
import os

file_path = "../data_brute/mediane revenu par UC.xlsx"
output_folder = "../data_clean/"
output_file = os.path.join(output_folder, "rev_med_com.csv")
xls = pd.ExcelFile(file_path)
df = pd.read_excel(xls, sheet_name="Data")

df_clean = df.iloc[4:].reset_index(drop=True)
df_clean.columns = ["codegeo","lib_geo","année", "stat_rev_med_com"]
df_clean["année"] = pd.to_numeric(df_clean["année"], errors= "coerce")
df_clean = df_clean.sort_values("année").groupby("codegeo").last().reset_index()

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

df_clean.to_csv(output_file, index= False)

