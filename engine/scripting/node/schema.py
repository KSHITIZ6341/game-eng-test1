
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
                "required": ["id", "type", "params"],
                "properties": {
                    "id": {"type": "string"},
                    "type": {"type": "string"},
                    "params": {"type": "object"},
                },
            },
        },
        "links": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["src", "dst"],
                "properties": {
                    "src": {"type": "string"},
                    "dst": {"type": "string"},
                },
            },
        },
    },
}
