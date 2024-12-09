import pandas as pd
import datetime as dt

dataFrame = pd.read_csv("Aufagben/Transformation/FinancialSample.csv",
                        sep=";",
                        encoding="utf-8-sig")

# Überprüfen, ob die Spalte "Date" vorhanden ist

for date in dataFrame["Date"]:
    newDate = []
    if "/" in date:
        newDate.append(date.split("/"))
        


print(dataFrame.tail(10))

#print only date column
for date in dataFrame["Date"]:
    date = dt.datetime.strptime(date, "%d.%m.%Y")
    print(date.strftime("%m.%d.%Y"))


    """
    #one die library zu verwenden.
    date = date.split(".")
    date = date[1] + "." + date[0] + "." + date[2]
    print(date)"""

#read a file with panda

