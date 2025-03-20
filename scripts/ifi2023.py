import pandas as pd
import os

file_path = "../data_brute/ifi 2023 par UC.xlsx"
output_folder = "../data_clean/"
output_file = os.path.join(output_folder, "ifi2023.csv")
xls = pd.ExcelFile(file_path)
df = pd.read_excel(xls)

df_clean = df.iloc[1:,:]
df_clean.columns=["Région","Département","Code commune", "Commune","Nombre redevables","Patrimoine moyen en €","Impôt Moyen en €"]

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

df_clean.to_csv(output_file, index= False)