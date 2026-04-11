from langgraph.graph import StateGraph, END
from .state import WorkoutBuilderState
from .nodes import intake_node, matcher_node, builder_node, validator_node


# Initialize the StateGraph
workflow = StateGraph(WorkoutBuilderState)

# Add nodes
workflow.add_node("intake", intake_node)
workflow.add_node("matcher", matcher_node)
workflow.add_node("builder", builder_node)
workflow.add_node("validator", validator_node)


# Define conditional edge from intake
def route_after_intake(state: WorkoutBuilderState):
    """Route to matcher if we need RAG/synthetic, else straight to builder."""
    mode = state.get("generation_mode", "manual")
    prompt = state.get("natural_language_prompt", "")

    if mode in ["rag_match", "synthetic"] or prompt:
        return "matcher"
    return "builder"


# Define conditional edge from matcher
def route_after_matcher(state: WorkoutBuilderState):
    """Always go to builder after matcher."""
    return "builder"


# Set up the graph flow
workflow.set_entry_point("intake")
workflow.add_conditional_edges(
    "intake",
    route_after_intake,
    {
        "matcher": "matcher",
        "builder": "builder"
    }
)
workflow.add_conditional_edges(
    "matcher",
    route_after_matcher,
    {"builder": "builder"}
)
workflow.add_edge("builder", "validator")
workflow.add_edge("validator", END)

# Compile the graph
workout_builder_app = workflow.compile()
