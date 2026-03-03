ANNEX_CN_CODE = [
    # Steel
    "7205", "7206", "7207", "7208", "7209", "7210", "7211",
    "7212", "7213", "7214", "7215", "7216", "7217", "7218",
    "7225", "7226", "7318",
    # Aluminium
    "7601", "7602", "7603", "7604", "7605", "7606", "7616",
    # Cement
    "2523",
    # Fertilizers
    "3102", "3105",
    # Hydrogen
    "2804",
    # Electricity
    "2716",
]

def is_cbam_covered(cn_code: str) -> bool:
    if not cn_code:
        return False
    
    # Check first 4 digits only
    # because user may provide 4, 6, or 8 digit CN code
    cn_short = str(cn_code).strip()[:4]
    
    return cn_short in ANNEX_CN_CODE