import pandas as pd


def get_country_name_list(
        data: list[dict]
) -> list:
    """
        Gibt eine Liste der Länder zurück, die in den Daten enthalten sind. Die Reihenfolge entspricht der Reihenfolge in den Daten.

    :param data: Die Daten als Liste von Dictionaries.

    :return: Eine Liste der Länder, die in den Daten enthalten sind.
    """

    countries = []

    for row in data:
        if row["Country"] not in countries:
            countries.append(row["Country"])

    return countries


def convert_to_dataframe(
        data: dict
) -> pd.DataFrame:
    """
        Konvertiert Daten in ein DataFrame

    :param data: Die Daten, die in ein DataFrame konvertiert werden sollen
    :return: Ein DataFrame mit den konvertierten Daten
    """

    if not data:
        return pd.DataFrame()

    return pd.DataFrame(data)
