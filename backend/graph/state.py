from typing import Optional, TypedDict

# This is the "bag" that carries data through the pipeline
# Every node reads from this and adds its result back into it

class CBAMState(TypedDict):

    # What user gives us
    product_description: str
    country_of_origin: str
    volume_tonnes: float
    supplier: Optional[str]

    # Classification node will fill these
    cn_code: Optional[str]
    category: Optional[str]
    classification_note: Optional[str]

    # Annex node will fill this
    cbam_covered: Optional[bool]

    # Emission node will fill these
    emission_factor: Optional[float]
    embedded_emissions: Optional[float]

    # ETS node will fill this
    ets_price: Optional[float]

    # Cost node will fill this
    estimated_cbam_cost: Optional[float]

    # Final status
    status: Optional[str]  # "covered" or "not_covered"