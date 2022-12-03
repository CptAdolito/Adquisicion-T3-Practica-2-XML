import pandas as pd
import re
import datetime

def limpiar_order_details(archivo):

    #El archivo nuevo se llama igual pero le quito los últimos 4 caracteres (.csv) y le añado limpio.csv
    archivo_nuevo = archivo[:-4] + "_limpio.csv"

    #Abro el archivo 'sucio' en lectura
    with open(archivo, 'r') as f:

        lines = f.readlines()

        #Abro el archivo 'limpio' en escritura
        with open(archivo_nuevo, 'w') as f2:

            for line in lines:
                line.strip()

                #Despues de un espacio hay un numero, lo cambio por ; (por posible error entre columnas)
                if ' ' in line and line[line.index(' ')+1].isdigit():
                    line = line.replace(' ', ';')

                #Despues de un espacio hay una letra, lo cambio por _ (por posible error en pizza_id)
                elif ' ' in line: # and line[line.index(' ')+1].isalpha()
                    line = line.replace(' ', '_')

                #Si hay un '-' lo cambio por un '_' (por posible error en pizza_id)
                if "-" in line:
                    line = line.replace("-", "_")

                #Si tiene 2 ';' seguidos o si acaba la linea con ';' es que faltan los datos de una columna, así que no tengo esa lina en cuenta
                if ';;' not in line and ';\n' not in line:
                    f2.write(line)

    #Sigo limpiando el archivo ahora con problemas de caracteres raros en numeros p.ej. 3 por e, @ por a, three por 3, etc.
    df = pd.read_csv(archivo_nuevo, sep=';')

    #Los numeros que están escritos con letras los cambio por numeros de verdad
    num_letra = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]
    num = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']

    for i in range(len(num_letra)):

        #Para no tener en cuenta las mayusculas y minusculas hago case=False
        df['quantity'] = df['quantity'].str.replace(num_letra[i], num[i], case=False)


    #Ahora cambio los caracteres raros por el valor que deberían tener
    car_error = ["@", "3", "4", "5", "6", "7", "8", "9", "0"]
    car_correcto = ["a", "e", "f", "s", "g", "t", "b", "g", "o"]

    for i in range(len(car_error)):

        df['pizza_id'] = df['pizza_id'].str.replace(car_error[i], car_correcto[i])

    #Guardo el archivo limpio
    df.to_csv(archivo_nuevo, sep=';', index=False)

def limpiar_order(archivo):

    #Abro el csv
    df = pd.read_csv(archivo, sep=';')

    #Elimino la columna 'time'
    df = df.drop(columns=['time'])

    #Elimino las filas con valores nulos o vacíos
    df = df.dropna()

    #Guardo el archivo limpio

    df.to_csv('data2016/orders_limpio.csv', sep=';', index=False) #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!



    df = pd.read_csv('data2016/orders_limpio.csv', sep=';')

    #Convierto la columna 'date' a datetime
    

    #If the value in df['date'] is a float, it is a date in python timestamp format
    #I will convert it to a date in the format YYYY-MM-DD
    for i in range(len(df['date'])):
        try:
            df.loc[i, 'date'] = float(df['date'][i])
            df.loc[i, 'date'] = datetime.datetime.fromtimestamp(df.loc[i, 'date']).strftime('%Y-%m-%d')
        except:
            pass
    df["date"] = pd.to_datetime(df["date"])

    #Quito los ultimos 8 caracteres de la columna 'date' (los que son la hora)
    df['date'] = df['date'].astype(str)
    df['date'] = df['date'].str[:-9]

    #guardo el archivo
    df.to_csv('data2016/orders_limpio.csv', sep=';', index=False)

if __name__ == "__main__":
    limpiar_order('data2016/orders.csv')
    limpiar_order_details('data2016/order_details.csv')
    print('Datos limpios')