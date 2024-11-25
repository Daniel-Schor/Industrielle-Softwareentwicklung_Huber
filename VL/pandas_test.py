import pandas as pd
import matplotlib.pyplot as plt


PATH = "Aufagben/Extraction/FinancialSample.csv"
SEPERATOR = ";"

financials = pd.read_csv(PATH, sep=SEPERATOR)

financials["Units Sold"] = financials["Units Sold"].apply(lambda x: float(x.replace(",", ".")))

financials.plot()

plt.show()