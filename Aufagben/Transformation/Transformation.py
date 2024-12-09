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
