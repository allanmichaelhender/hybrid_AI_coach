from langgraph.graph import StateGraph, END
from agents.state import AgentState
from agents.nodes.analyzer import analyzer_node
from agents.nodes.retriever import retriever_node
from agents.nodes.summarizer import summarizer_node

# 1. Initialize the StateGraph with our custom AgentState
workflow = StateGraph(AgentState)

# 2. Add the Nodes
# These are the Python functions we just built
workflow.add_node("analyzer", analyzer_node)
workflow.add_node("retriever", retriever_node)
workflow.add_node("summarizer", summarizer_node)

workflow.set_entry_point("analyzer")
workflow.add_edge("analyzer", "retriever")
workflow.add_edge("retriever", "summarizer") # 👈 Route to the Editor
workflow.add_edge("summarizer", END)

# 6. Compile the Graph
# This 'app' is what you will call from your FastAPI endpoints
app = workflow.compile()
