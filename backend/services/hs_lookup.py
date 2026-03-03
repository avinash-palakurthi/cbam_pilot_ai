import pandas as pd 
import os
#  Load the CSV once when file is imported
# df =pd.read_csv("data/cbam_hscode.csv")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
df = pd.read_csv(os.path.join(BASE_DIR, "data", "cbam_master_2026.csv"))

def validate_hscode(cbam_hscode:str)->dict:
  # search for hs code in dataframe
  result = df[df[cbam_hscode].astype(str).str.startswith(str(cbam_hscode))]
  
  if result.empty:
    return{
      "found":False,
      "description":None,
      "category":None
    }
    
  # return the first match as dict
  row = result.iloc[0]
  return{
    "found":True,
    "description":row.get("description",""),
    "category":row.get("category","")
  }