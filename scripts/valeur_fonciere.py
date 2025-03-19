import pandas as pd
import os

input_file = "../data_brute/valeurs foncières2023.csv"
output_folder = "../data_clean/"
output_file = os.path.join(output_folder,"valeur_fonciere.csv")

df = pd.read_csv(input_file, delimiter = ",")
df_modified = df.iloc[:,[1,-2]]

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

df_modified.to_csv(output_file, index =False)

