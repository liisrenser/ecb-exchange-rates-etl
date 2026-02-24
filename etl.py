import requests
import zipfile
import sys


r_today = requests.get('https://www.ecb.europa.eu/stats/eurofxref/eurofxref.zip')
r_history = requests.get('https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist.zip')


def extract_history():
    with open('data.zip2', 'wb') as f1:
        f1.write(r_history.content)

    rows = []
    with zipfile.ZipFile('data.zip2', 'r') as data_zip:
        csv_name = data_zip.namelist()[0]
        with data_zip.open(csv_name) as data:
            for row in data:
                rows.append(row.decode("utf-8").strip())
    return rows

def extract_today():
    with open('data.zip2', 'wb') as f2:
        f2.write(r_today.content)

    rows = []
    with zipfile.ZipFile('data.zip2', 'r') as data_zip:
        csv_name = data_zip.namelist()[0]
        with data_zip.open(csv_name) as data:
            for row in data:
                rows.append(row.decode("utf-8").strip())
    return rows


def calculate_historical_mean_rates():
    header = extract_history()[0]
    cols = header.strip().split(",")

    currencies = ["USD", "SEK", "GBP", "JPY"]
    indexes = {}

    for currency in currencies:
        index = cols.index(currency)
        indexes[currency] = index

    sums = {"USD": 0.0, "SEK": 0.0, "GBP": 0.0, "JPY": 0.0}
    counts = {"USD": 0,   "SEK": 0,   "GBP": 0,   "JPY": 0}

    keys = list(indexes.keys())
    rows = extract_history()[1:]

    for value in indexes.values():
        currency = keys[list(indexes.values()).index(value)]

        for row in rows:
            parts = row.strip().split(",")

            if value >= len(parts) or parts[value] == "":
                continue

            sums[currency] += float(parts[value])
            counts[currency] += 1

    for currency in sums:
        if counts[currency] == 0:
            sums[currency] = None
        else:
            sums[currency] = sums[currency] / counts[currency]

    print(sums)
    return sums
