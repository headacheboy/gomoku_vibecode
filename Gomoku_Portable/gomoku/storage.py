import json
from typing import Any

def save_state(path: str, state: Any) -> None:
    with open(path, 'w', encoding='utf8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

def load_state(path: str) -> Any:
    with open(path, 'r', encoding='utf8') as f:
        return json.load(f)
