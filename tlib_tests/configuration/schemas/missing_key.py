from tlib.config import (
    ConfigSchema,
    String,
    Integer,
    Float,
    ExpectedNull
)


class MissingKeySchema(ConfigSchema):
    """
    A valid schema implementation:

    Only keys with strict typing are within the schema, other keys will be as-is.
    """

    always_string = String()
    always_integer = Integer()
    always_float = Float()
    always_null = ExpectedNull()

    # Missing all keys after