import pandas as pd
import xml.etree.ElementTree as ET
from xml.dom import minidom


def indentar(elem):
    #Pone los strings para que se vean bien en el xml
    string = ET.tostring(elem, 'utf-8')
    string_bien = minidom.parseString(string)
    return string_bien.toprettyxml(indent="  ")


def analisis(df, f):
    
    #Atencion con los nombres, no se pueden usar espacios
    ET.SubElement(f,"Total_de_Nans_por_comlumna").text = str(df.isna().sum())
    ET.SubElement(f,"Total_de_Nulls_por_columna").text = str(df.isnull().sum())
    ET.SubElement(f,"Data_type_por_columna").text = str(df.dtypes)


def informe():
    
    #Abrimos el xml
    archivo = "data2016/informe.xml"

    #Usamos los archivos limpiados de antes
    datos =  ("data2016/orders_limpio.csv", "data2016/order_details_limpio.csv")

    #Creamos el xml
    raiz = ET.Element("root")

    #Guardamos los subelementos como tablas
    for i in datos:
        tabla = ET.SubElement(raiz, "tabla")
        tabla.set("archivo_csv", i)
        analisis(pd.read_csv(i, sep=';', encoding="LATIN_1"), tabla)

    #Guardamos el xml
    with open(archivo, "w") as f:
        f.write(indentar(raiz))
    print("Informe finalizado")


if __name__ == "__main__":
    informe()