from configuration import Schema
from configuration.types import (
    String,
    Integer,
    Float,
    Boolean,
    OneOf,
    NullOr,
    ExpectedNull,
    Nested,
    Array,
    Datetime,
    Filepath
)


class InvalidTypedSchema(Schema):
    
    always_string = Integer() # String()
    always_integer = Integer()
    always_float = Float()
    always_null = ExpectedNull()
    
    maybe_string_or_integer = OneOf(String(), Integer())
    maybe_null_or_false = NullOr(Boolean(False))
    maybe_true_or_false = Boolean()
    
    nested_one = Nested(
        ("always_string", String()),
        ("always_integer", Integer()),
        ("always_float", Float())
    )
    
    nested_two = Nested(
        ('sub_nested', Nested(
            ("nested_always_string", String()),
            ("nested_always_integer", Integer()),
            ("nested_always_float", Float())
        ))
    )
    unique_array = Array(String())
    datetime_value = Datetime()
    
    real_path = Filepath()
    fake_path = Filepath()
    