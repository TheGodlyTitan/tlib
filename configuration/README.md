# **TLib Configuration**

## **Overview**
The TLib Configuration package provides a structured, flexible, and efficient way to manage and load configuration files in various formats (YAML, JSON, etc.). It includes a core configuration object, utility functions, and format-specific loaders, making it easy to integrate across different projects.

## **Features**
- Multi-format support: Easily load YAML, JSON, and other configuration formats.
- Structured access: Configuration values are accessible via attribute-style access.
- Custom loaders: Create custom loaders to extend format support.
- Error handling: Provides clear error messages for syntax and loading issues.
- Strict keys: Define configuration keys and accepted values with schemas.

## **Installation**
To install the package, use:
```
# Currently Unavailable
```

## **Basic Usage**
The core feature of the module is loading a source config file and constructing a `Configuration` object where the keys become the class attributes.
This simplifies the retrivial of your configuration values, as well as the editing and saving of the source file when needed.
### **Example Config (config.yml)**
```yaml
app_name: "TestApp"
settings:
    max_users: 100
    debug_mode: false
flags:
    - "flag_one"
    - "flag_two"
```
### **Loading Config (app.py)**
```py
# app.py
from tlib.configuration import (
    errors,
    load_config, 
    Configuration
)

PATH = "config.yml"

try:
    config: Configuration = load_config(PATH)
except errors.ConfigError as e:
    print(f'Failed to load configuration: {e}')

print(config.app_name)  # "TestApp"
print(config.settings.max_users)  # 100
print(config.settings.debug_mode)  # False
print(config.flags)  # ['flag_one', 'flag_two']
```
### **Expected Output**
```py
>>> "TestApp"
>>> 100
>>> False
>>> ['flag_one', 'flag_two']
```

## **Custom Parsers**
Although the module contains multiple file type parsers; you may want to handle your own parsing for your own custom/complex configuration structures.
The `Parser` class allows you create a parsing handler, which can be passed though the `load_config` function.
### **Class Construction (your_parser.py)**
```py
from pathlib import Path
from tlib.configuration import (
    Parser,
    ConfigurationData,
    ConfigError,
    ConfigParsingError,
)

class ABCParser(Parser):
    def parse(source: Path) -> ConfigurationData:
        try:
            with source.open("r", encoding="utf-8") as file:
                data = file.read()  # Adjust based on the format being loaded
            return data
        except SomeFileSyntaxError as e:
            raise ConfigParsingError(source, f"Invalid Configuration Syntax: {e}")
        except OtherErrors as e:
            raise ConfigError(f"Failed to open {source}: {e}")
```
### **Class Usage (app.py)**
```py
from tlib.config import (
    errors,
    load_config,
    Configuration
)
from your_parser import ABCParser

path = 'config.abc'

try:
    config = load_config(path, parser=ABCParser)
except errors.ConfigError as e:
    print(f'Failed to load configuration: {e}')
```

## **Schema Validation**
The module also contains a configuration validation mechanic, this can be used to ensure that configurations have valid values and required keys.
The `ConfigSchema` class allows your to create a validator handler, which can be passed through the `load_config` function.
### **Example Config (config.yml)**
```yaml
app_name: "TestApp"
settings:
    max_users: 100
    debug_mode: false
flags:
    - "flag_one"
    - "flag_two"
```
### **Class Construction (your_schema.py)**
```py
from tlib.config import (
    ConfigSchema, # Config Schema Class
    Nested, # Schema Values Types
    String,
    Integer,
    Boolean,
    Array,
)

class CustomSchema(ConfigSchema):

    app_name = String(min_chars=5)
    settings = Nested(
        ('max_users', Integer()),
        ('debug_mode', Boolean())
    )
    flags = Array(String(), elements=2)
```
### **Class Usage (app.py)**
```py
from tlib.config import (
    errors,
    load_config,
    Configuration,
)
from my_schema import CustomSchema

path = 'config.yml'

try:
    config = load_config(path, schema=CustomSchema)
except errors.ConfigValidationError as e:
    print(f'Config schema validation failed: {e}')
except errors.ConfigError as e:
    print(f'Failed to load configuration: {e}')

```

## **Module Errors**
- `ConfigError`:
- `FileTypeError`:
- `ConfigParsingError`:
- `ConfigValidationError`: