
def router_agent(state):
    query = state["query"].lower()

    if any(keyword in query for keyword in ("storm", "weather", "delay", "airport", "flight")):
        state["route"] = "weather"
    else:
        state["route"] = "rag"

    return state
