from typing import Optional


class BaseAppException(Exception):
    """Base exception for all application exceptions."""
    
    def __init__(self, message: str, status_code: int = 400, description: Optional[str] = None):
        self.message = message
        self.status_code = status_code
        self.description = description or message
        super().__init__(self.message)
    
    def to_dict(self):
        """Convert exception to dictionary format."""
        return {
            "status": self.status_code,
            "message": self.message,
            "description": self.description,
        }