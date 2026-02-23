from langgraph.graph import StateGraph, END
from agents.state import AgentState
from agents.nodes.analyzer import analyzer_node
from agents.nodes.retriever import retriever_node
from agents.nodes.summarizer import summarizer_node

# Initialize the StateGraph with our custom AgentState
workflow = StateGraph(AgentState)

# Add the Nodes
workflow.add_node("analyzer", analyzer_node)
workflow.add_node("retriever", retriever_node)
workflow.add_node("summarizer", summarizer_node)

# Set the graph traversal route
workflow.set_entry_point("analyzer")
workflow.add_edge("analyzer", "retriever")
workflow.add_edge("retriever", "summarizer")
workflow.add_edge("summarizer", END)

app = workflow.compile()
