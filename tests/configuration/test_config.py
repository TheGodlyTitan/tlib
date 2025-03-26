import unittest

from configuration import (
    load_config,
    Configuration,
    FileTypeError,
    ConfigParsingError,
)


SOURCE_FILES = "tlib/tlib_tests/configuration/configs"


class TestConfiguration(unittest.TestCase):
    
    def setUp(self):
        # Valid Files
        self.ini_file  = f"{SOURCE_FILES}/valid_config.ini"
        self.cfg_file  = f"{SOURCE_FILES}/valid_config.cfg"
        self.json_file = f"{SOURCE_FILES}/valid_config.json"
        self.toml_file = f"{SOURCE_FILES}/valid_config.toml"
        self.yaml_file = f"{SOURCE_FILES}/valid_config.yml"
        self.env_file  = f"{SOURCE_FILES}/valid_config.env"
        
    """Value Getting"""
    
    def test_config_get(self) -> None:
        config = load_config(self.yaml_file)
        app_name = config.get('app_name')
        self.assertEqual(app_name, 'TestApp')
        
    def test_config_get_nested(self) -> None:
        config = load_config(self.yaml_file)
        owner_ids = config.get('settings.owner_ids')
        self.assertEqual(owner_ids, [1, 2, 3])
        
    def test_config_get_nested_two(self) -> None:
        config = load_config(self.yaml_file)
        is_enabled = config.get('settings.flags.is_enabled')
        self.assertTrue(is_enabled)
    
    """Value Setting"""
    
    def test_config_set(self) -> None:
        config = load_config(self.yaml_file)
        k = 'app_name'
        v = 'ProdApp'
        config.set(k, v)
        self.assertEqual(config.get(k), v)
        self.assertEqual(config.app_name, v)
        
    def test_config_set_nested(self) -> None:
        config = load_config(self.yaml_file)
        k = 'settings'
        v = {
            'admin_ids': 100,
            'is_enabled': True
        }
        config.set(k, v)
        self.assertEqual(config.get(k), v)
        self.assertEqual(config.settings, v)
        self.assertEqual(config.settings.admin_ids, 100)
        self.assertTrue(config.settings.is_enabled)
        
    def test_config_set_nested_two(self) -> None:
        config = load_config(self.yaml_file)
        k = 'settings'
        v = {
            'flags': {
                'is_enabled': True,
                'in_debug': False
            }
        }
        config.set(k, v)
        self.assertEqual(config.get(k), v)
        self.assertEqual(config.settings, v)
        self.assertTrue(config.settings.flags.is_enabled)
        self.assertFalse(config.settings.flags.in_debug)