PATH: str = "Aufagben/Extraction/FinancialSample.csv"

def read_csv(path: str = PATH) -> dict: 
    financial_sample: dict = {}

    with open(path, encoding="utf-8-sig") as datei:
        # Init dictionary with empty lists
        for value in datei.readline().split(";"):
            value = value.strip()
            financial_sample[value] = []

        # Get indexes (list of keys. 0 = "Segment", ...)
        index: list = list(financial_sample.keys())

        for i, line in enumerate(datei):
            # Append values to financial_sample
            for j, value in enumerate(line.split(";")):
                financial_sample[index[j]].append(value.strip())
            
    return financial_sample

def units_sold(dictionary: dict = read_csv()) -> None:
    """Prints the top 3, bottom 3 and average of the "Units Sold" column"""
    unit_sold_values: list = [float(value.replace(",", ".")) for value in dictionary["Units Sold"]]

    top_3_values: list = sorted(unit_sold_values, reverse=True)[:3]
    bottom_3_values: list = sorted(unit_sold_values)[:3]
    average_value: float = sum(unit_sold_values) / len(unit_sold_values)

    print("Highest Values", top_3_values,"Lowest Values", bottom_3_values, "Average",  average_value )

def usd_to_eur(usd: any) -> any:
    # Early return for non-USD values
    if "$" not in usd:
        return usd
    if "-" in usd:
        return usd.replace("$", "€")
    
    # Remove bloat
    usd = usd.replace(" ", "").replace(".", "").replace(",", ".").replace("(", "").replace(")", "")

    # Convert USD to EUR
    eur = str(round(float(usd.replace("$", ""))*1.07, 2))
    # Add 0 if necessary
    while True:
        if len(eur.split(".")[1]) < 2:
            eur += "0"
        else:
            break

    # Add € to the string
    if usd.startswith("$"):
        usd = f'€{eur}'
    else:
        usd = f'{eur}€'

    return usd

def dollar(dictionary: dict = read_csv()) -> dict:
    new_dict: dict = {}

    for key in dictionary:
        new_dict[key] = [usd_to_eur(value) for value in dictionary[key]]
    return new_dict

def print_dict(dictionary: dict = read_csv()) -> str:
    print("{")
    for keys, values in dictionary.items():
        string: str = "["
        for value in values[:2]:
            string+= f'"{value}",'
        string = f"{string}...]"
        print(f'"{keys}": {string},')
    print("}")

def month_as_number(month: str) -> int:
    months: dict = {
        "January": 1,
        "February": 2,
        "March": 3,
        "April": 4,
        "May": 5,
        "June": 6,
        "July": 7,
        "August": 8,
        "September": 9,
        "October": 10,
        "November": 11,
        "December": 12
    }

    return months[month]

def count_rows_with_year(dictionary: dict = read_csv(), year: int = 9999) -> int:
    count: int = 0
    for i in dictionary["Year"]:
        if int(i) == year:
            count += 1
    return count

def count_rows_without_discount(dictionary: dict = read_csv()) -> int:
    count: int = 0
    for i in dictionary["Discounts"]:
        if "-" in i:
            count += 1
    return count

if __name__ == "__main__":
    financial_sample = read_csv()

    # 1)
    print("1)")
    print_dict(financial_sample)
    
    # 2)
    print("\n2)")
    units_sold(financial_sample)
    
    # 3)
    print("\n3)")
    print(dollar(financial_sample)["Manufacturing Price"][:30:10])
    
    # 4)
    print("\n4)")
    print(count_rows_with_year(financial_sample, 2013))
    print(count_rows_with_year(financial_sample, 2014))
    print(count_rows_without_discount(financial_sample))

    # 5)
    print("\n5)")
    print([month_as_number(i) for i in financial_sample["Month Name"]])