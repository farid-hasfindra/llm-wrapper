from typing import List, Dict

class ConversationMemory:
    """
    Manages chat history.
    Currently in-memory, but designed to be swappable with Redis/Postgres.
    """
    def __init__(self):
        self._history: Dict[str, List[Dict[str, str]]] = {}

    def add_message(self, session_id: str, role: str, content: str):
        if session_id not in self._history:
            self._history[session_id] = []
        self._history[session_id].append({"role": role, "content": content})

    def get_history(self, session_id: str) -> List[Dict[str, str]]:
        return self._history.get(session_id, [])

    def clear_history(self, session_id: str):
        if session_id in self._history:
            del self._history[session_id]

conversation_memory = ConversationMemory()
