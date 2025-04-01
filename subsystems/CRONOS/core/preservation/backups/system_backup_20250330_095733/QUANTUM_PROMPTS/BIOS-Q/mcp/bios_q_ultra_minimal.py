#!/usr/bin/env python3
import sys
import json

def read_message():
    try:
        line = sys.stdin.readline()
        if not line:
            return None
        return json.loads(line)
    except:
        return None

def write_message(message):
    try:
        sys.stdout.write(json.dumps(message) + "\n")
        sys.stdout.flush()
    except:
        pass

def main():
    while True:
        message = read_message()
        if not message:
            continue

        msg_type = message.get("type")
        msg_id = message.get("id")

        if msg_type == "shutdown":
            write_message({"type": "response", "id": msg_id, "status": "success"})
            break
        elif msg_type == "list_tools":
            write_message({
                "type": "response",
                "id": msg_id,
                "status": "success",
                "data": {
                    "tools": [{
                        "name": "bios_q_status",
                        "description": "Get BIOS-Q status",
                        "schema": {"type": "object", "properties": {}}
                    }]
                }
            })
        else:
            write_message({"type": "response", "id": msg_id, "status": "success"})

if __name__ == "__main__":
    main() 