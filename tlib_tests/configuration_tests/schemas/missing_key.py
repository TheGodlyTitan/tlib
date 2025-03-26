from configuration import Schema
from configuration.types import (
    String,
    Integer,
    Float,
    ExpectedNull
)


class MissingKeySchema(Schema):

    always_string = String()
    always_integer = Integer()
    always_float = Float()
    always_null = ExpectedNull()

    # Missing All Keys After