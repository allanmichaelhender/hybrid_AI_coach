from langgraph.graph import StateGraph, END
from agents.state import AgentState
from agents.nodes.analyzer import analyzer_node
from agents.nodes.retriever import retriever_node

# 1. Initialize the StateGraph with our custom AgentState
workflow = StateGraph(AgentState)

# 2. Add the Nodes
# These are the Python functions we just built
workflow.add_node("analyzer", analyzer_node)
workflow.add_node("retriever", retriever_node)

# 3. Define the Flow (Edges)
# The Brain (Analyzer) thinks first, then passes thoughts to the Hands (Retriever)
workflow.add_edge("analyzer", "retriever")

# 4. Define the Exit
# Once the Retriever has updated the calendar with real workouts, we finish
workflow.add_edge("retriever", END)

# 5. Set the Entry Point
workflow.set_entry_point("analyzer")

# 6. Compile the Graph
# This 'app' is what you will call from your FastAPI endpoints
app = workflow.compile()
