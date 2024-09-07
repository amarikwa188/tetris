from typing import Any


class StateManager:
    """Represents an instance of the state manager."""
    def __init__(self) -> None:
        self.current_state: Any = None
        self.states: dict[str, Any] = []


    def set_state(self, state: Any) -> None:
        """Set a given state as the current state."""
        self.current_state = state  


    def get_state(self) -> Any:
        """
        Return the current state.
        
        :return: the current state.
        """
        return self.current_state  
