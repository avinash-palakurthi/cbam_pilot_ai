from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from rag.query import query_rag
from services.annex import is_cbam_covered
from services.emissions import get_emission_factor
from services.ets import get_ets_price
from services.cost_engine import calculate_cost
from graph.state import CBAMState

# Create the LLM once, reuse everywhere
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


# NODE 1 - CLASSIFICATION
# This node uses AI to find the CN code from product description
def classify_node(state: CBAMState) -> CBAMState:

    description = state["product_description"]

    # Step 1: Get relevant regulation text from Qdrant
    rag_context = query_rag(description)

    # Step 2: Ask GPT-4 to classify the product
    prompt = ChatPromptTemplate.from_template("""
You are a EU trade classification expert.

Using the regulation context below, classify the product.

Product: {description}

Context from EU regulations:
{context}

Return ONLY this JSON:
{{
  "cn_code": "4-digit CN code or null if unknown",
  "category": "product category name",
  "note": "one line explanation"
}}
""")

    chain = prompt | llm | JsonOutputParser()

    result = chain.invoke({
        "description": description,
        "context": rag_context
    })

    # Step 3: Add result to state
    state["cn_code"] = result.get("cn_code")
    state["category"] = result.get("category")
    state["classification_note"] = result.get("note")

    return state


# NODE 2 - ANNEX CHECK
# Simple yes/no — is this product covered under CBAM?
def annex_node(state: CBAMState) -> CBAMState:

    cn_code = state.get("cn_code") or ""

    # This is just a lookup, no AI needed
    covered = is_cbam_covered(cn_code)

    state["cbam_covered"] = covered
    state["status"] = "covered" if covered else "not_covered"

    return state


# CONDITIONAL EDGE - decides which node to go to next
def route_after_annex(state: CBAMState) -> str:

    if state.get("cbam_covered") == True:
        return "emission_node"   # continue pipeline
    else:
        return "end_node"        # stop here, not applicable


# NODE 3 - EMISSION FACTOR
# Gets the emission factor from our dataset (pandas lookup)
def emission_node(state: CBAMState) -> CBAMState:

    cn_code = state.get("cn_code") or ""
    volume = float(state.get("volume_tonnes") or 0.0)

    # Simple dictionary/pandas lookup - no AI
    emission_factor = float(get_emission_factor(cn_code) or 0.0)
    embedded_emissions = volume * emission_factor

    state["emission_factor"] = emission_factor
    state["embedded_emissions"] = embedded_emissions

    return state


# NODE 4 - ETS PRICE
# Gets the current carbon price
def ets_node(state: CBAMState) -> CBAMState:

    # Static for now, can connect to live API later
    ets_price = get_ets_price()

    state["ets_price"] = ets_price

    return state


# NODE 5 - COST CALCULATION
# Simple math: emissions x price = cost
def cost_node(state: CBAMState) -> CBAMState:

    volume = float(state.get("volume_tonnes") or 0.0)
    emission_factor = float(state.get("emission_factor") or 0.0)
    ets_price = float(state.get("ets_price") or 0.0)

    _, cost = calculate_cost(volume, emission_factor, ets_price)

    state["estimated_cbam_cost"] = cost
    state["status"] = "covered"

    return state


# NODE 6 - END NODE
# This runs when product is NOT covered under CBAM
def end_node(state: CBAMState) -> CBAMState:

    state["estimated_cbam_cost"] = 0.0
    state["emission_factor"] = 0.0
    state["embedded_emissions"] = 0.0
    state["ets_price"] = 0.0
    state["status"] = "not_covered"

    return state
