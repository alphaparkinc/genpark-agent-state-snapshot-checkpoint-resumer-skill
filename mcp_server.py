import sys
import json
from client import StateSnapshotCheckpointResumer

def handle_request(req):
    method = req.get("method")
    params = req.get("params", {})
    req_id = req.get("id")

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "save_snapshot",
                        "description": "Saves agent execution memory and returns integrity checksum.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "session_id": {"type": "string"},
                                "state_data": {"type": "object"},
                                "step_index": {"type": "integer"}
                            }
                        }
                    },
                    {
                        "name": "restore_snapshot",
                        "description": "Verifies checksum and restores agent state from checkpoint.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "session_id": {"type": "string"}
                            }
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        args = params.get("arguments", {})
        resumer = StateSnapshotCheckpointResumer()
        name = params.get("name")
        if name == "save_snapshot":
            res = resumer.save_checkpoint(args.get("session_id", "s1"), args.get("state_data", {}), args.get("step_index", 1))
        else:
            res = resumer.restore_checkpoint(args.get("session_id", "s1"))
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "content": [{"type": "text", "text": json.dumps(res, indent=2)}]
            }
        }
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def main():
    resumer = StateSnapshotCheckpointResumer()
    print(json.dumps(resumer.save_checkpoint("s1", {"a": 1}, 1), indent=2))

if __name__ == "__main__":
    main()
