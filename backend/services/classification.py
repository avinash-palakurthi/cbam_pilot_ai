def classify_product(description:str):
    desc=description.lower()
    
    if "iron" in desc or "steel" in desc:
        return "7208", "Iron & Steel"
    if "cement" in desc:
        return "2523","Cement"
    if "aluminium" in desc:
        return "7601","Aluminium"
    
    return None, "Other"
