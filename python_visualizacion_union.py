# Este será mi script para visualización
import pandas as pd
import numpy as np
import matplotlib.pyplot  as plt
import seaborn as sns


# Primero usamos exit() para salir de python e ir a poweshell
# Luego usamos:
# python -m pip install xlrd
# o pip install xlrd
# Depende del caso

df_countries = pd.read_excel("data\API_GC.REV.XGRT.GD.ZS_DS2_es_excel_v2_6362010.xls",sheet_name="Metadata - Countries")

df_index = pd.read_excel("data\API_GC.REV.XGRT.GD.ZS_DS2_es_excel_v2_6362010.xls",sheet_name="Data",skiprows=  3)

# Cuantos paises tienen ingresos mediano alto

grouped_c = df_countries.groupby("Income_Group").size().reset_index(name = "Frecuencia")

# Son 54 paises

plt.bar(grouped_c["Income_Group"],grouped_c["Frecuencia"])

plt.show()

grouped_c["Income_Group"] = grouped_c["Income_Group"].astype("category")

grouped_c["Income_Group"] = grouped_c["Income_Group"].cat.reorder_categories(['Países de ingreso bajo',
                                                  'Países de ingreso mediano bajo', 
                                                  'Ingreso mediano alto', 'Ingreso alto',
                                                  'Agregados', 
                                                  'No clasificado'])


sns.barplot(
    data=grouped_c,
    x='Income_Group',
    y="Frecuencia", 
    order = ['Países de ingreso bajo',
             'Países de ingreso mediano bajo', 
             'Ingreso mediano alto', 'Ingreso alto',
             'Agregados', 
             'No clasificado']
)

plt.show()

grouped_c = df_countries.groupby(["Income_Group","Region"]).size().reset_index(name = "Frecuencia")

df_countries.groupby(["Region"]).size().reset_index(name = "Frecuencia")

ancho = 0.10

sns.barplot(
    data=grouped_c,
    y="Region",
    x="Frecuencia", 
    hue="Income_Group"
)

plt.show()


# Como filtrar un dataframe:

index_ecuador = df_index["Country Name"] == "Ecuador"

df_index[index_ecuador]

index_paises = df_index["Country Name"].isin(["Ecuador","Colombia"])

df_index[index_paises]

# Como obtengo los indicadores de America Latina

america_latina = df_countries[df_countries["Region"] == "América Latina y el Caribe (excluido altos ingresos)"]

df_index.merge(america_latina,on= ["Country Name" , "Country Code"],how = "left")

america_latina.merge(df_index,on= ["Country Name" , "Country Code"],how = "left")