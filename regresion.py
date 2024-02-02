# Importación de bibliotecas necesarias
import pandas as pd
import numpy as np

# Carga de datos desde un archivo de texto
datos = pd.read_table("data\sample_endi_10p.txt")

# Descripción estadística de los datos
datos.describe()

# Creación de una tabla cruzada entre sexo y desnutrición crónica
tabla_cruzada = pd.crosstab(datos["sexo"], datos["dcronica"])

# Cálculo del total de observaciones
total = tabla_cruzada.sum().sum()

# Normalización de la tabla cruzada para obtener proporciones
tabla_cruzada / total

# Creación de una nueva variable categórica basada en 'dcronica'
datos["dcronica_factor"] = datos["dcronica"].apply(lambda x: "Desnutrición" if x == 1 else "No")

# Creación de una nueva tabla cruzada incluyendo la categoría 'All' (márgenes)
tabla_cruzada = pd.crosstab(datos["sexo"], datos["dcronica_factor"], margins=True)

# Normalización de la tabla cruzada para obtener proporciones
tabla_cruzada / total

# Creación de una nueva variable para clasificar el tamaño del hogar
datos["tamanio_hogar"] = datos["n_hijos"].apply(lambda x: "Hogar grande" if x > 3 else "Hogar pequeño")

# Nueva tabla cruzada entre desnutrición crónica y sexo
cruzada_2 = pd.crosstab(datos["dcronica"], datos["sexo"])

# Cálculo del total de observaciones para la segunda tabla cruzada
total_2 = cruzada_2.sum().sum()

# Normalización de la segunda tabla cruzada para obtener proporciones, incluyendo 'All'
pd.crosstab(datos["dcronica"], datos["sexo"], margins=True) / total_2

# Creación de una tabla pivot para resumen estadístico por sexo y desnutrición crónica
pd.pivot_table(datos, values="n_hijos", index=["sexo", "dcronica"], aggfunc=["count", "sum", "mean", "max"])

# Versión más detallada de la tabla pivot con funciones personalizadas
pivot_table = pd.pivot_table(datos, values='n_hijos', index=['sexo', 'dcronica'], 
                             aggfunc={'n_hijos': [ 'mean', 
                                                   ("casos", lambda x: x.count()),
                                                   ("proporcion", lambda x: x.count()/total_2)
                                                 ]})

# Importación de la clase LinearRegression para realizar regresión lineal
from sklearn.linear_model import LinearRegression
# Importación de matplotlib para graficación
import matplotlib.pyplot as plt
# Importación de statsmodels para análisis estadístico
import statsmodels.api as sm

# Simulación de datos para la regresión lineal
np.random.seed(451)
x = np.random.rand(100) * 10  # Valores aleatorios uniformemente distribuidos
error = np.random.randn(100)  # Error normalmente distribuido
y = 3.5 + 1.7 * x + error  # Variable dependiente simulada

# Ajuste del modelo de regresión lineal con mínimos cuadrados
model = LinearRegression()
result = model.fit(x.reshape(-1, 1), y)

# Impresión de coeficientes y estadísticas del modelo
print(result.coef_)
print(result.intercept_)

# Graficación de datos y la línea de regresión ajustada
plt.scatter(x, y)
plt.plot(x, result.predict(x.reshape(-1, 1)), color='red')  # Línea de regresión
plt.show()

# Preparación de datos para una prueba de hipótesis (eliminación de NA)
datos = datos[~datos["dcronica"].isna()]
datos = datos[~datos["n_hijos"].isna()]

# Variables para el modelo
x = datos["dcronica"]
y = datos["n_hijos"]
x2 = sm.add_constant(x)  # Añadir constante al modelo

# Ajuste del modelo de regresión lineal usando statsmodels
est = sm.OLS(y, x2)
est2 = est.fit()

# Impresión del resumen del modelo ajustado
print(est2.summary())
