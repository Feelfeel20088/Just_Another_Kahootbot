class KahootWarning(Warning):
    """a warning not fatel"""
    def __init__(self, message, /) -> None:
        super().__init__(message)
        self.message = message

    def __str__(self) -> str:
        return f"[WARNING]: {self.message}"

class KahootFatel(Exception):
    """fatel nothing for kahoot bot to fall back to"""
    def __init__(self, message, /) -> None:
        super().__init__(message)  
        self.message = message

    def __str__(self) -> str:
        return f"[FATEL]: {self.message}"

__all__ = [KahootFatel, KahootWarning]