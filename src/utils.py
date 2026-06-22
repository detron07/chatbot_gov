import json
import re

def fix_json_output(msg):
    text = msg.content if hasattr(msg, "content") else str(msg)
    try:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            data = json.loads(match.group(0))
            if "properties" in data:
                return json.dumps(data["properties"])
            return match.group(0)
    except Exception:
        pass
    return text
