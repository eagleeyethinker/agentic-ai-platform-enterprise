
import os
from neo4j import GraphDatabase

def graph_agent(state):
    state.setdefault("graph_data", [])
    uri = os.getenv("NEO4J_URI", "bolt://neo4j:7687")
    user = os.getenv("NEO4J_USER", "neo4j")
    pwd = os.getenv("NEO4J_PASSWORD", "password")

    try:
        with GraphDatabase.driver(uri, auth=(user, pwd)) as driver:
            with driver.session() as session:
                result = session.run("MATCH (f:Flight) RETURN f.flight_id LIMIT 5")
                state["graph_data"] = [record[0] for record in result]
    except Exception as exc:
        state["errors"] = [*state.get("errors", []), f"graph_agent: {exc}"]

    return state
