from typing import Any


class StateManager:
    def __init__(self) -> None:
        self.current_state: Any = None
        self.states: dict[str, Any] = []


    def set_state(self, state: Any) -> None:
        self.current_state = state  


    def get_state(self) -> None:
        return self.current_state  
