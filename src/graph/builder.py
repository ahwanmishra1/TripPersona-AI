from langgraph.graph import StateGraph, END
from src.graph.state import TripState
from src.graph.nodes import (
    normalize_input_node,
    gather_context_node,
    generate_base_plan_node,
    apply_personalities_node,
    format_response_node,
)


def build_graph():
    graph = StateGraph(TripState)

    graph.add_node("normalize_input", normalize_input_node)
    graph.add_node("gather_context", gather_context_node)
    graph.add_node("generate_base_plan", generate_base_plan_node)
    graph.add_node("apply_personalities", apply_personalities_node)
    graph.add_node("format_response", format_response_node)

    graph.set_entry_point("normalize_input")
    graph.add_edge("normalize_input", "gather_context")
    graph.add_edge("gather_context", "generate_base_plan")
    graph.add_edge("generate_base_plan", "apply_personalities")
    graph.add_edge("apply_personalities", "format_response")
    graph.add_edge("format_response", END)

    return graph.compile()