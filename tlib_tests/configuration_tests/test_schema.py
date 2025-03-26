import unittest

from configuration import (
    load_config,
    ValidationError
)

from .schemas import (
    ValidTypedSchema,
    InvalidTypedSchema,
    ValidRestrictionsSchema,
    MissingKeySchema
)


SOURCE_FILES = "tlib_tests/configuration_tests/configs"


class TestSchemas(unittest.TestCase):
    
    def setUp(self):
        self.schema_test = SOURCE_FILES + '/schema_test.yml'

    def test_valid_typed_schema(self) -> None:
        load_config(self.schema_test, schema=ValidTypedSchema)
        
    def test_invalid_typed_schema(self) -> None:
        with self.assertRaises(ValidationError):
            load_config(self.schema_test, schema=InvalidTypedSchema)
    
    def test_valid_restrictions_schema(self) -> None:
        load_config(self.schema_test, schema=ValidRestrictionsSchema)
        
    def test_missing_key_schema(self) -> None:
        load_config(self.schema_test, schema=MissingKeySchema)
        