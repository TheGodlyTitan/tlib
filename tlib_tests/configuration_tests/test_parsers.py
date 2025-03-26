import unittest

from configuration import (
    load_config,
    Configuration,
    ParsingError,
    SourceError,
)


SOURCE_FILES = "tlib_tests/configuration_tests/configs"


class TestParsers(unittest.TestCase):
        
    def setUp(self):
        # Valid Files
        self.ini_file  = f"{SOURCE_FILES}/valid_config.ini"
        self.cfg_file  = f"{SOURCE_FILES}/valid_config.cfg"
        self.json_file = f"{SOURCE_FILES}/valid_config.json"
        self.toml_file = f"{SOURCE_FILES}/valid_config.toml"
        self.yaml_file = f"{SOURCE_FILES}/valid_config.yml"
        # Invalid Files
        self.missing_file = f"{SOURCE_FILES}/missing_file.json"
        self.invalid_types = [
            f"{SOURCE_FILES}/invalid_type_one.md",
            f"{SOURCE_FILES}/invalid_type_two.txt",
            f"{SOURCE_FILES}/invalid_type_three.doc",
        ]
        self.invalid_syntaxs = [
            f"{SOURCE_FILES}/syntax_error_one.yml",
            f"{SOURCE_FILES}/syntax_error_two.yml",
            f"{SOURCE_FILES}/syntax_error_three.yml"
        ]
        # Empty Config
        self.empty_config = f"{SOURCE_FILES}/empty_config.yml"
        
    def assertIsConfiguration(self, obj: object) -> None:
        self.assertIsInstance(obj, Configuration)
        
    """Parser Completions"""
    
    def test_ini(self) -> None:
        config = load_config(self.ini_file)
        self.assertIsConfiguration(config)
        self.assertEqual(config.general.app_name, "TestApp")
        self.assertEqual(config.general.version, "1.0")
        self.assertEqual(config.general.is_enabled, True)
        self.assertEqual(config.general.is_active, "true")
        self.assertEqual(config.settings.max_users, 100)
        self.assertEqual(config.settings.timeout, 15.5)
        self.assertIsNone(config.settings.debug_mode)

    def test_cfg(self) -> None:
        config = load_config(self.cfg_file)
        self.assertIsConfiguration(config)
        self.assertEqual(config.general.app_name, "TestApp")
        self.assertEqual(config.general.version, "1.0")
        self.assertEqual(config.general.is_enabled, True)
        self.assertEqual(config.general.is_active, "true")
        self.assertEqual(config.settings.max_users, 100)
        self.assertEqual(config.settings.timeout, 15.5)
        self.assertIsNone(config.settings.debug_mode)
        
    def test_json(self) -> None:
        config = load_config(self.json_file)
        self.assertIsConfiguration(config)
        self.assertEqual(config.app_name, "TestApp")
        self.assertEqual(config.owner_ids, [1, 2, 3, 4, 5])
        self.assertEqual(config.nested_config.version, 1)
        self.assertEqual(config.nested_config.other_ids, [1, 2, 3, 4, 5])

    def test_toml(self) -> None:
        config = load_config(self.toml_file)
        self.assertIsConfiguration(config)
        self.assertEqual(config.general.app_name, "TestApp")
        self.assertEqual(config.general.version, "1.0")
        self.assertEqual(config.settings.max_users, 100)
        self.assertTrue(config.settings.debug_mode)
        self.assertEqual(config.settings.timeout, 30.5)
        self.assertEqual(config.settings.owner_ids, [1, 2, 3])
    
    def test_yaml(self) -> None:
        config = load_config(self.yaml_file)
        self.assertIsConfiguration(config)
        self.assertEqual(config.app_name, "TestApp")
        self.assertEqual(config.version, "1.0")
        self.assertEqual(config.settings.max_users, 100)
        self.assertTrue(config.settings.debug_mode)
        self.assertIsNone(config.settings.timeout)
        self.assertEqual(config.settings.owner_ids, [1, 2, 3])
        self.assertTrue(config.settings.flags.is_enabled)
   
    """Parser Exceptions"""
    
    def test_bad_file_type(self) -> None:
        for file in self.invalid_types:
            with self.assertRaises(SourceError):
                config = load_config(file)
    
    def test_bad_config_syntax(self) -> None:
        for file in self.invalid_syntaxs:
            with self.assertRaises(ParsingError):
                config = load_config(file)
                
        
    