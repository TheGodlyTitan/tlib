import unittest

from tlib.config import (
    load_config,
    ConfigValidationError
)

from .schemas import (
    ValidTypedSchema,
    InvalidTypedSchema,
    ValidRestrictionsSchema
)


SOURCE_FILES = "tlib/tlib_tests/configuration/configs"


class TestSchemas(unittest.TestCase):
    
    def setUp(self):
        self.schema_test = SOURCE_FILES + '/schema_test.yml'

    def test_valid_typed_schema(self) -> None:
        c = load_config(self.schema_test, schema=ValidTypedSchema)
        
    def test_invalid_typed_schema(self) -> None:
        with self.assertRaises(ConfigValidationError):
            c = load_config(self.schema_test, schema=InvalidTypedSchema)
    
    def test_valid_restrictions_schema(self) -> None:
        c = load_config(self.schema_test, schema=ValidRestrictionsSchema)
        