# External-Data

A collection of scripts for fetching external security datasets.

## CISA Known Exploited Vulnerabilities (KEV) Catalog

**Source:** https://www.cisa.gov/known-exploited-vulnerabilities-catalog

`cisa_kev.py` downloads the CISA KEV catalog directly from the official CSV feed,
prints a summary, and saves the data as both CSV and Excel files.

### Setup

```bash
pip install -r requirements.txt
```

### Usage

```bash
python cisa_kev.py
```

**Output files:**
- `known_exploited_vulnerabilities.csv`
- `known_exploited_vulnerabilities.xlsx`