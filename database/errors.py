
class Error(Exception):
    """
    Base exception for all `database` module errors.
    """
    pass

class InterfaceError(Error):
    """
    Raised when a problem occurs within the code or interface itself.
    
    These errors indicate a problem within the module source code.
    """
    def __init__(self, message: str) -> None:
        super().__init__(f"Unexpected module failure occured: {message}")
        
class ConnectionError(Error):
    """
    Raised when a database connection cannot be established.
    """
    def __init__(self, message: str):
        super().__init__(f"Database failed to connect: {message}")