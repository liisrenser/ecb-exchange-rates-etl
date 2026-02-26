## ecb-exchange-rates-etl

This project implements a simple Extract, Transform, Load process in Python that retrieves Euro foreign exchange reference rates from the European Central Bank , processes the data, and outputs the results into a Markdown table.

# 

**The following ECB endpoints are used:**

Daily exchange rates
https://www.ecb.europa.eu/stats/eurofxref/eurofxref.zip

Historical exchange rates
https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist.zip

Both endpoints return ZIP archives containing CSV files.

#

**The transformation process includes:**

Loading daily and historical exchange rate CSV files

Selecting the following currencies: USD, SEK, GBP, JPY

Calculating the historical mean exchange rate for each selected currency using all available historical data

Extracting the most recent daily rate for each currency

The final output is a Markdown file named: exchange_rates.md

# How to run
**1. Clone the repository**

Open your development environment (for example VS Code) and open its integrated terminal.

```bash
git clone https://github.com/liisrenser/ecb-exchange-rates-etl.git
cd ecb-exchange-rates-etl
```

(Optional) Open the project in VS Code

If you want to view and edit the project files in a development environment (such as Visual Studio Code), run the following command:

```bash
code .
```

**2. Install required dependency**

Install the required Python package using pip:

```bash
pip install requests
```

**3. Run the script**

Execute the Python script from the terminal:

```bash
python etl.py
```

This will generate a Markdown file containing the exchange rate table.

**4. Open the generated Markdown file**

After the script finishes, *exchange_rates.md* will be created

You can open it directly from your development environment or using the terminal:

```bash
notepad .\exchange_rates.md
```

**Notes**

All commands are intended to be run inside a development environment terminal (such as VS Code’s integrated terminal).

#

**Used sources:**

No AI was used during the project.

zip reading: https://www.youtube.com/watch?v=z0gguhEmWiY , https://docs.python.org/3/library/csv.html

generating a markdown file: https://www.reddit.com/r/learnpython/comments/gx3ho0/how_can_generate_markdown_file_with_python/


