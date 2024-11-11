PATH: str = "Aufagben/Extraction/FinancialSample.csv"

def read_csv(path: str = PATH) -> dict: 
    financial_sample: dict = {}

    with open(path, encoding="utf-8-sig") as datei:
        # Init dictionary with empty lists
        for value in datei.readline().split(";"):
            value = value.strip()
            financial_sample[value] = []

        # Get indexes
        index = list(financial_sample.keys())

        for i, line in enumerate(datei):
            # Append values to financial_sample
            for j, value in enumerate(line.split(";")):
                financial_sample[index[j]].append(value.strip())
            
            # Break after 3 values
            #if i >= 2:
            #    break

    return financial_sample


def units_sold(dictionary: dict) -> None:
    """Prints the top 3, bottom 3 and average of the "Units Sold" column"""
    unit_sold_values = [float(value.replace(",", ".")) for value in dictionary["Units Sold"]]

    top_3_values = sorted(unit_sold_values, reverse=True)[:3]
    bottom_3_values = sorted(unit_sold_values)[:3]
    average_value = sum(unit_sold_values) / len(unit_sold_values)

    print("Highest Values", top_3_values,"Lowest Values", bottom_3_values, "Average",  average_value )

def dollar():
    pass

if __name__ == "__main__":
    financial_sample = read_csv()
    #units_sold(financial_sample)

    