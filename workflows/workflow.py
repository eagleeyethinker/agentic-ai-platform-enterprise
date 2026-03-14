
from typing import TypedDict

from langgraph.graph import END, StateGraph
from agents.router_agent import router_agent
from agents.retrieval_agent import retrieval_agent
from agents.graph_agent import graph_agent
from agents.tool_agent import tool_agent
from agents.reasoning_agent import reasoning_agent

class State(TypedDict, total=False):
    query: str
    route: str
    weather: dict
    rag_context: list[str]
    graph_data: list[str]
    errors: list[str]
    decision: str

def build():
    graph = StateGraph(State)

    graph.add_node("router", router_agent)
    graph.add_node("retrieval", retrieval_agent)
    graph.add_node("graph", graph_agent)
    graph.add_node("tool", tool_agent)
    graph.add_node("reasoning", reasoning_agent)

    graph.set_entry_point("router")
    graph.add_conditional_edges(
        "router",
        lambda state: state["route"],
        {
            "rag": "retrieval",
            "weather": "tool",
        },
    )
    graph.add_edge("retrieval", "graph")
    graph.add_edge("tool", "graph")
    graph.add_edge("graph", "reasoning")
    graph.add_edge("reasoning", END)

    return graph.compile()

workflow = build()

def run_query(q):
    return workflow.invoke({"query": q})
