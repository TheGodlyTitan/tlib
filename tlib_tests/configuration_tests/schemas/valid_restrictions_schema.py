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

class ValidRestrictionsSchema(Schema):

    always_string = String(min_length=7, max_length=7)
    always_integer = Integer(min_value=10, max_value=10, is_even=True, is_odd=False)
    always_float = Float(min_value=10, max_value=10.0, min_precision=1, max_precision=1)
    always_null = ExpectedNull()
    
    maybe_string_or_integer = OneOf(String(min_length=1, max_length=1), Integer(min_value=1, max_value=1))
    maybe_null_or_false = NullOr(Boolean(False))
    maybe_true_or_false = Boolean()
    
    nested_one = Nested(
        ("always_string", String(min_length=7, max_length=7)),
        ("always_integer", Integer(min_value=10, max_value=10, is_even=True, is_odd=False)),
        ("always_float", Float(min_value=10, max_value=10.0, min_precision=1, max_precision=1))
    )
    
    nested_two = Nested(
        ('sub_nested', Nested(
            ("nested_always_string", String(min_length=7, max_length=7)),
            ("nested_always_integer", Integer(min_value=10, max_value=10, is_even=True, is_odd=False)),
            ("nested_always_float", Float(min_value=10, max_value=10.0, min_precision=1, max_precision=1))
        ))
    )
    
    unique_array = Array(String(min_length=8), max_length=3),
    
    datetime_value = Datetime()
    
    real_path = Filepath(exists=True, file_extension='.yml')
    fake_path = Filepath(exists=False)
    