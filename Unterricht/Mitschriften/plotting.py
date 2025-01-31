import random
import datetime as dt
import os

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


def convert_str_amount_to_float(amount: str) -> float:
    "Konvertiert einen Betrag in string Form zu einem float"
    if amount.strip() == "$-":
        return 0.0
    else:
        return float(amount
                     .replace("$", "")
                     .replace(".", "")
                     .replace(")", "")
                     .replace("(", "")
                     .replace(",", ".")
                     )


def calculate_counts(data: list) -> tuple[list, list]:
    "Kalkuliert wie häufig ein listenelement vorkommt"

    counts = {}
    for data_point in data:
        if data_point in counts:
            counts[data_point] += 1
        else:
            counts[data_point] = 1

    return zip(*counts.items())


def random_color() -> str:
    "Generiert eine zufällige Farbe"

    return random.choice(list(mcolors.CSS4_COLORS.keys()))


def random_colors(n: int) -> list[str]:
    "Generiert n zufällige Farben"

    return [random_color() for _ in range(n)]


def plot_bar_chart(
    data: list,
    ylabe: str,
    title: str
) -> None:

    fig, ax = plt.subplots()

    countries, values = calculate_counts(data)
    ax.bar(countries, values, color=random_colors(len(countries)))
    ax.set_ylabel(ylabe)
    ax.set_title(title)

    plt.show()


def plot_pie_chart(
        data: list
) -> None:
    """Plottet einen Pie-Chart"""

    lables, sizes = calculate_counts(data)
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=lables, autopct="%1.1f%%",
           colors=random_colors(len(lables)))

    plt.show()


def plt_timeseries(
        data: list,
        time: list,
        title: str
) -> None:
    "Plottet eine Zeitreihe"

    x_axis = [dt.datetime.strptime(date, "%d.%m.%Y").strftime(
        "%d/%m/%Y") for date in time]

    plt.plot(x_axis, data)
    plt.title(title)

    plt.show()


def main() -> None:

    financial_data = pd.read_csv(
        "Unterricht/Mitschriften/FinancialSample.csv", sep=";")

    financial_data.columns = list(
        map(lambda x: x.strip(), financial_data.columns))

    """
    plot_bar_chart(
        financial_data["Country"],
        "Countries",
        "Country Plot"
    )

    """
    """
    plot_pie_chart(
        financial_data["Product"],
    )
    """
    cleaned_up_sales_data = list(
        map(convert_str_amount_to_float, financial_data["Sales"]))
    zipped_sales_per_date = tuple(
        zip(cleaned_up_sales_data, financial_data["Date"].to_list()))

    sales_transform = {}

    for sale in zipped_sales_per_date:
        if sale[1] not in sales_transform:
            sales_transform[sale[1]] = sale[0]
        else:
            sales_transform[sale[1]] += sale[0]

    dates, total_sales_amount = zip(*sales_transform.items())

    plt_timeseries(
        total_sales_amount,
        dates,
        "Verkäufe nach Datum",
    )


if __name__ == "__main__":
    main()
