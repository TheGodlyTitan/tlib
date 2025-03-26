from typing import Any

from datetime import datetime, timedelta

from .type import Type


class Datetime(Type):
    """
    A schema type that validates whether a string is in a valid datetime format. 
    
    Parameters
    ----------
    format : `str`
        The expected datetime format using `datetime.strptime` format strings.
        Defaults to ISO 8601 format ("%Y-%m-%d %H:%M:%S.%f").
    before : Optional[`datetime`]
        Ensures the provided datetime is **before** this datetime.
    after : Optional[`datetime`]
        Ensures the provided datetime is **after** this datetime.
    max_delta : Optional[`timedelta`]
        The maximum time difference between the provided datetime and `now`.
        Example: `max_delta=timedelta(days=7)` ensures the datetime is within the last 7 days.
        
    Example
    -------
    **example.yml**
    ```
    timestamp: "2025-02-16 09:03:58.374746"
    ```
    
    **your_schema.py**
    ```
    class YourSchema(ConfigSchema):
        timestamp = Datetime()
    ```
    """
    
    def __init__(
        self, 
        format: str = "%Y-%m-%d %H:%M:%S.%f",
        before: datetime = None,
        after: datetime = None,
        max_delta: timedelta = None,
    ) -> None:
        
        self.format = format
        self.before = before
        self.after = after
        self.max_delta = max_delta
    
    def __call__(self, value: Any) -> None:
        
        if not isinstance(value, str):
            raise TypeError(f"Expected a string, but got {type(value).__name__}")
        
        try:
            parsed_datetime = datetime.strptime(value, self.format)
        except Exception:
            raise ValueError(f"Invalid datetime: {value}. Expected format: {self.format}")
        
        # Validate 'before' constraint
        if self.before and parsed_datetime >= self.before:
            raise ValueError(f"Datetime {value} must be before {self.before}")

        # Validate 'after' constraint
        if self.after and parsed_datetime <= self.after:
            raise ValueError(f"Datetime {value} must be after {self.after}")
        
        # Validate 'max_delta' constraint
        if self.max_delta:
            now = datetime.now()
            delta = abs(now - parsed_datetime)
            if delta > self.max_delta:
                raise ValueError(
                    f"Datetime {value} exceeds the maximum delta: {self.max_delta}."
                )