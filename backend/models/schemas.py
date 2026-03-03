from pydantic import BaseModel
from typing import Optional

class ImportItem(BaseModel):
  product_description:str
  country_of_origin:str
  volume_tonnes:float
  supplier:Optional[str]
  # Alternative column names from real world CSV data
  cn_code: Optional[str] = None            # if user already has CN code
  weight_tonnes: Optional[float] = None    # alternative to volume_tonnes
  supplier_country: Optional[str] = None   # alternative to country_of_origin
  importer: Optional[str] = None           # alternative to product_description
  sector: Optional[str] = None             # steel / aluminium / cement
  actual_emissions: Optional[float] = None # if supplier provides real emissions



class ClassificationResult(Optional):
  product_description:str
  country_of_origin:str
  volumes_tonnes:float
  
  cn_code:Optional[str]
  category:str
  cbam_covered:bool
  
  emmision_factor:float
  embedd_emissions:float
  
  ets_prise:float
  estimated_cbam_cost:float
  
  confidense:float
  ai_note:Optional[str]
  
  
  