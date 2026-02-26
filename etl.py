import requests
import zipfile
import sys


r_today = requests.get('https://www.ecb.europa.eu/stats/eurofxref/eurofxref.zip')
r_history = requests.get('https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist.zip')


def extract_history():
    with open('data.zip1', 'wb') as f1:
        f1.write(r_history.content)

    rows = []
    with zipfile.ZipFile('data.zip1', 'r') as data_zip:
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

def get_todays_rate():
    rows = extract_today()

    header = rows[0].lstrip("\ufeff").split(",")
    data = rows[1].split(",")

    currencies = [" USD", " SEK", " GBP", " JPY"]
    rates = {}

    for currency in currencies:
        index = header.index(currency)
        rates[currency.strip()] = float(data[index])
    return rates

def generate_table(today_rates, mean_rates):
    with open("exchange_rates.md", "w", encoding="utf-8") as f:
        f.write("| Currency Code |    Rate | Mean Historical Rate |\n")
        f.write("|---------------|---------|----------------------|\n")
        
        for currency in today_rates:
            rate = today_rates[currency]
            mean = mean_rates[currency]
            f.write(
                f"| {currency:<13} | {rate:>7.3f} | {mean:>20.4f} |\n"
            )

if __name__ == "__main__":
    today = get_todays_rate()
    mean = calculate_historical_mean_rates()
    generate_table(today, mean)