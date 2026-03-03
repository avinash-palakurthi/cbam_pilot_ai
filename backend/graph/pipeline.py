from langgraph.graph import StateGraph, END

from graph.state import CBAMState
from graph.nodes import (
    classify_node,
    annex_node,
    emission_node,
    ets_node,
    cost_node,
    end_node,
    route_after_annex,
)


def build_cbam_pipeline():

    # Step 1: Create a graph with our state
    graph = StateGraph(CBAMState)

    # Step 2: Add all nodes to the graph
    graph.add_node("classify_node", classify_node)
    graph.add_node("annex_node", annex_node)
    graph.add_node("emission_node", emission_node)
    graph.add_node("ets_node", ets_node)
    graph.add_node("cost_node", cost_node)
    graph.add_node("end_node", end_node)

    # Step 3: Set where the pipeline starts
    graph.set_entry_point("classify_node")

    # Step 4: Connect nodes in order
    graph.add_edge("classify_node", "annex_node")

    # Step 5: After annex check — conditional split
    # If covered  → go to emission_node
    # If not      → go to end_node
    graph.add_conditional_edges(
        "annex_node",
        route_after_annex,
        {
            "emission_node": "emission_node",
            "end_node": "end_node",
        }
    )

    # Step 6: Continue covered path
    graph.add_edge("emission_node", "ets_node")
    graph.add_edge("ets_node", "cost_node")
    graph.add_edge("cost_node", END)

    # Step 7: End not-covered path
    graph.add_edge("end_node", END)

    # Step 8: Compile and return
    return graph.compile()


# Build the pipeline once — import this in main.py and api
cbam_pipeline = build_cbam_pipeline()