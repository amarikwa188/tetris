from typing import Any


class StateManager:
    """Represents an instance of the state manager."""
    def __init__(self) -> None:
        """
        Initialize an instance of the state manager.
        """
        self.current_state: Any = None
        self.states: dict[str, Any] = {}


    def set_state(self, state: Any) -> None:
        """
        Set a given state as the current state.
        
        :param state: an instance of a state class.
        """
        self.current_state = state  


    def get_state(self, state_name: str) -> Any:
        """
        Return the a specified state class.
        
        :param state_name: the string key that indentifies the state class
        in the states dictionary.
        :return: the given state.
        """

        return self.states[state_name]
        

    def get_current_state(self) -> Any:
        """
        Return the current state.

        :return: the current state.
        """
        return self.current_state  
