"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""
import pandas as pd
import os
import glob


def pregunta_01():
    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.

    El archivo limpio debe escribirse en "files/output/solicitudes_de_credito.csv"

    """
    archivo_entrada = "files/input/solicitudes_de_credito.csv"
    carpeta_salida = "files/output"
    
    datos = pd.read_csv(archivo_entrada, index_col=0, sep=";")
    datos = datos.copy()
    datos = datos.dropna()
    
    columnas = datos.columns.to_list()
    
    for col in columnas:
        if datos[col].dtype == "object" and col != "barrio":
            datos[col] = (
                datos[col]
                .str.lower()
                .str.replace("-", " ", regex=False)
                .str.replace("_", " ", regex=False)
                .str.strip()
            )
    
    datos["comuna_ciudadano"] = datos["comuna_ciudadano"].astype(int)
    datos["monto_del_credito"] = (
        pd.to_numeric(
            datos["monto_del_credito"]
            .str.replace("$", "", regex=False)
            .str.replace(",", "", regex=False)
            .str.replace(" ", "", regex=False)
        ).astype(int)
    )
    datos["barrio"] = (
        datos["barrio"]
        .str.lower()
        .str.replace("-", " ", regex=False)
        .str.replace("_", " ", regex=False)
    )
    datos["fecha_de_beneficio"] = datos["fecha_de_beneficio"].apply(
        lambda x: f"{x.split('/')[2]}/{x.split('/')[1]}/{x.split('/')[0]}"
        if len(x.split('/')[0]) == 4
        else x
    )
    
    datos = datos.drop_duplicates()
    
    if os.path.exists(carpeta_salida):
        for f in glob.glob(f"{carpeta_salida}/*"):
            os.remove(f)
        os.rmdir(carpeta_salida)
    os.makedirs(carpeta_salida)
    
    datos.to_csv(os.path.join(carpeta_salida, "solicitudes_de_credito.csv"), sep=";", index=False)
    
    return
