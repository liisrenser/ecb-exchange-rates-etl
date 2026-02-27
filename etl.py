import requests
import zipfile

r_today: requests.Response = requests.get('https://www.ecb.europa.eu/stats/eurofxref/eurofxref.zip')
r_history: requests.Response = requests.get('https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist.zip')


def extract_history() -> list[str]:
    with open('data.zip1', 'wb') as f1:
        f1.write(r_history.content)

    rows: list[str] = []
    with zipfile.ZipFile('data.zip1', 'r') as data_zip:
        csv_name: str = data_zip.namelist()[0]
        with data_zip.open(csv_name) as data:
            for row in data:
                rows.append(row.decode("utf-8").strip())
    return rows


def extract_today() -> list[str]:
    with open('data.zip2', 'wb') as f2:
        f2.write(r_today.content)

    rows: list[str] = []
    with zipfile.ZipFile('data.zip2', 'r') as data_zip:
        csv_name: str = data_zip.namelist()[0]
        with data_zip.open(csv_name) as data:
            for row in data:
                rows.append(row.decode("utf-8").strip())
    return rows


def calculate_historical_mean_rates() -> dict[str, float | None]:
    header: str = extract_history()[0]
    cols: list[str] = header.strip().split(",")

    currencies: list[str] = ["USD", "SEK", "GBP", "JPY"]
    indexes: dict[str, int] = {}

    for currency in currencies:
        index: int = cols.index(currency)
        indexes[currency] = index

    sums: dict[str, float | None] = {"USD": 0.0, "SEK": 0.0, "GBP": 0.0, "JPY": 0.0}
    counts: dict[str, int] = {"USD": 0,   "SEK": 0,   "GBP": 0,   "JPY": 0}

    keys: list[str] = list(indexes.keys())
    rows: list[str] = extract_history()[1:]

    for value in indexes.values():
        currency: str = keys[list(indexes.values()).index(value)]

        for row in rows:
            parts: list[str] = row.strip().split(",")

            if value >= len(parts) or parts[value] == "":
                continue

            sums[currency] = float(sums[currency]) + float(parts[value])
            counts[currency] += 1

    for currency in sums:
        if counts[currency] == 0:
            sums[currency] = None
        else:
            sums[currency] = float(sums[currency]) / counts[currency]

    return sums


def get_todays_rate() -> dict[str, float]:
    rows: list[str] = extract_today()

    header: list[str] = rows[0].lstrip("\ufeff").split(",")
    data: list[str] = rows[1].split(",")

    currencies: list[str] = [" USD", " SEK", " GBP", " JPY"]
    rates: dict[str, float] = {}

    for currency in currencies:
        index: int = header.index(currency)
        rates[currency.strip()] = float(data[index])
    return rates


def generate_table(today_rates: dict[str, float], mean_rates: dict[str, float | None]) -> None:
    with open("exchange_rates.md", "w", encoding="utf-8") as f:
        f.write("| Currency Code |    Rate | Mean Historical Rate |\n")
        f.write("|---------------|---------|----------------------|\n")

        for currency in today_rates:
            rate: float = today_rates[currency]
            mean: float | None = mean_rates[currency]
            f.write(
                f"| {currency:<13} | {rate:>7.3f} | {mean:>20.4f} |\n"
            )


if __name__ == "__main__":
    today: dict[str, float] = get_todays_rate()
    mean: dict[str, float | None] = calculate_historical_mean_rates()
    generate_table(today, mean)
