import pandas as pd
import datetime as dt

dataFrame = pd.read_csv("Aufagben/Transformation/FinancialSample.csv",
                        sep=";",
                        encoding="utf-8-sig")
dataFrame.columns = dataFrame.columns.str.strip()
# Überprüfen, ob die Spalte "Date" vorhanden ist


print(dataFrame.tail(10))


#Aufgabe 2

#print only date column
for date in dataFrame["Date"]:
    date = dt.datetime.strptime(date, "%d.%m.%Y")
    print(date.strftime("%m.%d.%Y"))


    """
    #one die library zu verwenden.
    date = date.split(".")
    date = date[1] + "." + date[0] + "." + date[2]
    print(date) """

#Aufgabe 3
#Erzeugt ein neues Pandas Dataframe, welches nur die folgenden Spalten enthält und gebt die ersten 5 Einträge aus: 
#Product, Profit, COGS, Sales


newDataFrame = dataFrame[["Product", "Profit", "COGS", "Sales"]]
print(newDataFrame.head(5))


#Aufgabe 4
#Lest die Spalten “Month Number”, “Month Name” und “Year” in eine einzige 
#Spalte mit einem kombinierten Datum aus allen drei Bestandteilen und löscht 
#den Rest.

dataFrame["Datum"] = dataFrame["Month Number"].astype(str) + "." + dataFrame["Month Name"] + "." + dataFrame["Year"].astype(str)
print(dataFrame["Datum"])

#Aufgabe 5
#Findet die Positionen der zehn größten lokalen Maxima. Ein lokales Maximum ist 
#ein Wert, der von zwei kleineren Werten umschlossen wird. Zum Beispiel [1, 3, 8, 
#5, 10, 4] → 8 und 10 sind lokale Maxima. Das Ergebnis lautet in dem Fall also 
#Position 2 und Position 4.

maxima = []
for i in range(1, len(dataFrame["Profit"]) - 1):
    if dataFrame["Profit"][i] > dataFrame["Profit"][i - 1] and dataFrame["Profit"][i] > dataFrame["Profit"][i + 1]:
        maxima.append(i)
print(maxima)
