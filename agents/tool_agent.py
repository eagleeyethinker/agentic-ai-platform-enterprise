
import os
import re

import requests


def extract_airport(query: str) -> str:
    match = re.search(r"\b([A-Z]{3})\b", query.upper())
    return match.group(1) if match else os.getenv("DEFAULT_AIRPORT", "ATL")


def tool_agent(state):
    state.setdefault("weather", {})
    airport = extract_airport(state["query"])
    weather_url = os.getenv("WEATHER_MCP_URL", "http://weather-mcp:9001")

    try:
        response = requests.get(f"{weather_url}/weather/{airport}", timeout=5)
        response.raise_for_status()
        state["weather"] = response.json()
    except Exception as exc:
        state["errors"] = [*state.get("errors", []), f"tool_agent: {exc}"]

    return state
