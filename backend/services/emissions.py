import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
df = pd.read_csv(os.path.join(BASE_DIR, "data", "cbam_master_2026.csv"))

# Normalize column names to lowercase
df.columns = [col.strip().lower() for col in df.columns]


def get_emission_factor(cn_code: str) -> float:

    if not cn_code:
        return 0.0

    # Step 1: Try exact 4-digit match in our EU CSV
    result = df[df["cn_code"].astype(str).str.startswith(str(cn_code)[:4])]

    if not result.empty:
        return float(result.iloc[0]["total_2026"])

    # Step 2: Fallback by first 2 digits
    two_digit = str(cn_code)[:2]

    fallback = {
        "72": 2.210,
        "73": 2.210,
        "76": 10.500,
        "25": 0.852,
        "31": 1.340,
        "28": 12.700,
        "27": 0.450,
    }

    return fallback.get(two_digit, 0.0)


def get_sector(cn_code: str) -> str:

    if not cn_code:
        return "Unknown"

    result = df[df["cn_code"].astype(str).str.startswith(str(cn_code)[:4])]

    if not result.empty:
        return str(result.iloc[0]["sector"])

    return "Unknown"