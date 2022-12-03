import xml.etree.ElementTree as ET
import pandas as pd



def indentar(elem, level=0):

    i = "\n" + level*"  "
    j = "\n" + (level-1)*"  "

    if len(elem):

        if not elem.text or not elem.text.strip():
            elem.text = i + "  "

        if not elem.tail or not elem.tail.strip():
            elem.tail = i

        for subelem in elem:
            indentar(subelem, level+1)

        if not elem.tail or not elem.tail.strip():
            elem.tail = j

    else:
        
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = j


def csv_to_xml(df, f):

    #Creo la raiz del xml
    raiz = ET.Element("root")

    for i in df.index:

        #Creo los subelementos de la raiz como filas
        filas = ET.SubElement(raiz, "filas")
        #Cada fila tiene un índice
        filas.set("indice", str(i))

        #Añdadimos los elementos de la fila (columnas del csv)
        #Columna de ingredientes coge el valor de ingredientes
        #Columna de cantidad coge el valor de cantidad
        for j in df.columns:
            ET.SubElement(filas, j).text = str(df.loc[i,j])


    indentar(raiz)

    #Creo el archivo xml sobre la raiz y lo guardo
    arbol = ET.ElementTree(raiz)
    arbol.write(f)


if __name__ == "__main__":

    df = pd.read_csv("data2016/proxima_compra.csv")
    csv_to_xml(df, "data2016/proxima_compra.xml")