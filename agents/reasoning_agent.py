
import os
from openai import OpenAI


def build_fallback_decision(state):
    airport = state.get("weather", {}).get("airport", "the impacted airport")
    weather_event = state.get("weather", {}).get("event")
    severity = state.get("weather", {}).get("severity")
    graph_data = state.get("graph_data") or []
    rag_context = state.get("rag_context") or []

    parts = []
    if weather_event and severity:
        parts.append(f"Monitor {airport} operations due to {severity.lower()} {weather_event.lower()} conditions.")
    if graph_data:
        parts.append(f"Review affected flights first: {', '.join(graph_data[:3])}.")
    if rag_context:
        parts.append(f"Relevant guidance: {rag_context[0]}")
    if not parts:
        parts.append("Insufficient live system context is available. Escalate to an operations controller for manual review.")
    if state.get("errors"):
        parts.append(f"Warnings: {'; '.join(state['errors'])}")
    return " ".join(parts)


def reasoning_agent(state):
    prompt = f'''
You are an airline operations AI.

Weather:
{state.get("weather")}

RAG Context:
{state.get("rag_context")}

Graph Data:
{state.get("graph_data")}

User Question:
{state["query"]}

Provide an operational recommendation.
'''

    try:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is not set")
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[{"role": "user", "content": prompt}],
        )
        state["decision"] = response.choices[0].message.content
    except Exception as exc:
        state["errors"] = [*state.get("errors", []), f"reasoning_agent: {exc}"]
        state["decision"] = build_fallback_decision(state)

    return state
