"""Node‑Graph JSON schema v2 (pins + links)."""
GRAPH_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Reaper NodeGraph",
    "type": "object",
    "required": ["version", "nodes", "links"],
    "properties": {
        "version": {"type": "string"},
        "nodes": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["id", "type", "params", "inputs", "outputs"],
                "properties": {
                    "id": {"type": "string"},
                    "type": {"type": "string"},
                    "params": {"type": "object"},
                    "inputs": {"type": "array", "items": {"type": "string"}},
                    "outputs": {"type": "array", "items": {"type": "string"}},
                },
            },
        },
        "links": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["src", "dst"],
                "properties": {
                    "src": {"type": "string"},  # "node.outputPin"
                    "dst": {"type": "string"}   # "node.inputPin"
                },
            },
        },
    },
}
