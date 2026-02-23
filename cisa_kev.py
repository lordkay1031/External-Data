"""
Fetch the CISA Known Exploited Vulnerabilities (KEV) catalog.

Data source: https://www.cisa.gov/known-exploited-vulnerabilities-catalog
Direct CSV feed: https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.csv
"""

from io import StringIO

import pandas as pd
import requests

CSV_URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.csv"
CSV_OUTPUT = "known_exploited_vulnerabilities.csv"
EXCEL_OUTPUT = "known_exploited_vulnerabilities.xlsx"


def fetch_kev_catalog(url: str = CSV_URL) -> pd.DataFrame:
    """Download the CISA KEV catalog and return it as a DataFrame."""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
    except requests.exceptions.RequestException as exc:
        raise SystemExit(f"Failed to fetch KEV catalog from {url}: {exc}") from exc
    df = pd.read_csv(StringIO(response.text))
    return df


def main():
    print("Fetching CISA Known Exploited Vulnerabilities catalog...")
    df = fetch_kev_catalog()

    print(f"\nTotal entries: {len(df)}")
    print(f"Columns: {list(df.columns)}")
    print("\nFirst 5 rows:")
    print(df.head().to_string(index=False))

    df.to_csv(CSV_OUTPUT, index=False)
    print(f"\nSaved CSV to: {CSV_OUTPUT}")

    df.to_excel(EXCEL_OUTPUT, index=False)
    print(f"Saved Excel to: {EXCEL_OUTPUT}")


if __name__ == "__main__":
    main()
